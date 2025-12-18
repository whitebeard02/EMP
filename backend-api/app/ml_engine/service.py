import os
import json
import pandas as pd
import xgboost as xgb

class MLEngine:
    def __init__(self):
        self.base_dir = os.path.dirname(__file__)
        self.model = None
        self.signature = None
        self.eeg_db = None
        self.load_artifacts()

    def load_artifacts(self):
        """Load model artifacts into memory on startup."""
        print("Loading ML Artifacts...")
        try:
            # 1. Load Model as Native Booster (Bypasses sklearn errors)
            self.model = xgb.Booster()
            self.model.load_model(os.path.join(self.base_dir, "foundation_model_v1.ubj"))
            
            # 2. Load Signature
            with open(os.path.join(self.base_dir, "model_signature.json"), "r") as f:
                self.signature = json.load(f)
                
            # 3. Load EEG DB
            self.eeg_db = pd.read_csv(os.path.join(self.base_dir, "master_eeg_features.csv"))
            print("✅ ML Engine Loaded Successfully.")
        except Exception as e:
            print(f"❌ Failed to load ML artifacts: {e}")

    def predict_risk(self, sleep_hours: float, stress_level: int, meds_taken: int, eeg_profile_id: str = "chb01"):
        """
        Calculates seizure risk based on dynamic inputs + static EEG baseline.
        """
        if not self.model:
            raise RuntimeError("ML Model not loaded.")

        # 1. Get EEG Baseline
        # Matches partial string id (e.g. '101' finds 'chb01')
        mask = self.eeg_db['eeg_source_id'].astype(str).str.contains(str(eeg_profile_id))
        if mask.any():
            patient_eeg = self.eeg_db[mask].iloc[0]
        else:
            patient_eeg = self.eeg_db.iloc[0] # Fallback to default

        # 2. Prepare Input Vector
        input_data = {
            'hours_of_sleep_7day_avg': sleep_hours,
            'stress_level_7day_avg': float(stress_level),
            'medication_taken_7day_avg': float(meds_taken),
            'hours_of_sleep': sleep_hours,
            'stress_level': float(stress_level),
            'medication_taken': float(meds_taken)
        }

        # Merge Static EEG features (excluding ID)
        for col in patient_eeg.index:
            if col.startswith("eeg_") and col != 'eeg_source_id':
                input_data[col] = float(patient_eeg[col])

        # 3. Align with Signature
        df = pd.DataFrame([input_data])
        expected_cols = self.signature['feature_order']
        
        # Zero-fill missing & Reorder
        for col in expected_cols:
            if col not in df.columns:
                df[col] = 0.0
        df = df[expected_cols]

        # 4. Predict using Native DMatrix
        dmatrix = xgb.DMatrix(df)
        prediction = self.model.predict(dmatrix)
        
        # Native predict returns an array of probabilities, we take the first one
        probability = float(prediction[0])
        
        return {
            "risk_percentage": round(probability * 100, 2),
            "status": "High Risk" if probability > 0.5 else "Stable",
            "baseline_used": patient_eeg.get('eeg_source_id', 'Unknown')
        }

# Create a singleton instance to be imported
ml_service = MLEngine()