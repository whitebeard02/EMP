from pydantic import BaseModel
from typing import Optional


class PatientProfile(BaseModel):
    patient_id: str
    assigned_model_id: Optional[str] = None
    primary_clinician_id: Optional[str] = None


class PatientMeResponse(BaseModel):
    user_id: str
    role: str
    patient: PatientProfile
