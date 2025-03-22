from mcp.server.fastmcp import FastMCP
from daraja.auth.generate_access_token import get_access_token

# Initialize the MCP server
mcp = FastMCP("Daraja MCP", "1.0.0")


def main():
    print("Hello from darajamcp!")

    # Demonstrate getting an access token
    try:
        token_info = get_access_token()
        print(f"Access Token: {token_info['access_token']}")
        print(f"Expires in: {token_info['expires_in']} seconds")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
