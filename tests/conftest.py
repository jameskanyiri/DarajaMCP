import pytest
import os
from unittest.mock import patch


@pytest.fixture
def mock_env_variables():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'MPESA_CONSUMER_KEY': 'test_consumer_key',
        'MPESA_CONSUMER_SECRET': 'test_consumer_secret', 
        'BASE_URL': 'https://sandbox.safaricom.co.ke',
        'MPESA_PASSKEY': 'test_passkey',
        'BUSINESS_SHORTCODE': '174379',
        'PHONE_NUMBER': '254708374149',
        'CALLBACK_URL': 'https://example.com/callback'
    }):
        yield


@pytest.fixture
def sample_token_response():
    """Sample access token response"""
    return {
        "access_token": "SGWcJeCrWBHB8bSRp5SMy7Wc",
        "expires_in": "3599"
    }


@pytest.fixture
def sample_stk_response():
    """Sample STK push response"""
    return {
        "MerchantRequestID": "92071-10669096-1",
        "CheckoutRequestID": "ws_CO_191220191020363925",
        "ResponseCode": "0",
        "ResponseDescription": "Success. Request accepted for processing",
        "CustomerMessage": "Success. Request accepted for processing"
    }
