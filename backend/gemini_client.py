from backend.mcp_client import list_tools, call_tool
from google.generativeai.types import content_types
from pathlib import Path
import json
import os
from google import genai
from google.genai.types import Tool
from backend import firestore_client

with open("gemini_api.txt", "r") as fin:
    api_key = fin.read().strip()
    
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
client = genai.Client(api_key=api_key)

# history_file = Path("backend/context_store/chat_history.json")
# if history_file.exists():
#     with open(history_file, "r") as f:
#         chat_history = json.load(f)
# else:
#     chat_history = []
    
agent_behavior = open("backend/context_store/behavior.txt", "r").read()

class agent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        dummy_call = call_tool("whoami", self.session_id)
        res_dict: dict = eval(dummy_call)
        self.phone_number = 1414141414
        if res_dict.get("status") == "login_required":
            login_url = res_dict["login_url"]
            print("Please open the following login URL in your browser:")
            print(login_url)

            input("Press Enter after you've completed the login...")
        else:
            self.phone_number = res_dict.get("phoneNumber")
            print(self.phone_number)
        self.fs_client = firestore_client.Client(self.phone_number)
        self.chat = client.chats.create(
                    model="gemini-2.0-flash",
                    config=genai.types.GenerateContentConfig(
                    temperature=0,
                    tools=[Tool(function_declarations=list_tools(session_id)),],
                    system_instruction=self.get_updated_behavior(self.fs_client),
                    ),
                    history=self.fs_client.get_chat_history(),
                )

    @staticmethod
    def get_updated_behavior(fs_client: firestore_client.Client) -> str:
        with open("backend/context_store/behavior.txt", "r") as fin:
            fifi_behavior =  fin.read().strip()
        context = "This is the updated context about user: " + str(fs_client.get_chat_context())
        return fifi_behavior + "\n" + context
    def call_gemini(self, prompt: str) -> str:

        response = self.chat.send_message(prompt)

        messages = response.candidates[0].content.parts
        tool_outputs = []

        for part in messages:
            if hasattr(part, "function_call") and part.function_call:
                tool_call = part.function_call                
                tool_name = tool_call.name
                
                if not tool_name:
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

            final = self.chat.send_message(f"Here is the result of {tool_name}:\n{tool_response}")
            return final.text

        return response.text
    def update_fs(self):
        history = self.chat.get_history()
        self.fs_client.store_chat_history([item.to_json_dict() for item in history])
        context = json.load(open("tmp/mock_ctx.json"))
        self.fs_client.store_chat_context(context)