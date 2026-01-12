"""FastMCP server for Google Jules API."""

import os
from typing import Optional
from fastmcp import FastMCP

from client import JulesClient
from models import SessionState

# Initialize FastMCP server
mcp = FastMCP(
    "jules",
    instructions="MCP server for Google Jules API - Create and manage coding sessions with Jules AI",
)


def get_client() -> JulesClient:
    """Get Jules API client with API key from environment."""
    api_key = os.environ.get("JULES_API_KEY")
    if not api_key:
        raise ValueError("JULES_API_KEY environment variable is required")
    return JulesClient(api_key)


@mcp.tool()
async def list_sources(
    page_size: int = 30,
    page_token: Optional[str] = None,
) -> dict:
    """
    List available GitHub repositories that Jules can work with.

    Args:
        page_size: Number of sources to return (1-100, default 30)
        page_token: Token for pagination from previous response

    Returns:
        Dictionary with sources list and optional nextPageToken
    """
    client = get_client()
    response = await client.list_sources(page_size=page_size, page_token=page_token)
    return response.model_dump(by_alias=True, exclude_none=True)


@mcp.tool()
async def get_source(source_name: str) -> dict:
    """
    Get details about a specific source repository.

    Args:
        source_name: Resource name of the source (e.g., "sources/github/owner/repo")

    Returns:
        Source details including branches and repository info
    """
    client = get_client()
    response = await client.get_source(source_name)
    return response.model_dump(by_alias=True, exclude_none=True)


@mcp.tool()
async def list_sessions(
    page_size: int = 30,
    page_token: Optional[str] = None,
    active_only: bool = False,
) -> dict:
    """
    List Jules sessions (coding tasks).

    Args:
        page_size: Number of sessions to return (1-100, default 30)
        page_token: Token for pagination from previous response
        active_only: If True, filter to only show non-completed/failed sessions

    Returns:
        Dictionary with sessions list and optional nextPageToken
    """
    client = get_client()
    response = await client.list_sessions(page_size=page_size, page_token=page_token)

    sessions = response.sessions
    if active_only:
        sessions = [
            s for s in sessions
            if s.state not in (SessionState.COMPLETED, SessionState.FAILED)
        ]

    return {
        "sessions": [s.model_dump(by_alias=True, exclude_none=True) for s in sessions],
        "nextPageToken": response.next_page_token,
    }


@mcp.tool()
async def get_session(session_name: str) -> dict:
    """
    Get details about a specific session.

    Args:
        session_name: Resource name of the session (e.g., "sessions/abc123")

    Returns:
        Session details including state, outputs, and URL
    """
    client = get_client()
    response = await client.get_session(session_name)
    return response.model_dump(by_alias=True, exclude_none=True)


@mcp.tool()
async def create_session(
    prompt: str,
    source: str,
    branch: Optional[str] = None,
    title: Optional[str] = None,
    require_plan_approval: bool = False,
) -> dict:
    """
    Create a new Jules session to work on a coding task.

    Args:
        prompt: The coding task description for Jules to work on
        source: Resource name of the source repository (e.g., "sources/github/owner/repo")
        branch: Optional branch name to use (defaults to repository default branch)
        title: Optional title for the session (auto-generated if not provided)
        require_plan_approval: If True, Jules will wait for plan approval before executing

    Returns:
        Created session details including ID, state, and URL to view progress
    """
    client = get_client()
    response = await client.create_session(
        prompt=prompt,
        source=source,
        branch=branch,
        title=title,
        require_plan_approval=require_plan_approval,
    )
    return response.model_dump(by_alias=True, exclude_none=True)


@mcp.tool()
async def send_message(session_name: str, message: str) -> dict:
    """
    Send a follow-up message to an active Jules session.

    Use this to provide additional context, clarify requirements, or respond to
    Jules when it's waiting for user feedback.

    Args:
        session_name: Resource name of the session (e.g., "sessions/abc123")
        message: The message to send to Jules

    Returns:
        Success confirmation
    """
    client = get_client()
    return await client.send_message(session_name, message)


@mcp.tool()
async def approve_plan(session_name: str) -> dict:
    """
    Approve Jules's plan for a session.

    Use this when a session is in AWAITING_PLAN_APPROVAL state and you want
    Jules to proceed with its proposed plan.

    Args:
        session_name: Resource name of the session (e.g., "sessions/abc123")

    Returns:
        Success confirmation
    """
    client = get_client()
    return await client.approve_plan(session_name)


@mcp.tool()
async def list_activities(
    session_name: str,
    page_size: int = 50,
    page_token: Optional[str] = None,
) -> dict:
    """
    List activities (work history) for a session.

    Activities represent individual work units within a session, showing
    the conversation and actions taken by Jules.

    Args:
        session_name: Resource name of the session (e.g., "sessions/abc123")
        page_size: Number of activities to return (1-100, default 50)
        page_token: Token for pagination from previous response

    Returns:
        Dictionary with activities list and optional nextPageToken
    """
    client = get_client()
    response = await client.list_activities(
        session_name=session_name,
        page_size=page_size,
        page_token=page_token,
    )
    return response.model_dump(by_alias=True, exclude_none=True)


@mcp.tool()
async def create_pull_request(
    prompt: str,
    source: str,
    branch: Optional[str] = None,
    title: Optional[str] = None,
) -> dict:
    """
    Create a session that will result in a pull request.

    This is a convenience wrapper around create_session that instructs Jules
    to create a PR. The session will automatically create a merge/pull request
    when the work is complete.

    Args:
        prompt: Description of changes to make (be specific about what you want)
        source: Resource name of the source repository (e.g., "sources/github/owner/repo")
        branch: Optional base branch to create PR against (defaults to repository default)
        title: Optional title for the session/PR

    Returns:
        Created session details - check the 'outputs' field for PR URL once completed
    """
    # Add explicit instruction to create a PR
    full_prompt = f"{prompt}\n\nPlease create a pull request with these changes."

    client = get_client()
    response = await client.create_session(
        prompt=full_prompt,
        source=source,
        branch=branch,
        title=title,
        require_plan_approval=False,
    )
    return response.model_dump(by_alias=True, exclude_none=True)


def main():
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
