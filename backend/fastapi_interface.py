from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend import uncontextual_gemini_client as gemini_client

app = FastAPI()

class UserRequest(BaseModel):
    session_id: str
class UserMessage(BaseModel):
    msg: str

clients = {}

# @app.post("/update_session_id/")
# def update_session_id(request: UserRequest):
#     try:
#         # Example: create a Firestore client using user_id
#         # (You may want to customize this logic as needed)
#         if not hasattr(clients, "fs_client"):
#             client = firestore_client.Client(user_id=request.user_id)
#             clients["fs_client"] = client
#         client = clients["fs_client"]
#         # You can't return the client object directly; instead, confirm creation or perform an action
#         return {"user_id": request.user_id, "session_id": client.get_session_id()}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/init_gemini/")
def init_gemini(request: UserRequest):
    try:
        if "gemini_client" not in clients:
            client = gemini_client.agent(session_id=request.session_id)
            clients["gemini_client"] = client
        agent = clients["gemini_client"]
        # You can't return the client object directly; instead, confirm creation or perform an action
        return agent.login_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/send_message/")
def send_message(request: UserMessage):
    try:
        agent: gemini_client.agent = clients["gemini_client"]
        reply = agent.call_gemini(request.msg)
        return {"text": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))