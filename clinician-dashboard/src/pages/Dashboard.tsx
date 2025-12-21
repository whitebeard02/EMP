// src/pages/Dashboard.tsx
import { useState, useEffect } from 'react';
import { ControlPanel, type PatientInputs } from '../components/ControlPanel';
import { RiskCard } from '../components/RiskCard';
import { getSeizureRisk, getDemoPatients, getPatientStats, type RiskPrediction, type DemoPatient } from '../services/api';
import { Activity, Users, Database, LogOut } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { signOut } = useAuth(); // Hook to handle logout
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<RiskPrediction | null>(null);
  const [patients, setPatients] = useState<DemoPatient[]>([]);
  
  const [inputs, setInputs] = useState<PatientInputs>({
    sleep_hours: 7.5,
    stress_level: 2,
    meds_taken: 1,
    eeg_profile_id: 'chb01'
  });

  // 1. Load the Patient List from Backend on Startup
  useEffect(() => {
    const init = async () => {
      const list = await getDemoPatients();
      setPatients(list);
      
      // Auto-select the first patient if available
      if (list.length > 0) {
        handlePatientSelect(list[0].id, list[0].eeg_id);
      }
    };
    init();
  }, []);

  // 2. Logic to handle selecting a patient
  const handlePatientSelect = async (filename: string, eegId: string) => {
    setLoading(true);
    
    // A. Fetch Real History from CSV
    const stats = await getPatientStats(filename);
    
    if (stats) {
      // B. Update inputs with Real Data
      const newInputs = {
        sleep_hours: stats.sleep_hours,
        stress_level: stats.stress_level,
        meds_taken: stats.meds_taken,
        eeg_profile_id: eegId
      };
      setInputs(newInputs);
      
      // C. Auto-Run Prediction
      const prediction = await getSeizureRisk(newInputs);
      setResult(prediction);
    }
    setLoading(false);
  };

  const handlePredict = async () => {
    if (loading) return;
    setLoading(true);
    try {
      await new Promise(r => setTimeout(r, 500)); 
      const data = await getSeizureRisk(inputs);
      setResult(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans">
      <nav className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between sticky top-0 z-10">
        <div className="flex items-center gap-3">
          <div className="bg-medical-600 p-2 rounded-lg text-white">
            <Activity size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-800 leading-none">Epilepsy Management Platform</h1>
            <span className="text-xs font-semibold text-medical-600 uppercase tracking-widest">Clinician Dashboard</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 px-3 py-1 bg-green-50 rounded-full text-sm font-medium text-green-700 border border-green-100">
            <Database size={14} /> 
            Data Source: {patients.length > 0 ? "Live CSV" : "Offline"}
          </div>
          
          {/* LOGOUT BUTTON ADDED HERE */}
          <button 
            onClick={signOut}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
          >
            <LogOut size={16} />
            Log Out
          </button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-8 mt-4">
        <div className="lg:col-span-7 space-y-6">
          
          {/* Dynamic Patient Selector */}
          <div className="bg-white p-4 rounded-xl border border-slate-200 flex items-center gap-4 shadow-sm">
            <div className="p-3 bg-slate-100 rounded-full text-slate-500">
              <Users size={24} />
            </div>
            <div className="flex-1">
              <label className="block text-xs font-bold text-slate-400 uppercase">Select Real Patient Data</label>
              <select 
                className="w-full bg-transparent font-semibold text-lg outline-none cursor-pointer mt-1"
                onChange={(e) => {
                  const p = patients.find(pat => pat.id === e.target.value);
                  if (p) handlePatientSelect(p.id, p.eeg_id);
                }}
              >
                {patients.map(p => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>
          </div>

          <ControlPanel 
            inputs={inputs} 
            setInputs={setInputs} 
            onPredict={handlePredict} 
          />
        </div>

        <div className="lg:col-span-5 space-y-6">
          <div className="sticky top-28">
            <RiskCard 
              risk={result?.risk_percentage ?? null} 
              status={result?.status ?? "Unknown"} 
              loading={loading} 
            />
            
            {/* Real Data Evidence Panel */}
            <div className="mt-6 p-4 rounded-lg border border-slate-200 bg-white text-xs text-slate-500">
              <div className="font-bold mb-3 uppercase tracking-wider text-slate-400">Data Provenance</div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <span className="block text-slate-400">Bio-Signal Source</span>
                  <span className="font-mono font-medium text-slate-700">{result?.baseline_used || '...'}</span>
                </div>
                <div>
                  <span className="block text-slate-400">Lifestyle Data</span>
                  <span className="font-mono font-medium text-slate-700">7-Day Moving Avg</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;