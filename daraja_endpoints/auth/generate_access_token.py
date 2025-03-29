"""
Token generation module for Daraja M-Pesa API.
"""

import os
import base64
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()


async def get_access_token():
    """
    Get an access token from the Safaricom API.

    Returns:
        dict: A dictionary containing the access token and expiry time.
    """
    # Get credentials from environment variables
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
    base_url = os.getenv("BASE_URL")

    if not consumer_key or not consumer_secret or not base_url:
        raise ValueError(
            "Missing required environment variables: MPESA_CONSUMER_KEY or MPESA_CONSUMER_SECRET or BASE_URL"
        )

    # Create the authentication string
    auth_string = f"{consumer_key}:{consumer_secret}"
    encoded_auth = base64.b64encode(auth_string.encode()).decode()

    # Set up the request
    url = f"{base_url}/oauth/v1/generate"
    headers = {"Authorization": f"Basic {encoded_auth}"}
    params = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "access_token": data.get("access_token"),
                "expires_in": data.get("expires_in"),
            }
        except httpx.RequestException as e:
            raise Exception(f"Error fetching access token: {str(e)}")
