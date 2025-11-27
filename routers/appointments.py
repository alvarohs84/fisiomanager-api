from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Appointment
from schemas import AppointmentCreate
from datetime import date

router = APIRouter(prefix="/appointments")

@router.get("")
def list(db: Session = Depends(get_db)):
    return db.query(Appointment).all()

@router.get("/today")
def today(db: Session = Depends(get_db)):
    today = date.today()
    return db.query(Appointment).filter(Appointment.date == today).all()

@router.get("/by-patient/{name}")
def patient(name: str, db: Session = Depends(get_db)):
    return db.query(Appointment).filter(Appointment.patient_name == name).all()

@router.post("")
def create(data: AppointmentCreate, db: Session = Depends(get_db)):
    a = Appointment(**data.dict())
    db.add(a)
    db.commit()
    return a
