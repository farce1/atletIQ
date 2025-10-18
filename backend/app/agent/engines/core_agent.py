import asyncio
import logging
from typing import Any, AsyncIterator, Dict, List, Optional
from uuid import UUID

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ClaudeSDKClient,
    AssistantMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
    CLINotFoundError,
    ProcessError,
    CLIJSONDecodeError,
    McpServerConfig,
)
from pydantic import BaseModel

from app.core.config import get_settings

from app.agent.prompts.agent_prompts import TEXT_QUERY_EXTRACT_PROMPT

logger = logging.getLogger(__name__)
settings = get_settings()


def create_mcp_http_server_config(
    name: str, url: str, headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Create an MCP HTTP server configuration.
    
    Args:
        name: Name of the MCP server
        url: URL of the MCP server
        headers: Optional headers for the HTTP request
        
    Returns:
        Dict[str, Any]: Configuration for the MCP HTTP server
    """
    config: Dict[str, Any] = {
        "type": "http",
        "url": url,
    }
    if headers:
        config["headers"] = headers
    return config


class ConversationContext(BaseModel):
    """Context for maintaining conversation state."""

    session_id: UUID
    conversation_history: List[Dict[str, Any]] = []
    current_topic: Optional[str] = None
    user_preferences: Dict[str, Any] = {}


class ClaudeAgent:
    """
    Claude Agent for handling conversations using the Claude Agent SDK.

    This class provides a high-level interface for managing conversations
    with Claude, including context management, error handling, and streaming responses.
    """

    def __init__(
        self,
        system_prompt: Optional[str] = None,
        allowed_tools: Optional[List[str]] = None,
        permission_mode: str = "bypassPermissions",
        cwd: Optional[str] = None,
        max_conversation_length: int = 50,
        mcp_servers: Optional[Dict[str, Dict[str, Any]]] = None,
    ):
        """
        Initialize the Claude Agent.

        Args:
            system_prompt: Custom system prompt for the agent
            allowed_tools: List of allowed tools for the agent
            permission_mode: Permission mode for tool usage
            cwd: Working directory for the agent
            max_conversation_length: Maximum number of messages to keep in context
            mcp_servers: Dictionary of MCP server configurations
        """
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.allowed_tools = allowed_tools or ["Read", "Write", "Bash", "WebSearch"]
        self.permission_mode = permission_mode
        self.cwd = cwd
        self.max_conversation_length = max_conversation_length
        self.mcp_servers = mcp_servers or {}

        # Conversation contexts by session ID
        self._conversations: Dict[UUID, ConversationContext] = {}

        # Agent options
        self._agent_options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=self.allowed_tools,
            permission_mode=self.permission_mode,
            cwd=self.cwd,
            mcp_servers=self.mcp_servers,
        )

    def _get_default_system_prompt(self) -> str:
        """Get the default system prompt for the agent."""
        return """
You are a specialized, intelligent AI assistant designated to help users with their queries.
You are helpful, accurate, and provide detailed responses when appropriate.
When using tools, be efficient and explain what you're doing.
Always maintain a professional and friendly tone.
"""

    def _get_conversation_context(self, session_id: UUID) -> ConversationContext:
        """Get or create conversation context for a session."""
        if session_id not in self._conversations:
            self._conversations[session_id] = ConversationContext(session_id=session_id)
        return self._conversations[session_id]

    def _update_conversation_history(
        self,
        session_id: UUID,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update conversation history for a session."""
        context = self._get_conversation_context(session_id)

        message = {
            "role": role,
            "content": content,
            "timestamp": asyncio.get_event_loop().time(),
        }

        if metadata:
            message["metadata"] = metadata

        context.conversation_history.append(message)

        # Trim conversation history if it exceeds max length
        if len(context.conversation_history) > self.max_conversation_length:
            context.conversation_history = context.conversation_history[
                -self.max_conversation_length :
            ]

    def _build_conversation_context(self, session_id: UUID) -> str:
        """Build conversation context from history."""
        context = self._get_conversation_context(session_id)

        if not context.conversation_history:
            return ""

        context_parts = ["Previous conversation context:"]
        for msg in context.conversation_history[-10:]:  # Last 10 messages
            role = msg["role"]
            content = msg["content"]
            context_parts.append(f"{role}: {content}")

        return "\n".join(context_parts)

    async def process_message(
        self, session_id: UUID, message: str, stream: bool = False
    ) -> str | AsyncIterator[str]:
        """
        Process a user message and return Claude's response.

        Args:
            session_id: Unique session identifier
            message: User message to process
            stream: Whether to stream the response

        Returns:
            Claude's response as string or async iterator for streaming
        """
        try:
            # Update conversation history
            self._update_conversation_history(session_id, "user", message)

            # Build context-aware prompt
            conversation_context = self._build_conversation_context(session_id)
            full_prompt = f"{conversation_context}\n\nUser: {message}"

            if stream:
                return self._process_message_stream(session_id, full_prompt)
            else:
                return await self._process_message_sync(session_id, full_prompt)

        except CLINotFoundError:
            error_msg = (
                "Claude Code CLI not found. Please ensure it is installed in the container. "
                "The CLI should be installed during the Docker build process. "
                "If you're running locally, install with: npm install -g @anthropic-ai/claude-code"
            )
            logger.error(error_msg)
            raise ClaudeAgentError("Claude Code CLI not installed")
        except ProcessError as e:
            logger.error(f"Claude process failed with exit code: {e.exit_code}")
            raise ClaudeAgentError(f"Claude process failed: {e}")
        except CLIJSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {e}")
            raise ClaudeAgentError(f"Failed to parse response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in Claude agent: {e}")
            raise ClaudeAgentError(f"Unexpected error: {e}")

    async def _process_message_sync(self, session_id: UUID, prompt: str) -> str:
        """Process message synchronously and return full response."""
        response_parts = []

        async with ClaudeSDKClient(options=self._agent_options) as client:
            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_parts.append(block.text)
                        elif isinstance(block, ToolUseBlock):
                            logger.info(f"Using tool: {block.name}")
                        elif isinstance(block, ToolResultBlock):
                            logger.info(f"Tool {block.name} completed")

        full_response = "".join(response_parts)

        # Update conversation history with response
        self._update_conversation_history(session_id, "assistant", full_response)

        return full_response

    async def _process_message_stream(
        self, session_id: UUID, prompt: str
    ) -> AsyncIterator[str]:
        """Process message with streaming response."""
        response_buffer = []

        async with ClaudeSDKClient(options=self._agent_options) as client:
            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            response_buffer.append(block.text)
                            yield block.text
                        elif isinstance(block, ToolUseBlock):
                            logger.info(f"Using tool: {block.name}")
                            yield f"\n[Using tool: {block.name}]\n"
                        elif isinstance(block, ToolResultBlock):
                            logger.info(f"Tool {block.name} completed")
                            yield f"\n[Tool {block.name} completed]\n"

        # Update conversation history with complete response
        full_response = "".join(response_buffer)
        self._update_conversation_history(session_id, "assistant", full_response)

    def get_conversation_history(self, session_id: UUID) -> List[Dict[str, Any]]:
        """Get conversation history for a session."""
        context = self._get_conversation_context(session_id)
        return context.conversation_history.copy()

    def clear_conversation(self, session_id: UUID) -> None:
        """Clear conversation history for a session."""
        if session_id in self._conversations:
            self._conversations[session_id].conversation_history.clear()

    def set_user_preference(self, session_id: UUID, key: str, value: Any) -> None:
        """Set a user preference for a session."""
        context = self._get_conversation_context(session_id)
        context.user_preferences[key] = value

    def get_user_preference(
        self, session_id: UUID, key: str, default: Any = None
    ) -> Any:
        """Get a user preference for a session."""
        context = self._get_conversation_context(session_id)
        return context.user_preferences.get(key, default)

    def update_system_prompt(self, new_prompt: str) -> None:
        """Update the system prompt for the agent."""
        self.system_prompt = new_prompt
        self._agent_options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=self.allowed_tools,
            permission_mode=self.permission_mode,
            cwd=self.cwd,
            mcp_servers=self.mcp_servers,
        )

    def update_mcp_servers(self, mcp_servers: Dict[str, Dict[str, Any]]) -> None:
        """Update the MCP servers for the agent."""
        self.mcp_servers = mcp_servers
        self._agent_options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=self.allowed_tools,
            permission_mode=self.permission_mode,
            cwd=self.cwd,
            mcp_servers=self.mcp_servers,
        )

    def add_mcp_server(self, name: str, config: Dict[str, Any]) -> None:
        """Add a single MCP server to the agent."""
        self.mcp_servers[name] = config
        self._agent_options = ClaudeAgentOptions(
            system_prompt=self.system_prompt,
            allowed_tools=self.allowed_tools,
            permission_mode=self.permission_mode,
            cwd=self.cwd,
            mcp_servers=self.mcp_servers,
        )

    def remove_mcp_server(self, name: str) -> None:
        """Remove an MCP server from the agent."""
        if name in self.mcp_servers:
            del self.mcp_servers[name]
            self._agent_options = ClaudeAgentOptions(
                system_prompt=self.system_prompt,
                allowed_tools=self.allowed_tools,
                permission_mode=self.permission_mode,
                cwd=self.cwd,
                mcp_servers=self.mcp_servers,
            )

    def get_session_stats(self, session_id: UUID) -> Dict[str, Any]:
        """Get statistics for a session."""
        context = self._get_conversation_context(session_id)
        return {
            "session_id": str(session_id),
            "message_count": len(context.conversation_history),
            "current_topic": context.current_topic,
            "user_preferences": context.user_preferences,
        }


