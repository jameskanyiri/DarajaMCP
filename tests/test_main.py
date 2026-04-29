import pytest
import asyncio
from unittest.mock import patch, AsyncMock, MagicMock
from main import AppContext, refresh_access_token


class TestAppContext:
    """Test cases for main application functionality"""
    
    def test_app_context_creation(self):
        """Test AppContext dataclass creation"""
        context = AppContext(
            access_token="test_token",
            token_expiry=3600,
            refresh_task=None,
            unstructured_pipeline=MagicMock()
        )
        
        assert context.access_token == "test_token"
        assert context.token_expiry == 3600
        assert context.refresh_task is None
        assert context.unstructured_pipeline is not None
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_success(self):
        """Test successful token refresh"""
        mock_pipeline = MagicMock()
        context = AppContext(
            access_token="old_token",
            token_expiry=120,  # Short expiry for testing
            refresh_task=None,
            unstructured_pipeline=mock_pipeline
        )
        
        new_token_data = {
            "access_token": "new_token", 
            "expires_in": "3600"
        }
        
        with patch('main.get_access_token', return_value=new_token_data) as mock_get_token, \
             patch('asyncio.sleep', return_value=None) as mock_sleep:
            
            # Create a task that will be cancelled after one iteration
            task = asyncio.create_task(refresh_access_token(context))
            
            # Let it run briefly then cancel
            await asyncio.sleep(0.1)
            task.cancel()
            
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            # Verify sleep was called with correct wait time (120 - 60 = 60)
            mock_sleep.assert_called_with(60)
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_minimum_wait_time(self):
        """Test that minimum wait time is enforced"""
        mock_pipeline = MagicMock()
        context = AppContext(
            access_token="old_token",
            token_expiry=30,  # Very short expiry
            refresh_task=None,
            unstructured_pipeline=mock_pipeline
        )
        
        with patch('main.get_access_token', return_value={"access_token": "new", "expires_in": "3600"}), \
             patch('asyncio.sleep', return_value=None) as mock_sleep:
            
            task = asyncio.create_task(refresh_access_token(context))
            await asyncio.sleep(0.1)
            task.cancel()
            
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            # Should use minimum wait time of 60 seconds
            mock_sleep.assert_called_with(60)
    
    @pytest.mark.asyncio
    async def test_refresh_access_token_error_handling(self):
        """Test error handling during token refresh"""
        mock_pipeline = MagicMock()
        context = AppContext(
            access_token="old_token",
            token_expiry=120,
            refresh_task=None,
            unstructured_pipeline=mock_pipeline
        )
        
        with patch('main.get_access_token', side_effect=Exception("Network error")) as mock_get_token, \
             patch('asyncio.sleep', return_value=None) as mock_sleep, \
             patch('builtins.print') as mock_print:
            
            task = asyncio.create_task(refresh_access_token(context))
            await asyncio.sleep(0.1)
            task.cancel()
            
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            # Verify error was printed
            mock_print.assert_called_with("Error refreshing access token: Network error")
