import React from 'react';
import { AlertTriangle, CheckCircle, Activity } from 'lucide-react';

interface Props {
  risk: number | null;
  status: string;
  loading: boolean;
}

export const RiskCard: React.FC<Props> = ({ risk, status, loading }) => {
  if (loading) {
    return (
      <div className="h-64 flex items-center justify-center bg-white rounded-xl shadow-lg border border-slate-200 animate-pulse">
        <div className="text-slate-400">Analyzing Bio-signals...</div>
      </div>
    );
  }

  if (risk === null) return null;

  const isHighRisk = risk > 50;
  
  return (
    <div className={`relative overflow-hidden rounded-2xl shadow-xl border-2 transition-all duration-500 ${
      isHighRisk 
        ? 'bg-red-50 border-red-200 shadow-red-100' 
        : 'bg-emerald-50 border-emerald-200 shadow-emerald-100'
    }`}>
      <div className="p-8 text-center">
        <div className="flex justify-center mb-4">
          {isHighRisk ? (
            <div className="p-4 bg-red-100 rounded-full text-red-600 animate-bounce">
              <AlertTriangle size={48} />
            </div>
          ) : (
            <div className="p-4 bg-emerald-100 rounded-full text-emerald-600">
              <CheckCircle size={48} />
            </div>
          )}
        </div>
        
        <h2 className="text-slate-500 font-semibold uppercase tracking-wider text-sm mb-1">
          Seizure Probability
        </h2>
        <div className={`text-6xl font-bold mb-2 ${
          isHighRisk ? 'text-red-700' : 'text-emerald-700'
        }`}>
          {risk}%
        </div>
        
        <div className={`inline-flex items-center gap-2 px-4 py-1.5 rounded-full font-medium text-sm ${
          isHighRisk ? 'bg-red-200 text-red-800' : 'bg-emerald-200 text-emerald-800'
        }`}>
          <Activity size={16} />
          {status.toUpperCase()}
        </div>
      </div>
    </div>
  );
};