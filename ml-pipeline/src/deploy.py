import os
from supabase import create_client, Client
from dotenv import load_dotenv
from . import config

def deploy_to_cloud():
    print("\n☁️ STARTING CLOUD DEPLOYMENT (Supabase Registry)")
    
    # 1. Load Credentials
    env_path = config.BASE_DIR / ".env"
    load_dotenv(env_path)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Error: Missing SUPABASE_URL or SUPABASE_KEY in .env")
        return False

    try:
        # 2. Connect to Supabase
        supabase: Client = create_client(url, key)
        bucket_name = "model-registry"
        
        # 3. Define Artifacts to Upload
        # Format: (Name inside Cloud Bucket, Path on Local Disk)
        artifacts = [
            ("foundation_model_v1.ubj", config.MODEL_FILE),
            ("model_signature.json", config.SIGNATURE_FILE),
            ("master_eeg_features.csv", config.MASTER_EEG_FILE),
        ]
        
        # Optional: Upload Explainer if it exists
        if config.EXPLAINER_FILE.exists():
            artifacts.append(("shap_explainer.joblib", config.EXPLAINER_FILE))

        # 4. Upload Loop
        for cloud_name, local_path in artifacts:
            if not local_path.exists():
                print(f"   ⚠️ Skipping {cloud_name} (Not found locally)")
                continue

            print(f"   ⬆️ Uploading: {cloud_name}...")
            
            with open(local_path, 'rb') as f:
                # "upsert": "true" means Overwrite if exists
                supabase.storage.from_(bucket_name).upload(
                    path=cloud_name,
                    file=f,
                    file_options={"upsert": "true"}
                )
        
        print("✅ DEPLOYMENT SUCCESS: All artifacts synced to Cloud.")
        return True

    except Exception as e:
        print(f"❌ Deployment Failed: {e}")
        return False