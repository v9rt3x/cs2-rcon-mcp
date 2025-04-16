import os
from dataclasses import dataclass
import logging
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class ServerConfig:
    """Configuration for the CS2 server connection."""
    host: str
    port: int
    password: str

    @classmethod
    def from_env(cls) -> 'ServerConfig':
        """Create a ServerConfig instance from environment variables.
        
        Returns:
            ServerConfig: The configured server settings.
            
        Raises:
            ValueError: If required environment variables are missing or invalid.
        """
        host = os.getenv("HOST")
        port = os.getenv("SERVER_PORT")
        password = os.getenv("RCON_PASSWORD")

        if not all([host, port, password]):
            raise ValueError(
                "Missing required environment variables: HOST, SERVER_PORT, RCON_PASSWORD"
            )

        try:
            port_int = int(port)
        except ValueError:
            raise ValueError(f"Invalid SERVER_PORT value: {port}")

        return cls(host=host, port=port_int, password=password)

@dataclass
class AppConfig:
    """Configuration for the MCP application."""
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8080

    @classmethod
    def from_args(cls, args: Optional[dict] = None) -> 'AppConfig':
        """Create an AppConfig instance from command line arguments.
        
        Args:
            args: Optional dictionary of command line arguments.
            
        Returns:
            AppConfig: The configured application settings.
        """
        if args is None:
            return cls()
        return cls(
            debug=args.get("debug", False),
            host=args.get("host", "0.0.0.0"),
            port=args.get("port", 8080)
        ) 