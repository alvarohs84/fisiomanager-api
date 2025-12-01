from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# =============================
# AUTH
# =============================
class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    username: str
    password: str
    
class AdminCreate(BaseModel):
    username: str
    password: str

# =============================
# PACIENTES
# =============================
class PatientBase(BaseModel):
    name: str
    birth_date: date            
    sex: Optional[str] = None
    phone: Optional[str] = None
    insurance: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int
    idade: int  # O Pydantic agora vai ler isso da @property do model!

    class Config:
        from_attributes = True

# =============================
# EVOLUTIONS
# =============================
class EvolutionCreate(BaseModel):
    patient_id: int
    description: str

class EvolutionOut(BaseModel):
    id: int
    patient_id: int
    description: str

    class Config:
        from_attributes = True

# =============================
# APPOINTMENTS
# =============================
class AppointmentCreate(BaseModel):
    patient_id: int
    date: str
    time: str
    notes: Optional[str] = None

class AppointmentOut(BaseModel):
    id: int
    patient_id: int
    date: str
    time: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True
        

        
        
