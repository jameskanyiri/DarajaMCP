def register_mpesa_prompts(mcp):
    @mcp.prompt()
    async def stk_push_prompt(phone_number: str, amount: int, purpose: str):
        """
        This prompt help to initiate a STK Push.

        Args:
            phone_number (str): The phone number of the customer.
            amount (int): The amount to be paid.
            purpose (str): The purpose of the payment.

        Returns:
            str: String
        """
        return f"I want you to initiate an M-Pesa STK Push payment request. Here are the details User phone number: {phone_number}, Amount: {amount}, Purpose: {purpose}"

    @mcp.prompt()
    async def generate_qr_code_prompt(
        merchant_name: str,
        amount: int,
        transaction_type: str,
        identifier: str,
        reference: str = None,
    ):
        """
        This prompt helps generate a QR code for M-Pesa payments.

        Args:
            merchant_name (str): Name of the merchant/business
            amount (int): Amount to be paid
            transaction_type (str): Type of transaction (BG for Buy Goods, WA for Wallet, PB for Paybill,
                                  SM for Send Money, SB for Send to Business)
            identifier (str): The recipient identifier (till number, paybill, phone number)
            reference (str, optional): Transaction reference number. If not provided, a default will be used.

        Returns:
            str: Prompt string for QR code generation
        """
        transaction_types = {
            "BG": "Buy Goods",
            "WA": "Wallet",
            "PB": "Paybill",
            "SM": "Send Money",
            "SB": "Send to Business",
        }

        transaction_description = transaction_types.get(
            transaction_type.upper(), transaction_type
        )
        reference = reference or "QR_PAYMENT"

        return f"""I want to generate an M-Pesa QR code with the following details:
- Merchant/Business Name: {merchant_name}
- Amount: KES {amount}
- Transaction Type: {transaction_description} ({transaction_type})
- Recipient Identifier: {identifier}
- Reference Number: {reference}

Please generate a QR code that customers can scan to make this payment."""
