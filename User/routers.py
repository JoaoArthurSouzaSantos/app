from User.models import User
from shared.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta
from User.schemas import UserCreate, UserOut
from User.auth import verify_password, get_password_hash, create_access_token, get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/login/")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "perfil": user.perfil}


@router.post("/create/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    password_hash = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=password_hash, perfil=user.perfil)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/read/{user_id}", response_model=UserOut)
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.password_hash = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/delete/{user_id}", response_model=UserOut)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user
