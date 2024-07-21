from datetime import datetime, timedelta
from typing import Dict, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jose import JWTError, jwt

from app.config import Settings
from app.dependencies import get_settings
from app.routers.account.models import LoginRequest, LoginResponse, User

router = APIRouter(
    prefix="/api/account",
    tags=["Account"],
)

fake_users_db = {
    "demo@minimals.cc": {
        "email": "demo@minimals.cc",
        "displayName": "John Doe",
        "password": "demo1234",
        "role": "hardcoded user :)",
    }
}


def authenticate_user(email: str, password: str) -> Optional[Dict]:
    user = fake_users_db.get(email)
    if not user:
        return None

    if password != user["password"]:
        return None

    return user


def create_access_token(data: Dict, ttl: int, secret_key: str, algorithm: str) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ttl)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm)

    return encoded_jwt


@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(
    login_request: LoginRequest,
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    user = authenticate_user(login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user["email"]},
        ttl=settings.jwt_ttl_minutes,
        secret_key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )
    return LoginResponse(accessToken=access_token, user=User(**user))


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    settings: Settings = Depends(get_settings),
) -> User:
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = fake_users_db.get(email)
    if user is None:
        raise credentials_exception

    return User(**user)


@router.get("/my-account", response_model=Dict[Literal["user"], User])
async def user_info(
    user: User = Depends(get_current_user),
) -> Dict[Literal["user"], User]:
    return {"user": user}
