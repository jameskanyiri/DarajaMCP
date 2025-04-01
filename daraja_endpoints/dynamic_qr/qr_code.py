from typing import Dict, Any, Literal
import httpx
import os


async def qr_code(
    access_token: str,
    merchant_name: str,
    transaction_reference_no: str,
    amount: int,
    transaction_type: Literal["BG", "WA", "PB", "SM", "SB"],
    credit_party_identifier: str,
):
    """
    Generate a QR code for a transaction.

    Args:
        access_token (str): Valid M-PESA access token.

        merchant_name (str): Name of the company/M-Pesa Merchant Name.

        transaction_reference_no (str): Transaction reference number.

        amount (int): The total amount for the sale/transaction.

        transaction_type (Literal["BG", "WA", "PB", "SM", "SB"]): Transaction type.

        credit_party_identifier (str): Credit Party Identifier.

    Returns:
        str: JSON formatted M-PESA API response
    """

    base_url = os.getenv("BASE_URL")

    # validate required variables
    if not all(
        [
            access_token,
            merchant_name,
            transaction_reference_no,
            amount,
            transaction_type,
            credit_party_identifier,
        ]
    ):
        raise ValueError("Missing required variables for QR code generation")

    # prepare the request
    url = f"{base_url}/mpesa/qrcode/v1/generate"

    # headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # payload
    payload = {
        "MerchantName": merchant_name,
        "RefNo": transaction_reference_no,
        "Amount": amount,
        "TrxCode": transaction_type,
        "CPI": credit_party_identifier,
        "Size": "300",
    }

    # send request
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {
                "error": "QR code generation failed",
                "status_code": e.response.status_code,
                "details": e.response.json(),
            }
        except httpx.RequestError as e:
            return {"error": "Request error", "details": str(e)}
