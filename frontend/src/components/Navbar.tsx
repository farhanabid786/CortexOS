import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import { Sun, Moon, LogOut, Layers } from 'lucide-react';

export const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="sticky top-0 z-50 glass-effect border-b border-glassBorder py-4 px-6 md:px-12 flex justify-between items-center">
      <Link to="/" className="flex items-center space-x-3 group">
        <div className="bg-gradient-to-tr from-cyan-500 to-indigo-600 dark:from-cyan-400 dark:to-indigo-600 p-2 rounded-xl text-white shadow-lg group-hover:scale-105 transition-transform">
          <Layers className="h-6 w-6 animate-pulse-slow" />
        </div>
        <span className="font-extrabold text-xl md:text-2xl tracking-tight bg-gradient-to-r from-slate-900 via-slate-800 to-slate-600 dark:from-white dark:via-slate-200 dark:to-slate-500 bg-clip-text text-transparent">
          Cortex<span className="text-cyan-600 dark:text-cyan-400">OS</span>
        </span>
      </Link>

      <div className="flex items-center space-x-6">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg bg-white/5 border border-white/10 hover:bg-white/10 text-slate-300 hover:text-white transition-colors"
          aria-label="Toggle Theme"
        >
          {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </button>

        {user ? (
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex flex-col text-right">
              <span className="text-sm font-semibold text-white">{user.full_name || user.email}</span>
              <span className="text-xs text-cyan-400 capitalize">{user.role}</span>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center space-x-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 hover:text-rose-100 border border-rose-500/20 px-3 py-1.5 rounded-lg text-sm font-semibold transition-all"
            >
              <LogOut className="h-4 w-4" />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        ) : (
          <div className="flex space-x-3">
            <Link
              to="/login"
              className="bg-cyan-500 hover:bg-cyan-600 text-slate-950 font-bold px-4 py-2 rounded-lg text-sm transition-all shadow-md hover:shadow-cyan-500/20"
            >
              Login
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};
export default Navbar;
