from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="user") # user, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    prompt = Column(Text, nullable=False)
    status = Column(String, default="pending") # pending, running, completed, failed
    current_agent = Column(String, nullable=True) # Name of currently executing agent
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User", back_populates="projects")
    blueprint = relationship("Blueprint", uselist=False, back_populates="project", cascade="all, delete-orphan")
    agent_logs = relationship("AgentLog", back_populates="project", cascade="all, delete-orphan")

class Blueprint(Base):
    __tablename__ = "blueprints"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Store complete output details from agent runs
    requirement_analysis = Column(JSON, nullable=True)
    prd = Column(JSON, nullable=True)
    architecture_design = Column(JSON, nullable=True)
    database_schema = Column(JSON, nullable=True)
    api_design = Column(JSON, nullable=True)
    backend_plan = Column(JSON, nullable=True)
    frontend_plan = Column(JSON, nullable=True)
    testing_strategy = Column(JSON, nullable=True)
    security_report = Column(JSON, nullable=True)
    deployment_guide = Column(JSON, nullable=True)
    review_report = Column(JSON, nullable=True)
    
    # Human-readable markdown compilations for download/view
    markdown_output = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="blueprint")

class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    agent_name = Column(String, nullable=False)
    log_level = Column(String, default="INFO") # INFO, WARNING, ERROR, SUCCESS
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    project = relationship("Project", back_populates="agent_logs")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String, nullable=False) # e.g., LOGIN, PROJECT_CREATE, EXPORT
    ip_address = Column(String, nullable=True)
    status_code = Column(Integer, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="audit_logs")
