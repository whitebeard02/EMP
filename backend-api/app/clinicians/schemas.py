from pydantic import BaseModel, EmailStr
from typing import Optional


class ClinicianProfile(BaseModel):
    clinician_id: str
    email: EmailStr
    full_name: str
    specialty: Optional[str] = None
    is_active: bool


class PatientSummary(BaseModel):
    patient_id: str
    has_logs: bool | None = None
    # extend later with more fields if needed


class ClinicianDashboard(BaseModel):
    clinician: ClinicianProfile
    patients: list[PatientSummary]
