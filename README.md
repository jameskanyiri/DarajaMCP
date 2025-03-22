# Daraja MCP

A Model Context Protocol (MCP) server designed to integrate AI applications with Safaricom's Daraja API, enabling seamless interaction with M-Pesa services.

## Overview

Daraja MCP is a bridge between AI, fintech, and M-Pesa, making AI-driven financial automation accessible and efficient. By standardizing the connection between LLMs (Large Language Models) and financial transactions, Daraja MCP allows AI-driven applications to process payments, retrieve transaction data, and automate financial workflows effortlessly.

### Key Capabilities

- ✅ **AI-Powered M-Pesa Transactions** – Enable LLMs to handle B2C, C2B, and B2B payments
- ✅ **Standardized Integration** – MCP ensures compatibility with multiple AI tools
- ✅ **Secure & Scalable** – Implements OAuth authentication and supports enterprise-grade transaction handling
- ✅ **Flexible Automation** – AI agents can query account balances, generate invoices, and automate reconciliation

## What is an MCP Server?

MCP (Model Context Protocol) servers provide capabilities for LLMs to interact with external systems. MCP servers can provide three main types of capabilities:

- **Resources**: File-like data that can be read by clients (like API responses)
- **Tools**: Functions that can be called by the LLM (with user approval)
- **Prompts**: Pre-written templates that help users accomplish specific tasks

Daraja MCP specifically leverages this architecture to connect AI systems with Safaricom's Daraja M-Pesa API.

## Tools

### generate_access_token

Generate an OAuth access token for the Daraja API.

**Inputs:**

- None (uses environment variables for authentication)

**Returns:** Access token information including:

- `access_token` (string): The OAuth access token
- `expires_in` (number): Token validity period in seconds

### stk_push (Future Implementation)

Initiate an M-Pesa STK push request.

**Inputs:**

- `phone_number` (string): The customer's phone number (format: 254XXXXXXXXX)
- `amount` (number): Transaction amount
- `account_reference` (string): Reference ID for the transaction
- `transaction_desc` (optional string): Description of the transaction

**Returns:** STK push response including:

- `MerchantRequestID` (string): Unique request identifier
- `CheckoutRequestID` (string): Checkout request identifier
- `ResponseDescription` (string): Description of the response

### query_transaction_status (Future Implementation)

Check the status of an M-Pesa transaction.

**Inputs:**

- `checkout_request_id` (string): The checkout request ID from STK push
- `transaction_id` (optional string): M-Pesa transaction ID

**Returns:** Transaction status details

### b2c_payment (Future Implementation)

Initiate a Business to Customer payment.

**Inputs:**

- `phone_number` (string): Recipient's phone number
- `amount` (number): Amount to send
- `remarks` (string): Comments about the transaction
- `occasion` (optional string): Description of the occasion

**Returns:** B2C payment response details

### account_balance (Future Implementation)

Check account balance.

**Inputs:**

- `party_a` (optional string): The organization shortcode (defaults to BUSINESS_SHORTCODE env var)

**Returns:** Account balance information

## Requirements

- Python 3.13+
- MCP SDK 1.2.0+
- Requests
- python-dotenv
- httpx

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

1. Install uv:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/DarajaMCP.git
   cd DarajaMCP
   ```

3. Create a virtual environment and activate it:

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   uv pip install -e .
   ```

## Configuration

Create a `.env` file in the root directory with the following variables:

```
MPESA_CONSUMER_KEY="your_consumer_key"
MPESA_CONSUMER_SECRET="your_consumer_secret"
PASSKEY="your_passkey"
BUSINESS_SHORTCODE="your_shortcode"
CALLBACK_URL="your_callback_url"
BASE_URL="https://sandbox.safaricom.co.ke"
PHONE_NUMBER="your_phone_number"
ACCOUNT_REFERENCE="your_account_reference"
TRANSACTION_TYPE="CustomerPayBillOnline"
TRANSACTION_DESC="your_transaction_description"
```

> Note: For development, use the sandbox environment. Switch to the production URL when ready.

## Setup

### Safaricom Daraja API Credentials

1. Register for a Safaricom Developer account at [developer.safaricom.co.ke](https://developer.safaricom.co.ke)
2. Create a new app to get your Consumer Key and Secret
3. For production access, you'll need to go through Safaricom's verification process

### Usage with Claude Desktop

Add the following to your `claude_desktop_config.json`:

#### Docker (Recommended)

```json
{
  "mcpServers": {
    "daraja": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e",
        "MPESA_CONSUMER_KEY",
        "-e",
        "MPESA_CONSUMER_SECRET",
        "-e",
        "PASSKEY",
        "-e",
        "BUSINESS_SHORTCODE",
        "-e",
        "BASE_URL",
        "yourusername/darajamcp"
      ],
      "env": {
        "MPESA_CONSUMER_KEY": "<YOUR_CONSUMER_KEY>",
        "MPESA_CONSUMER_SECRET": "<YOUR_CONSUMER_SECRET>",
        "PASSKEY": "<YOUR_PASSKEY>",
        "BUSINESS_SHORTCODE": "<YOUR_SHORTCODE>",
        "BASE_URL": "https://sandbox.safaricom.co.ke"
      }
    }
  }
}
```

#### Direct Python Module

```json
{
  "mcpServers": {
    "daraja": {
      "command": "python",
      "args": ["-m", "main"],
      "cwd": "/path/to/DarajaMCP",
      "env": {
        "MPESA_CONSUMER_KEY": "<YOUR_CONSUMER_KEY>",
        "MPESA_CONSUMER_SECRET": "<YOUR_CONSUMER_SECRET>",
        "PASSKEY": "<YOUR_PASSKEY>",
        "BUSINESS_SHORTCODE": "<YOUR_SHORTCODE>",
        "BASE_URL": "https://sandbox.safaricom.co.ke"
      }
    }
  }
}
```

### Environment Variables

- `MPESA_CONSUMER_KEY`: Your Safaricom API consumer key (required)
- `MPESA_CONSUMER_SECRET`: Your Safaricom API consumer secret (required)
- `PASSKEY`: Your Safaricom API passkey (required for STK Push)
- `BUSINESS_SHORTCODE`: Your M-Pesa till/paybill number (required)
- `BASE_URL`: Safaricom API base URL (defaults to sandbox URL)
- `CALLBACK_URL`: Callback URL for notifications (optional)

## Usage

### Basic Authentication Example

Here's a basic example of how to use the library to generate an access token:

```python
from daraja.auth.generate_access_token import get_access_token

# Get an access token
try:
    token_info = get_access_token()
    print(f"Access Token: {token_info['access_token']}")
    print(f"Expires in: {token_info['expires_in']} seconds")
except Exception as e:
    print(f"Error: {e}")
```

### Connecting to an MCP Client

To use Daraja MCP with a compatible client (like Claude for Desktop):

1. Start the MCP server:

   ```bash
   python main.py
   ```

2. Connect your MCP client to the server using the provided URL.

3. Your AI assistant can now use the provided tools to interact with M-Pesa services.

## Development

This project uses Python 3.13 and uv for dependency management. Make sure you have them installed before contributing.

### Docker Build

To build a Docker image for the project:

```bash
docker build -t yourusername/darajamcp .
```

## License

[MIT License](LICENSE)

## Acknowledgments

- Safaricom for providing the Daraja API
- Anthropic for the MCP framework
- Contributors to the project

## Contact

For any inquiries, please open an issue on the GitHub repository.
