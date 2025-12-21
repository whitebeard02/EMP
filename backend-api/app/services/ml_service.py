import os
import xgboost as xgb
import pandas as pd
import numpy as np
from pathlib import Path

class MLService:
    def __init__(self):
        self.model = None
        self.model_path = self._find_model_path()
        self.load_model()

    def _find_model_path(self):
        # 1. Try to find the model relative to the backend folder
        current_dir = Path(__file__).resolve().parent
        # Go up 3 levels: app/services -> app -> backend-api -> EMP
        project_root = current_dir.parent.parent.parent
        
        target_path = project_root / "ml-pipeline" / "models" / "foundation_model_v1.ubj"
        
        print(f"🔍 Looking for model at: {target_path}")
        return target_path

    def load_model(self):
        try:
            if not self.model_path.exists():
                print(f"❌ Model file NOT found at {self.model_path}")
                return

            self.model = xgb.Booster()
            self.model.load_model(str(self.model_path))
            print("✅ XGBoost Model loaded successfully!")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            self.model = None

    def predict(self, input_data: dict):
        if not self.model:
            print("⚠️ Attempted prediction with no model loaded.")
            return {"error": "Model not loaded. Check server logs."}

        try:
            # 1. Define Baseline EEG Features (The "Missing Piece")
            # In a real system, these would come from the live EEG stream.
            # For the Demo/Simulator, we use standard "resting state" values.
            baseline_eeg = {
                "eeg_mean_amp": 0.0,
                "eeg_std_amp": 15.5,
                "eeg_skewness": 0.1,
                "eeg_kurtosis": 3.2,
                "eeg_peak_to_peak": 50.0,
                "eeg_delta_power": 0.45,
                "eeg_theta_power": 0.25,
                "eeg_alpha_power": 0.15,
                "eeg_beta_power": 0.15
            }

            # 2. Combine Lifestyle Inputs with EEG Data
            features = {
                # --- Lifestyle Features (From Sliders) ---
                "hours_of_sleep": float(input_data.get("hours_of_sleep", 0)),
                "stress_level": int(input_data.get("stress_level", 0)),
                "medication_taken": int(input_data.get("medication_taken", 0)),
                
                # --- Moving Averages (Fallback to current if missing) ---
                "hours_of_sleep_7day_avg": float(input_data.get("hours_of_sleep_7day_avg", input_data.get("hours_of_sleep", 0))),
                "stress_level_7day_avg": float(input_data.get("stress_level_7day_avg", input_data.get("stress_level", 0))),
                "medication_taken_7day_avg": float(input_data.get("medication_taken_7day_avg", input_data.get("medication_taken", 0))),

                # --- EEG Features (The Fix) ---
                **baseline_eeg 
            }

            # 3. Convert to DataFrame (Crucial for XGBoost column matching)
            df = pd.DataFrame([features])
            
            # Ensure columns are in the exact order the model expects
            # (XGBoost is sensitive to column order)
            model_columns = [
                'hours_of_sleep', 'stress_level', 'medication_taken',
                'hours_of_sleep_7day_avg', 'stress_level_7day_avg', 'medication_taken_7day_avg',
                'eeg_mean_amp', 'eeg_std_amp', 'eeg_skewness', 'eeg_kurtosis', 'eeg_peak_to_peak',
                'eeg_delta_power', 'eeg_theta_power', 'eeg_alpha_power', 'eeg_beta_power'
            ]
            df = df[model_columns]

            # 4. Predict
            dmatrix = xgb.DMatrix(df)
            prediction = self.model.predict(dmatrix)
            risk_score = float(prediction[0])

            # 5. Logic: Thresholding
            status = "Low Risk"
            if risk_score > 0.7:
                status = "High Risk"
            elif risk_score > 0.4:
                status = "Medium Risk"

            return {
                "risk_percentage": round(risk_score * 100, 1),
                "status": status,
                "baseline_used": input_data.get("patient_id", "Standard Baseline")
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {"error": f"Prediction Logic Failed: {str(e)}"}

# ---------------------------------------------------------
# CRITICAL: This line creates the 'predictor' variable
# that router.py is trying to import.
# ---------------------------------------------------------
predictor = MLService()