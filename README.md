# CS2 RCON MCP

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://cursor.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Model Context Protocol server for CS2 RCON management.

## Description

This project provides a Model Context Protocol (MCP) server interface for managing CS2 game servers via RCON. It allows remote control and monitoring of CS2 servers through a standardized protocol.

![CS2 RCON MCP Demo](cs2-rcon-mcp.gif)

## Features

- Manage your CS2 server in natural language
- RCON command execution
- Manage workshop maps (host, list, change) - [Explore Workshop Maps](https://steamcommunity.com/app/730/workshop/)
- SSE-based communication
- Docker support

## Available Tools

| Tool | Short Description |
|------|-------------------|
| `rcon` | Execute any RCON command |
| `status` | Get current server status |
| `list_workshop_maps` | List all workshop maps on the server |
| `host_workshop_map` | Host a workshop map by its ID |
| `workshop_changelevel` | Change the map to a given workshop map |

## Installation

### Environment Variables

- `HOST`: CS2 server IP
- `SERVER_PORT`: CS2 server port
- `RCON_PASSWORD`: RCON password

### Docker (recommended)

Pull the Docker image from GitHub Container Registry:

```bash
docker pull ghcr.io/v9rt3x/cs2-rcon-mcp:latest
```

### Docker Environment Variables

When running with Docker, you can set the environment variables in two ways:

1. **Directly in the command**:
   ```bash
   docker run -p 8080:8080 \
     -e HOST=your_server_ip \
     -e SERVER_PORT=your_server_port \
     -e RCON_PASSWORD=your_password \
     ghcr.io/v9rt3x/cs2-rcon-mcp:latest
   ```

2. **Using a `.server-env` file**:
   Create a file named `.server-env` with the following content:
   ```
   HOST=your_server_ip
   SERVER_PORT=your_server_port
   RCON_PASSWORD=your_password
   ```

   Then run the container like this:
   ```bash
   docker run -p 8080:8080 --env-file .server-env ghcr.io/v9rt3x/cs2-rcon-mcp:latest
   ```

This provides users with an alternative method to set environment variables, making it easier to manage sensitive information like passwords.

### Connecting from Visual Studio Code (GitHub Copilot)

To configure Visual Studio Code to work with the MCP server, follow these steps:

1. **Start the MCP Server**: Ensure that your MCP server is running before attempting to connect from VS Code.

2. **Open Visual Studio Code**: Launch VS Code and ensure that you have the GitHub Copilot extension installed and configured.

3. **Configure GitHub Copilot**:
   - Change the mode from "Ask" to "Agent" mode.

4. **Add MCP Server Configuration**:
   - Click on the toolbox icon in the upper left corner of the Copilot prompt.
   - Select "Add MCP Server" and choose the option for **HTTP - server-sent events**.

5. **Enter the Server URL**:
   - For the URL, input: `http://localhost:8080/cs2server/sse`. This is the endpoint for the MCP server's SSE connection.

### Alternative: Connecting from Cursor (or any other MCP-Client)

1. Start the MCP server
2. Configure Cursor's MCP settings by creating or updating `~/.cursor/mcp.json`:
   ```json
   {
     "mcpServers": {
       "cs2server": {
         "url": "http://localhost:8080/cs2server/sse"
       }
     }
   }
   ```
3. In Cursor, open the MCP panel (usually in the sidebar)
4. The server should automatically connect using the configured URL

Once connected, you can manage your server in natural language.

Example prompts:

1. "Add 5 bots to the server and start a competitive match on de_dust2"
2. "What's the current server status? How many players are connected and what map are we on?"

Happy fragging! 😊
