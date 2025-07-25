from backend.mcp_client import list_tools, call_tool
import os
import google.generativeai as genai

with open("gemini_api.txt", "r") as fin:
    api_key = fin.read().strip()
    
# genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
genai.configure(api_key=api_key)

class agent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            tools=list_tools(session_id)
        )
        self.convo = self.model.start_chat()

    def call_gemini(self, prompt: str) -> str:

        response = self.convo.send_message(prompt)

        messages = response.candidates[0].content.parts
        tool_outputs = []

        for part in messages:
            if hasattr(part, "function_call"):
                tool_call = part.function_call
                tool_name = tool_call.name
                
                if not tool_name:
                    print("⚠️ Skipping tool call with no name\n")
                    continue

                print(f"Calling tool: {tool_name}")

                result = call_tool(tool_name, self.session_id)
                tool_outputs.append((tool_name, result))

        if tool_outputs:
            followup = "\n\n".join(
                f"Result of `{name}`:\n{output}" for name, output in tool_outputs
            )
            final_response = self.convo.send_message(followup)
            return final_response.text
        
        return response.text

    def call_gemini_for_dashboard(self, dashboard: str) -> str:
        response = self.convo.send_message(f"Generate data to fetch {dashboard} information and display it in a format that can be used in a streamlit dashboard.")

        if response.candidates[0].content.parts[0].function_call:
            tool_call = response.candidates[0].content.parts[0].function_call
            tool_name = tool_call.name

            tool_response = call_tool(tool_name, self.session_id)

            # Continue conversation with tool output
            final = self.convo.send_message(f"Here is the result of {tool_name}:\n{tool_response}")
            return final.text

        return response.text