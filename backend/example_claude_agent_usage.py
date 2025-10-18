#!/usr/bin/env python3
"""
Example usage of the Claude Agent for conversation handling.

This script demonstrates how to use the ClaudeAgent class for handling
conversations with Claude using the Agent SDK.
"""

import asyncio
from uuid import uuid4

from app.agent.engines.core_agent import (
    ClaudeAgent,
    create_general_agent,
    create_specialized_agent,
)


async def basic_conversation_example():
    """Example of basic conversation with Claude agent."""
    print("=== Basic Conversation Example ===")

    # Create a new agent instance
    agent = create_general_agent()
    session_id = uuid4()

    # Process a message (non-streaming by default)
    response = await agent.process_message(
        session_id=session_id,
        message="Hello! Can you help me understand what you can do?",
    )

    print("User: Hello! Can you help me understand what you can do?")
    print(f"Claude: {response}")
    print()

    # Follow-up conversation
    response = await agent.process_message(
        session_id=session_id,
        message="Can you write a simple Python function to calculate fibonacci numbers?",
    )

    print(
        "User: Can you write a simple Python function to calculate fibonacci numbers?"
    )
    print(f"Claude: {response}")
    print()


async def streaming_conversation_example():
    """Example of streaming conversation with Claude agent."""
    print("=== Streaming Conversation Example ===")

    # Create a specialized agent for coding
    agent = create_specialized_agent(
        specialization="Python programming and software development",
        custom_tools=["Read", "Write", "Bash"],
    )
    session_id = uuid4()

    print("User: Please create a simple web server using FastAPI")
    print("Claude (streaming): ", end="", flush=True)

    # Process message with streaming
    async for chunk in agent.process_message(
        session_id=session_id,
        message="Please create a simple web server using FastAPI",
        stream=True,
    ):
        print(chunk, end="", flush=True)

    print("\n")


async def conversation_context_example():
    """Example showing conversation context management."""
    print("=== Conversation Context Example ===")

    agent = create_general_agent()
    session_id = uuid4()

    # First message
    response = await agent.process_message(
        session_id=session_id,
        message="My name is Alice and I'm working on a machine learning project.",
    )
    print("User: My name is Alice and I'm working on a machine learning project.")
    print(f"Claude: {response}")
    print()

    # Second message - should remember the context
    response = await agent.process_message(
        session_id=session_id,
        message="What programming language would you recommend for my project?",
    )
    print("User: What programming language would you recommend for my project?")
    print(f"Claude: {response}")
    print()

    # Show conversation history
    history = agent.get_conversation_history(session_id)
    print(f"Conversation history has {len(history)} messages")
    print()


async def user_preferences_example():
    """Example showing user preference management."""
    print("=== User Preferences Example ===")

    agent = create_general_agent()
    session_id = uuid4()

    # Set user preferences
    agent.set_user_preference(session_id, "programming_language", "Python")
    agent.set_user_preference(session_id, "experience_level", "intermediate")
    agent.set_user_preference(session_id, "preferred_style", "detailed explanations")

    # Get session stats
    stats = agent.get_session_stats(session_id)
    print(f"Session stats: {stats}")
    print()


async def error_handling_example():
    """Example showing error handling."""
    print("=== Error Handling Example ===")

    # Create agent with restricted tools
    agent = ClaudeAgent(
        system_prompt="You are a helpful assistant.",
        allowed_tools=["Read"],  # Only allow Read tool
        permission_mode="acceptEdits",
    )
    session_id = uuid4()

    try:
        response = await agent.process_message(
            session_id=session_id,
            message="Please create a new file called test.txt with some content",
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error occurred: {e}")

    print()


async def main():
    """Run all examples."""
    print("Claude Agent Usage Examples")
    print("=" * 50)
    print()

    try:
        await basic_conversation_example()
        await streaming_conversation_example()
        await conversation_context_example()
        await user_preferences_example()
        await error_handling_example()

        print("All examples completed successfully!")

    except Exception as e:
        print(f"Error running examples: {e}")
        print(
            "Make sure Claude Code CLI is installed: npm install -g @anthropic-ai/claude-code"
        )


if __name__ == "__main__":
    asyncio.run(main())
