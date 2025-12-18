import React from 'react';
import { Moon, Brain, Pill } from 'lucide-react';

// 1. Define the "Shape" of your data (The Fix)
export interface PatientInputs {
  sleep_hours: number;
  stress_level: number;
  meds_taken: number;
  eeg_profile_id: string;
}

interface Props {
  inputs: PatientInputs; // No more 'any'
  setInputs: React.Dispatch<React.SetStateAction<PatientInputs>>; // The correct React type
  onPredict: () => void;
}

export const ControlPanel: React.FC<Props> = ({ inputs, setInputs, onPredict }) => {
  
  // We specify that 'key' must be one of the keys in PatientInputs (like 'sleep_hours')
  const handleChange = (key: keyof PatientInputs, value: number | string) => {
    setInputs((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 space-y-8">
      <div>
        <h3 className="text-lg font-bold text-slate-800 mb-6 flex items-center gap-2">
          <span className="w-1 h-6 bg-medical-600 rounded-full"></span>
          Live Patient Data Simulator
        </h3>
        
        {/* Sleep Slider */}
        <div className="space-y-3">
          <div className="flex justify-between">
            <label className="flex items-center gap-2 text-slate-600 font-medium">
              <Moon size={18} className="text-indigo-500" /> Sleep Duration (Avg)
            </label>
            <span className="text-indigo-600 font-bold">{inputs.sleep_hours} hrs</span>
          </div>
          <input 
            type="range" min="0" max="12" step="0.5"
            value={inputs.sleep_hours}
            // We explicitely tell it we are changing 'sleep_hours'
            onChange={(e) => handleChange('sleep_hours', parseFloat(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-indigo-600"
          />
        </div>

        {/* Stress Slider */}
        <div className="space-y-3 mt-6">
          <div className="flex justify-between">
            <label className="flex items-center gap-2 text-slate-600 font-medium">
              <Brain size={18} className="text-orange-500" /> Stress Level
            </label>
            <span className="text-orange-600 font-bold">{inputs.stress_level} / 5</span>
          </div>
          <input 
            type="range" min="1" max="5" step="1"
            value={inputs.stress_level}
            onChange={(e) => handleChange('stress_level', parseInt(e.target.value))}
            className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-orange-500"
          />
          <div className="flex justify-between text-xs text-slate-400 px-1">
            <span>Low</span><span>High</span>
          </div>
        </div>

        {/* Meds Toggle */}
        <div className="mt-8 p-4 bg-slate-50 rounded-lg flex items-center justify-between border border-slate-100">
          <div className="flex items-center gap-3">
            <div className={`p-2 rounded-lg ${inputs.meds_taken ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'}`}>
              <Pill size={24} />
            </div>
            <div>
              <div className="font-semibold text-slate-700">Medication Adherence</div>
              <div className="text-xs text-slate-500">Has the patient taken meds?</div>
            </div>
          </div>
          <button
            onClick={() => handleChange('meds_taken', inputs.meds_taken ? 0 : 1)}
            className={`px-4 py-2 rounded-md font-medium transition-colors ${
              inputs.meds_taken 
                ? 'bg-green-600 text-white hover:bg-green-700' 
                : 'bg-red-500 text-white hover:bg-red-600'
            }`}
          >
            {inputs.meds_taken ? 'Yes, Taken' : 'No, Missed'}
          </button>
        </div>
      </div>

      <button 
        onClick={onPredict}
        className="w-full py-4 bg-medical-600 hover:bg-medical-700 text-white rounded-xl font-bold text-lg shadow-lg shadow-medical-500/30 transition-all active:scale-95"
      >
        Run AI Prediction Model
      </button>
    </div>
  );
};