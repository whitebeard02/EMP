import xgboost as xgb
import joblib
import pandas as pd
import json
import numpy as np
from pathlib import Path

# Paths to the downloaded artifacts
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ML_ENGINE_DIR = BASE_DIR / "app/ml_engine"
MODEL_PATH = ML_ENGINE_DIR / "foundation_model_v1.ubj"
EXPLAINER_PATH = ML_ENGINE_DIR / "shap_explainer.joblib"
SIGNATURE_PATH = ML_ENGINE_DIR / "model_signature.json"

class Predictor:
    def __init__(self):
        # LAZY LOADING: Start empty so we don't crash at startup
        self.model = None
        self.explainer = None
        self.feature_order = []
        self.is_ready = False

    def load_artifacts(self):
        """
        Called by main.py AFTER the files are guaranteed to be downloaded.
        """
        print("   🧠 Loading ML Model into Memory...")
        try:
            # 1. Load Model
            if not MODEL_PATH.exists():
                raise FileNotFoundError(f"Model file missing at {MODEL_PATH}")
            
            self.model = xgb.Booster()
            self.model.load_model(MODEL_PATH)

            # 2. Load Signature (Crucial for correct column order)
            if SIGNATURE_PATH.exists():
                with open(SIGNATURE_PATH, "r") as f:
                    sig = json.load(f)
                    self.feature_order = sig.get("feature_order", [])
            
            # 3. Load Explainer (Optional, safe to skip)
            if EXPLAINER_PATH.exists():
                try:
                    self.explainer = joblib.load(EXPLAINER_PATH)
                except Exception as e:
                    print(f"      ⚠️ Warning: Could not load SHAP explainer ({e})")

            self.is_ready = True
            print("      ✅ Model Ready for Predictions.")

        except Exception as e:
            print(f"      ❌ CRITICAL: Failed to load ML artifacts: {e}")
            self.is_ready = False

    def predict(self, patient_data: dict):
        if not self.is_ready:
            return {"error": "Model is not loaded yet."}

        # Convert input dict to DataFrame
        # Ensure we only use columns the model expects, in the right order
        try:
            df = pd.DataFrame([patient_data])
            
            # Reorder columns to match training
            if self.feature_order:
                # Add missing cols with 0, drop extra cols
                for col in self.feature_order:
                    if col not in df.columns:
                        df[col] = 0
                df = df[self.feature_order]
            
            # Convert to DMatrix (Required for XGBoost)
            dmatrix = xgb.DMatrix(df)
            
            # Predict
            prob = self.model.predict(dmatrix)[0] # Returns float 0.0 to 1.0
            is_seizure = prob > 0.5 
            
            return {
                "probability": float(prob),
                "prediction": int(is_seizure),
                "risk_level": "High" if prob > 0.7 else "Medium" if prob > 0.3 else "Low"
            }
        except Exception as e:
            return {"error": f"Prediction failed: {e}"}

# Create a global instance
predictor = Predictor()