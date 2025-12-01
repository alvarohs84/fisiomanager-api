from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user 

router = APIRouter(prefix="/patients", tags=["Patients"])

# --- CRIAR PACIENTE (Onde está o erro) ---
@router.post("/", response_model=schemas.PatientOut)
def create_patient(
    patient: schemas.PatientCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verifica se já existe um paciente com esse nome (opcional, para evitar duplicatas)
    # db_patient_exists = db.query(models.Patient).filter(models.Patient.name == patient.name).first()
    # if db_patient_exists:
    #    raise HTTPException(status_code=400, detail="Paciente já cadastrado")

    # Cria o objeto usando os campos NOVOS
    db_patient = models.Patient(
        name=patient.name,
        birth_date=patient.birth_date, # O Backend agora espera isso!
        sex=patient.sex,
        phone=patient.phone,
        insurance=patient.insurance
    )
    
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    # O Schema calcula a idade automaticamente na volta
    return db_patient

# --- LISTAR ---
@router.get("/", response_model=List[schemas.PatientOut])
def list_patients(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Patient).all()

# --- DELETAR ---
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


