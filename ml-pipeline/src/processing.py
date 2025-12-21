import numpy as np
import pandas as pd
import mne
import warnings
from tqdm import tqdm
from scipy.stats import skew, kurtosis
from . import config

# Clean logs
mne.set_log_level('ERROR')
warnings.filterwarnings("ignore")

def extract_statistical_features(data, sfreq):
    features = {}
    
    # Time Domain
    features['mean_amp'] = np.mean(data)
    features['std_amp'] = np.std(data)
    features['skewness'] = skew(data)
    features['kurtosis'] = kurtosis(data)
    features['peak_to_peak'] = np.ptp(data)
    
    # Frequency Domain (Power Spectral Density)
    psd, freqs = mne.time_frequency.psd_array_welch(
        data, sfreq, fmin=0.5, fmax=30.0, n_fft=int(sfreq), verbose=False
    )
    psd /= np.sum(psd) # Normalize
    
    features['delta_power'] = np.sum(psd[(freqs >= 0.5) & (freqs < 4)])
    features['theta_power'] = np.sum(psd[(freqs >= 4) & (freqs < 8)])
    features['alpha_power'] = np.sum(psd[(freqs >= 8) & (freqs < 13)])
    features['beta_power'] = np.sum(psd[(freqs >= 13) & (freqs <= 30)])
    
    return {f"eeg_{k}": v for k, v in features.items()}

def run_eeg_processing():
    print(f"\n🧠 STARTING BATCH EEG PROCESSING")
    edf_files = sorted(list(config.RAW_EEG_DIR.glob("*.edf")))
    
    if not edf_files:
        print("❌ No .edf files found in data/raw/eeg/")
        return False

    all_features = []
    
    # Process files sequentially to save RAM
    for file_path in tqdm(edf_files, desc="Processing Patients"):
        try:
            raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
            if len(raw.ch_names) > 0:
                data = raw.get_data()[0]
                sfreq = raw.info['sfreq']
                stats = extract_statistical_features(data, sfreq)
                stats['eeg_source_id'] = file_path.stem 
                all_features.append(stats)
            del raw # Free memory immediately
        except Exception as e:
            print(f"⚠️ Error: {e}")

    if all_features:
        df = pd.DataFrame(all_features)
        df.to_csv(config.MASTER_EEG_FILE, index=False)
        print(f"✅ Saved master EEG features to: {config.MASTER_EEG_FILE}")
        return True
    return False