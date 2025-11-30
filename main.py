from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa suas rotas
from routers.users import router as users_router
from routers.patients import router as patients_router
from routers.evolutions import router as evolutions_router
from routers.appointments import router as appointments_router

app = FastAPI(
    title="FisioManager API",
    description="Backend oficial do FisioManager Premium",
    version="1.0.0"
)

# =====================================================
# 🚀 CONFIGURAÇÃO CORRETA DE CORS PARA O RENDER
# =====================================================
origins = [
    "https://fisiomanager-frontend1.onrender.com",
    "http://localhost:3000",
    "http://localhost:5500",
    "*",  # Opcional, mas útil no desenvolvimento
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# ROTAS REGISTRADAS
# =====================================================
app.include_router(users_router)
app.include_router(patients_router)
app.include_router(evolutions_router)
app.include_router(appointments_router)


# =====================================================
# ROTA RAIZ PARA TESTE
# =====================================================
@app.get("/")
def root():
    return {"status": "online", "message": "Fisiomanager API rodando!"}
