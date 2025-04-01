# Daraja MCP

A Model Context Protocol (MCP) server designed to integrate AI applications with Safaricom's Daraja API, enabling seamless interaction with M-Pesa services.

> ⚠️ **Warning: Not Production Ready**
>
> This project is currently in development and is not recommended for production use. It's designed for:
>
> - Learning and experimentation
> - Development and testing environments
> - Proof of concept implementations
>
> For production use, please ensure:
>
> - Thorough security testing
> - Proper error handling
> - Complete implementation of all planned features
> - Compliance with Safaricom's production requirements

## What is an MCP Server?

MCP (Model Context Protocol) servers provide capabilities for LLMs to interact with external systems. MCP servers can provide three main types of capabilities:

- **Resources**: File-like data that can be read by clients (like API responses)
- **Tools**: Functions that can be called by the LLM (with user approval)
- **Prompts**: Pre-written templates that help users accomplish specific tasks

Daraja MCP specifically leverages this architecture to connect AI systems with Safaricom's Daraja M-Pesa API.

## Overview

Daraja MCP is a bridge between AI, fintech, and M-Pesa, making AI-driven financial automation accessible and efficient. By standardizing the connection between LLMs (Large Language Models) and financial transactions, Daraja MCP allows AI-driven applications to process payments, retrieve transaction data, and automate financial workflows effortlessly.

### Key Capabilities

- ✅ **AI-Powered M-Pesa Transactions** – Enable LLMs to handle B2C, C2B, and B2B payments
- ✅ **Standardized Integration** – MCP ensures compatibility with multiple AI tools
- ✅ **Secure & Scalable** – Implements OAuth authentication and supports enterprise-grade transaction handling
- ✅ **Flexible Automation** – AI agents can query account balances, generate invoices, and automate reconciliation

## Requirements

- Python 3.12
- Safaricom Daraja API Credentials (Consumer Key and Secret)

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

## Tools and Prompts

### Payment Tools

#### stk_push

Initiate an M-Pesa STK push request to prompt the customer to authorize a payment on their mobile device.

**Inputs:**

- `amount` (int): The amount to be paid
- `phone_number` (int): The phone number of the customer

**Returns:** JSON formatted M-PESA API response

#### generate_qr_code

Generate a QR code for a payment request that customers can scan to make payments.

**Inputs:**

- `merchant_name` (str): Name of the company/M-Pesa Merchant Name
- `transaction_reference_no` (str): Transaction reference number
- `amount` (int): The total amount for the sale/transaction
- `transaction_type` (Literal["BG", "WA", "PB", "SM", "SB"]): Transaction type
- `credit_party_identifier` (str): Credit Party Identifier (Mobile Number, Business Number, Agent Till, Paybill, or Merchant Buy Goods)

**Returns:** JSON formatted M-PESA API response containing the QR code data

### Payment Prompts

#### stk_push_prompt

Generate a prompt for initiating an M-Pesa STK push payment request.

**Inputs:**

- `phone_number` (str): The phone number of the customer
- `amount` (int): The amount to be paid
- `purpose` (str): The purpose of the payment

**Returns:** Formatted prompt string for STK push request

#### generate_qr_code_prompt

Generate a prompt for creating an M-Pesa QR code payment request.

**Inputs:**

- `merchant_name` (str): Name of the merchant/business
- `amount` (int): Amount to be paid
- `transaction_type` (str): Type of transaction (BG for Buy Goods, WA for Wallet, PB for Paybill, SM for Send Money, SB for Send to Business)
- `identifier` (str): The recipient identifier (till number, paybill, phone number)
- `reference` (str, optional): Transaction reference number. If not provided, a default will be used.

**Returns:** Formatted prompt string for QR code generation

### Document Processing Tools

#### create_source

Create a connector from data source to unstructured server for processing.

**Inputs:**

- `connector_name` (str): The name of the source connector to create

**Returns:** Source connector details including name and ID

#### create_destination

Create a connector from unstructured server to destination for data storage.

**Inputs:**

- `connector_name` (str): The name of the destination connector to create

**Returns:** Destination connector details including name and ID

#### create_workflow

Create a workflow to process data from source connector to destination connector.

**Inputs:**

- `workflow_name` (str): The name of the workflow to create
- `source_id` (str): The ID of the source connector
- `destination_id` (str): The ID of the destination connector

**Returns:** Workflow details including name, ID, status, type, sources, destinations, and schedule

#### run_workflow

Execute a workflow.

**Inputs:**

- `workflow_id` (str): The ID of the workflow to run

**Returns:** Workflow execution status

#### get_workflow_details

Get detailed information about a workflow.

**Inputs:**

- `workflow_id` (str): The ID of the workflow to get details

**Returns:** Workflow details including name, ID, and status

#### fetch_documents

Fetch documents analyzed during workflow execution.

**Inputs:** None

**Returns:** List of analyzed documents

### Prompts

#### create_and_run_workflow_prompt

Generate a prompt to create and run a workflow for document processing.

**Inputs:**

- `user_input` (str): The user's processing requirements

**Returns:** Formatted prompt for workflow creation and execution

**Example:**

```python
# Example usage
prompt = await create_and_run_workflow_prompt(
    user_input="Process all PDF invoices from the invoices folder and store them in the processed folder"
)
# Returns: "The user wants to achieve Process all PDF invoices from the invoices folder and store them in the processed folder. Assist them by creating a source connector and a destination connector, then setting up the workflow and executing it."
```

### Resources

Currently, no resources are available.

## License

[MIT License](LICENSE)

## Acknowledgments

- Safaricom for providing the Daraja API
- Anthropic for the MCP framework
- Contributors to the project

## Contact

For any inquiries, please open an issue on the GitHub repository.
