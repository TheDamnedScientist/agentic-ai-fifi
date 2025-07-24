# gemini_mock.py

TOOL_MAPPING = {
    "net worth": "fetch_net_worth",
    "credit score": "fetch_credit_report",
    "credit report": "fetch_credit_report",
    "epf": "fetch_epf_details",
    "mutual funds": "fetch_mf_transactions",
    "sip": "fetch_mf_transactions",
}

def detect_tool(user_input: str) -> str | None:
    user_input = user_input.lower()
    for keyword, tool in TOOL_MAPPING.items():
        if keyword in user_input:
            return tool
    return None
