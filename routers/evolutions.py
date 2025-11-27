from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Evolution
from schemas import EvolutionCreate

router = APIRouter(prefix="/evolutions")

@router.get("")
def list(db: Session = Depends(get_db)):
    return db.query(Evolution).all()

@router.post("")
def create(data: EvolutionCreate, db: Session = Depends(get_db)):
    evo = Evolution(**data.dict())
    db.add(evo)
    db.commit()
    return evo

@router.get("/by-patient/{name}")
def by_patient(name: str, db: Session = Depends(get_db)):
    return db.query(Evolution).filter(Evolution.patient_name == name).all()
