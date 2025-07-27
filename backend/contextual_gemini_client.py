from backend.context_store.context_manager import contextTools
from backend.mcp_client import list_tools, call_tool
from google import genai
from google.genai.types import Tool, FunctionDeclaration
from pathlib import Path
import inspect
import json
import os

with open("gemini_api.txt", "r") as fin:
    api_key = fin.read().strip()
    
client = genai.Client(api_key=api_key)
agent_behavior = open("backend/context_store/behavior.txt", "r").read()

CONTEXT_DIR = Path("backend/context_store/memory")
    
def send_notification(message: str):
    """
    Send a notification to the user.
    This is a placeholder function. Replace with actual notification logic.
    """
    print(f"🔔 Notification: {message}")

def get_context_path(user_id: str) -> str:
    """
    Get the path to the context file for a given user ID.
    Args:
        user_id (str): The user ID for which to get the context path.
    Returns:
        str: The path to the context file.
    """
    user_path = os.path.join(CONTEXT_DIR, user_id, 'context.json')

    return user_path

def load_context(user_id: str):
    """
    Load the context for the user.
    Args:
        user_id (str): The user ID for which to load the context.
    Returns:
        dict: The context data for the user.
    """
    path = get_context_path(user_id)
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_context(user_id: str, ctx: dict):
    """
    Save the context for the user.
    Args:
        user_id (str): The user ID for which to save the context.
        ctx (dict): The context data to save.
    """
    path = get_context_path(user_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(ctx, f, indent=2)
        
    return "Context updated."

def update_context(user_id: str, updates: dict):
    """
    Update the context with new data.
    Args:
        user_id (str): The user ID for which to update the context.
        updates (dict): A dictionary containing the updates to apply to the context.
    Returns:
        dict: The updated context.
    """
    ctx = load_context(user_id)
    for section in updates:
        if not isinstance(updates[section], dict):
            raise ValueError(f"Updates for section '{section}' must be a dictionary.")
        else:
            ctx[section] = updates[section]
    save_context(user_id, ctx)
    
    return ctx

history_file = Path("backend/context_store/chat_history.json")
if history_file.exists():
    with open(history_file, "r") as f:
        chat_history = json.load(f)
else:
    chat_history = []
    
def create_function_declaration(func):
    """
    Create a FunctionDeclaration from a Python function with proper parameter extraction.
    """
    sig = inspect.signature(func)
    parameters = {}
    required = []
    
    for name, param in sig.parameters.items():
        param_info = {"type": "string"}
        
        if param.annotation != param.empty:
            if param.annotation == str:
                param_info["type"] = "string"
            elif param.annotation == int:
                param_info["type"] = "integer"
            elif param.annotation == float:
                param_info["type"] = "number"
            elif param.annotation == bool:
                param_info["type"] = "boolean"
            elif param.annotation == dict:
                param_info["type"] = "object"
        
        parameters[name] = param_info
        
        if param.default == param.empty:
            required.append(name)
    
    return FunctionDeclaration(
        name=func.__name__,
        description=func.__doc__ or f"Function {func.__name__}",
        parameters={
            "type": "object",
            "properties": parameters,
            "required": required
        }
    )

class agent:
    def __init__(self, session_id: str):
        self.session_id = session_id
        dummy_call = call_tool("whoami", self.session_id)
        res_dict: dict = eval(dummy_call)
        if res_dict.get("status") == "login_required":
            login_url = res_dict["login_url"]
            print("Please open the following login URL in your browser:")
            print(login_url)

            input("Press Enter after you've completed the login...")
        else:
            self.user_id = res_dict.get("phoneNumber")
        
        mcp_tools = list_tools(session_id)
        auto_callable_tools = [
            create_function_declaration(send_notification),
            create_function_declaration(update_context)
        ]
        all_tools = [Tool(function_declarations=mcp_tools + auto_callable_tools)]
        
        self.chat = client.chats.create(
            model="gemini-2.0-flash",
            config=genai.types.GenerateContentConfig(
                temperature=0,
                tools=all_tools,
                system_instruction=[
                    agent_behavior,
                    """
                    IMPORTANT TOOL USAGE INSTRUCTIONS:
                    - For MCP tools (from external services), only return the function call without executing
                    - For local tools (send_notification, update_context), execute them directly
                    - MCP tools will be handled by the backend system
                    - Update the context without user prompt in a proper format (json) whenever you feel necessary
                    """
                ],
            ),
            history=chat_history,
        )
        
        self.mcp_tool_names = {tool["name"] for tool in mcp_tools}

    def call_gemini(self, prompt: str) -> str:
        user_id = self.user_id
        response = self.chat.send_message(prompt)

        messages = response.candidates[0].content.parts
        tool_outputs = []
        text_parts = []

        for part in messages:
            if hasattr(part, "function_call") and part.function_call:
                tool_call = part.function_call                
                tool_name = tool_call.name
                tool_args = tool_call.args if hasattr(tool_call, 'args') else {}
                
                if not tool_name:
                    continue

                print(f"Calling tool: {tool_name} with args: {tool_args}")

                if tool_name in self.mcp_tool_names:
                    result = call_tool(tool_name, self.session_id)
                    tool_outputs.append((tool_name, result))
                else:
                    try:
                        if tool_name == "send_notification":
                            result = send_notification(tool_args.get("message", ""))
                            tool_outputs.append((tool_name, result or "Notification sent"))
                        elif tool_name == "update_context":
                            result = update_context(self.user_id, tool_args.get("updates", {}))
                            tool_outputs.append((tool_name, result or "Context updated"))
                        else:
                            print(f"Warning: Unknown local tool {tool_name}")
                    except Exception as e:
                        print(f"Error executing {tool_name}: {e}")
                        tool_outputs.append((tool_name, f"Error: {str(e)}"))
            
            elif hasattr(part, "text") and part.text:
                text_parts.append(part.text)

        combined_text = "".join(text_parts)

        if tool_outputs:
            followup_parts = []
            if combined_text.strip():
                followup_parts.append(combined_text)
            
            tool_results = "\n\n".join(
                f"Result of `{name}`:\n{output}" for name, output in tool_outputs
            )
            followup_parts.append(tool_results)
            
            followup = "\n\n".join(followup_parts)
            final_response = self.chat.send_message(followup)
            return final_response.text
                
        return combined_text if combined_text else "No response generated."

    def call_gemini_for_dashboard(self, dashboard: str) -> str:
        response = self.chat.send_message(f"Generate data to fetch {dashboard} information and display it in a format that can be used in a streamlit dashboard.")

        if response.candidates[0].content.parts[0].function_call:
            tool_call = response.candidates[0].content.parts[0].function_call
            tool_name = tool_call.name

            tool_response = call_tool(tool_name, self.session_id)

            final = self.chat.send_message(f"Here is the result of {tool_name}:\n{tool_response}")
            return final.text

        return response.text