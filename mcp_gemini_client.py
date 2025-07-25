from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import asyncio
from google import genai
import os
from google.genai import types
import json
from pathlib import Path


API_KEY = os.getenv("GOOGLE_AI_STUDIO_API_KEY")

client = genai.Client(api_key=API_KEY)
session_id = "mcp-session-8c84c952-118c-4ace-b79b-e21c26b57b51"
headers = {
        "Content-Type": "application/json",
        "Mcp-Session-Id": session_id
    }

history = Path("backend/context_store/chat_history.json")
if history.exists():
    with open(history, "r") as f:
        chat_history = json.load(f)
else:
    chat_history = []

agent_behavior = open("backend/context_store/behavior.txt", "r").read()

async def main():
    # try:
        async with streamablehttp_client("http://localhost:8080/mcp/stream", headers=headers) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:
                # try:
                    await session.initialize()

                    tools = await session.list_tools()
                    # Check if login is required
                    res = await session.call_tool("fetch_bank_transactions", {})
                    res_dict: dict = eval(res.content[0].text)
                    if res_dict.get("status") == "login_required":
                        login_url = res_dict["login_url"]
                        print("Please open the following login URL in your browser:")
                        print(login_url)

                        input("Press Enter after you've completed the login...")
                    chat = client.aio.chats.create(
                        model="gemini-2.5-flash",
                        config=genai.types.GenerateContentConfig(
                        temperature=0,
                        tools=[session],
                        system_instruction=agent_behavior,
                        ),
                        history=chat_history
                    )
                    while user_input := input("You: "):
                        if user_input.lower() == "exit":
                            break
                        response = await chat.send_message(user_input)
                        print("Model: ", response.text)
                    print("Chat ended.")
                    history = chat.get_history()
                    json_history = [item.to_json_dict() for item in history]
                    with open(history, "w") as f:
                        json.dump(json_history, f, indent=2)
                # except Exception as e:
                #     print(f"error: {e}")
    # except asyncio.exceptions.CancelledError:
    #     print("Process interrupted by user.")
    # except Exception as e:
    #     print(f"error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

