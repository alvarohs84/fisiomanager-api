from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models
import schemas
from auth import get_current_user

router = APIRouter(prefix="/assessments", tags=["Assessments"])

@router.get("/", response_model=List[schemas.AssessmentOut])
def list_assessments(patient_id: int = None, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    query = db.query(models.Assessment)
    if patient_id:
        query = query.filter(models.Assessment.patient_id == patient_id)
    return query.order_by(models.Assessment.date.desc()).all()

@router.post("/", response_model=schemas.AssessmentOut)
def create_assessment(data: schemas.AssessmentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    db_assessment = models.Assessment(
        patient_id=data.patient_id,
        specialty=data.specialty,
        content=data.content
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    return db_assessment

@router.delete("/{id}")
def delete_assessment(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    item = db.query(models.Assessment).filter(models.Assessment.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Não encontrado")
    db.delete(item)
    db.commit()
    return {"message": "Deletado"}