import pytest
import base64
from unittest.mock import patch, AsyncMock
from datetime import datetime
from daraja_endpoints.mpesa_express.stk_push import initiate_stk_push


class TestStkPush:
    """Test cases for STK Push functionality"""
    
    @pytest.mark.asyncio
    async def test_initiate_stk_push_success(self, mock_env_variables, sample_stk_response):
        """Test successful STK push initiation"""
        mock_response = AsyncMock()
        mock_response.json.return_value = sample_stk_response
        mock_response.raise_for_status.return_value = None
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post.return_value = mock_response
            
            result = await initiate_stk_push("test_token", 100, 254712345678)
            
            assert result["ResponseCode"] == "0"
            assert result["ResponseDescription"] == "Success. Request accepted for processing"
            assert "MerchantRequestID" in result
    
    @pytest.mark.asyncio
    async def test_initiate_stk_push_missing_env_vars(self):
        """Test STK push with missing environment variables"""
        with patch.dict('os.environ', {'BASE_URL': 'https://sandbox.safaricom.co.ke'}, clear=True):
            with pytest.raises(ValueError) as exc_info:
                await initiate_stk_push("test_token", 100, 254712345678)
            
            assert "Missing required environment variables" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_initiate_stk_push_http_error(self, mock_env_variables):
        """Test STK push with HTTP error"""
        from httpx import HTTPStatusError, Response, Request
        
        mock_response = AsyncMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"errorMessage": "Bad Request"}
        
        error_response = Response(400)
        request = Request("POST", "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest")
        http_error = HTTPStatusError("HTTP Error", request=request, response=error_response)
        http_error.response.json = lambda: {"errorMessage": "Bad Request"}
        http_error.response.status_code = 400
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.post.side_effect = http_error
            
            result = await initiate_stk_push("test_token", 100, 254712345678)
            
            assert result["error"] == "STK Push failed"
            assert result["status_code"] == 400
    
    @pytest.mark.asyncio
    async def test_password_generation(self, mock_env_variables):
        """Test that password is generated correctly"""
        mock_response = AsyncMock()
        mock_response.json.return_value = {"ResponseCode": "0"}
        mock_response.raise_for_status.return_value = None
        
        with patch('httpx.AsyncClient') as mock_client, \
             patch('daraja_endpoints.mpesa_express.stk_push.datetime') as mock_datetime:
            
            # Mock timestamp
            mock_datetime.now.return_value.strftime.return_value = "20231201120000"
            
            mock_post = mock_client.return_value.__aenter__.return_value.post
            mock_post.return_value = mock_response
            
            await initiate_stk_push("test_token", 100, 254712345678)
            
            # Verify the call was made with correct payload
            call_args = mock_post.call_args
            payload = call_args[1]['json']
            
            # Verify password generation
            expected_password = base64.b64encode(
                "174379test_passkey20231201120000".encode()
            ).decode()
            
            assert payload["Password"] == expected_password
            assert payload["Timestamp"] == "20231201120000"
            assert payload["Amount"] == 100
            assert payload["PhoneNumber"] == 254712345678
