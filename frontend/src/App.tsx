import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';
import LandingPage from './pages/LandingPage';
import AuthPage from './pages/AuthPage';
import Dashboard from './pages/Dashboard';
import WizardPage from './pages/WizardPage';
import BlueprintPage from './pages/BlueprintPage';

// Protected route middleware wrapper
const RequireAuth: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen bg-darkBg flex justify-center items-center">
        <div className="h-8 w-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }
  
  return token ? <>{children}</> : <Navigate to="/login" replace />;
};

// Anonymous route middleware wrapper
const GuestOnly: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { token, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen bg-darkBg flex justify-center items-center">
        <div className="h-8 w-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }
  
  return !token ? <>{children}</> : <Navigate to="/dashboard" replace />;
};

export const App: React.FC = () => {
  return (
    <ThemeProvider>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route 
              path="/login" 
              element={
                <GuestOnly>
                  <AuthPage />
                </GuestOnly>
              } 
            />
            <Route 
              path="/dashboard" 
              element={
                <RequireAuth>
                  <Dashboard />
                </RequireAuth>
              } 
            />
            <Route 
              path="/wizard" 
              element={
                <RequireAuth>
                  <WizardPage />
                </RequireAuth>
              } 
            />
            <Route 
              path="/project/:id" 
              element={
                <RequireAuth>
                  <BlueprintPage />
                </RequireAuth>
              } 
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </ThemeProvider>
  );
};
export default App;
