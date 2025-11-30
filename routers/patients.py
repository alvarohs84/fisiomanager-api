from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
# Importe a função de verificar usuário logado (geralmente fica em auth.py ou main.py)
# Se der erro de importação aqui, me avise onde você colocou a função get_current_user
from auth import get_current_user 

router = APIRouter(prefix="/patients", tags=["Patients"])

# --- CRIAR PACIENTE ---
@router.post("/", response_model=schemas.PatientOut)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Exige login
):
    # Mapeia explicitamente para evitar erros
    db_patient = models.Patient(
        name=patient.name,
        birth_date=patient.birth_date, # Novo campo fundamental
        sex=patient.sex,
        phone=patient.phone,
        insurance=patient.insurance
    )
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    # O Schema PatientOut vai calcular a idade automaticamente antes de responder
    return db_patient

# --- LISTAR PACIENTES ---
@router.get("/", response_model=List[schemas.PatientOut])
def list_patients(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Exige login
):
    return db.query(models.Patient).all()

# --- BUSCAR UM PACIENTE ---
@router.get("/{patient_id}", response_model=schemas.PatientOut)
def get_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return patient

# --- DELETAR PACIENTE ---
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Proteção Crítica!
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(patient)
    db.commit()
    return {"message": "Paciente removido com sucesso"}



