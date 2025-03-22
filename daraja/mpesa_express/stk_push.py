import os
import json
import requests
import logging
from datetime import datetime
import base64
from typing import Dict, Any

from ..auth.generate_access_token import get_access_token
from dotenv import load_dotenv

load_dotenv()


def initiate_stk_push(amount: int) -> Dict[str, Any]:
    """
    Initiate an STK Push transaction.

    Args:
        amount (int): Amount to be paid

    Returns:
        Dict[str, Any]: M-PESA API response

    Raises:
        ValueError: If required environment variables are missing
        requests.RequestException: If the API request fails
    """
    # Get required environment variables
    business_shortcode = os.getenv("BUSINESS_SHORTCODE")
    passkey = os.getenv("PASSKEY")
    phone_number = os.getenv("PHONE_NUMBER")
    callback_url = os.getenv("CALLBACK_URL")
    account_ref = os.getenv("ACCOUNT_REFERENCE")
    base_url = os.getenv("BASE_URL", "https://sandbox.safaricom.co.ke")

    # Validate required variables
    if not all([business_shortcode, passkey, phone_number, callback_url, account_ref]):
        raise ValueError("Missing required environment variables for STK Push")

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate password
    password = base64.b64encode(
        f"{business_shortcode}{passkey}{timestamp}".encode()
    ).decode()

    # Get access token
    access_token = get_access_token()["access_token"]

    # Prepare request
    url = f"{base_url}/mpesa/stkpush/v1/processrequest"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": business_shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": business_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_ref,
        "TransactionDesc": "Payment of goods/services",
    }

    # Make API request
    response = requests.post(url, headers=headers, json=payload)

    try:
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise
