"""Pydantic models for the Google Jules API."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class SessionState(str, Enum):
    """Session state enum."""

    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    AWAITING_PLAN_APPROVAL = "AWAITING_PLAN_APPROVAL"
    AWAITING_USER_FEEDBACK = "AWAITING_USER_FEEDBACK"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"


class AutomationMode(str, Enum):
    """Automation mode enum."""

    AUTOMATION_MODE_UNSPECIFIED = "AUTOMATION_MODE_UNSPECIFIED"
    FULLY_AUTOMATIC = "FULLY_AUTOMATIC"
    SEMI_AUTOMATIC = "SEMI_AUTOMATIC"


class Branch(BaseModel):
    """Git branch information."""

    display_name: Optional[str] = Field(None, alias="displayName")


class GitHubRepo(BaseModel):
    """GitHub repository information."""

    owner: str
    repo: str
    is_private: Optional[bool] = Field(None, alias="isPrivate")
    default_branch: Optional[Branch] = Field(None, alias="defaultBranch")
    branches: Optional[list[Branch]] = None


class Source(BaseModel):
    """Source resource representing a GitHub repository."""

    name: str
    id: str
    github_repo: Optional[GitHubRepo] = Field(None, alias="githubRepo")


class ListSourcesResponse(BaseModel):
    """Response from list sources API."""

    sources: list[Source] = []
    next_page_token: Optional[str] = Field(None, alias="nextPageToken")


class SourceContext(BaseModel):
    """Source context for creating a session."""

    source: str = Field(
        ..., description="Resource name of the source (e.g., sources/github/owner/repo)"
    )
    branch: Optional[str] = Field(None, description="Branch name to use")


class PullRequest(BaseModel):
    """Pull request output from a session."""

    url: Optional[str] = None
    title: Optional[str] = None
    state: Optional[str] = None


class SessionOutput(BaseModel):
    """Output from a session."""

    pull_request: Optional[PullRequest] = Field(None, alias="pullRequest")


class Session(BaseModel):
    """Session resource representing a coding task."""

    name: Optional[str] = Field(None, description="Resource name (e.g., sessions/123)")
    id: Optional[str] = Field(None, description="Session ID")
    prompt: str = Field(..., description="Initial prompt for the session")
    source_context: Optional[SourceContext] = Field(None, alias="sourceContext")
    title: Optional[str] = Field(
        None, description="Session title (auto-generated if not provided)"
    )
    require_plan_approval: Optional[bool] = Field(None, alias="requirePlanApproval")
    automation_mode: Optional[AutomationMode] = Field(None, alias="automationMode")
    create_time: Optional[str] = Field(None, alias="createTime")
    update_time: Optional[str] = Field(None, alias="updateTime")
    state: Optional[SessionState] = None
    url: Optional[str] = Field(
        None, description="URL to view the session in Jules web app"
    )
    outputs: Optional[list[SessionOutput]] = None


class ListSessionsResponse(BaseModel):
    """Response from list sessions API."""

    sessions: list[Session] = []
    next_page_token: Optional[str] = Field(None, alias="nextPageToken")


class SendMessageRequest(BaseModel):
    """Request to send a message to a session."""

    prompt: str = Field(..., description="The user prompt to send")


class ApprovePlanRequest(BaseModel):
    """Request to approve a plan."""

    pass


class Activity(BaseModel):
    """Activity resource representing work within a session."""

    name: Optional[str] = None
    id: Optional[str] = None
    create_time: Optional[str] = Field(None, alias="createTime")
    update_time: Optional[str] = Field(None, alias="updateTime")
    state: Optional[str] = None
    actor: Optional[str] = None
    content: Optional[dict] = None


class ListActivitiesResponse(BaseModel):
    """Response from list activities API."""

    activities: list[Activity] = []
    next_page_token: Optional[str] = Field(None, alias="nextPageToken")


class CreateSessionRequest(BaseModel):
    """Request to create a new session."""

    prompt: str = Field(..., description="Initial prompt for the coding task")
    source_context: SourceContext = Field(..., alias="sourceContext")
    title: Optional[str] = None
    require_plan_approval: Optional[bool] = Field(None, alias="requirePlanApproval")
    automation_mode: Optional[AutomationMode] = Field(None, alias="automationMode")
