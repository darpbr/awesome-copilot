# server.py
import asyncio
import logging
from typing import Any

# Ajuste import conforme o SDK instalado; você já mostrou FastMCP disponível.
from fastmcp import FastMCP

from config import Settings
from tools import register_tools  # ajuste o caminho se for package (ex: from awesome_copilot.tools import register_tools)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-server")

settings = Settings()


def create_mcp() -> FastMCP:
    """
    Cria a instância do FastMCP usando os argumentos corretos (name, version, host, port).
    Mantemos defensiva: se a assinatura do construtor não aceitar algum argumento,
    tentamos com menos argumentos.
    """
    kwargs: dict[str, Any] = {}
    # parâmetros conhecidos da sua versão
    if getattr(settings, "server_name", None):
        kwargs["name"] = settings.server_name
    else:
        # manter compatibilidade: name is primary param
        kwargs["name"] = getattr(settings, "name", "my-company/mcp")

    if getattr(settings, "version", None):
        kwargs["version"] = settings.version
    if getattr(settings, "host", None):
        kwargs["host"] = settings.host
    if getattr(settings, "port", None):
        kwargs["port"] = settings.port

    # tente construir com os kwargs; se falhar, tente com menos argumentos
    try:
        mcp = FastMCP(**kwargs)
    except TypeError as e:
        logger.warning("Construtor FastMCP não aceitou kwargs %s — tentando sem host/port: %s", kwargs, e)
        reduced = {k: v for k, v in kwargs.items() if k in ("name", "version")}
        mcp = FastMCP(**reduced)

    # registra tools/resources/prompts
    try:
        register_tools(mcp)
    except Exception as e:
        logger.exception("Erro ao registrar tools: %s", e)

    return mcp


async def run_with_transport(mcp: FastMCP, transport: str) -> None:
    """
    Chama o método de execução apropriado do FastMCP dependendo do transporte pedido.
    Faz fallback para run_async() se métodos específicos não existirem.
    """
    t = (transport or "stdio").lower()
    logger.info("Executando MCP com transporte '%s'...", t)

    # Priorize chamadas explícitas se existirem
    if t == "stdio":
        if hasattr(mcp, "run_stdio_async"):
            await mcp.run_stdio_async()
            return
        # fallback
        if hasattr(mcp, "run_async"):
            await mcp.run_async()
            return

    if t in ("sse", "http-sse", "server-sent-events"):
        if hasattr(mcp, "run_sse_async"):
            # tente passar host/port se aceito
            try:
                await mcp.run_sse_async(host=settings.host, port=settings.port)
            except TypeError:
                await mcp.run_sse_async()
            return

    if t in ("streamable-http", "streamable_http", "streamable"):
        if hasattr(mcp, "run_streamable_http_async"):
            try:
                await mcp.run_streamable_http_async(host=settings.host, port=settings.port)
            except TypeError:
                await mcp.run_streamable_http_async()
            return

    # Generic HTTP fallback: algumas versões usam run_http_async/run_async
    if hasattr(mcp, "run_http_async"):
        try:
            await mcp.run_http_async(host=settings.host, port=settings.port)
            return
        except TypeError:
            await mcp.run_http_async()
            return

    # Último recurso: run_async se disponível
    if hasattr(mcp, "run_async"):
        await mcp.run_async()
        return

    # Se nenhuma função de run disponível, raise
    raise RuntimeError("Nenhum método de execução compatível encontrado no FastMCP.")


async def main() -> None:
    mcp = create_mcp()
    logger.info("MCP criado: name=%s version=%s", getattr(mcp, "name", None), getattr(mcp, "version", None))
    await run_with_transport(mcp, settings.transport)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("MCP server encerrado")
    except Exception as exc:
        logger.exception("Erro ao iniciar MCP: %s", exc)
        raise
