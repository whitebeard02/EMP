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

export const getSeizureRisk = async (inputs: PatientInputs): Promise<RiskPrediction | null> => {
  try {
    const response = await axios.post(`${API_URL}/ml/predict`, inputs);
    return response.data;
  } catch (error) {
    console.error("Failed to connect to ML Engine:", error);
    return null;
  }
};