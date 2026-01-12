from enum import Enum
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime

# Enums
class SessionState(str, Enum):
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
    AUTOMATION_MODE_UNSPECIFIED = "AUTOMATION_MODE_UNSPECIFIED"
    AUTO_CREATE_PR = "AUTO_CREATE_PR"

# Context Models
class GitHubRepoContext(BaseModel):
    startingBranch: str = Field(..., description="The name of the branch to start the session from.")

class SourceContext(BaseModel):
    source: str = Field(..., description="The name of the source (e.g. sources/my-repo).")
    githubRepoContext: Optional[GitHubRepoContext] = None

class Source(BaseModel):
    """Represents a source repository."""
    name: str = Field(..., description="The resource name of the source.")
    displayName: Optional[str] = Field(None, description="The display name of the source.")
    branch: Optional[str] = Field(None, description="The default branch.")

# Output Models
class PullRequest(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

class SessionOutput(BaseModel):
    pullRequest: Optional[PullRequest] = None

# Session Model
class Session(BaseModel):
    """Represents a Jules session."""
    name: str = Field(..., description="Output only. The resource name of the session.")
    id: str = Field(..., description="Output only. The id of the session.")
    prompt: str = Field(..., description="Required. The prompt to start the session with.")
    sourceContext: SourceContext = Field(..., description="Required. The source context.")
    title: Optional[str] = Field(None, description="Optional. The session title.")
    requirePlanApproval: Optional[bool] = Field(None, description="Whether plan approval is required.")
    automationMode: Optional[AutomationMode] = None
    createTime: Optional[datetime] = Field(None, description="Output only. Creation timestamp.")
    updateTime: Optional[datetime] = Field(None, description="Output only. Last update timestamp.")
    state: SessionState = Field(..., description="Output only. Current state.")
    url: Optional[str] = Field(None, description="Output only. URL to web app.")
    outputs: Optional[List[SessionOutput]] = Field(None, description="Output only. Session outputs.")

# Activity Content Models
class PlanStep(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    index: int

class Plan(BaseModel):
    id: str
    steps: List[PlanStep]
    createTime: Optional[datetime] = None

class PlanGenerated(BaseModel):
    plan: Plan

class PlanApproved(BaseModel):
    planId: str

class AgentMessaged(BaseModel):
    agentMessage: str

class UserMessaged(BaseModel):
    userMessage: str

class ProgressUpdated(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class SessionFailed(BaseModel):
    reason: Optional[str] = None

class SessionCompleted(BaseModel):
    pass

# Artifacts
class GitPatch(BaseModel):
    unidiffPatch: Optional[str] = None
    baseCommitId: Optional[str] = None
    suggestedCommitMessage: Optional[str] = None

class ChangeSet(BaseModel):
    source: str
    gitPatch: Optional[GitPatch] = None

class Artifact(BaseModel):
    changeSet: Optional[ChangeSet] = None
    # Media and BashOutput omitted for brevity unless needed,
    # but could be added similarly.

# Activity Model
class Activity(BaseModel):
    """Represents an activity within a session."""
    name: str = Field(..., description="The resource name of the activity.")
    id: str = Field(..., description="The id of the activity.")
    description: Optional[str] = Field(None, description="Description of the activity.")
    createTime: Optional[datetime] = Field(None, description="Creation timestamp.")
    originator: Optional[str] = Field(None, description="Originator (e.g. user, agent).")
    artifacts: Optional[List[Artifact]] = None

    # Union fields
    agentMessaged: Optional[AgentMessaged] = None
    userMessaged: Optional[UserMessaged] = None
    planGenerated: Optional[PlanGenerated] = None
    planApproved: Optional[PlanApproved] = None
    progressUpdated: Optional[ProgressUpdated] = None
    sessionCompleted: Optional[SessionCompleted] = None
    sessionFailed: Optional[SessionFailed] = None
