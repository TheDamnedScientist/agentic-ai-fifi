# cli.py

import os
from backend.mcp_client import call_tool
from backend.mock_flow.gemini_mock import detect_tool

def main():
    session_id = os.getenv("MCP_SESSION_ID")
    if not session_id:
        session_id = input("🔐 Enter your MCP session ID (first time login): ").strip()

    print("\n💬 Welcome to your Financial Assistant (Mock Gemini CLI)\n")
    print("Type a question like:")
    print(" - What's my net worth?")
    print(" - Show me my EPF details.")
    print(" - What is my credit score?\n")

    while True:
        try:
            user_input = input("🧑 You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                print("👋 Bye!")
                break

            tool = detect_tool(user_input)
            if not tool:
                print("🤖 Gemini: Sorry, I don't know how to answer that yet.\n")
                continue

            print(f"🤖 Gemini: Calling `{tool}` tool...\n")
            result = call_tool(tool, session_id)
            print(f"📊 Result:\n{result}\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break

if __name__ == "__main__":
    main()
