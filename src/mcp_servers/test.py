import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path

from core.llm_wrapper import LLM

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
            llm = LLM()
            response = llm.generate_with_tools(
                "Create a PDF demonstration of the pythagoras theorem. Make it pretty, don't add images nor latex", 
                mcp_tools.tools
            )
            raw = response["message"]["content"]
            if raw:
                print(raw)
                parsed = json.loads(raw)   # convert string → dict
                arguments = parsed["arguments"]
                print(arguments)
            # 3. Call the PDF creation tool
            # Example: Creating a simple PDF invoice or document
                result = await session.call_tool("pdf-document", arguments=arguments)
                print(f"Server Response: {result}")

if __name__ == "__main__":
    asyncio.run(run_pdf_agent())