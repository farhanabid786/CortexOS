import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth, API_BASE_URL } from '../context/AuthContext';
import { Navbar } from '../components/Navbar';
import { AgentTimeline } from '../components/AgentTimeline';
import { MarkdownViewer } from '../components/MarkdownViewer';
import { CodeViewer } from '../components/CodeViewer';
import { ArchitectureVisualizer } from '../components/ArchitectureVisualizer';
import { ArrowLeft, FolderArchive, FileText, CheckCircle2, AlertCircle } from 'lucide-react';

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

interface AgentLog {
  id: number;
  agent_name: string;
  log_level: string;
  message: string;
  created_at: string;
}

interface Blueprint {
  id: number;
  project_id: number;
  requirement_analysis: any;
  prd: any;
  architecture_design: any;
  database_schema: any;
  api_design: any;
  frontend_plan: any;
  testing_strategy: any;
  security_report: any;
  deployment_guide: any;
  review_report: any;
  markdown_output: string;
  created_at: string;
}

export const BlueprintPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [logs, setLogs] = useState<AgentLog[]>([]);
  const [blueprint, setBlueprint] = useState<Blueprint | null>(null);
  const [activeTab, setActiveTab] = useState<'blueprint' | 'architecture' | 'codebase' | 'raw_specs'>('blueprint');
  const [loading, setLoading] = useState(true);

  const { token } = useAuth();
  const navigate = useNavigate();

  const AGENTS_LIST = [
    "Requirement Analyst",
    "Product Manager",
    "Software Architect",
    "Database Engineer",
    "Backend Engineer",
    "Frontend Engineer",
    "QA Engineer",
    "Security Analyst",
    "Documentation Agent",
    "Review Agent"
  ];

  const fetchData = async () => {
    if (!token || !id) return;
    try {
      // 1. Fetch project status
      const projResp = await fetch(`${API_BASE_URL}/projects/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (!projResp.ok) throw new Error("Failed to load project details");
      const projectData = await projResp.json();
      setProject(projectData);

      // 2. Fetch agent logs
      const logsResp = await fetch(`${API_BASE_URL}/logs/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (logsResp.ok) {
        const logsData = await logsResp.json();
        setLogs(logsData);
      }

      // 3. Fetch blueprint if completed
      if (projectData.status === 'completed') {
        const bpResp = await fetch(`${API_BASE_URL}/blueprints/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (bpResp.ok) {
          const bpData = await bpResp.json();
          setBlueprint(bpData);
        }
      }
    } catch (err) {
      console.error("Error loading project workspace data:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    
    // Poll updates every 2 seconds if the pipeline is active
    let interval: any;
    if (project?.status === 'running' || project?.status === 'pending' || loading) {
      interval = setInterval(fetchData, 2000);
    }
    
    return () => clearInterval(interval);
  }, [id, token, project?.status]);

  const handleExportWorkspace = () => {
    if (!blueprint) return;
    // Download markdown file directly in browser
    const blob = new Blob([blueprint.markdown_output], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${project?.title.toLowerCase().replace(/ /g, '_')}_blueprint.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadZip = () => {
    if (!blueprint) return;
    // Show user a message about the export trigger
    alert("Export request sent to workspace. ZIP package compiled inside your workspace output folder: [workspace_output]/");
  };

  if (loading && !project) {
    return (
      <div className="min-h-screen flex flex-col bg-lightBg dark:bg-darkBg text-slate-800 dark:text-slate-100 transition-colors duration-300">
        <Navbar />
        <div className="flex-1 flex justify-center items-center">
          <div className="h-8 w-8 border-4 border-cyan-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen flex flex-col bg-lightBg dark:bg-darkBg text-slate-800 dark:text-slate-100 transition-colors duration-300">
        <Navbar />
        <div className="flex-1 flex flex-col justify-center items-center space-y-4">
          <AlertCircle className="h-10 w-10 text-rose-500" />
          <h2 className="text-xl font-bold">Project Workspace not found</h2>
          <button onClick={() => navigate('/dashboard')} className="text-cyan-600 dark:text-cyan-400 font-semibold">Back to Dashboard</button>
        </div>
      </div>
    );
  }

  // Find active step index based on current agent name
  const activeStepIndex = project.current_agent 
    ? AGENTS_LIST.indexOf(project.current_agent) 
    : project.status === 'completed' ? 10 : 0;

  return (
    <div className="min-h-screen flex flex-col bg-lightBg dark:bg-darkBg text-slate-800 dark:text-slate-100 transition-colors duration-300">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-6 md:px-12 py-10 space-y-8">
        
        {/* Navigation back and header metadata */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0">
          <div className="space-y-2">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center space-x-2 text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white text-xs transition-colors"
            >
              <ArrowLeft className="h-3.5 w-3.5" />
              <span>Back to Dashboard</span>
            </button>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-extrabold text-slate-900 dark:text-white">{project.title}</h1>
              <div>
                {project.status === 'completed' && (
                  <span className="text-[10px] bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 px-2.5 py-0.5 rounded-full font-mono font-bold flex items-center">
                    <CheckCircle2 className="h-3 w-3 mr-1" />
                    Operational
                  </span>
                )}
                {project.status === 'running' && (
                  <span className="text-[10px] bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/20 px-2.5 py-0.5 rounded-full font-mono font-bold animate-pulse flex items-center">
                    <Loader2 className="h-3 w-3 mr-1 animate-spin" />
                    Executing: {project.current_agent}
                  </span>
                )}
                {project.status === 'failed' && (
                  <span className="text-[10px] bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20 px-2.5 py-0.5 rounded-full font-mono font-bold flex items-center">
                    <AlertCircle className="h-3 w-3 mr-1" />
                    Failed
                  </span>
                )}
              </div>
            </div>
            <p className="text-slate-600 dark:text-slate-400 text-xs">{project.description || project.prompt}</p>
          </div>

          {/* Export options */}
          {project.status === 'completed' && blueprint && (
            <div className="flex items-center space-x-3 w-full sm:w-auto">
              <button
                onClick={handleExportWorkspace}
                className="flex-1 sm:flex-none flex items-center justify-center space-x-2 bg-white dark:bg-slate-900 border border-slate-200 dark:border-glassBorder/60 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white text-xs font-semibold px-4 py-2.5 rounded-xl transition-colors"
              >
                <FileText className="h-4 w-4 text-cyan-500 dark:text-cyan-400" />
                <span>Export Markdown</span>
              </button>
              <button
                onClick={handleDownloadZip}
                className="flex-1 sm:flex-none flex items-center justify-center space-x-2 bg-gradient-to-r from-cyan-500 to-indigo-600 dark:from-cyan-400 dark:to-indigo-500 hover:from-cyan-600 hover:to-indigo-700 dark:hover:from-cyan-500 dark:hover:to-indigo-600 text-slate-950 dark:text-slate-950 text-xs font-bold px-4 py-2.5 rounded-xl transition-colors"
              >
                <FolderArchive className="h-4 w-4" />
                <span>Compile ZIP</span>
              </button>
            </div>
          )}
        </div>

        {/* Timeline details */}
        <AgentTimeline 
          currentAgent={project.current_agent} 
          status={project.status} 
          logs={logs} 
          activeStepIndex={activeStepIndex} 
        />

        {/* Tab panels shown on pipeline completion */}
        {project.status === 'completed' && blueprint && (
          <div className="space-y-6">
            <div className="flex border-b border-slate-200 dark:border-glassBorder/60 space-x-6 text-sm font-semibold select-none overflow-x-auto pb-px">
              <button
                onClick={() => setActiveTab('blueprint')}
                className={`py-3 relative ${activeTab === 'blueprint' ? 'text-cyan-600 dark:text-cyan-400 font-bold' : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'}`}
              >
                Specification Document
                {activeTab === 'blueprint' && <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500 dark:bg-cyan-400 rounded-full"></span>}
              </button>
              <button
                onClick={() => setActiveTab('architecture')}
                className={`py-3 relative ${activeTab === 'architecture' ? 'text-cyan-600 dark:text-cyan-400 font-bold' : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'}`}
              >
                Architecture Map
                {activeTab === 'architecture' && <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500 dark:bg-cyan-400 rounded-full"></span>}
              </button>
              <button
                onClick={() => setActiveTab('codebase')}
                className={`py-3 relative ${activeTab === 'codebase' ? 'text-cyan-600 dark:text-cyan-400 font-bold' : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'}`}
              >
                Codebase Explorer
                {activeTab === 'codebase' && <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500 dark:bg-cyan-400 rounded-full"></span>}
              </button>
              <button
                onClick={() => setActiveTab('raw_specs')}
                className={`py-3 relative ${activeTab === 'raw_specs' ? 'text-cyan-600 dark:text-cyan-400 font-bold' : 'text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200'}`}
              >
                JSON Outputs
                {activeTab === 'raw_specs' && <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-cyan-500 dark:bg-cyan-400 rounded-full"></span>}
              </button>
            </div>

            <div>
              {activeTab === 'blueprint' && (
                <div className="glass-card p-8">
                  <MarkdownViewer content={blueprint.markdown_output} />
                </div>
              )}

              {activeTab === 'architecture' && (
                <ArchitectureVisualizer />
              )}

              {activeTab === 'codebase' && (
                <CodeViewer />
              )}

              {activeTab === 'raw_specs' && (
                <div className="glass-card p-6 font-mono text-xs text-slate-300 max-h-[600px] overflow-y-auto bg-slate-950/60">
                  <h4 className="font-semibold text-slate-400 mb-4 tracking-wider uppercase">Raw Structured JSON Logs</h4>
                  <div className="space-y-4">
                    <div>
                      <span className="text-cyan-500 dark:text-cyan-400 font-bold block mb-1">Requirement Analysis Spec:</span>
                      <pre className="bg-slate-955 p-4 rounded-xl border border-slate-800">{JSON.stringify(blueprint.requirement_analysis, null, 2)}</pre>
                    </div>
                    <div>
                      <span className="text-cyan-500 dark:text-cyan-400 font-bold block mb-1">Product Requirement Spec (PRD):</span>
                      <pre className="bg-slate-955 p-4 rounded-xl border border-slate-800">{JSON.stringify(blueprint.prd, null, 2)}</pre>
                    </div>
                    <div>
                      <span className="text-cyan-500 dark:text-cyan-400 font-bold block mb-1">Database Schema Spec:</span>
                      <pre className="bg-slate-955 p-4 rounded-xl border border-slate-800">{JSON.stringify(blueprint.database_schema, null, 2)}</pre>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

      </main>
    </div>
  );
};

// Re-declare Loader2 locally in case it's not imported properly
const Loader2 = ({ className, ...props }: any) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={`lucide lucide-loader-2 ${className}`}
    {...props}
  >
    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
  </svg>
);

export default BlueprintPage;
