from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from auth import authenticate_user, create_access_token, hash_password
from schemas import UserLogin, Token
from models import User

router = APIRouter()

@router.post("/token", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, data.username, data.password)
    if not user:
        raise HTTPException(401, "Usuário ou senha inválidos")
    token = create_access_token({"sub": user.username})
    return Token(access_token=token)

@router.post("/create-admin")
def create_admin(db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == "admin").first():
        return {"detail": "Admin já existe"}
    admin = User(username="admin", hashed_password=hash_password("admin"))
    db.add(admin)
    db.commit()
    return {"detail": "Admin criado: admin / admin"}
