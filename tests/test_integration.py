import pytest
from unittest.mock import patch, AsyncMock
from mcp.server.fastmcp import FastMCP
from main import app_lifespan, AppContext


class TestIntegration:
    """Integration tests for the application"""
    
    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_app_lifespan_integration(self, mock_env_variables, sample_token_response):
        """Test the complete application lifespan"""
        mock_app = AsyncMock(spec=FastMCP)
        
        with patch('main.get_access_token', return_value=sample_token_response) as mock_get_token, \
             patch('file_processing.unstructured_workflow.UnstructuredPipeline') as mock_pipeline:
            
            # Test lifespan context manager
            async with app_lifespan(mock_app) as context:
                assert isinstance(context, AppContext)
                assert context.access_token == "SGWcJeCrWBHB8bSRp5SMy7Wc"
                assert context.token_expiry == "3599"
                assert context.refresh_task is not None
                assert context.unstructured_pipeline is not None
            
            # Verify access token was fetched
            mock_get_token.assert_called_once()
            # Verify pipeline was initialized
            mock_pipeline.assert_called_once()
    
    @pytest.mark.asyncio 
    @pytest.mark.integration
    async def test_tool_registration_integration(self, mock_env_variables):
        """Test that all tools and prompts are properly registered"""
        from main import mcp
        
        # This is a basic test to ensure the MCP server is properly configured
        assert mcp.name == "Daraja MCP"
        assert mcp.version == "1.0.0"
        assert mcp.lifespan is not None
