from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ============================================================
# CORS — Libera o Frontend para acessar o Backend no Render
# ============================================================
origins = [
    "https://fisiomanager-frontend1.onrender.com",       # SEU FRONTEND
    "https://fisiomanager-backend.onrender.com",         # BACKEND OFICIAL
    "https://fisiomanager-backend-nr.onrender.com",      # BACKEND SECUNDÁRIO DO RENDER
    "http://localhost:3000",
    "http://localhost:5500",
    "http://localhost",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# IMPORTS & ROTAS
# ============================================================

from routers import users, patients, evolutions, appointments  # se existirem

app.include_router(users.router)
app.include_router(patients.router)
app.include_router(evolutions.router)
app.include_router(appointments.router)


@app.get("/")
def root():
    return {"message": "FisioManager Backend OK (CORS liberado)"}

