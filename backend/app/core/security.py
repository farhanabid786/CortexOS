from datetime import datetime, timedelta
from typing import Optional, Tuple
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.models import AuditLog

import bcrypt

# Direct bcrypt hashing helper
def hash_password(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        pwd_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pwd_bytes, hashed_bytes)
    except Exception:
        return False

# JWT Configuration
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Audit Logger Helper
async def log_audit_action(
    db: AsyncSession,
    action: str,
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    status_code: Optional[int] = None,
    details: Optional[str] = None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        ip_address=ip_address,
        status_code=status_code,
        details=details,
        created_at=datetime.utcnow()
    )
    db.add(audit_log)
    await db.commit()

# Prompt Injection Detector
# Scans user prompt inputs for system-override attempts, escape commands, or jailbreak attempts.
SUSPICIOUS_KEYWORDS = [
    "ignore previous instructions",
    "ignore all previous",
    "system override",
    "developer mode",
    "you are now a",
    "new rule:",
    "ignore rules",
    "disregard guidelines",
    "bypass instructions",
    "jailbreak",
    "dan mode",
    "do anything now",
    "override security",
    "system prompt",
    "you must ignore"
]

def detect_prompt_injection(user_input: str) -> Tuple[bool, Optional[str]]:
    """
    Checks the user input for common prompt injection/jailbreak patterns.
    Returns: (is_injection_detected, matched_pattern_reason)
    """
    if not user_input:
        return False, None
        
    normalized_input = user_input.lower().strip()
    
    # Check for direct keyword matches
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in normalized_input:
            return True, f"Suspicious pattern match: '{keyword}'"
            
    # Check for excessive shell escaping or scripting attempt indicators
    if normalized_input.count("`") > 6 or normalized_input.count("${") > 4:
        return True, "Suspicious script execution or variable expansion syntax"
        
    return False, None
