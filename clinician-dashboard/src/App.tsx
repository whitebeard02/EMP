// src/App.tsx
import { type ReactNode } from 'react'; // <--- FIX 1: Import the type explicitly
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';

// Security Wrapper
// FIX 2: Use ReactNode instead of JSX.Element
const ProtectedRoute = ({ children }: { children: ReactNode }) => {
    const { session, loading } = useAuth();
    
    if (loading) return <div className="p-10 text-center text-slate-500">Loading System...</div>;
    if (!session) return <Navigate to="/login" replace />;

    return children;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Route */}
          <Route path="/login" element={<Login />} />
          
          {/* Protected Route */}
          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />

          {/* Default Redirect */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;