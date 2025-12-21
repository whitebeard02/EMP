from src import processing, training

if __name__ == "__main__":
    # 1. Process Raw Data
    success = processing.run_eeg_processing()
    
    # 2. Train Model if step 1 worked
    if success:
        training.run_training_pipeline()