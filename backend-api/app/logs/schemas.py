from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime 

class LogCreate(BaseModel):
    # ML Features (REQUIRED)
    hours_of_sleep: float
    stress_level: int
    medication_taken: bool
    seizure_occurred: bool
    
    # UI Features (OPTIONAL)
    mood: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[date] = None # Optional, defaults to today if missing

class LogRead(LogCreate):
    log_id: str
    patient_id: str
    created_at: datetime