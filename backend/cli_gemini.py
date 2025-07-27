import json
import os
from backend.gemini_client import agent
from pathlib import Path

history_file = Path("backend/context_store/chat_history.json")

def main():
    session_id = os.getenv("MCP_SESSION_ID")
    if not session_id:
        session_id = input("🔐 Enter your MCP session ID (first time login): ").strip()

    gemini_agent = agent(session_id)

    print("\n💬 Welcome to your Financial Assistant\n")
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
            print(f"📊 Result:\n{response}\n")

        except KeyboardInterrupt:
            print("\n👋 Exiting.")
            break
        
    history = gemini_agent.chat.get_history()
    json_history = [item.to_json_dict() for item in history]
    
    with open(history_file, "w") as f:
        json.dump(json_history, f, indent=2)
        
if __name__ == "__main__":
    main()  
