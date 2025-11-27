from sqlalchemy import Column, Integer, String, Date, Text
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    plan = Column(String)
    status = Column(String)

class Evolution(Base):
    __tablename__ = "evolutions"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    date = Column(Date)
    text = Column(Text)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String)
    time = Column(String)
    note = Column(String)
    type = Column(String)
    date = Column(Date)
