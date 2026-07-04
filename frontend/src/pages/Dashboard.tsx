import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth, API_BASE_URL } from '../context/AuthContext';
import { Navbar } from '../components/Navbar';
import { Plus, FolderGit2, Trash2, Cpu, Calendar, Activity, CheckSquare } from 'lucide-react';

interface Project {
  id: number;
  title: string;
  description: string;
  prompt: string;
  status: string;
  current_agent: string | null;
  created_at: string;
  user_id: number;
}

export const Dashboard: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const fetchProjects = async () => {
    if (!token) return;
    try {
      const response = await fetch(`${API_BASE_URL}/projects/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setProjects(data);
      } else if (response.status === 401) {
        logout();
        navigate('/login');
      }
    } catch (err) {
      console.error("Error loading projects list:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProjects();
    // Poll project list status every 5 seconds to show live updates during runs
    const interval = setInterval(fetchProjects, 5000);
    return () => clearInterval(interval);
  }, [token]);

  const handleDelete = async (e: React.MouseEvent, projectId: number) => {
    e.preventDefault(); // Stop navigation to detail
    e.stopPropagation();
    
    if (!confirm("Are you sure you want to delete this project blueprint?")) return;
    
    setDeletingId(projectId);
    try {
      const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.ok) {
        setProjects(prev => prev.filter(p => p.id !== projectId));
      }
    } catch (err) {
      console.error("Error deleting project:", err);
    } finally {
      setDeletingId(null);
    }
  };

  // Compute stats
  const totalProjects = projects.length;
  const runningProjects = projects.filter(p => p.status === 'running').length;
  const completedProjects = projects.filter(p => p.status === 'completed').length;
  const successRate = totalProjects > 0 ? Math.round((completedProjects / totalProjects) * 100) : 0;

  return (
    <div className="min-h-screen flex flex-col bg-darkBg text-slate-100">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 md:px-12 py-10 space-y-10">
        
        {/* Header Title with Button */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-white">Project Workspaces</h1>
            <p className="text-slate-400 text-xs mt-1">Manage and evaluate your multi-agent code blueprints.</p>
          </div>
          <Link
            to="/wizard"
            className="flex items-center space-x-2 bg-gradient-to-r from-cyan-400 to-indigo-500 hover:from-cyan-500 hover:to-indigo-600 text-slate-950 font-extrabold px-5 py-3 rounded-xl transition-all transform hover:-translate-y-0.5 shadow-lg shadow-cyan-500/20"
          >
            <Plus className="h-5 w-5" />
            <span>Launch Design Wizard</span>
          </Link>
        </div>

        {/* Analytics Statistics Panel */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div className="glass-card p-5 flex items-center space-x-4">
            <div className="bg-cyan-500/10 text-cyan-400 p-3 rounded-xl"><FolderGit2 className="h-5 w-5" /></div>
            <div>
              <span className="text-[10px] text-slate-500 font-mono tracking-wider block">BLUEPRINTS</span>
              <span className="text-2xl font-extrabold text-white">{totalProjects}</span>
            </div>
          </div>
          <div className="glass-card p-5 flex items-center space-x-4">
            <div className="bg-indigo-500/10 text-indigo-400 p-3 rounded-xl animate-pulse"><Activity className="h-5 w-5" /></div>
            <div>
              <span className="text-[10px] text-slate-500 font-mono tracking-wider block">ACTIVE RUNS</span>
              <span className="text-2xl font-extrabold text-white">{runningProjects}</span>
            </div>
          </div>
          <div className="glass-card p-5 flex items-center space-x-4">
            <div className="bg-emerald-500/10 text-emerald-400 p-3 rounded-xl"><CheckSquare className="h-5 w-5" /></div>
            <div>
              <span className="text-[10px] text-slate-500 font-mono tracking-wider block">COMPLETED</span>
              <span className="text-2xl font-extrabold text-white">{completedProjects}</span>
            </div>
          </div>
          <div className="glass-card p-5 flex items-center space-x-4">
            <div className="bg-amber-500/10 text-amber-400 p-3 rounded-xl"><Cpu className="h-5 w-5" /></div>
            <div>
              <span className="text-[10px] text-slate-500 font-mono tracking-wider block">SUCCESS RATE</span>
              <span className="text-2xl font-extrabold text-white">{successRate}%</span>
            </div>
          </div>
        </div>

        {/* Workspaces List Grid */}
        {loading ? (
          <div className="flex justify-center items-center py-20">
            <div className="h-8 w-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : projects.length === 0 ? (
          <div className="text-center py-16 border border-slate-800 border-dashed rounded-2xl space-y-4">
            <div className="text-slate-500 italic text-sm">You haven't generated any software blueprints yet.</div>
            <Link
              to="/wizard"
              className="inline-flex items-center space-x-2 text-cyan-400 hover:text-cyan-300 text-sm font-semibold"
            >
              <span>Build your first blueprint now</span>
              <Plus className="h-4 w-4" />
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {projects.map((project) => (
              <Link
                key={project.id}
                to={`/project/${project.id}`}
                className="group block relative glass-card p-6 space-y-4 cursor-pointer"
              >
                {/* Delete overlay button */}
                <button
                  onClick={(e) => handleDelete(e, project.id)}
                  disabled={deletingId === project.id}
                  className="absolute top-4 right-4 p-1.5 rounded-lg text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 border border-transparent hover:border-rose-500/20 transition-all opacity-0 group-hover:opacity-100"
                  title="Delete blueprint"
                >
                  <Trash2 className="h-4 w-4" />
                </button>

                <div className="space-y-2">
                  <div className="flex justify-between items-center pr-6">
                    <h3 className="font-bold text-white text-lg group-hover:text-cyan-400 transition-colors truncate">
                      {project.title}
                    </h3>
                  </div>
                  <p className="text-slate-400 text-xs leading-relaxed line-clamp-2 h-8">
                    {project.description || project.prompt}
                  </p>
                </div>

                <div className="pt-4 border-t border-slate-800/80 flex justify-between items-center">
                  <div className="flex items-center text-slate-500 text-[10px] font-mono">
                    <Calendar className="h-3.5 w-3.5 mr-1" />
                    <span>{new Date(project.created_at).toLocaleDateString()}</span>
                  </div>

                  {/* Status badge */}
                  <div>
                    {project.status === 'completed' && (
                      <span className="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded font-mono font-bold capitalize">
                        Success
                      </span>
                    )}
                    {project.status === 'running' && (
                      <span className="text-[10px] bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded font-mono font-bold capitalize animate-pulse flex items-center">
                        <span className="h-1.5 w-1.5 rounded-full bg-cyan-400 animate-ping mr-1"></span>
                        {project.current_agent || "Orchestration"}
                      </span>
                    )}
                    {project.status === 'failed' && (
                      <span className="text-[10px] bg-rose-500/10 text-rose-400 border border-rose-500/20 px-2 py-0.5 rounded font-mono font-bold capitalize">
                        Failed
                      </span>
                    )}
                    {project.status === 'pending' && (
                      <span className="text-[10px] bg-slate-800 text-slate-400 border border-slate-700 px-2 py-0.5 rounded font-mono font-bold capitalize">
                        Pending
                      </span>
                    )}
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

      </main>
    </div>
  );
};
export default Dashboard;
