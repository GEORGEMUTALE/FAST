from pydantic import BaseModel, Field
from uuid import UUID, uuid4

class MedicationBase(BaseModel):
    name: str = Field(...)
    dosage: str = Field(...)
    manufacturer: str = Field(...)

class MedicationCreate(MedicationBase):
    pass                    

class Medication(MedicationBase):
    id: UUID = Field(default_factory=uuid4)
    stock_level: int = Field(default=0, ge=0)

    class Config:
        form_attributes = True

class StockUpdate(BaseModel):
    stock_change: int = Field(...)
    

class PrescriptionBase(BaseModel):
    patient_name: str = Field(...)
    medication_id: UUID = Field(...)
    quantity: int = Field(..., gt=0)
    instructions: str = Field(...)

class Prescription(PrescriptionBase):
    id: UUID = Field(default_factory=uuid4)
    status: str = Field(default="Pending")

    class Config:
        form_attributes = True