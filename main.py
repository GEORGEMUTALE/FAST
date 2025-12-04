from models import MedicationCreate, Medication, StockUpdate, PrescriptionBase, Prescription
from fastapi import FastAPI, HTTPException
from typing import List, Dict, Optional
from uuid import UUID

medications_db: Dict[UUID, Medication] = {}
prescriptions_db: Dict[UUID, Prescription] = {}

app = FastAPI(title="Pharmacy Inventory and Prescription Management")

@app.post("/medications/", response_model=Medication, status_code=201, tags=["Medications"])
def create_medication(medication: MedicationCreate):
    new_medication = Medication(
        name = medication.name,
        dosage = medication.dosage,
        manufacturer = medication.manufacturer
    )
    medications_db[new_medication.id] = new_medication
    return new_medication

@app.get("/medications/", response_model=List[Medication], tags=["Medications"])
def list_medications():
    return list(medications_db.values())    

@app.patch("/medications/{medication_id}/stock", response_model=Medication, tags=["Medications"])
def update_stock(medication_id: UUID, stock_update: StockUpdate):
    medication = medications_db.get(medication_id)
    if not  medication:
        raise HTTPException(status_code=404, detail="Medication not found")
    new_stock_level = medication.stock_level + stock_update.stock_change
    if new_stock_level < 0:
        raise HTTPException(status_code=400, detail="Stock level cannot be negative")
    medication.stock_level = new_stock_level
    medications_db[medication_id] = medication
    return medication

@app.post("/prescriptions/", response_model=Prescription, status_code=201, tags=["Prescriptions"])
def create_prescription(prescription: PrescriptionBase):
    for med_id in prescription.medication_ids:
        if med_id not in medications_db:
            raise HTTPException(status_code=404, detail=f"Medication with ID {med_id} not found")
    new_prescription = Prescription(
        patient_name = prescription.patient_name,
        medication_ids = prescription.medication_ids,
        prescribed_date = prescription.prescribed_date
    )
    prescriptions_db[new_prescription.id] = new_prescription
    return new_prescription

