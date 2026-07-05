import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, API_BASE_URL } from '../context/AuthContext';
import { Navbar } from '../components/Navbar';
import { BrainCircuit, Play, ArrowLeft, ShieldAlert } from 'lucide-react';

export const WizardPage: React.FC = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [prompt, setPrompt] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const { token } = useAuth();
  const navigate = useNavigate();

  const handleLaunch = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);

    try {
      const response = await fetch(`${API_BASE_URL}/projects/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          title,
          description: description || undefined,
          prompt
        })
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to initialize pipeline");
      }

      const project = await response.json();
      navigate(`/project/${project.id}`);
    } catch (err: any) {
      setError(err.message || "An error occurred launching the orchestrator.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-lightBg dark:bg-darkBg text-slate-800 dark:text-slate-100 transition-colors duration-300">
      <Navbar />

      <main className="flex-1 max-w-4xl w-full mx-auto px-6 md:px-12 py-10 space-y-8">
        
        {/* Back Link */}
        <button
          onClick={() => navigate('/dashboard')}
          className="flex items-center space-x-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-sm transition-colors"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Dashboard</span>
        </button>

        {/* Header Title */}
        <div className="flex items-center space-x-4">
          <div className="bg-gradient-to-tr from-cyan-500 to-indigo-600 p-3 rounded-2xl text-white shadow-lg">
            <BrainCircuit className="h-6 w-6" />
          </div>
          <div>
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">Blueprint Design Wizard</h1>
            <p className="text-slate-500 dark:text-slate-400 text-xs mt-1">Specify parameters to launch the multi-agent software engineering grid.</p>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl border bg-rose-500/10 border-rose-500/20 text-rose-600 dark:text-rose-300 text-xs flex items-start space-x-3">
            <ShieldAlert className="h-5 w-5 flex-shrink-0 text-rose-500 dark:text-rose-400" />
            <div className="space-y-1">
              <span className="font-bold">System Validation Blocked Request</span>
              <p className="text-rose-500 dark:text-rose-400/90 leading-relaxed">{error}</p>
            </div>
          </div>
        )}

        {/* Input Form */}
        <form onSubmit={handleLaunch} className="glass-card p-8 space-y-6">
          <div className="space-y-1">
            <label className="text-[10px] text-slate-500 dark:text-slate-400 font-mono tracking-wider block">PROJECT WORKSPACE TITLE *</label>
            <input
              type="text"
              required
              minLength={3}
              maxLength={100}
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. SmartHome Analytics Dashboard"
              className="w-full px-4 py-2.5 glass-input text-sm"
            />
          </div>

          <div className="space-y-1">
            <label className="text-[10px] text-slate-500 dark:text-slate-400 font-mono tracking-wider block">SHORT SUBTITLE DESCRIPTION</label>
            <input
              type="text"
              maxLength={500}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="e.g. Real-time energy tracking and smart appliance controls"
              className="w-full px-4 py-2.5 glass-input text-sm"
            />
          </div>

          <div className="space-y-1">
            <label className="text-[10px] text-slate-500 dark:text-slate-400 font-mono tracking-wider block">DETAILED SOFTWARE IDEA SPECIFICATION *</label>
            <textarea
              required
              minLength={10}
              rows={6}
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the application you want the AI agents to design. Include target features, database models, user roles, security, and styling preferences..."
              className="w-full px-4 py-3 glass-input text-sm font-sans resize-none"
            />
            <span className="text-[10px] text-slate-500 dark:text-slate-400 block italic">Minimum 10 characters required. Scanned for safety bypass/jailbreak attempts.</span>
          </div>

          {/* Submit/Launch Button */}
          <div className="pt-4 border-t border-slate-200 dark:border-slate-800/80 flex justify-end">
            <button
              type="submit"
              disabled={submitting}
              className="bg-gradient-to-r from-cyan-500 to-indigo-600 dark:from-cyan-400 dark:to-indigo-500 hover:from-cyan-600 hover:to-indigo-700 dark:hover:from-cyan-500 dark:hover:to-indigo-600 text-slate-950 dark:text-slate-950 font-extrabold px-8 py-3.5 rounded-xl flex items-center justify-center space-x-2 transition-all disabled:opacity-50"
            >
              <span>Initialize AI Orchestration</span>
              {submitting ? (
                <div className="h-4 w-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <Play className="h-4 w-4" />
              )}
            </button>
          </div>
        </form>

      </main>
    </div>
  );
};
export default WizardPage;
