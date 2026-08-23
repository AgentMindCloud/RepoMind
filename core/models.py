from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum

class SafetyLevel(str, Enum):
    LOW = "low"
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

class SkillContract(BaseModel):
    name: str
    version: str = "0.1.0"
    description: str
    inputs: Dict[str, Any] = Field(default_factory=dict)
    outputs: Dict[str, Any] = Field(default_factory=dict)
    requires: List[str] = Field(default_factory=list)
    safety_level: SafetyLevel = SafetyLevel.STANDARD

class AgentRole(BaseModel):
    name: str
    system_prompt: str
    allowed_skills: List[str] = Field(default_factory=list)
    max_iterations: int = 5
    tools: List[str] = Field(default_factory=list)

class Task(BaseModel):
    issue_number: int
    title: str
    body: str
    labels: List[str] = Field(default_factory=list)
    state: str = "open"
    html_url: Optional[str] = None

class ActionResult(BaseModel):
    success: bool
    summary: str
    output: Any = None
    pr_url: Optional[str] = None
    comments: List[str] = Field(default_factory=list)
    artifacts: List[str] = Field(default_factory=list)
