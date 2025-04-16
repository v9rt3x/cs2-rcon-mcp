from .config import AppConfig
from .server import MCPServer
from .utils import setup_logging, parse_args
from .commands import mcp_server
import logging

logger = logging.getLogger(__name__)

def main() -> None:
    """Main entry point for the RCON Model Context Protocol application."""
    # Setup logging
    setup_logging()
    
    try:
        # Load configurations
        app_config = AppConfig.from_args(parse_args())
        
        # Create and run the server
        server = MCPServer(mcp_server, app_config)
        server.run()
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main() 