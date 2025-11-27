from pydantic import BaseModel
from datetime import date

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    username: str
    password: str

class PatientBase(BaseModel):
    name: str
    plan: str
    status: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    class Config:
        orm_mode = True

class EvolutionBase(BaseModel):
    patient_name: str
    date: date
    text: str

class EvolutionCreate(EvolutionBase):
    pass

class Evolution(EvolutionBase):
    id: int
    class Config:
        orm_mode = True

class AppointmentBase(BaseModel):
    patient_name: str
    time: str
    note: str | None = None
    type: str
    date: date

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    class Config:
        orm_mode = True
