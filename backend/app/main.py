import time
from contextlib import asynccontextmanager
from collections import defaultdict
from typing import Dict, List
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import Base, engine, async_session
from app.core.security import log_audit_action
from app.api import auth, projects, blueprints, logs, audit

# In-memory Rate Limiter
# Maps IP Address to list of timestamps
request_history: Dict[str, List[float]] = defaultdict(list)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite or Postgres tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Autonomous Multi-Agent Software Engineering Platform Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development convenience. Can be restricted in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom Rate Limiter Middleware
@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    # Bypass docs and health check endpoints
    if request.url.path in ["/docs", "/openapi.json", "/redoc", "/"]:
        return await call_next(request)
        
    client_ip = request.client.host
    now = time.time()
    
    # Filter out requests older than 60 seconds
    request_history[client_ip] = [t for t in request_history[client_ip] if now - t < 60]
    
    if len(request_history[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        # Rate limit exceeded - Log to database audit log
        async with async_session() as session:
            await log_audit_action(
                db=session,
                action="RATE_LIMIT_EXCEEDED",
                ip_address=client_ip,
                status_code=429,
                details=f"IP {client_ip} triggered rate limit on path {request.url.path}"
            )
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Too many requests. Please try again later."}
        )
        
    # Record current request timestamp
    request_history[client_ip].append(now)
    return await call_next(request)

# Health Check Route
@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "CortexOS API"}

# Include Routers
app.include_router(auth.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(blueprints.router, prefix="/api")
app.include_router(logs.router, prefix="/api")
app.include_router(audit.router, prefix="/api")
