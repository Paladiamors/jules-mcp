import os
import httpx
from typing import List, Optional, Dict, Any
from models import Session, Source, Activity

class JulesClient:
    """
    Async client for the Google Jules API.
    """
    def __init__(self):
        self.base_url = "https://jules.googleapis.com/v1alpha"
        self.api_key = os.environ.get("JULES_API_KEY")

        self.headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            self.headers["X-Goog-Api-Key"] = self.api_key

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self.headers,
            timeout=60.0
        )

    async def list_sources(self) -> List[Source]:
        """
        Fetches available repositories (sources).
        """
        resp = await self.client.get("/sources")
        resp.raise_for_status()
        data = resp.json()
        return [Source(**item) for item in data.get("sources", [])]

    async def create_session(self, source: str, user_prompt: str) -> Session:
        """
        Starts a new task (session).

        Args:
            source: The resource name of the source repository.
            user_prompt: The initial prompt from the user.
        """
        body = {
            "source": source,
            "userPrompt": user_prompt
        }
        resp = await self.client.post("/sessions", json=body)
        resp.raise_for_status()
        return Session(**resp.json())

    async def list_sessions(self, order_by_recent: bool = True, active_only: bool = True) -> List[Session]:
        """
        Lists sessions with optional filtering and sorting.

        Args:
            order_by_recent: If True, sort by createTime desc.
            active_only: If True, exclude COMPLETED and FAILED sessions.
        """
        params = {}
        if order_by_recent:
            params["orderBy"] = "createTime desc"

        if active_only:
            # constructing filter
            params["filter"] = 'state != "COMPLETED" AND state != "FAILED"'

        resp = await self.client.get("/sessions", params=params)
        resp.raise_for_status()
        data = resp.json()
        return [Session(**item) for item in data.get("sessions", [])]

    async def send_message(self, session_name: str, message: str) -> Any:
        """
        Sends a message to an active session.

        Args:
            session_name: The resource name of the session.
            message: The message content.
        """
        # Ensure session_name doesn't duplicate the path if it already contains it,
        # but here we rely on the API returning full resource names like "sessions/uuid".
        # The base URL is .../v1alpha, so we append /{session_name}:sendMessage
        url = f"/{session_name}:sendMessage"
        body = {"message": message}
        resp = await self.client.post(url, json=body)
        resp.raise_for_status()
        return resp.json()

    async def approve_plan(self, session_name: str) -> Any:
        """
        Approves a session's plan.

        Args:
            session_name: The resource name of the session.
        """
        url = f"/{session_name}:approvePlan"
        resp = await self.client.post(url, json={})
        resp.raise_for_status()
        return resp.json()

    async def get_activities(self, session_name: str) -> List[Activity]:
        """
        Retrieves session history (activities).

        Args:
            session_name: The resource name of the session.
        """
        url = f"/{session_name}/activities"
        resp = await self.client.get(url)
        resp.raise_for_status()
        data = resp.json()
        return [Activity(**item) for item in data.get("activities", [])]

    async def close(self):
        await self.client.aclose()
