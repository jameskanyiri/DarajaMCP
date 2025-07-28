import pytest
import json
from unittest.mock import AsyncMock, MagicMock, patch
from mcp.server.fastmcp import Context


class TestMpesaTools:
    """Test cases for M-Pesa tools"""
    
    @pytest.fixture
    def mock_context(self):
        """Create a mock context for testing"""
        context = MagicMock(spec=Context)
        context.request_context = MagicMock()
        context.request_context.lifespan_context = MagicMock()
        context.request_context.lifespan_context.access_token = "test_access_token"
        return context
    
    @pytest.mark.asyncio
    async def test_stk_push_success(self, mock_context, sample_stk_response):
        """Test successful STK push tool execution"""
        with patch('mpesa.tools.initiate_stk_push', return_value=sample_stk_response) as mock_stk:
            # Import here to avoid import issues during collection
            from mpesa.tools import register_mpesa_tools
            
            # Create a mock MCP instance
            mcp = MagicMock()
            tools = []
            
            def mock_tool():
                def decorator(func):
                    tools.append(func)
                    return func
                return decorator
            
            mcp.tool = mock_tool
            
            # Register tools
            register_mpesa_tools(mcp)
            
            # Get the stk_push tool function
            stk_push_tool = tools[0]  # First registered tool
            
            result = await stk_push_tool(mock_context, 100, 254712345678)
            
            # Verify the result is JSON formatted
            result_data = json.loads(result)
            assert result_data["ResponseCode"] == "0"
            assert result_data["ResponseDescription"] == "Success. Request accepted for processing"
            
            # Verify the underlying function was called correctly
            mock_stk.assert_called_once_with("test_access_token", 100, 254712345678)
    
    @pytest.mark.asyncio
    async def test_stk_push_error(self, mock_context):
        """Test STK push tool with error"""
        with patch('mpesa.tools.initiate_stk_push', side_effect=Exception("API Error")) as mock_stk:
            from mpesa.tools import register_mpesa_tools
            
            mcp = MagicMock()
            tools = []
            
            def mock_tool():
                def decorator(func):
                    tools.append(func)
                    return func
                return decorator
            
            mcp.tool = mock_tool
            register_mpesa_tools(mcp)
            
            stk_push_tool = tools[0]
            result = await stk_push_tool(mock_context, 100, 254712345678)
            
            assert "Failed to initiate STK Push: API Error" in result
    
    @pytest.mark.asyncio
    async def test_generate_qr_code_success(self, mock_context):
        """Test successful QR code generation"""
        qr_response = {
            "ResponseCode": "00",
            "ResponseDescription": "Success",
            "QRCode": "iVBORw0KGgoAAAANSUhEUgAAAQYAAAE..."
        }
        
        with patch('mpesa.tools.qr_code', return_value=qr_response) as mock_qr:
            from mpesa.tools import register_mpesa_tools
            
            mcp = MagicMock()
            tools = []
            
            def mock_tool():
                def decorator(func):
                    tools.append(func)
                    return func
                return decorator
            
            mcp.tool = mock_tool
            register_mpesa_tools(mcp)
            
            # Get the QR code tool function (second registered tool)
            qr_tool = tools[1]
            
            result = await qr_tool(
                mock_context,
                "Test Merchant",
                "TXN123456",
                500,
                "BG",
                "600000"
            )
            
            # Verify the result is JSON formatted
            result_data = json.loads(result)
            assert result_data["ResponseCode"] == "00"
            assert "QRCode" in result_data
            
            # Verify the underlying function was called correctly
            mock_qr.assert_called_once_with(
                "test_access_token",
                "Test Merchant", 
                "TXN123456",
                500,
                "BG", 
                "600000"
            )
