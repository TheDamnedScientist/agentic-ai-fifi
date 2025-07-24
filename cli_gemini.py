# cli.py

import os
from mcp_client import call_tool
from gemini_client import agent

def main():
    session_id = os.getenv("MCP_SESSION_ID")
    if not session_id:
        session_id = input("🔐 Enter your MCP session ID (first time login): ").strip()

    gemini_agent = agent(session_id)

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

            response = gemini_agent.call_gemini(user_input)

            # result = call_tool(tool, session_id)
            print(f"📊 Result:\n{response}\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break

if __name__ == "__main__":
    main()
