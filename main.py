from mcp.server.fastmcp import FastMCP
from daraja.auth.generate_access_token import get_access_token
from daraja.mpesa_express import initiate_stk_push
import json


# Initialize the MCP server
mcp = FastMCP("Daraja MCP", "1.0.0")


@mcp.tool()
def stk_push(amount: int) -> str:
    """
    Prompts the customer to authorize a payment on their mobile device.

    Args:
        amount (int): The amount to be paid.

    Returns:
        str: JSON formatted M-PESA API response
    """
    try:
        response = initiate_stk_push(amount)
        return json.dumps(response, indent=2)
    except Exception as e:
        return f"Failed to initiate STK Push: {str(e)}"


def main():
    # Start the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
