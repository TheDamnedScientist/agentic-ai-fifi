import firebase_admin
from firebase_admin import credentials, firestore

# Path to your downloaded service account key JSON
# cred = credentials.Certificate("agentic-ai-day-465019-firebase-adminsdk-fbsvc-0c99c403de.json")

class Client:
    def __init__(self, user_id: int):
        firebase_admin.initialize_app()
        self.db = firestore.client(database_id="fifi-users-info")
        self.user_id = str(user_id)

    def store_session_id(self, session_id):
        doc_ref = self.db.collection("users").document(self.user_id)
        doc_ref.set({"session_id": session_id})    

    def store_chat_history(self, history: list):
        doc_ref = self.db.collection("users").document(self.user_id)
        doc_ref.set({"chat_history": history}, merge=True)

    def store_chat_context(self, context: dict):
        doc_ref = self.db.collection("users").document(self.user_id)
        doc_ref.set({"chat_context": context}, merge=True)
    
    def get_chat_history(self):
        doc_ref = self.db.collection("users").document(self.user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get("chat_history", [])
        else:
            return []
            
    def get_chat_context(self):
        doc_ref = self.db.collection("users").document(self.user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict().get("chat_context", {})
        else:
            return {}
