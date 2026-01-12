from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class SessionState(str, Enum):
    QUEUED = "QUEUED"
    PLANNING = "PLANNING"
    AWAITING_PLAN_APPROVAL = "AWAITING_PLAN_APPROVAL"
    AWAITING_USER_FEEDBACK = "AWAITING_USER_FEEDBACK"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

class Source(BaseModel):
    """Represents a source repository."""
    name: str = Field(..., description="The resource name of the source.")
    displayName: Optional[str] = Field(None, description="The display name of the source.")
    branch: Optional[str] = Field(None, description="The default branch.")

class Session(BaseModel):
    """Represents a Jules session."""
    name: str = Field(..., description="The resource name of the session.")
    state: SessionState = Field(..., description="The current state of the session.")
    createTime: Optional[datetime] = Field(None, description="The creation timestamp.")
    updateTime: Optional[datetime] = Field(None, description="The last update timestamp.")
    userPrompt: Optional[str] = Field(None, description="The initial user prompt.")

class Activity(BaseModel):
    """Represents an activity within a session."""
    name: str = Field(..., description="The resource name of the activity.")
    type: Optional[str] = Field(None, description="The type of activity.")
    createTime: Optional[datetime] = Field(None, description="The creation timestamp.")
    detail: Optional[Dict[str, Any]] = Field(None, description="Detailed information about the activity.")
