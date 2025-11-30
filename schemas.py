from pydantic import BaseModel
from datetime import date

class PatientBase(BaseModel):
    name: str
    birthdate: date
    phone: str
    notes: str | None = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True

