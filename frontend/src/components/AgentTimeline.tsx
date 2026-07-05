import React from 'react';
import { Loader2, CheckCircle2, AlertCircle, Hourglass, Terminal } from 'lucide-react';

interface AgentLog {
  id: number;
  agent_name: string;
  log_level: string;
  message: string;
  created_at: string;
}

interface AgentTimelineProps {
  currentAgent: string | null;
  status: string;
  logs: AgentLog[];
  activeStepIndex: number;
}

const AGENTS = [
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

export const AgentTimeline: React.FC<AgentTimelineProps> = ({ currentAgent, status, logs, activeStepIndex }) => {
  
  const getAgentStatus = (agentName: string, idx: number) => {
    if (status === 'completed') return 'completed';
    if (status === 'failed' && currentAgent === agentName) return 'failed';
    if (status === 'failed' && idx > activeStepIndex) return 'pending';
    if (status === 'failed' && idx < activeStepIndex) return 'completed';
    
    if (status === 'running') {
      if (currentAgent === agentName) return 'running';
      if (idx < activeStepIndex) return 'completed';
      return 'pending';
    }
    
    return 'pending'; // For status == 'pending'
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Visual Timeline Nodes */}
      <div className="lg:col-span-1 glass-card p-6 flex flex-col space-y-4 max-h-[600px] overflow-y-auto">
        <h3 className="font-bold text-lg text-slate-900 dark:text-white mb-2 flex items-center">
          <Loader2 className={`mr-2 h-5 w-5 text-cyan-600 dark:text-cyan-400 ${status === 'running' ? 'animate-spin' : ''}`} />
          Multi-Agent Pipeline
        </h3>
        
        <div className="relative border-l-2 border-slate-200 dark:border-slate-700/60 ml-3 pl-6 space-y-6">
          {AGENTS.map((agent, index) => {
            const agentStatus = getAgentStatus(agent, index);
            
            return (
              <div key={agent} className="relative flex flex-col items-start">
                {/* Node icon indicators */}
                <div className="absolute -left-[35px] top-1">
                  {agentStatus === 'completed' && (
                    <div className="bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 p-1.5 rounded-full border border-emerald-500/30">
                      <CheckCircle2 className="h-4 w-4" />
                    </div>
                  )}
                  {agentStatus === 'running' && (
                    <div className="bg-cyan-500/20 text-cyan-600 dark:text-cyan-400 p-1.5 rounded-full border border-cyan-500/30 animate-pulse">
                      <Loader2 className="h-4 w-4 animate-spin" />
                    </div>
                  )}
                  {agentStatus === 'failed' && (
                    <div className="bg-rose-500/20 text-rose-600 dark:text-rose-400 p-1.5 rounded-full border border-rose-500/30">
                      <AlertCircle className="h-4 w-4" />
                    </div>
                  )}
                  {agentStatus === 'pending' && (
                    <div className="bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 p-1.5 rounded-full border border-slate-200 dark:border-slate-700">
                      <Hourglass className="h-4 w-4" />
                    </div>
                  )}
                </div>

                <div className={`pl-2 ${agentStatus === 'running' ? 'text-cyan-600 dark:text-cyan-400 font-bold' : agentStatus === 'completed' ? 'text-slate-700 dark:text-slate-300' : 'text-slate-400 dark:text-slate-500'}`}>
                  <span className="text-sm block font-semibold">{agent}</span>
                  {agentStatus === 'running' && (
                    <span className="text-xs text-cyan-600/80 dark:text-cyan-400/80 animate-pulse">Executing code-generation models...</span>
                  )}
                  {agentStatus === 'completed' && (
                    <span className="text-xs text-emerald-600/80 dark:text-emerald-400/80">Documentation generated</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Log Console Terminal - Kept dark for standard terminal console aesthetics */}
      <div className="lg:col-span-2 glass-card p-6 flex flex-col h-[500px] bg-slate-950/80 border border-slate-800/80 rounded-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
          <div className="flex items-center space-x-2 text-slate-300">
            <Terminal className="h-4 w-4 text-cyan-400" />
            <span className="font-mono text-xs font-semibold">cortexos-orchestrator@log-stream</span>
          </div>
          <div className="flex space-x-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-rose-500/80"></span>
            <span className="h-2.5 w-2.5 rounded-full bg-amber-500/80"></span>
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-500/80"></span>
          </div>
        </div>

        {/* Console logs output */}
        <div className="flex-1 overflow-y-auto font-mono text-xs space-y-2.5 pr-2 select-text">
          {logs.length === 0 ? (
            <div className="text-slate-500 italic">No agent logs generated yet. Starting execution engine...</div>
          ) : (
            logs.map((log) => {
              let textClass = "text-slate-300";
              if (log.log_level === "ERROR") textClass = "text-rose-400 font-bold";
              else if (log.log_level === "SUCCESS") textClass = "text-emerald-400";
              else if (log.log_level === "WARNING") textClass = "text-amber-400";

              return (
                <div key={log.id} className="flex items-start space-x-2">
                  <span className="text-slate-500 select-none">[{new Date(log.created_at).toLocaleTimeString()}]</span>
                  <span className="text-cyan-400/90 font-semibold select-none">[{log.agent_name}]:</span>
                  <span className={textClass}>{log.message}</span>
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
};
export default AgentTimeline;
