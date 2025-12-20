import { useState } from 'react';
import { 
  Moon, 
  Pill, 
  Activity, 
  CheckCircle2, 
  ChevronRight, 
  Calendar,
  ShieldCheck,
  AlertCircle
} from 'lucide-react';

export default function PatientApp() {
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  // --- Form State ---
  const [sleep, setSleep] = useState<number>(7.5);
  const [medsTaken, setMedsTaken] = useState<boolean | null>(null);
  const [hasStress, setHasStress] = useState<boolean | null>(null); // "Are you in any stress?"
  const [stressLevel, setStressLevel] = useState<number>(3); // 1-5 Rating

  const handleSubmit = async () => {
    setLoading(true);
    // Simulate Web API Call
    console.log("Submitting Payload:", { sleep, medsTaken, hasStress, stressLevel });
    await new Promise(resolve => setTimeout(resolve, 1500));
    setLoading(false);
    setSubmitted(true);
  };

  // --- Success View ---
  if (submitted) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-sans">
        <div className="bg-white w-full max-w-md p-8 rounded-3xl shadow-xl text-center space-y-6 animate-in fade-in zoom-in duration-500 border border-slate-100">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto text-green-600 shadow-sm">
            <CheckCircle2 size={48} strokeWidth={3} />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-800">You're All Set!</h2>
            <p className="text-slate-500 mt-2">Your daily log has been securely sent to your clinician. Have a great day!</p>
          </div>
          <button 
            onClick={() => window.location.reload()}
            className="w-full py-3 bg-slate-100 text-slate-600 font-semibold rounded-xl hover:bg-slate-200 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    );
  }

  // --- Main Web Form View ---
  return (
    <div className="min-h-screen bg-slate-50 font-sans pb-12">
      
      {/* 1. Hero / Header Section */}
      <header className="bg-medical-600 text-white pt-12 pb-32 px-6 rounded-b-[3rem] shadow-xl relative overflow-hidden">
        {/* Background Decorative Elements */}
        <div className="absolute top-0 right-0 p-12 opacity-10 pointer-events-none">
          <Activity size={120} />
        </div>
        <div className="absolute bottom-0 left-10 w-32 h-32 bg-white/10 rounded-full blur-3xl"></div>
        
        <div className="max-w-md mx-auto relative z-10">
          <div className="flex items-center justify-between mb-4">
            <span className="opacity-80 text-xs font-bold uppercase tracking-widest">EMP Patient Portal</span>
            <div className="flex items-center gap-1 bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-[10px] font-bold shadow-sm">
              <ShieldCheck size={12} /> ENCRYPTED
            </div>
          </div>
          <h1 className="text-3xl font-bold tracking-tight">Good Morning, Alex</h1>
          <p className="text-medical-100 mt-2 flex items-center gap-2 text-sm font-medium">
            <Calendar size={16} /> 
            {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })}
          </p>
        </div>
      </header>

      {/* 2. Main Card Container (Overlapping Header) */}
      <main className="max-w-md mx-auto px-6 -mt-20 relative z-20 space-y-6">
        
        {/* --- Card A: Sleep --- */}
        <section className="bg-white p-6 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 transition-transform hover:scale-[1.01] duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-indigo-100 rounded-2xl flex items-center justify-center text-indigo-600 shadow-sm">
              <Moon size={20} strokeWidth={2.5} />
            </div>
            <h2 className="text-lg font-bold text-slate-800">Sleep Duration</h2>
          </div>
          
          <div className="flex items-end justify-center mb-8 gap-2">
            <span className="text-6xl font-bold text-slate-800 tracking-tighter">{sleep}</span>
            <span className="text-slate-400 font-bold text-lg mb-2">hours</span>
          </div>
          
          <input 
            type="range" min="0" max="12" step="0.5"
            value={sleep}
            onChange={(e) => setSleep(parseFloat(e.target.value))}
            className="w-full h-3 bg-slate-100 rounded-full appearance-none cursor-pointer accent-indigo-600 hover:accent-indigo-500 transition-all"
          />
          <div className="flex justify-between text-xs text-slate-400 mt-3 font-semibold px-1">
            <span>0h</span>
            <span>6h</span>
            <span>12h+</span>
          </div>
        </section>

        {/* --- Card B: Medication --- */}
        <section className="bg-white p-6 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 transition-transform hover:scale-[1.01] duration-300">
          <div className="flex items-center gap-3 mb-2">
            <div className="w-10 h-10 bg-emerald-100 rounded-2xl flex items-center justify-center text-emerald-600 shadow-sm">
              <Pill size={20} strokeWidth={2.5} />
            </div>
            <h2 className="text-lg font-bold text-slate-800">Medication</h2>
          </div>
          <p className="text-slate-400 text-sm mb-6 ml-13">Did you take your prescribed dosage?</p>
          
          <div className="grid grid-cols-2 gap-4">
            <button 
              onClick={() => setMedsTaken(true)}
              className={`p-4 rounded-2xl border-2 flex flex-col items-center gap-2 transition-all duration-200 ${
                medsTaken === true 
                ? 'border-emerald-500 bg-emerald-50 text-emerald-700 shadow-md transform scale-[1.02]' 
                : 'border-slate-100 hover:border-emerald-200 text-slate-400 bg-slate-50/50'
              }`}
            >
              <CheckCircle2 size={28} className={medsTaken === true ? 'fill-emerald-500 text-white' : ''} />
              <span className="font-bold text-sm">Yes, Taken</span>
            </button>
            
            <button 
              onClick={() => setMedsTaken(false)}
              className={`p-4 rounded-2xl border-2 flex flex-col items-center gap-2 transition-all duration-200 ${
                medsTaken === false 
                ? 'border-red-500 bg-red-50 text-red-700 shadow-md transform scale-[1.02]' 
                : 'border-slate-100 hover:border-red-200 text-slate-400 bg-slate-50/50'
              }`}
            >
              <div className={`w-7 h-7 rounded-full border-2 flex items-center justify-center font-bold text-sm ${medsTaken === false ? 'border-red-600 bg-red-600 text-white' : 'border-current'}`}>✕</div>
              <span className="font-bold text-sm">Skipped</span>
            </button>
          </div>
        </section>

        {/* --- Card C: Stress Check + Rating --- */}
        <section className="bg-white p-6 rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 transition-transform hover:scale-[1.01] duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 bg-orange-100 rounded-2xl flex items-center justify-center text-orange-600 shadow-sm">
              <AlertCircle size={20} strokeWidth={2.5} />
            </div>
            <h2 className="text-lg font-bold text-slate-800">Stress Check</h2>
          </div>

          {/* Question 1: Yes/No */}
          <div className="mb-6">
            <p className="text-sm font-semibold text-slate-600 mb-3">Are you feeling stressed today?</p>
            <div className="flex bg-slate-100 p-1 rounded-xl">
              <button
                onClick={() => { setHasStress(false); setStressLevel(1); }}
                className={`flex-1 py-3 rounded-lg text-sm font-bold transition-all ${
                  hasStress === false 
                  ? 'bg-white text-slate-800 shadow-sm' 
                  : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                No, I'm good
              </button>
              <button
                onClick={() => setHasStress(true)}
                className={`flex-1 py-3 rounded-lg text-sm font-bold transition-all ${
                  hasStress === true 
                  ? 'bg-white text-orange-600 shadow-sm' 
                  : 'text-slate-400 hover:text-slate-600'
                }`}
              >
                Yes, a bit
              </button>
            </div>
          </div>

          {/* Question 2: Rating (Only if Yes) */}
          <div className={`transition-all duration-300 overflow-hidden ${hasStress ? 'max-h-40 opacity-100' : 'max-h-0 opacity-0'}`}>
            <div className="pt-4 border-t border-slate-100">
              <div className="flex justify-between items-center mb-4">
                 <span className="text-xs font-bold text-slate-400 uppercase tracking-wide">Rate Intensity</span>
                 <span className="text-xs font-bold text-orange-600 bg-orange-50 px-2 py-1 rounded-md">Level {stressLevel}</span>
              </div>

              <div className="flex gap-2">
                {[1, 2, 3, 4, 5].map((level) => (
                  <button
                    key={level}
                    onClick={() => setStressLevel(level)}
                    className={`flex-1 aspect-square rounded-xl font-bold text-lg transition-all duration-200 border-2 ${
                      stressLevel === level 
                      ? 'bg-orange-500 text-white border-orange-500 shadow-lg shadow-orange-500/30 scale-110' 
                      : 'bg-white text-slate-300 border-slate-100 hover:border-orange-200'
                    }`}
                  >
                    {level}
                  </button>
                ))}
              </div>
              <div className="flex justify-between text-[10px] text-slate-400 mt-2 px-1 font-medium">
                <span>Mild</span>
                <span>Severe</span>
              </div>
            </div>
          </div>
        </section>

        {/* 3. Submit Action */}
        <button
          onClick={handleSubmit}
          disabled={loading || medsTaken === null || hasStress === null}
          className="w-full bg-medical-600 text-white py-4 rounded-2xl font-bold text-lg shadow-lg shadow-medical-500/30 flex items-center justify-center gap-3 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-medical-700 hover:shadow-xl hover:-translate-y-1 transition-all active:scale-95"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              Saving...
            </span>
          ) : (
            <>Save Daily Log <ChevronRight size={20} /></>
          )}
        </button>

        <p className="text-center text-xs text-slate-400 pb-8">
          This data is for tracking purposes only. <br/>
          <span className="underline cursor-pointer hover:text-medical-600">Privacy Policy</span>
        </p>
      </main>
    </div>
  );
}