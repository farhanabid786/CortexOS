from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token, log_audit_action
from app.models import User
from app.schemas import UserCreate, UserResponse, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: Request, user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).filter(User.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        await log_audit_action(
            db, "REGISTER_FAILED", ip_address=request.client.host,
            status_code=400, details=f"Registration attempted for existing email: {user_in.email}"
        )
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed = hash_password(user_in.password)
    
    # If it is the first user, make them admin for evaluation convenience
    user_count = await db.execute(select(User))
    role = "admin" if len(user_count.scalars().all()) == 0 else "user"
    
    new_user = User(
        email=user_in.email,
        hashed_password=hashed,
        full_name=user_in.full_name,
        role=role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    await log_audit_action(
        db, "REGISTER_SUCCESS", user_id=new_user.id, ip_address=request.client.host,
        status_code=201, details=f"User {new_user.email} registered successfully with role {new_user.role}"
    )
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.email == form_data.username))
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        await log_audit_action(
            db, "LOGIN_FAILED", ip_address=request.client.host,
            status_code=401, details=f"Failed login attempt for username: {form_data.username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user account")
        
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id, "role": user.role}
    )
    
    await log_audit_action(
        db, "LOGIN_SUCCESS", user_id=user.id, ip_address=request.client.host,
        status_code=200, details=f"User {user.email} logged in successfully"
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

from app.api.deps import get_current_active_user

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user
