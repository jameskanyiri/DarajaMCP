import unittest
from unittest.mock import AsyncMock, MagicMock, patch
import json
import asyncio

# Assuming mpesa.tools is accessible in the PYTHONPATH
# If not, we might need to adjust sys.path or ensure the test runner handles it
from mpesa.tools import stk_push, generate_qr_code

class TestMpesaTools(unittest.TestCase):

    def setUp(self):
        # Prepare common mock objects if needed
        self.mock_ctx = MagicMock()
        self.mock_ctx.request_context.lifespan_context.access_token = "test_access_token"
        self.loop = asyncio.get_event_loop()

    @patch('daraja_endpoints.mpesa_express.initiate_stk_push', new_callable=AsyncMock)
    async def test_stk_push_success(self, mock_initiate_stk_push):
        # Mock successful API response
        api_response = {"ResponseCode": "0", "ResponseMessage": "Success"}
        mock_initiate_stk_push.return_value = api_response

        amount = 100
        phone_number = 254712345678

        result = await stk_push(self.mock_ctx, amount, phone_number)
        expected_json_response = json.dumps(api_response, indent=2)

        mock_initiate_stk_push.assert_called_once_with(
            "test_access_token", amount, phone_number
        )
        self.assertEqual(result, expected_json_response)

    @patch('daraja_endpoints.mpesa_express.initiate_stk_push', new_callable=AsyncMock)
    async def test_stk_push_api_error(self, mock_initiate_stk_push):
        # Mock API error
        error_message = "API Error"
        mock_initiate_stk_push.side_effect = Exception(error_message)

        amount = 100
        phone_number = 254712345678

        result = await stk_push(self.mock_ctx, amount, phone_number)
        expected_error_response = json.dumps(
            {"error": {"type": "Exception", "message": error_message}}, indent=2
        )

        mock_initiate_stk_push.assert_called_once_with(
            "test_access_token", amount, phone_number
        )
        self.assertEqual(result, expected_error_response)

    @patch('daraja_endpoints.dynamic_qr.qr_code.qr_code', new_callable=AsyncMock)
    async def test_generate_qr_code_success(self, mock_qr_code_func):
        # Mock successful API response
        api_response = {"qr_code": "base64_encoded_qr", "ResponseCode": "0"}
        mock_qr_code_func.return_value = api_response

        merchant_name = "TestMerchant"
        transaction_reference_no = "TestRef123"
        amount = 200
        transaction_type = "BG" # Buy Goods
        credit_party_identifier = "123456"

        result = await generate_qr_code(
            self.mock_ctx,
            merchant_name,
            transaction_reference_no,
            amount,
            transaction_type,
            credit_party_identifier,
        )
        expected_json_response = json.dumps(api_response, indent=2)

        mock_qr_code_func.assert_called_once_with(
            "test_access_token",
            merchant_name,
            transaction_reference_no,
            amount,
            transaction_type,
            credit_party_identifier,
        )
        self.assertEqual(result, expected_json_response)

    @patch('daraja_endpoints.dynamic_qr.qr_code.qr_code', new_callable=AsyncMock)
    async def test_generate_qr_code_api_error(self, mock_qr_code_func):
        # Mock API error
        error_message = "QR API Error"
        mock_qr_code_func.side_effect = Exception(error_message)

        merchant_name = "TestMerchant"
        transaction_reference_no = "TestRef123"
        amount = 200
        transaction_type = "WA" # Withdraw Cash Agent
        credit_party_identifier = "AgentTill1"

        result = await generate_qr_code(
            self.mock_ctx,
            merchant_name,
            transaction_reference_no,
            amount,
            transaction_type,
            credit_party_identifier,
        )
        expected_error_response = json.dumps(
            {"error": {"type": "Exception", "message": error_message}}, indent=2
        )

        mock_qr_code_func.assert_called_once_with(
            "test_access_token",
            merchant_name,
            transaction_reference_no,
            amount,
            transaction_type,
            credit_party_identifier,
        )
        self.assertEqual(result, expected_error_response)

if __name__ == '__main__':
    # This is to make test discovery work with async tests more easily in some environments
    # For unittest TestLoader to discover async tests, they need to be wrapped or the test runner needs to support it.
    # unittest.main() might not run async tests correctly out of the box without a suitable test runner.
    # However, modern versions of unittest and popular test runners like pytest handle this.
    # For the purpose of this environment, we'll assume the test runner handles it.
    unittest.main()
