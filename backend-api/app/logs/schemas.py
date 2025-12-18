from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LogCreate(BaseModel):
    seizure_occurred: bool
    mood: Optional[str] = None
    notes: Optional[str] = None


class LogRead(BaseModel):
    log_id: str
    patient_id: str
    created_at: datetime
    seizure_occurred: bool
    mood: Optional[str] = None
    notes: Optional[str] = None
