# atletIQ Backend

## Project setup

### Prerequisites

- uv (https://docs.astral.sh/uv/)

### Steps

- `make build`
- `make run`

## MCP Server Configuration

The atletIQ backend supports MCP (Model Context Protocol) server configuration for enhanced Claude agent capabilities.

### Configuration

MCP servers can be configured in your `.env` file:

```bash
# Example MCP server configuration
CLAUDE_AGENT_MCP_SERVERS={"weather_api": {"type": "http", "url": "https://api.weather.com/mcp", "headers": {"Authorization": "Bearer your-key"}}}
```

### Usage Examples

The MCP server configuration supports:
- Basic MCP server configuration via environment variables
- Dynamic MCP server management at runtime
- Using global agents with MCP servers
- Conversation handling with MCP-enabled agents

### MCP Server Types

Currently supported MCP server types:
- **HTTP**: `{"type": "http", "url": "https://api.example.com/mcp", "headers": {...}}`

### Dynamic Management

You can also manage MCP servers programmatically:

```python
from app.agent.engines.core_agent import ClaudeAgent, create_mcp_http_server_config

# Create agent
agent = ClaudeAgent()

# Add MCP server
agent.add_mcp_server(
    "my_service",
    create_mcp_http_server_config(
        name="my_service",
        url="https://api.myservice.com/mcp",
        headers={"Authorization": "Bearer token"}
    )
)

# Remove MCP server
agent.remove_mcp_server("my_service")
```  
