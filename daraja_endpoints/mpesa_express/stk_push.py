import os
from datetime import datetime
import base64
from typing import Dict, Any
import httpx
from daraja_endpoints.auth.generate_access_token import get_access_token
from dotenv import load_dotenv

load_dotenv()


async def initiate_stk_push(
    access_token: str, amount: int, phone_number: int
) -> Dict[str, Any]:
    """
    Initiate an STK Push transaction.

    Args:
        access_token (str): Valid M-PESA access token
        amount (int): Amount to be paid
        phone_number (str): Phone number of the customer

    Returns:
        Dict[str, Any]: M-PESA API response

    Raises:
        ValueError: If required environment variables are missing
        requests.RequestException: If the API request fails
    """

    # Get required environment variables
    business_shortcode = os.getenv("BUSINESS_SHORTCODE")
    passkey = os.getenv("PASSKEY")
    callback_url = os.getenv("CALLBACK_URL")
    account_ref = os.getenv("ACCOUNT_REFERENCE")
    base_url = os.getenv("BASE_URL")

    # Validate required variables
    if not all([business_shortcode, passkey, phone_number, callback_url, account_ref]):
        raise ValueError("Missing required environment variables for STK Push")

    # Generate timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Generate password
    password = base64.b64encode(
        f"{business_shortcode}{passkey}{timestamp}".encode()
    ).decode()

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

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": "STK Push failed",
                "status_code": e.response.status_code,
                "details": e.response.json(),
            }
        except httpx.RequestError as e:
            return {"error": "Request error", "details": str(e)}
