# mcp_client.py

import requests
import json

MCP_BASE_URL = "http://localhost:8080/mcp/stream"

def list_tools(session_id: str) -> list:
    """
    List all available tools from the MCP server.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list"
    }

    headers = {
        "Content-Type": "application/json",
        "Mcp-Session-Id": session_id
    }

    try:
        response = requests.post(MCP_BASE_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        tools = data.get("result", {}).get("tools", [])
        
        return [{"name": tool["name"], "description": tool["description"]} for tool in tools]

    except Exception as e:
        return f"❌ Error contacting MCP server: {e}"

def call_tool(tool_name: str, session_id: str) -> str:    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": {}
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Mcp-Session-Id": session_id
    }

    try:
        response = requests.post(MCP_BASE_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        data = response.json()

        content = data.get("result", {}).get("content", [])
        if content and "text" in content[0]:
            return content[0]["text"]

        return f"⚠️ Unexpected response format: {data}"

    except Exception as e:
        return f"❌ Error contacting fi-mcp-dev: {e}"
