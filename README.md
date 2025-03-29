# Daraja MCP

A Model Context Protocol (MCP) server designed to integrate AI applications with Safaricom's Daraja API, enabling seamless interaction with M-Pesa services.

## Overview

Daraja MCP is a bridge between AI, fintech, and M-Pesa, making AI-driven financial automation accessible and efficient. By standardizing the connection between LLMs (Large Language Models) and financial transactions, Daraja MCP allows AI-driven applications to process payments, retrieve transaction data, and automate financial workflows effortlessly.

### Key Capabilities

- ✅ **AI-Powered M-Pesa Transactions** – Enable LLMs to handle B2C, C2B, and B2B payments
- ✅ **Standardized Integration** – MCP ensures compatibility with multiple AI tools
- ✅ **Secure & Scalable** – Implements OAuth authentication and supports enterprise-grade transaction handling
- ✅ **Flexible Automation** – AI agents can query account balances, generate invoices, and automate reconciliation

## Requirements

- Python 3.12

## Installation

### Step 1: Setting Up Your Environment

1. **Install uv Package Manager**

   For Mac/Linux:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   For Windows (PowerShell):

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone the Repository**

   ```bash
   git clone https://github.com/jameskanyiri/DarajaMCP.git
   cd DarajaMCP
   ```

3. **Create and Activate a Virtual Environment**

   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

   ✅ Expected Output: Your terminal prompt should change, indicating the virtual environment is activated.

4. **Install Dependencies**
   ```bash
   uv sync
   ```

### Step 2: Setting up Environment Variables

1. Copy the example environment file:

   ```bash
   cp .env.example .env
   ```

2. Update the `.env` file with your actual credentials and configuration values.

> Note: For development, use the sandbox environment. Switch to the production URL when ready.

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

## Setup

### Safaricom Daraja API Credentials

1. Register for a Safaricom Developer account at [developer.safaricom.co.ke](https://developer.safaricom.co.ke)
2. Create a new app to get your Consumer Key and Secret
3. For production access, you'll need to go through Safaricom's verification process

## Usage

### Testing with Claude Desktop

1. **Install Claude Desktop**

   - Download and install the latest version from [Claude Desktop](https://claude.ai/desktop)
   - Make sure you're running the latest version

2. **Configure Claude Desktop**

   - Open your Claude Desktop configuration file:

     ```bash
     # On MacOS/Linux
     code ~/Library/Application\ Support/Claude/claude_desktop_config.json

     # On Windows
     code %APPDATA%\Claude\claude_desktop_config.json
     ```

   - Create the file if it doesn't exist

3. **Add Server Configuration**
   Choose one of the following configurations:

   #### Anthropic's Recommended Format

   ```json
   {
     "mcpServers": {
       "daraja": {
         "command": "uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/PARENT/FOLDER/DarajaMCP",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

   #### Working Configuration (Tested)

   ```json
   {
     "mcpServers": {
       "DarajaMCP": {
         "command": "/ABSOLUTE/PATH/TO/PARENT/.local/bin/uv",
         "args": [
           "--directory",
           "/ABSOLUTE/PATH/TO/PARENT/FOLDER/DarajaMCP",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```

   > Note:
   >
   > - Replace `/ABSOLUTE/PATH/TO/PARENT` with your actual path
   > - To find the full path to `uv`, run:

   ```bash
   # On MacOS/Linux
   which uv

   # On Windows
   where uv
   ```

4. **Verify Configuration**
   - Save the configuration file
   - Restart Claude Desktop
   - Look for the hammer 🔨 icon in the interface
   - Click it to see the available tools:
     - generate_access_token
     - stk_push (Future Implementation)
     - query_transaction_status (Future Implementation)
     - b2c_payment (Future Implementation)
     - account_balance (Future Implementation)

## License

[MIT License](LICENSE)

## Acknowledgments

- Safaricom for providing the Daraja API
- Anthropic for the MCP framework
- Contributors to the project

## Contact

For any inquiries, please open an issue on the GitHub repository.
