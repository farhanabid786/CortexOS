import React, { useState } from 'react';
import { Cpu } from 'lucide-react';

export const ArchitectureVisualizer: React.FC = () => {
  const nodes = {
    client: {
      title: "React Frontend Client",
      desc: "Renders dashboard views, logs timeline, markdown specifications, and handles token authentications.",
      tech: "Vite + TypeScript + Tailwind + Framer Motion"
    },
    gateway: {
      title: "FastAPI Gateway Service",
      desc: "Validates incoming tokens, inspects commands for prompt injections, triggers Rate Limit middlewares, and serves routes.",
      tech: "FastAPI + Pydantic + Slowapi"
    },
    orchestrator: {
      title: "Cortex Orchestrator Engine",
      desc: "Manages the sequential execution of the 10-stage pipeline, propagates context, streams live step logs, and saves schemas.",
      tech: "Python Background Tasks + SQLite ORM"
    },
    database: {
      title: "SQLite / PostgreSQL",
      desc: "Stores user passwords (hashed), projects, intermediate blueprints, audit records, and step-by-step logs.",
      tech: "SQLAlchemy + SQLite + Asyncpg"
    },
    mcp: {
      title: "CortexOS MCP Server",
      desc: "Model Context Protocol interface providing standard JSON-RPC tools for File operations, GitHub mocks, sandbox terminal builds, and exports.",
      tech: "Python FastMCP SDK"
    }
  };

  const [activeNode, setActiveNode] = useState<keyof typeof nodes | null>(null);

  return (
    <div className="glass-card p-6 flex flex-col space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="font-bold text-lg text-white">Interactive Architecture Map</h3>
        <span className="text-xs text-cyan-400">Click any system component node to view details</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Diagram canvas (SVG mapping) */}
        <div className="lg:col-span-2 flex justify-center items-center p-4 bg-slate-950/40 rounded-xl border border-glassBorder/60 min-h-[350px]">
          <svg viewBox="0 0 600 350" className="w-full h-auto select-none">
            {/* Connection Lines with animation */}
            <path d="M 120 175 L 240 175" stroke="#4a5568" strokeWidth="2" className="node-line" strokeDasharray="5" />
            <path d="M 320 175 L 440 105" stroke="#00f2fe" strokeWidth="2" className="node-line" strokeDasharray="5" />
            <path d="M 320 175 L 440 245" stroke="#4facfe" strokeWidth="2" className="node-line" strokeDasharray="5" />
            <path d="M 480 145 L 480 205" stroke="#7c3aed" strokeWidth="2" className="node-line" strokeDasharray="5" />

            {/* Node: Client App */}
            <g onClick={() => setActiveNode('client')} className="cursor-pointer group">
              <rect x="20" y="130" width="100" height="90" rx="10" fill="#1e1b4b" stroke={activeNode === 'client' ? '#00f2fe' : '#312e81'} strokeWidth="2" className="transition-all duration-300" />
              <text x="70" y="170" fill="#ffffff" fontSize="12" fontWeight="bold" textAnchor="middle">React Client</text>
              <text x="70" y="190" fill="#a5f3fc" fontSize="10" textAnchor="middle">Browser App</text>
            </g>

            {/* Node: API Gateway */}
            <g onClick={() => setActiveNode('gateway')} className="cursor-pointer group">
              <rect x="220" y="130" width="100" height="90" rx="10" fill="#111827" stroke={activeNode === 'gateway' ? '#00f2fe' : '#374151'} strokeWidth="2" />
              <text x="270" y="170" fill="#ffffff" fontSize="12" fontWeight="bold" textAnchor="middle">FastAPI Router</text>
              <text x="270" y="190" fill="#9ca3af" fontSize="10" textAnchor="middle">API Gateway</text>
            </g>

            {/* Node: Orchestrator */}
            <g onClick={() => setActiveNode('orchestrator')} className="cursor-pointer group">
              <rect x="420" y="60" width="120" height="80" rx="10" fill="#1e1e38" stroke={activeNode === 'orchestrator' ? '#00f2fe' : '#2d2d59'} strokeWidth="2" />
              <text x="480" y="95" fill="#ffffff" fontSize="12" fontWeight="bold" textAnchor="middle">Cortex</text>
              <text x="480" y="115" fill="#818cf8" fontSize="10" textAnchor="middle">Orchestrator</text>
            </g>

            {/* Node: Database */}
            <g onClick={() => setActiveNode('database')} className="cursor-pointer group">
              <rect x="420" y="210" width="120" height="80" rx="10" fill="#0f172a" stroke={activeNode === 'database' ? '#00f2fe' : '#1e293b'} strokeWidth="2" />
              <text x="480" y="245" fill="#ffffff" fontSize="12" fontWeight="bold" textAnchor="middle">SQLite / DB</text>
              <text x="480" y="265" fill="#94a3b8" fontSize="10" textAnchor="middle">Persistence</text>
            </g>

            {/* Connection: Gateway to MCP */}
            <path d="M 270 220 L 270 280" stroke="#10b981" strokeWidth="2" className="node-line" strokeDasharray="5" />
            
            {/* Node: MCP Server */}
            <g onClick={() => setActiveNode('mcp')} className="cursor-pointer group">
              <rect x="210" y="280" width="120" height="60" rx="8" fill="#022c22" stroke={activeNode === 'mcp' ? '#10b981' : '#064e3b'} strokeWidth="2" />
              <text x="270" y="305" fill="#ffffff" fontSize="11" fontWeight="bold" textAnchor="middle">MCP Tool Server</text>
              <text x="270" y="322" fill="#a7f3d0" fontSize="9" textAnchor="middle">File/Terminal/Git</text>
            </g>
          </svg>
        </div>

        {/* Component Node Details Sidebar */}
        <div className="lg:col-span-1 flex flex-col justify-center">
          {activeNode ? (
            <div className="bg-slate-900/60 border border-slate-800/80 p-5 rounded-2xl space-y-3">
              <div className="flex items-center space-x-2 text-cyan-400">
                <Cpu className="h-5 w-5" />
                <h4 className="font-extrabold text-sm text-white uppercase">{nodes[activeNode].title}</h4>
              </div>
              <p className="text-slate-300 text-xs leading-relaxed">{nodes[activeNode].desc}</p>
              <div className="pt-2 border-t border-slate-800">
                <span className="text-[10px] text-slate-500 font-mono block">TECHNOLOGY STACK</span>
                <span className="text-xs text-indigo-400 font-semibold font-mono">{nodes[activeNode].tech}</span>
              </div>
            </div>
          ) : (
            <div className="text-center p-6 border border-slate-800 border-dashed rounded-2xl text-slate-500 text-xs">
              Select any block in the architecture map (e.g. React Client, FastAPI, MCP Server) to read its technical specifications.
            </div>
          )}
        </div>

      </div>
    </div>
  );
};
export default ArchitectureVisualizer;
