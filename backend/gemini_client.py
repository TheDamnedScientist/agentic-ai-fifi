from backend.mcp_client import list_tools, call_tool
from google.generativeai.types import content_types
from pathlib import Path
import json
import os
from google import genai
from google.genai.types import Tool

with open("gemini_api.txt", "r") as fin:
    api_key = fin.read().strip()
    
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
client = genai.Client(api_key=api_key)

history_file = Path("backend/context_store/chat_history.json")
if history_file.exists():
    with open(history_file, "r") as f:
        chat_history = json.load(f)
else:
    chat_history = []
    
agent_behavior = open("backend/context_store/behavior.txt", "r").read()

class agent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.chat = client.chats.create(
                    model="gemini-2.0-flash",
                    config=genai.types.GenerateContentConfig(
                    temperature=0,
                    tools=[Tool(function_declarations=list_tools(session_id)),],
                    system_instruction=agent_behavior,
                    ),
                    history=chat_history
                )
        dummy_call = call_tool("whoami", self.session_id)
        res_dict: dict = eval(dummy_call)
        if res_dict.get("status") == "login_required":
            login_url = res_dict["login_url"]
            print("Please open the following login URL in your browser:")
            print(login_url)

            input("Press Enter after you've completed the login...")
        else:
            self.phone_number = res_dict.get("phone_number")

    def call_gemini(self, prompt: str) -> str:

        response = self.chat.send_message(prompt)

        messages = response.candidates[0].content.parts
        tool_outputs = []

        for part in messages:
            if hasattr(part, "function_call") and part.function_call:
                tool_call = part.function_call                
                tool_name = tool_call.name
                
                if not tool_name:  # Handle blank or None tool name
                    continue

                print(f"Calling tool: {tool_name}")

                result = call_tool(tool_name, self.session_id)
                tool_outputs.append((tool_name, result))

        if tool_outputs:
            followup = "\n\n".join(
                f"Result of `{name}`:\n{output}" for name, output in tool_outputs
            )
            final_response = self.chat.send_message(followup)
            return final_response.text
                
        return response.text

    def call_gemini_for_dashboard(self, dashboard: str) -> str:
        response = self.chat.send_message(f"Generate data to fetch {dashboard} information and display it in a format that can be used in a streamlit dashboard.")

        if response.candidates[0].content.parts[0].function_call:
            tool_call = response.candidates[0].content.parts[0].function_call
            tool_name = tool_call.name

            tool_response = call_tool(tool_name, self.session_id)

            # Continue conversation with tool output
            final = self.chat.send_message(f"Here is the result of {tool_name}:\n{tool_response}")
            return final.text

        return response.text