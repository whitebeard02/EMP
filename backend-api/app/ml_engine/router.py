from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .service import ml_service

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# Input Schema
class PredictionRequest(BaseModel):
    sleep_hours: float
    stress_level: int
    meds_taken: int
    eeg_profile_id: str = "chb01"

@router.post("/predict")
def get_seizure_risk(data: PredictionRequest):
    try:
        result = ml_service.predict_risk(
            sleep_hours=data.sleep_hours,
            stress_level=data.stress_level,
            meds_taken=data.meds_taken,
            eeg_profile_id=data.eeg_profile_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))