from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
# NEW IMPORT: Pointing to the correct global predictor
from app.services.ml_service import predictor

router = APIRouter(prefix="/ml", tags=["Machine Learning"])

# Input matches the Database/CSV columns exactly
class PredictionRequest(BaseModel):
    hours_of_sleep: float
    stress_level: int
    medication_taken: int  # 1 for Yes, 0 for No (ML expects numbers)
    eeg_profile_id: str = "chb01" # Default to chb01 for now

@router.post("/predict")
def get_seizure_risk(data: PredictionRequest):
    try:
        # Call the NEW predictor logic
        result = predictor.predict({
            "hours_of_sleep": data.hours_of_sleep,
            "stress_level": data.stress_level,
            "medication_taken": data.medication_taken,
            
            # TODO: In the future, we will calculate these 7-day avgs from the DB.
            # For now, we pass current values to get the connection working.
            "hours_of_sleep_7day_avg": data.hours_of_sleep,
            "stress_level_7day_avg": data.stress_level,
            "medication_taken_7day_avg": data.medication_taken,
            
            "patient_id": data.eeg_profile_id 
        })
        
        if "error" in result:
             raise HTTPException(status_code=500, detail=result["error"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))