import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

# docs: https://mcpservers.org/servers/github-com-kmalakoff-mcp-pdf

async def run_pdf_agent():
    relative_path = Path("src/generated_artifacts")
    relative_path.mkdir(parents=True, exist_ok=True)
    output_dir = str(relative_path.resolve())

    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@mcp-z/mcp-pdf", f"--resource-store-uri={output_dir}"],
        cwd=output_dir,
    )

    # 2. Connect to the server via stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            mcp_tools = await session.list_tools()
            print(mcp_tools)

            # 3. Call the PDF creation tool
            # Example: Creating a simple PDF invoice or document
            result = await session.call_tool("pdf-document", arguments={
                "filename": "my_report.pdf",
                "content": [
                    {
                        "type": "text",
                        "text": "Hello from my Python Agent!"
                    },
                    {
                        "type": "text",
                        "text": "This line is now properly structured for the PDF server."
                    }
                ]
            })

            print(f"Server Response: {result}")

if __name__ == "__main__":
    asyncio.run(run_pdf_agent())