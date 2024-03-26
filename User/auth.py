from passlib.context import CryptContext
import jwt
from User.models import User
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime, timedelta
from shared.dependencies import get_db
from jwt import PyJWTError  # Import PyJWTError for exception handling

# Configuração do JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


# Gerar Token JWT
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Verificar token JWT
async def get_current_user(token: str = Header(...), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:  # Corrected exception handling
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

