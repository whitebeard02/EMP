import pandas as pd
import numpy as np
import xgboost as xgb
import shap
import joblib
import json
import os
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import classification_report
from . import config

def run_training_pipeline():
    print("\n🚀 STARTING CPU TRAINING PIPELINE (Intel Optimized)")
    
    # --- 1. Load & Integrate Data ---
    if not config.MASTER_EEG_FILE.exists():
        print("❌ Missing EEG features. Run processing first.")
        return

    eeg_df = pd.read_csv(config.MASTER_EEG_FILE)
    csv_files = sorted(list(config.RAW_LIFESTYLE_DIR.glob("*.csv")))
    life_df = pd.concat((pd.read_csv(f) for f in csv_files), ignore_index=True)
    
    # Feature Engineering (7-Day Rolling Avg)
    cols = ['hours_of_sleep', 'stress_level', 'medication_taken']
    for c in cols:
        life_df[f"{c}_7day_avg"] = life_df.groupby('patient_id')[c].transform(
            lambda x: x.rolling(7, min_periods=1).mean()
        )

    # Dynamic Merge (12 Patients <-> 12 EEG Profiles)
    patient_ids = sorted(life_df['patient_id'].unique())
    eeg_ids = sorted(eeg_df['eeg_source_id'].unique())
    
    merged_frames = []
    for i, pid in enumerate(patient_ids):
        assigned_eeg = eeg_ids[i % len(eeg_ids)]
        p_data = life_df[life_df['patient_id'] == pid].copy()
        eeg_row = eeg_df[eeg_df['eeg_source_id'] == assigned_eeg].iloc[0]
        
        for col in eeg_df.columns:
            if col != 'eeg_source_id':
                p_data[col] = eeg_row[col]
        merged_frames.append(p_data)
        
    df = pd.concat(merged_frames, ignore_index=True)
    
    # --- 2. Train Model (STRICT CPU MODE) ---
    # Drop non-numeric and target columns
    X = df.drop(columns=['patient_id', 'date', 'seizure_occurred', 'notes', 'mood', 'eeg_feature_1', 'mri_lesion_present'], errors='ignore')
    X = X.select_dtypes(include=[np.number])
    y = df['seizure_occurred']
    
    # Split
    gss = GroupShuffleSplit(n_splits=1, test_size=config.TEST_SIZE, random_state=42)
    train_idx, test_idx = next(gss.split(X, y, df['patient_id']))
    X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
    X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
    
    print("   ⚙️ Training XGBoost on CPU (Hist mode)...")
    
    # XGBoost CPU Configuration
    # We remove 'device' parameter to let XGBoost auto-detect CPU
    model = xgb.XGBClassifier(
        tree_method="hist",  # <--- FORCE CPU HISTOGRAM
        n_estimators=300, 
        learning_rate=0.05,
        max_depth=6,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # --- 3. Save Model Artifacts ---
    print(f"   💾 Saving model to {config.MODEL_FILE}...")
    model.save_model(config.MODEL_FILE)
    
    # Save Signature
    with open(config.SIGNATURE_FILE, "w") as f:
        json.dump({"feature_order": list(X.columns)}, f)

    # --- 4. SHAP Explanation (Safety Block) ---
    print("   📊 Generating Explainer...")
    try:
        # We use the generic Explainer which is more robust to version mismatches
        explainer = shap.Explainer(model)
        joblib.dump(explainer, config.EXPLAINER_FILE)
        print("      ✅ Explainer saved successfully.")
    except Exception as e:
        print(f"      ⚠️ Warning: SHAP generation failed ({e}).")
        print("      ⚠️ Skipping Explainer. The Model is still safe to use.")

    print(f"\n✅ PIPELINE COMPLETE. Model ready at: {config.MODELS_DIR}")
    print("\nModel Performance:")
    print(classification_report(y_test, model.predict(X_test)))