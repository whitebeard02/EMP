from src import processing, training, deploy  # <--- Import the new module

if __name__ == "__main__":
    # 1. Process
    success_proc = processing.run_eeg_processing()
    
    # 2. Train
    if success_proc:
        training.run_training_pipeline()
        
        # 3. Deploy (New Step)
        deploy.deploy_to_cloud()