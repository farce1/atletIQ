#!/usr/bin/env python3
"""
Health check script to verify Claude Code CLI is installed and accessible.
"""

import subprocess
import sys


def check_claude_cli():
    """Check if Claude Code CLI is installed and accessible."""
    try:
        # Try to run claude-code --version
        result = subprocess.run(
            ["claude-code", "--version"], capture_output=True, text=True, timeout=10
        )

        if result.returncode == 0:
            print(f"✅ Claude Code CLI is installed: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Claude Code CLI returned error: {result.stderr}")
            return False

    except FileNotFoundError:
        print(
            "❌ Claude Code CLI not found. Please install it with: npm install -g @anthropic-ai/claude-code"
        )
        return False
    except subprocess.TimeoutExpired:
        print("❌ Claude Code CLI check timed out")
        return False
    except Exception as e:
        print(f"❌ Error checking Claude Code CLI: {e}")
        return False


if __name__ == "__main__":
    if check_claude_cli():
        print("Claude Code CLI health check passed")
        sys.exit(0)
    else:
        print("Claude Code CLI health check failed")
        sys.exit(1)
