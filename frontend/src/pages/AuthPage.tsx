import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Mail, Lock, User, AlertCircle, ArrowRight } from 'lucide-react';
import Navbar from '../components/Navbar';

export const AuthPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      if (isLogin) {
        const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        await login(formData);
        navigate('/dashboard');
      } else {
        await register(email, password, fullName);
        // Toggle to login and show success
        setIsLogin(true);
        setError("Account created successfully. Please login.");
      }
    } catch (err: any) {
      setError(err.message || "An authentication error occurred.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-darkBg text-slate-100">
      <Navbar />

      <div className="flex-1 flex justify-center items-center px-4 py-12 relative overflow-hidden">
        {/* Glow orb */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-indigo-600/5 rounded-full blur-3xl -z-10"></div>

        <div className="w-full max-w-md glass-card p-8 space-y-6">
          <div className="text-center space-y-2">
            <h2 className="text-2xl font-extrabold text-white tracking-tight">
              {isLogin ? "Sign In to CortexOS" : "Create Developer Profile"}
            </h2>
            <p className="text-slate-400 text-xs">
              {isLogin ? "Access your agent software blueprints pipeline" : "Initialize details to build software agents"}
            </p>
          </div>

          {error && (
            <div className={`p-3 rounded-lg border text-xs flex items-center space-x-2 ${
              error.includes("successfully") 
                ? "bg-emerald-500/10 border-emerald-500/30 text-emerald-400" 
                : "bg-rose-500/10 border-rose-500/30 text-rose-400"
            }`}>
              <AlertCircle className="h-4 w-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            {!isLogin && (
              <div className="space-y-1">
                <label className="text-[10px] text-slate-400 font-mono tracking-wider block">FULL NAME</label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Jane Doe"
                    className="w-full pl-10 pr-4 py-2.5 glass-input text-sm"
                  />
                </div>
              </div>
            )}

            <div className="space-y-1">
              <label className="text-[10px] text-slate-400 font-mono tracking-wider block">EMAIL ADDRESS</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="jane.doe@example.com"
                  className="w-full pl-10 pr-4 py-2.5 glass-input text-sm"
                />
              </div>
            </div>

            <div className="space-y-1">
              <label className="text-[10px] text-slate-400 font-mono tracking-wider block">PASSWORD</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full pl-10 pr-4 py-2.5 glass-input text-sm"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full bg-gradient-to-r from-cyan-400 to-indigo-500 hover:from-cyan-500 hover:to-indigo-600 text-slate-950 font-extrabold py-3 rounded-xl flex items-center justify-center space-x-2 transition-all disabled:opacity-50"
            >
              <span>{isLogin ? "Sign In" : "Register Profile"}</span>
              {submitting ? (
                <div className="h-4 w-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <ArrowRight className="h-4 w-4" />
              )}
            </button>
          </form>

          <div className="text-center pt-2">
            <button
              onClick={() => {
                setIsLogin(!isLogin);
                setError(null);
              }}
              className="text-xs text-cyan-400 hover:text-cyan-300 font-semibold focus:outline-none"
            >
              {isLogin ? "Need a developer profile? Register here" : "Already registered? Login here"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
export default AuthPage;
