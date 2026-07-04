from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    prompt: str = Field(..., min_length=10)

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    status: str
    current_agent: Optional[str] = None
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

# Blueprint Schemas
class BlueprintResponse(BaseModel):
    id: int
    project_id: int
    requirement_analysis: Optional[Dict[str, Any]] = None
    prd: Optional[Dict[str, Any]] = None
    architecture_design: Optional[Dict[str, Any]] = None
    database_schema: Optional[Dict[str, Any]] = None
    api_design: Optional[Dict[str, Any]] = None
    backend_plan: Optional[Dict[str, Any]] = None
    frontend_plan: Optional[Dict[str, Any]] = None
    testing_strategy: Optional[Dict[str, Any]] = None
    security_report: Optional[Dict[str, Any]] = None
    deployment_guide: Optional[Dict[str, Any]] = None
    review_report: Optional[Dict[str, Any]] = None
    markdown_output: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Agent Log Schemas
class AgentLogResponse(BaseModel):
    id: int
    project_id: int
    agent_name: str
    log_level: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    ip_address: Optional[str] = None
    status_code: Optional[int] = None
    details: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Orchestrator Request Schemas
class WizardRunRequest(BaseModel):
    prompt: str = Field(..., min_length=10, description="The natural language software idea/specification")
    title: str = Field(..., min_length=3, max_length=100, description="The project name")
    description: Optional[str] = Field(None, description="Optional high level context")
