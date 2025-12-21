import axios from 'axios';

// Ensure this matches your running Python backend URL
const API_URL = 'http://127.0.0.1:8000';

export interface RiskPrediction {
  risk_percentage: number;
  status: string;
  baseline_used: string;
}

export interface PatientInputs {
  sleep_hours: number;
  stress_level: number;
  meds_taken: number; // 1 for Yes, 0 for No
  eeg_profile_id: string;
}

// NEW: Interface for the Patient List
export interface DemoPatient {
  id: string;      // The filename (e.g., "P1001.csv")
  name: string;    // Display name
  eeg_id: string;  // The EEG profile (e.g., "chb01")
}

// NEW: Fetch list of patients from CSV folder
export const getDemoPatients = async (): Promise<DemoPatient[]> => {
  try {
    const response = await axios.get(`${API_URL}/demo/patients`);
    return response.data;
  } catch (error) {
    console.error("Failed to load demo patients:", error);
    return [];
  }
};

// NEW: Fetch real stats from a specific CSV
export const getPatientStats = async (filename: string) => {
  try {
    const response = await axios.get(`${API_URL}/demo/patient/${filename}`);
    return response.data; // Returns { sleep_hours: 5.5, ... }
  } catch (error) {
    console.error("Failed to load patient stats:", error);
    return null;
  }
};

// Inside src/services/api.ts

export const getSeizureRisk = async (inputs: PatientInputs): Promise<RiskPrediction> => {
  // 1. TRANSLATE Frontend names to Backend names
  const payload = {
    hours_of_sleep: inputs.sleep_hours,      // Backend expects 'hours_of_sleep'
    stress_level: inputs.stress_level,       // Matches
    medication_taken: Number(inputs.meds_taken), // Backend expects 'medication_taken' (as Number)
    eeg_profile_id: inputs.eeg_profile_id    // Matches
  };

  // 2. Send the Request
  // Ensure your API_URL is correct (e.g., 'http://localhost:8000')
  const response = await fetch(`${API_URL}/ml/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      // If your /ml/predict is protected, you might need to add:
      // 'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify(payload) // Send the TRANSLATED payload
  });

  if (!response.ok) {
    throw new Error('Prediction failed');
  }

  return response.json();
};