from fastapi import APIRouter

router = APIRouter(
    prefix="/api/account",
    tags=["Account"],
)

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Literal
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_TTL_MINUTES = 30

fake_users_db = {
    "demo@minimals.cc": {
        "email": "demo@minimals.cc",
        "displayName": "John Doe",
        "password": "demo1234",
        "role": "hardcoded user :)"
    }
}


class User(BaseModel):
    email: str
    displayName: str
    role: str
    photoURL: Optional[str] = None


def authenticate_user(email: str, password: str):
    user = fake_users_db.get(email)
    if not user:
        return None

    if password != user["password"]:
        return None

    return user


def create_access_token(data: Dict, ttl: int) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ttl)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


class LoginResponse(BaseModel):
    accessToken: str
    user: User


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=LoginResponse)
async def login_for_access_token(login_request: LoginRequest):
    user = authenticate_user(login_request.email, login_request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user["email"]}, ttl=ACCESS_TOKEN_TTL_MINUTES)
    return LoginResponse(accessToken=access_token, user=User(**user))


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = credentials.credentials

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    user = fake_users_db.get(email)
    if user is None:
        raise credentials_exception

    return user


@router.get("/my-account", response_model=Dict[Literal["user"], User])
async def user_info(user: User = Depends(get_current_user)):
    return {"user": user}