class ClaudeAgentError(Exception):
    """Custom exception for Claude agent errors."""

    pass


# Global agent instances
_global_agent: Optional[ClaudeAgent] = None
_global_extractor_agent: Optional[ClaudeAgent] = None


def get_claude_agent() -> ClaudeAgent:
    """Get the global Claude agent instance."""
    global _global_agent
    if _global_agent is None:
        _global_agent = ClaudeAgent(
            system_prompt=settings.CLAUDE_AGENT_SYSTEM_PROMPT,
            allowed_tools=[
                "mcp__healthion_mcp_server__fetch_workouts"
            ],
            permission_mode=settings.CLAUDE_AGENT_PERMISSION_MODE,
            cwd=settings.CLAUDE_AGENT_WORKING_DIR,
            max_conversation_length=settings.CLAUDE_AGENT_MAX_CONVERSATION_LENGTH,
            mcp_servers=settings.CLAUDE_AGENT_MCP_SERVERS,
        )
    return _global_agent


def get_extractor_claude_agent() -> ClaudeAgent:
    """Get the global extractor Claude agent instance."""
    global _global_extractor_agent
    if _global_extractor_agent is None:
        _global_extractor_agent = ClaudeAgent(
            system_prompt=TEXT_QUERY_EXTRACT_PROMPT,
            allowed_tools=[],
            permission_mode="acceptEdits",
            cwd=None,
            max_conversation_length=50,
            mcp_servers={},
        )
    return _global_extractor_agent


def create_general_agent() -> ClaudeAgent:
    """Create a new general-purpose Claude agent instance."""
    return ClaudeAgent(
        system_prompt="You are a helpful AI assistant specialized in general queries and tasks.",
        allowed_tools=["Read", "Write", "Bash", "WebSearch"],
        permission_mode="acceptEdits",
        mcp_servers={},
    )


def create_specialized_agent(
    specialization: str, custom_tools: Optional[List[str]] = None
) -> ClaudeAgent:
    """Create a specialized Claude agent instance."""
    system_prompt = f"You are a specialized AI assistant focused on {specialization}."

    tools = custom_tools or ["Read", "Write", "Bash", "WebSearch"]

    return ClaudeAgent(
        system_prompt=system_prompt,
        allowed_tools=tools,
        permission_mode="acceptEdits",
        mcp_servers={},
    )
