import os
from pathlib import Path

# Base Directory (Project Root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Input Paths
RAW_EEG_DIR = BASE_DIR / "data/raw/eeg"
RAW_LIFESTYLE_DIR = BASE_DIR / "data/raw/lifestyle"

# Output Paths
PROCESSED_DIR = BASE_DIR / "data/processed"
MODELS_DIR = BASE_DIR / "models"

# Artifact File Names
MASTER_EEG_FILE = PROCESSED_DIR / "master_eeg_features.csv"
TRAINING_DATA_FILE = PROCESSED_DIR / "training_ready_data.csv"
MODEL_FILE = MODELS_DIR / "foundation_model_v1.ubj"
EXPLAINER_FILE = MODELS_DIR / "shap_explainer.joblib"
SIGNATURE_FILE = MODELS_DIR / "model_signature.json"

# Create folders if missing
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Hyperparameters
TEST_SIZE = 0.2
RANDOM_SEED = 42