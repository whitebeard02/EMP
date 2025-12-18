import os
import glob
import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/demo", tags=["CSV Demo"])

# Path to your folder (relative to backend-api root)
CSV_FOLDER = "csv_data"

# Mapping logic (Same as before: 12 patients -> 12 profiles)
EEG_PROFILES = [
    "chb01", "chb02", "chb03", "chb04", "chb05", "chb06",
    "chb07", "chb08", "chb09", "chb10", "chb11", "chb12"
]

@router.get("/patients")
def get_csv_patients():
    """
    Scans the 'csv_data' folder and returns a list of available patients.
    """
    if not os.path.exists(CSV_FOLDER):
        raise HTTPException(status_code=404, detail="csv_data folder not found")

    files = sorted(glob.glob(os.path.join(CSV_FOLDER, "*.csv")))
    patients = []

    for index, file_path in enumerate(files):
        filename = os.path.basename(file_path)
        # Create a clean display name (e.g., "Patient 1 (P1001...)")
        display_name = f"Patient {index + 1} ({filename.split('_')[0]})"
        
        # Assign EEG Profile
        assigned_eeg = EEG_PROFILES[index % len(EEG_PROFILES)]
        
        patients.append({
            "id": filename, # We use the filename as the ID to find it later
            "name": display_name,
            "eeg_id": assigned_eeg
        })
    
    return patients

@router.get("/patient/{filename}")
def get_patient_data(filename: str):
    """
    Reads a specific CSV, calculates 7-day stats, and returns them for the dashboard.
    """
    file_path = os.path.join(CSV_FOLDER, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Patient file not found")

    try:
        df = pd.read_csv(file_path)
        
        # Ensure we have data
        if df.empty:
            raise ValueError("CSV is empty")

        # Get the LAST 7 days of data (Real History)
        last_7 = df.tail(7)
        
        # Calculate Real Averages
        avg_sleep = round(last_7['hours_of_sleep'].mean(), 1)
        avg_stress = int(last_7['stress_level'].mean())
        avg_meds = int(round(last_7['medication_taken'].mean())) # 0 or 1

        return {
            "sleep_hours": avg_sleep,
            "stress_level": avg_stress,
            "meds_taken": avg_meds,
            "recent_logs": last_7.to_dict(orient="records") # Optional: if you want to show a chart later
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))