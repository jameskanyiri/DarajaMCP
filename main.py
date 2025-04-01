from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP, Context
from daraja_endpoints.auth.generate_access_token import get_access_token
from daraja_endpoints.mpesa_express import initiate_stk_push
import json
import asyncio
from file_processing.unstructured_workflow import UnstructuredPipeline
from database.database import get_analyzed_documents
from daraja_endpoints.dynamic_qr.qr_code import qr_code
from typing import Literal


# Define application context
@dataclass
class AppContext:
    access_token: str
    token_expiry: int
    refresh_task: asyncio.Task | None
    unstructured_pipeline: UnstructuredPipeline


# Function to refresh token in the background
async def refresh_access_token(context: AppContext):
    """Periodically refreshes the access token"""
    while True:
        # Refresh token 60 seconds before expiry
        wait_time = max(context.token_expiry - 60, 60)
        await asyncio.sleep(wait_time)

        try:
            token_data = await get_access_token()
            context.access_token = token_data["access_token"]
            context.token_expiry = token_data["expires_in"]
        except Exception as e:
            print(f"Error refreshing access token: {e}")


# Lifespan manager with auto refresh  support
@asynccontextmanager
async def app_lifespan(app: FastMCP) -> AsyncIterator[AppContext]:
    """Handle application startup, token management and shutdown"""

    token_data = await get_access_token()
    access_token = token_data["access_token"]
    token_expiry = int(token_data["expires_in"])

    # Initialize unstructured pipeline
    unstructured_pipeline = UnstructuredPipeline()

    context = AppContext(
        access_token=access_token,
        token_expiry=token_expiry,
        refresh_task=None,
        unstructured_pipeline=unstructured_pipeline,
    )

    # Start background token refresh task
    context.refresh_task = asyncio.create_task(refresh_access_token(context))

    try:
        # Provide the content to tools
        yield context

    finally:
        # Cancel the refresh task on shutdown
        if context.refresh_task and not context.refresh_task.done():
            context.refresh_task.cancel()
            try:
                await context.refresh_task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Error during token refresh: {e}")


# Initialize the MCP server with lifespan
mcp = FastMCP("Daraja MCP", "1.0.0", lifespan=app_lifespan)

# ===============================================
# MPESA TOOLS
# ===============================================

# STK Push
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
        # Retrieve stored token
        app_ctx = ctx.request_context.lifespan_context
        access_token = app_ctx.access_token

        # Initiate STK Push
        response = await initiate_stk_push(access_token, amount, phone_number)

        # Return response
        return json.dumps(response, indent=2)

    except Exception as e:
        return f"Failed to initiate STK Push: {str(e)}"


# QR Code
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
        access_token (str): Valid M-PESA access token.

        merchant_name (str): Name of the company/M-Pesa Merchant Name.

        transaction_reference_no (str): Transaction reference number.

        amount (int): The total amount for the sale/transaction.

        transaction_type (Literal["BG", "WA", "PB", "SM", "SB"]): Transaction type.

        credit_party_identifier (str): Credit Party Identifier. Can be a Mobile Number, Business Number, Agent Till, Paybill or Business number, or Merchant Buy Goods.

    Returns:
        str: JSON formatted M-PESA API response
    """
    try:
        # Retrieve stored token
        app_ctx = ctx.request_context.lifespan_context
        access_token = app_ctx.access_token
    

        # Generate QR code
        response = await qr_code(
            access_token,
            merchant_name,
            transaction_reference_no,
            amount,
            transaction_type,
            credit_party_identifier,
        )
        # Return response
        return json.dumps(response, indent=2)

    except Exception as e:
        return f"Failed to generate QR code: {str(e)}"


# ===============================================
# UNSTRUCTURED TOOLS
# ===============================================


@mcp.tool()
async def create_source(ctx: Context, connector_name: str):
    """
    This tool help create a connector from data source to unstructured server where will be processed

    Args:
        connector_name (str): The name of the source connector to create.

    Returns:
        str: String
    """
    unstructured_pipeline = ctx.request_context.lifespan_context.unstructured_pipeline

    response = await unstructured_pipeline.create_source_connector(connector_name)

    return (
        f"Source Connector name: {response.name} \n Source Connector id: {response.id}"
    )


@mcp.tool()
async def create_destination(ctx: Context, connector_name: str):
    """
    This tool help create a connector from unstructured server  to destination where the data will be stored

    Args:
        connector_name (str): The name of the destination connector to create.

    Returns:
        str: String
    """
    unstructured_pipeline = ctx.request_context.lifespan_context.unstructured_pipeline

    response = await unstructured_pipeline.create_destination_connector(connector_name)

    return f"Connector name: {response.name} \n Connector id: {response.id}"


@mcp.tool()
async def create_workflow(
    ctx: Context, workflow_name: str, source_id: str, destination_id: str
):
    """
    This tool help create a workflow the workflow to process the data from the source connector to the destination connector

    Args:
        workflow_name (str): The name of the workflow to create.
        source_id (str): The id of the source connector.
        destination_id (str): The id of the destination connector.

    Returns:
        str: String
    """
    unstructured_pipeline = ctx.request_context.lifespan_context.unstructured_pipeline

    response = await unstructured_pipeline.create_workflow_unstructured(
        workflow_name, source_id, destination_id
    )

    return f"Workflow name: {response.name} \n Workflow id: {response.id} \n Workflow status: {response.status} \n Workflow type: {response.workflow_type} \n Source(s): {response.sources} \n Destination(s): {response.destinations} \n Schedule(s): {response.schedule.crontab_entries}"


@mcp.tool()
async def run_workflow(ctx: Context, workflow_id: str):
    """
    This tool help run a workflow.

    Args:
        workflow_id (str): The id of the workflow to run.

    Returns:
        str: String
    """
    unstructured_pipeline = ctx.request_context.lifespan_context.unstructured_pipeline

    response = await unstructured_pipeline.run_workflow_unstructured(workflow_id)

    return f"{response}"


@mcp.tool()
async def get_workflow_details(ctx: Context, workflow_id: str):
    """
    This tool help get a workflow details. such as name, id, status, type, sources, destinations, schedule.

    Args:
        workflow_id (str): The id of the workflow to get details.

    Returns:
        str: String
    """
    unstructured_pipeline = ctx.request_context.lifespan_context.unstructured_pipeline

    response = await unstructured_pipeline.get_workflow(workflow_id)

    return f"Workflow name: {response.name} \n Workflow id: {response.id} \n Workflow status: {response.status}"


@mcp.tool()
async def fetch_documents():
    """
    This tool will help fetch the document analyzed during the workflow execution

    Returns:
        str: String
    """
    return get_analyzed_documents()


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
async def create_and_run_workflow_prompt(user_input: str):
    """
    This prompt help to create a source connector and a destination connector, then setting up the workflow and executing it.

    Args:
        user_input (str): The user input.

    Returns:
        str: String
    """
    return f"The user wants to achieve {user_input}. Assist them by creating a source connector and a destination connector, then setting up the workflow and executing it."


def main():
    # Start the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
