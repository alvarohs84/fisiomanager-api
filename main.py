from fastapi import FastAPI
from database import Base, engine
from routers import users, patients, appointments, evolutions

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(evolutions.router)

@app.get("/")
def home():
    return {"msg": "FisioManager Backend OK!"}
