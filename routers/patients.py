from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
# Importamos a segurança para proteger as rotas
from auth import get_current_user 

router = APIRouter(prefix="/patients", tags=["Patients"])

# --- CRIAR PACIENTE (Onde estava dando Erro 500) ---
@router.post("/", response_model=schemas.PatientOut)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # O código antigo travava aqui. O novo mapeia os campos certos:
    db_patient = models.Patient(
        name=patient.name,
        birth_date=patient.birth_date, # Agora salvamos a DATA
        sex=patient.sex,
        phone=patient.phone,
        insurance=patient.insurance
    )
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    # O Schema de resposta vai calcular a idade automaticamente
    return db_patient

# --- LISTAR PACIENTES ---
@router.get("/", response_model=List[schemas.PatientOut])
def list_patients(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Patient).all()

# --- DELETAR PACIENTE ---
@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    
    db.delete(patient)
    db.commit()
    return {"message": "Paciente deletado"}
