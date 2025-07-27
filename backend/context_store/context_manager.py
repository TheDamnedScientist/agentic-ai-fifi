import os
import json

CONTEXT_DIR = "context_store/memory"

class contextTools:
    def __init__(self, user_id: str):
        """
        Initialize the context manager for a specific user.
        Args:
            user_id (str): The user ID for which to manage context.
        """
        self.user_id = user_id
        
    def get_context_path(self, user_id: str) -> str:
        """
        Get the path to the context file for a given user ID.
        Args:
            user_id (str): The user ID for which to get the context path.
        Returns:
            str: The path to the context file.
        """
        user_path = os.path.join(CONTEXT_DIR, user_id, 'context.json')

        return user_path

    def load_context(self, user_id: str) -> dict:
        """
        Load the context for the user.
        Args:
            user_id (str): The user ID for which to load the context.
        Returns:
            dict: The context data for the user.
        """
        path = self.get_context_path(user_id)
        if not os.path.exists(path):
            return {}
        with open(path, "r") as f:
            return json.load(f)

    def save_context(self, user_id: str, ctx: dict) -> None:
        """
        Save the context for the user.
        Args:
            user_id (str): The user ID for which to save the context.
            ctx (dict): The context data to save.
        """
        path = self.get_context_path(user_id)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(ctx, f, indent=2)
            
        return "Context updated."

    def update_context(self, user_id: str, updates: dict) -> dict:
        """
        Update the context with new data.
        Args:
            user_id (str): The user ID for which to update the context.
            updates (dict): A dictionary containing the updates to apply to the context.
        Returns:
            dict: The updated context.
        """
        ctx = self.load_context(user_id)
        for section in updates:
            if not isinstance(updates[section], dict):
                raise ValueError(f"Updates for section '{section}' must be a dictionary.")
            else:
                ctx[section] = updates[section]
        self.save_context(user_id, ctx)
        
        return ctx