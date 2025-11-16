import pytest
from mcp import FastMCP
from awesome_copilot.tools import register_tools




@pytest.mark.asyncio
async def test_add_tool():
    mcp = FastMCP(server_name="test")
    register_tools(mcp)
    res = await mcp.call_tool("utils.add", {"a": 2, "b": 3})
    assert res["result"] == 5