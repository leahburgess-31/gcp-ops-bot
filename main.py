#!/usr/bin/env python3
"""
GCP Monitoring Bot - Main Entry Point

A QnA interface for monitoring GCP environments using Google Gemini API
"""
import sys

from core.bot import create_bot
from core.utils.env_utils import load_environment_variables


def main():
    """
    Main entry point for the GCP Monitoring Bot
    """
    try:
        load_environment_variables()

        chat = create_bot()

        print("GCP Monitoring Bot started. Type 'q', 'quit', or 'exit' to stop.")
        print("-" * 50)

        while True:
            user_prompt = input("User :> ")
            if user_prompt.lower() in ("q", "quit", "exit"):
                break
            resp = chat.send_message(user_prompt)
            print(f"Bot  :> {resp.text}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
