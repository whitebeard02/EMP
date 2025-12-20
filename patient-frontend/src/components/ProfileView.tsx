import { User, Phone, Mail, MapPin, Shield } from 'lucide-react';

export default function ProfileView() {
  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      
      {/* 1. Main Identity Card */}
      <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm text-center relative overflow-hidden">
        <div className="w-24 h-24 bg-medical-100 rounded-full mx-auto flex items-center justify-center text-medical-600 text-3xl font-bold mb-4 shadow-inner">
          <User size={40} />
        </div>
        <h2 className="text-2xl font-bold text-slate-800">Alex Lewis</h2>
        <p className="text-slate-400 font-medium">Patient ID: #P-1001</p>
        
        {/* Decorative background blob */}
        <div className="absolute top-0 left-0 w-full h-24 bg-gradient-to-b from-medical-50/50 to-transparent -z-10" />
      </div>

      {/* 2. Contact Details (Uses the icons you were missing!) */}
      <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
        <h3 className="font-bold text-slate-800 mb-6 text-sm uppercase tracking-wider text-slate-400">Contact Information</h3>
        <div className="space-y-4">
          
          <div className="flex items-center gap-4 p-3 hover:bg-slate-50 rounded-xl transition-colors">
            <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500">
              <Phone size={18} />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-bold">Mobile Number</p>
              <p className="text-slate-700 font-medium">+1 (555) 123-4567</p>
            </div>
          </div>

          <div className="flex items-center gap-4 p-3 hover:bg-slate-50 rounded-xl transition-colors">
            <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500">
              <Mail size={18} />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-bold">Email Address</p>
              <p className="text-slate-700 font-medium">alex.lewis@example.com</p>
            </div>
          </div>

          <div className="flex items-center gap-4 p-3 hover:bg-slate-50 rounded-xl transition-colors">
            <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center text-slate-500">
              <MapPin size={18} />
            </div>
            <div>
              <p className="text-xs text-slate-400 font-bold">Home Address</p>
              <p className="text-slate-700 font-medium">42 Willow Lane, Springfield</p>
            </div>
          </div>

        </div>
      </div>

      {/* 3. Medical Info */}
      <div className="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm">
        <h3 className="font-bold text-slate-800 mb-6 flex items-center gap-2">
          <Shield size={18} className="text-medical-600" /> Medical Snapshot
        </h3>
        <div className="grid grid-cols-2 gap-4">
           <div className="p-4 bg-slate-50 rounded-2xl">
             <span className="block text-xs text-slate-400 mb-1">Condition</span>
             <span className="font-bold text-slate-700">Temporal Lobe Epilepsy</span>
           </div>
           <div className="p-4 bg-slate-50 rounded-2xl">
             <span className="block text-xs text-slate-400 mb-1">Blood Type</span>
             <span className="font-bold text-slate-700">O+</span>
           </div>
        </div>
      </div>
    </div>
  );
}