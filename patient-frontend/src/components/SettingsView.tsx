// Remove Smartphone and ChevronRight
import { Bell, Trash2 } from 'lucide-react';

export default function SettingsView() {
  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <h2 className="text-2xl font-bold text-slate-800 px-2">Settings</h2>

      {/* Notifications */}
      <div className="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden">
        <div className="p-6 flex items-center justify-between border-b border-slate-50">
          <div className="flex items-center gap-4">
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg"><Bell size={20} /></div>
            <div>
              <p className="font-bold text-slate-700">Daily Reminders</p>
              <p className="text-xs text-slate-400">Get notified at 8 PM to log data</p>
            </div>
          </div>
          <label className="relative inline-flex items-center cursor-pointer">
            <input type="checkbox" className="sr-only peer" defaultChecked />
            <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-indigo-600"></div>
          </label>
        </div>
      </div>

      {/* Danger Zone */}
      <div className="bg-red-50 rounded-3xl border border-red-100 shadow-sm p-6">
        <div className="flex items-start gap-4">
          <div className="p-2 bg-white text-red-500 rounded-lg shadow-sm"><Trash2 size={20} /></div>
          <div className="flex-1">
            <h3 className="font-bold text-red-900">Delete My Data</h3>
            <p className="text-sm text-red-700/80 mt-1 mb-4">
              This will permanently remove all your daily logs and profile information from our servers. This action cannot be undone.
            </p>
            <button className="w-full py-3 bg-white border border-red-200 text-red-600 font-bold rounded-xl hover:bg-red-600 hover:text-white transition-all shadow-sm">
              Delete All Data
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}