from typing import Any, Dict
from pydantic import BaseModel
from fastmcp import FastMCP  # ajuste conforme SDK real
from resources import get_resources


class SumArgs(BaseModel):
    a: float
    b: float


def register_tools(mcp: FastMCP):
    @mcp.tool(
        name="utils.add",
        description="Soma dois números",
    )
    async def add_tool(args: SumArgs) -> Dict[str, Any]:
        return {"result": args.a + args.b}


    # Exemplo de tool que usa recursos
    @mcp.tool(name="store.set", description="Salva um valor em store")
    async def store_set(key: str, value: Any) -> Dict[str, Any]:
        res = get_resources()
        res["store"].set(key, value)
        return {"ok": True}


    @mcp.tool(name="store.get", description="Recupera um valor do store")
    async def store_get(key: str) -> Dict[str, Any]:
        res = get_resources()
        return {"value": res["store"].get(key)}
