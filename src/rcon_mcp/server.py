import logging
from typing import Optional
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
from mcp.server.sse import SseServerTransport
from .config import AppConfig

logger = logging.getLogger(__name__)

class MCPServer:
    """Model Context Protocol server implementation for CS2 server management."""
    
    def __init__(self, mcp_server: Server, config: AppConfig):
        """Initialize the MCP server.
        
        Args:
            mcp_server: The MCP server instance to handle requests.
            config: Application configuration settings.
        """
        self.mcp_server = mcp_server
        self.config = config
        self.sse = SseServerTransport("/cs2server/messages/")
        self.app = self._create_starlette_app()

    def _create_starlette_app(self) -> Starlette:
        """Create the Starlette application with SSE support.
        
        Returns:
            Starlette: The configured Starlette application.
        """
        async def handle_sse(request: Request) -> None:
            """Handle SSE connections for the MCP server.
            
            Args:
                request: The incoming HTTP request.
                
            Raises:
                Exception: If there's an error handling the SSE connection.
            """
            logger.info("Handling new SSE connection")
            try:
                async with self.sse.connect_sse(
                    request.scope,
                    request.receive,
                    request._send,
                ) as (read_stream, write_stream):
                    await self.mcp_server.run(
                        read_stream,
                        write_stream,
                        self.mcp_server.create_initialization_options(),
                    )
            except Exception as e:
                logger.error(f"Error handling SSE connection: {e}")
                raise

        return Starlette(
            debug=self.config.debug,
            routes=[
                Route("/cs2server/sse", endpoint=handle_sse),
                Mount("/cs2server/messages/", app=self.sse.handle_post_message),
            ],
        )

    def run(self) -> None:
        """Run the MCP server."""
        import uvicorn
        logger.info(f"Starting server on {self.config.host}:{self.config.port}")
        uvicorn.run(self.app, host=self.config.host, port=self.config.port) 