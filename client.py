"""HTTP client for the Google Jules API."""

import httpx
from typing import Optional

from models import (
    Source,
    Session,
    Activity,
    ListSourcesResponse,
    ListSessionsResponse,
    ListActivitiesResponse,
    SourceContext,
)

BASE_URL = "https://jules.googleapis.com/v1alpha"


class JulesClient:
    """Client for interacting with the Google Jules API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "X-Goog-Api-Key": api_key,
            "Content-Type": "application/json",
        }

    async def list_sources(
        self,
        page_size: int = 30,
        page_token: Optional[str] = None,
        filter_expr: Optional[str] = None,
    ) -> ListSourcesResponse:
        """List available sources (repositories)."""
        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token
        if filter_expr:
            params["filter"] = filter_expr

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/sources",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return ListSourcesResponse.model_validate(response.json())

    async def get_source(self, source_name: str) -> Source:
        """Get a single source by name."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/{source_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Source.model_validate(response.json())

    async def list_sessions(
        self,
        page_size: int = 30,
        page_token: Optional[str] = None,
    ) -> ListSessionsResponse:
        """List sessions."""
        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/sessions",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return ListSessionsResponse.model_validate(response.json())

    async def get_session(self, session_name: str) -> Session:
        """Get a single session by name."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/{session_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Session.model_validate(response.json())

    async def create_session(
        self,
        prompt: str,
        source: str,
        branch: Optional[str] = None,
        title: Optional[str] = None,
        require_plan_approval: bool = False,
    ) -> Session:
        """Create a new session."""
        source_context = {"source": source}
        if branch:
            source_context["branch"] = branch

        body = {
            "prompt": prompt,
            "sourceContext": source_context,
        }
        if title:
            body["title"] = title
        if require_plan_approval:
            body["requirePlanApproval"] = require_plan_approval

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/sessions",
                headers=self.headers,
                json=body,
            )
            response.raise_for_status()
            return Session.model_validate(response.json())

    async def send_message(self, session_name: str, prompt: str) -> dict:
        """Send a message to a session."""
        # Ensure session_name is in correct format
        if not session_name.startswith("sessions/"):
            session_name = f"sessions/{session_name}"

        body = {"prompt": prompt}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/{session_name}:sendMessage",
                headers=self.headers,
                json=body,
            )
            response.raise_for_status()
            # Response body is empty on success
            return {"success": True, "session": session_name}

    async def approve_plan(self, session_name: str) -> dict:
        """Approve a plan for a session."""
        # Ensure session_name is in correct format
        if not session_name.startswith("sessions/"):
            session_name = f"sessions/{session_name}"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{BASE_URL}/{session_name}:approvePlan",
                headers=self.headers,
                json={},
            )
            response.raise_for_status()
            return {"success": True, "session": session_name}

    async def list_activities(
        self,
        session_name: str,
        page_size: int = 50,
        page_token: Optional[str] = None,
    ) -> ListActivitiesResponse:
        """List activities for a session."""
        # Ensure session_name is in correct format
        if not session_name.startswith("sessions/"):
            session_name = f"sessions/{session_name}"

        params = {"pageSize": page_size}
        if page_token:
            params["pageToken"] = page_token

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/{session_name}/activities",
                headers=self.headers,
                params=params,
            )
            response.raise_for_status()
            return ListActivitiesResponse.model_validate(response.json())

    async def get_activity(self, activity_name: str) -> Activity:
        """Get a single activity by name."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/{activity_name}",
                headers=self.headers,
            )
            response.raise_for_status()
            return Activity.model_validate(response.json())
