import { useState } from 'react';
import { Menu, Calendar } from 'lucide-react';

// Import your components
import Sidebar from './components/Sidebar';
import DashboardView from './components/DashboardView'; // Ensure this exists
import ProfileView from './components/ProfileView';
import SettingsView from './components/SettingsView';

// Simple placeholder for History if you haven't made it yet
const HistoryView = () => (
  <div className="text-center py-20 text-slate-400">
    <Calendar size={48} className="mx-auto mb-4 opacity-50" />
    <h3 className="text-lg font-bold">No History Yet</h3>
    <p>Complete your first daily log to see trends here.</p>
  </div>
);

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  // Dynamic Header Title based on Tab
  const getHeaderTitle = () => {
    switch(activeTab) {
      case 'dashboard': return 'Good Morning, Alex';
      case 'profile': return 'My Profile';
      case 'settings': return 'Preferences';
      case 'history': return 'Log History';
      default: return 'Farmlytics';
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans">
      
      {/* Sidebar (Navigation) */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab}
        isOpen={isSidebarOpen}
        setIsOpen={setIsSidebarOpen}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        
        {/* Top Header */}
        <header className="bg-white border-b border-slate-100 px-6 py-4 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setIsSidebarOpen(true)}
              className="p-2 -ml-2 text-slate-400 hover:bg-slate-100 rounded-lg lg:hidden"
            >
              <Menu size={24} />
            </button>
            <h1 className="text-xl font-bold text-slate-800">{getHeaderTitle()}</h1>
          </div>
          
          <div className="w-8 h-8 bg-medical-100 rounded-full flex items-center justify-center text-medical-700 font-bold text-xs">
            AL
          </div>
        </header>

        {/* Scrollable Page Content */}
        <main className="flex-1 overflow-y-auto p-6 scroll-smooth">
          <div className="max-w-4xl mx-auto">
            {activeTab === 'dashboard' && <DashboardView />}
            {activeTab === 'profile' && <ProfileView />}
            {activeTab === 'settings' && <SettingsView />}
            {activeTab === 'history' && <HistoryView />}
          </div>
        </main>

      </div>
    </div>
  );
}