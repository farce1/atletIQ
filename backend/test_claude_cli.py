#!/usr/bin/env python3
"""
Test script to verify Claude Code CLI installation and basic functionality.
"""

import asyncio
import sys
from uuid import uuid4

from app.agent.engines.core_agent import get_claude_agent


async def test_claude_cli():
    """Test basic Claude CLI functionality."""
    print("Testing Claude Code CLI installation...")

    try:
        # Get the global agent instance
        agent = get_claude_agent()
        session_id = uuid4()

        print("✅ Claude agent created successfully")
        print(f"Session ID: {session_id}")

        # Test a simple message
        print("Testing simple message processing...")
        response = await agent.process_message(
            session_id=session_id,
            message="Hello! Can you say 'Hello World' back to me?",
        )

        print(f"✅ Response received: {response[:100]}...")
        print("✅ Claude Code CLI is working correctly!")

        return True

    except Exception as e:
        print(f"❌ Error testing Claude CLI: {e}")
        return False


async def main():
    """Run the test."""
    print("Claude Code CLI Test")
    print("=" * 50)

    success = await test_claude_cli()

    if success:
        print("\n🎉 All tests passed! Claude Code CLI is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Tests failed! Please check the installation.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
