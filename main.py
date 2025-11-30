from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm # Importante para o login
from sqlalchemy.orm import Session

# Imports locais
from database import Base, engine, get_db
import models
import auth # Importa o nosso novo super arquivo
from routers import users, patients, evolutions, appointments

# Cria as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FisioManager Backend")

# --- CORS (GARANTA QUE ESTÁ ASSIM) ---
origins = [
    "http://localhost:3000",
    "https://fisiomanager-frontend1.onrender.com",
    "https://fisiomanager-frontend1.onrender.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ROTA DE LOGIN (TOKEN) ---
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Busca usuário no banco
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    
    # Valida senha usando a função do auth.py
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Cria token
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# --- ROTA DE CRIAR ADMIN ---
@app.post("/create-admin")
def create_admin(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == "admin").first()
    if user:
        return {"message": "Admin já existe"}
    
    # Usa o hash_password do auth.py
    new_user = models.User(username="admin", hashed_password=auth.hash_password("123456"))
    db.add(new_user)
    db.commit()
    return {"message": "Admin criado!"}

# --- ROTA DE RESET (MANTER) ---
@app.get("/reset-database-force")
def reset_database():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return {"message": "Banco resetado!"}

# Inclui as rotas
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(evolutions.router)
app.include_router(appointments.router)

