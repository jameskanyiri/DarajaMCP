from mcp.server.fastmcp import Context
from daraja_endpoints.mpesa_express import initiate_stk_push
from daraja_endpoints.dynamic_qr.qr_code import qr_code
from typing import Literal
import json


def register_mpesa_tools(mcp):
    @mcp.tool()
    async def stk_push(ctx: Context, amount: int, phone_number: int) -> str:
        """
        Prompts the customer to authorize a payment on their mobile device.

        Args:
            amount (int): The amount to be paid.
            phone_number (int): The phone number of the customer.

        Returns:
            str: JSON formatted M-PESA API response
        """
        try:
            app_ctx = ctx.request_context.lifespan_context
            access_token = app_ctx.access_token
            response = await initiate_stk_push(access_token, amount, phone_number)
            return json.dumps(response, indent=2)
        except Exception as e:
            return f"Failed to initiate STK Push: {str(e)}"

    @mcp.tool()
    async def generate_qr_code(
        ctx: Context,
        merchant_name: str,
        transaction_reference_no: str,
        amount: int,
        transaction_type: Literal["BG", "WA", "PB", "SM", "SB"],
        credit_party_identifier: str,
    ):
        """
        Generates a QR code for a payment request.

        Args:
            merchant_name (str): Name of the company/M-Pesa Merchant Name.
            transaction_reference_no (str): Transaction reference number.
            amount (int): The total amount for the sale/transaction.
            transaction_type (Literal["BG", "WA", "PB", "SM", "SB"]): Transaction type.
            credit_party_identifier (str): Credit Party Identifier. Can be a Mobile Number, Business Number, Agent Till, Paybill or Business number, or Merchant Buy Goods.

        Returns:
            str: JSON formatted M-PESA API response
        """
        try:
            app_ctx = ctx.request_context.lifespan_context
            access_token = app_ctx.access_token
            response = await qr_code(
                access_token,
                merchant_name,
                transaction_reference_no,
                amount,
                transaction_type,
                credit_party_identifier,
            )
            return json.dumps(response, indent=2)
        except Exception as e:
            return f"Failed to generate QR code: {str(e)}"
