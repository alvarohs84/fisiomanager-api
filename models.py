from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date  # <--- IMPORTANTE

# ======================================================
# USUÁRIOS
# ======================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# ======================================================
# PACIENTES
# ======================================================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String, index=True)
    birth_date = Column(Date, nullable=False)   
    sex = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    insurance = Column(String, nullable=True)

    evolutions = relationship("Evolution", back_populates="patient")
    appointments = relationship("Appointment", back_populates="patient")

    # --- O SEGREDO DO FIX: CAMPO CALCULADO ---
    @property
    def idade(self):
        if not self.birth_date:
            return 0
        today = date.today()
        # Cálculo preciso da idade
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

# ======================================================
# EVOLUÇÕES
# ======================================================
class Evolution(Base):
    __tablename__ = "evolutions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    description = Column(String, nullable=False)

    patient = relationship("Patient", back_populates="evolutions")

# ======================================================
# AGENDAMENTOS
# ======================================================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    date = Column(String)
    time = Column(String)
    notes = Column(String, nullable=True)
    
    patient = relationship("Patient", back_populates="appointments")