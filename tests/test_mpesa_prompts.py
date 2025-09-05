import unittest
import asyncio
from mpesa.prompts import stk_push_prompt, generate_qr_code_prompt

class TestMpesaPrompts(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    async def test_stk_push_prompt_generation(self):
        phone_number = 254712345678
        amount = 1500
        purpose = "Payment for goods"
        
        prompt = await stk_push_prompt(phone_number=phone_number, amount=amount, purpose=purpose)
        
        expected_prompt = (
            "Initiating M-Pesa STK push...\n"
            f"Phone Number: {phone_number}\n"
            f"Amount: KES {amount}\n"
            f"Purpose: {purpose}\n"
            "Please confirm the payment on your M-Pesa enabled phone."
        )
        self.assertEqual(prompt, expected_prompt)

    async def test_generate_qr_code_prompt_basic(self):
        merchant_name = "MySuperMarket"
        amount = 2500
        transaction_type = "BG"  # Buy Goods
        identifier = "TillNo12345"
        
        prompt = await generate_qr_code_prompt(
            merchant_name=merchant_name,
            amount=amount,
            transaction_type=transaction_type,
            credit_party_identifier=identifier
        )
        
        expected_prompt = (
            "Generating M-Pesa QR Code...\n"
            f"Merchant Name: {merchant_name}\n"
            f"Amount: KES {amount}\n"
            "Transaction Type: Buy Goods (Pay Merchant)\n"
            f"Credit Party Identifier: {identifier}\n"
            "Transaction Reference: Not Provided\n"
            "The QR code will be displayed once generated."
        )
        self.assertEqual(prompt, expected_prompt)

    async def test_generate_qr_code_prompt_with_reference(self):
        merchant_name = "CornerCafe"
        amount = 500
        transaction_type = "WA"  # Withdraw Cash Agent
        identifier = "Agent007"
        reference = "REF789XYZ"
        
        prompt = await generate_qr_code_prompt(
            merchant_name=merchant_name,
            amount=amount,
            transaction_type=transaction_type,
            credit_party_identifier=identifier,
            transaction_reference_no=reference
        )
        
        expected_prompt = (
            "Generating M-Pesa QR Code...\n"
            f"Merchant Name: {merchant_name}\n"
            f"Amount: KES {amount}\n"
            "Transaction Type: Withdraw Cash at Agent\n"
            f"Credit Party Identifier: {identifier}\n"
            f"Transaction Reference: {reference}\n"
            "The QR code will be displayed once generated."
        )
        self.assertEqual(prompt, expected_prompt)

    async def test_generate_qr_code_prompt_unknown_transaction_type(self):
        merchant_name = "OnlineStore"
        amount = 1200
        transaction_type = "XX"  # Unknown type
        identifier = "Paybill888"
        
        prompt = await generate_qr_code_prompt(
            merchant_name=merchant_name,
            amount=amount,
            transaction_type=transaction_type,
            credit_party_identifier=identifier
        )
        
        expected_prompt = (
            "Generating M-Pesa QR Code...\n"
            f"Merchant Name: {merchant_name}\n"
            f"Amount: KES {amount}\n"
            f"Transaction Type: {transaction_type}\n" # Should use the type directly
            f"Credit Party Identifier: {identifier}\n"
            "Transaction Reference: Not Provided\n"
            "The QR code will be displayed once generated."
        )
        self.assertEqual(prompt, expected_prompt)

if __name__ == '__main__':
    unittest.main()
