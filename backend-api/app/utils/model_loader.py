import os
from pathlib import Path
from supabase import create_client, Client
from dotenv import load_dotenv

# Path to where the backend stores its ML brains
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ML_ENGINE_DIR = BASE_DIR / "app/ml_engine"

def sync_models_from_cloud():
    """
    Downloads the latest model artifacts from Supabase Storage
    into the local ml_engine folder.
    """
    print("☁️ CHECKING MODEL REGISTRY FOR UPDATES...")
    
    # Ensure local folder exists
    ML_ENGINE_DIR.mkdir(parents=True, exist_ok=True)

    # Load Env Variables
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Ensure this is in backend-api/.env

    if not url or not key:
        print("⚠️ Warning: No Cloud Credentials. Using local models.")
        return

    try:
        supabase: Client = create_client(url, key)
        bucket = "model-registry"
        
        # Files to download
        files_to_sync = [
            "foundation_model_v1.ubj",
            "model_signature.json",
            "master_eeg_features.csv"
        ]

        for filename in files_to_sync:
            print(f"   ⬇️ Syncing {filename}...")
            
            # Download bytes
            data = supabase.storage.from_(bucket).download(filename)
            
            # Write to disk
            local_path = ML_ENGINE_DIR / filename
            with open(local_path, "wb") as f:
                f.write(data)
                
        print("✅ AI SYSTEM SYNCHRONIZED.")

    except Exception as e:
        print(f"⚠️ Cloud Sync Failed: {e}")
        print("   ➡️ Falling back to existing local models.")


if __name__ == "__main__":
    # This block runs ONLY when you execute the file directly
    sync_models_from_cloud()