from dataclasses import dataclass
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from daraja_endpoints.auth.generate_access_token import get_access_token
import asyncio
from file_processing.unstructured_workflow import UnstructuredPipeline

# Import the registration functions
from mpesa.tools import register_mpesa_tools
from mpesa.prompts import register_mpesa_prompts
from unstructured.tools import register_unstructured_tools
from unstructured.prompts import register_unstructured_prompts


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

# Register all tools and prompts
register_mpesa_tools(mcp)
register_mpesa_prompts(mcp)
register_unstructured_tools(mcp)
register_unstructured_prompts(mcp)


def main():
    # Start the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
