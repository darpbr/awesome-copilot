import pytest

# import resiliente de FastMCP (se já aplicou o try/except nos testes, mantenha)
try:
    from fastmcp import FastMCP
except Exception:
    try:
        from mcp.server.fastmcp import FastMCP
    except Exception:
        import mcp
        FastMCP = getattr(mcp, "FastMCP", None)
        if FastMCP is None:
            raise ImportError("FastMCP não encontrado")

from awesome_copilot.tools import register_tools


@pytest.mark.asyncio
async def test_add_tool():
    mcp = FastMCP(name="test-mcp", version="1.0")
    register_tools(mcp)

    # Use a API pública call_tool (evita chamar método interno _call_tool)
    # Muitos FastMCP implementam: await mcp.call_tool(tool_name, input_dict)
    res = await mcp.get_tool("utils.add")

    assert res is not None
