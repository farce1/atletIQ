# Claude Agent Implementation

This document describes the Claude Agent implementation for handling conversations using the Claude Agent SDK.

## Overview

The Claude Agent provides a high-level interface for managing conversations with Claude, including:
- Context management and conversation history
- Streaming and non-streaming responses
- Error handling and logging
- User preference management
- Tool usage and permissions

## Architecture

### Core Components

1. **ClaudeAgent Class** (`app/agent/engines/core_agent.py`)
   - Main agent class for handling conversations
   - Manages conversation context and history
   - Provides both streaming and non-streaming interfaces

2. **Configuration** (`app/core/config.py`)
   - Claude agent settings in the main configuration
   - Configurable system prompts, tools, and permissions

3. **API Integration** (`app/api/v1/endpoints/agent.py`)
   - REST endpoints for agent interactions
   - Support for both regular and streaming responses

4. **Service Layer** (`app/services/chat.py`)
   - Integration with existing chat service
   - Database persistence of conversations

## Features

### Conversation Management
- **Session-based conversations**: Each conversation is tied to a unique session ID
- **Context awareness**: Maintains conversation history for context-aware responses
- **History trimming**: Automatically trims conversation history to prevent memory issues
- **User preferences**: Store and retrieve user-specific preferences per session

### Response Modes
- **Synchronous**: Get complete response as a single string
- **Streaming**: Receive responses in real-time as they're generated
- **Tool integration**: Automatic tool usage with logging and progress tracking

### Error Handling
- **Graceful degradation**: Falls back to error messages when Claude is unavailable
- **Comprehensive logging**: Detailed error logging for debugging
- **User-friendly errors**: Clear error messages for end users

## Configuration

The Claude agent can be configured through environment variables or the settings file:

```python
# Claude Agent Configuration
CLAUDE_AGENT_SYSTEM_PROMPT: str = "You are a specialized, intelligent AI assistant..."
CLAUDE_AGENT_ALLOWED_TOOLS: list[str] = ["Read", "Write", "Bash", "WebSearch"]
CLAUDE_AGENT_PERMISSION_MODE: str = "acceptEdits"
CLAUDE_AGENT_WORKING_DIR: str | None = None
CLAUDE_AGENT_MAX_CONVERSATION_LENGTH: int = 50
CLAUDE_AGENT_ENABLE_STREAMING: bool = False
```

## Usage

### Basic Usage

```python
from app.agent.engines.core_agent import get_claude_agent
from uuid import uuid4

# Get the global agent instance
agent = get_claude_agent()
session_id = uuid4()

# Process a message (non-streaming by default)
response = await agent.process_message(
    session_id=session_id,
    message="Hello, how can you help me?"
)
print(response)
```

### Streaming Usage

```python
# Process message with streaming (explicitly enable streaming)
async for chunk in agent.process_message(
    session_id=session_id,
    message="Please explain machine learning",
    stream=True
):
    print(chunk, end="", flush=True)
```

### Creating Specialized Agents

```python
from app.agent.engines.core_agent import create_specialized_agent

# Create a coding-specialized agent
coding_agent = create_specialized_agent(
    specialization="Python programming and software development",
    custom_tools=["Read", "Write", "Bash", "WebSearch"]
)
```

### Managing User Preferences

```python
# Set user preferences
agent.set_user_preference(session_id, "programming_language", "Python")
agent.set_user_preference(session_id, "experience_level", "intermediate")

# Get user preferences
lang = agent.get_user_preference(session_id, "programming_language", "Python")
```

## API Endpoints

### Regular Query (Non-Streaming by Default)
```
POST /api/v1/agent/query?chat_session_id={uuid}
Content-Type: application/json

{
    "message": "Hello, how can you help me?"
}
```

### Streaming Query (Explicit Streaming)
```
POST /api/v1/agent/query/stream?chat_session_id={uuid}
Content-Type: application/json

{
    "message": "Please explain machine learning in detail"
}
```

## Dependencies

The implementation requires the following dependencies (already included in `pyproject.toml`):

- `claude-agent-sdk>=0.1.4`: Claude Agent SDK for Python
- `anthropic>=0.71.0`: Anthropic API client
- `fastapi>=0.116.1`: Web framework for API endpoints
- `pydantic>=2.0.0`: Data validation and settings management

## Prerequisites

Before using the Claude agent, ensure that:

1. **Claude Code CLI is installed**:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **Environment variables are set** (if using custom configuration):
   ```bash
   export CLAUDE_AGENT_SYSTEM_PROMPT="Your custom system prompt"
   export CLAUDE_AGENT_ALLOWED_TOOLS="Read,Write,Bash,WebSearch"
   ```

## Error Handling

The agent handles various error scenarios:

- **CLI Not Found**: When Claude Code CLI is not installed
- **Process Errors**: When the Claude process fails
- **JSON Decode Errors**: When response parsing fails
- **General Exceptions**: Unexpected errors with fallback responses

## Example Script

See `example_claude_agent_usage.py` for comprehensive usage examples including:
- Basic conversation handling
- Streaming responses
- Context management
- User preferences
- Error handling

## Performance Considerations

- **Memory Management**: Conversation history is automatically trimmed to prevent memory issues
- **Connection Pooling**: The agent reuses connections when possible
- **Async Operations**: All operations are asynchronous for better performance
- **Error Recovery**: Graceful error handling prevents service disruption

## Security

- **Tool Permissions**: Configurable tool permissions prevent unauthorized actions
- **Session Isolation**: Each session is isolated with its own context
- **Input Validation**: All inputs are validated before processing
- **Error Sanitization**: Error messages are sanitized before being sent to users

## Monitoring and Logging

The agent provides comprehensive logging for:
- Tool usage and execution
- Error conditions and stack traces
- Performance metrics
- User interactions (with privacy considerations)

## Future Enhancements

Potential future improvements include:
- Custom tool development framework
- Advanced conversation analytics
- Multi-modal support (images, documents)
- Integration with external knowledge bases
- Advanced prompt engineering tools
