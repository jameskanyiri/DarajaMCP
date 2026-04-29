import pytest
import base64
from unittest.mock import patch, AsyncMock
from daraja_endpoints.auth.generate_access_token import get_access_token


class TestGetAccessToken:
    """Test cases for access token generation"""
    
    @pytest.mark.asyncio
    async def test_get_access_token_success(self, mock_env_variables, sample_token_response):
        """Test successful access token generation"""
        mock_response = AsyncMock()
        mock_response.json.return_value = sample_token_response
        mock_response.raise_for_status.return_value = None
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await get_access_token()
            
            assert result["access_token"] == "SGWcJeCrWBHB8bSRp5SMy7Wc"
            assert result["expires_in"] == "3599"
    
    @pytest.mark.asyncio
    async def test_get_access_token_missing_env_vars(self):
        """Test access token generation with missing environment variables"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                await get_access_token()
            
            assert "Missing required environment variables" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_access_token_http_error(self, mock_env_variables):
        """Test access token generation with HTTP error"""
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = Exception("HTTP Error")
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(Exception) as exc_info:
                await get_access_token()
            
            assert "Error fetching access token" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_get_access_token_correct_auth_header(self, mock_env_variables):
        """Test that the correct authentication header is generated"""
        mock_response = AsyncMock()
        mock_response.json.return_value = {"access_token": "test", "expires_in": "3600"}
        mock_response.raise_for_status.return_value = None
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_get = mock_client.return_value.__aenter__.return_value.get
            mock_get.return_value = mock_response
            
            await get_access_token()
            
            # Verify the call was made with correct headers
            call_args = mock_get.call_args
            headers = call_args[1]['headers']
            
            # Decode the auth header to verify it's correct
            auth_header = headers['Authorization']
            encoded_auth = auth_header.replace('Basic ', '')
            decoded_auth = base64.b64decode(encoded_auth).decode()
            
            assert decoded_auth == "test_consumer_key:test_consumer_secret"
