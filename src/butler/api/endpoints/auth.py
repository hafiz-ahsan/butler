"""Authentication endpoints."""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from butler.core.config import settings
from butler.core.logging import get_logger

router = APIRouter()
logger = get_logger(__name__)

# Security
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class UserCreate(BaseModel):
    """User creation model."""

    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """User login model."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Token response model."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class User(BaseModel):
    """User model."""

    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )

    return encoded_jwt


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """Get the current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # In a real app, you would fetch the user from the database
    # For demo purposes, we'll return a mock user with the email from the token
    user = User(id=1, email=email, full_name="Demo User", is_active=True)

    return user


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate):
    """Register a new user."""
    logger.info("User registration attempt", email=user_data.email)

    # In a real app, you would:
    # 1. Check if user already exists
    # 2. Save user to database
    # 3. Send verification email

    hashed_password = get_password_hash(user_data.password)
    logger.info("User registered successfully", email=user_data.email)

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token, expires_in=settings.access_token_expire_minutes * 60
    )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    """Authenticate and login a user."""
    logger.info("User login attempt", email=user_data.email)

    # In a real app, you would:
    # 1. Fetch user from database
    # 2. Verify password
    # 3. Check if user is active

    # For demo purposes, we'll accept any login
    logger.info("User logged in successfully", email=user_data.email)

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user_data.email}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token, expires_in=settings.access_token_expire_minutes * 60
    )


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@router.post("/refresh", response_model=Token)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """Refresh access token."""
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": current_user.email}, expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token, expires_in=settings.access_token_expire_minutes * 60
    )
