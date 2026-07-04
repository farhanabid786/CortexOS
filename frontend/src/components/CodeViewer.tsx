import React, { useState } from 'react';
import { Folder, FileCode, Check, Copy, ChevronRight, ChevronDown } from 'lucide-react';

const MOCK_FILES: Record<string, { code: string; lang: string }> = {
  "backend/app/main.py": {
    lang: "python",
    code: `from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.database import get_db

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
def read_root():
    return {"status": "operational", "version": "1.0.0"}
`
  },
  "backend/app/core/database.py": {
    lang: "python",
    code: `from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db():
    async with async_session() as session:
        yield session
`
  },
  "backend/app/models/core_models.py": {
    lang: "python",
    code: `from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.core.database import Base

class DataRecord(Base):
    __tablename__ = "data_records"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
`
  },
  "frontend/src/App.tsx": {
    lang: "typescript",
    code: `import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
};
export default App;
`
  },
  "mcp_server/server.py": {
    lang: "python",
    code: `from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CortexOS MCP Server")

@mcp.tool()
def read_workspace_file(file_path: str) -> str:
    """Read a specific project blueprint file."""
    with open(file_path, 'r') as f:
        return f.read()
`
  }
};

export const CodeViewer: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<string>("backend/app/main.py");
  const [copied, setCopied] = useState(false);
  const [openFolders, setOpenFolders] = useState<Record<string, boolean>>({
    backend: true,
    "backend/app": true,
    "backend/app/core": true,
    "backend/app/models": true,
    frontend: true,
    "frontend/src": true,
    mcp_server: true
  });

  const handleCopy = () => {
    navigator.clipboard.writeText(MOCK_FILES[selectedFile]?.code || "");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const toggleFolder = (folder: string) => {
    setOpenFolders(prev => ({ ...prev, [folder]: !prev[folder] }));
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 rounded-2xl overflow-hidden border border-glassBorder/60 bg-slate-950/40">
      
      {/* Directory Sidebar */}
      <div className="md:col-span-1 border-r border-glassBorder/60 p-4 font-mono text-xs text-slate-300 max-h-[500px] overflow-y-auto bg-slate-950/45">
        <h4 className="font-semibold text-slate-400 mb-4 tracking-wider uppercase">Workspace Explorer</h4>
        
        <div className="space-y-1.5 select-none">
          {/* Backend */}
          <div>
            <div onClick={() => toggleFolder('backend')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors py-0.5">
              {openFolders.backend ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
              <Folder className="h-4 w-4 text-cyan-400" />
              <span>backend</span>
            </div>
            
            {openFolders.backend && (
              <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                <div onClick={() => toggleFolder('backend/app')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors py-0.5">
                  {openFolders["backend/app"] ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
                  <Folder className="h-4 w-4 text-cyan-400" />
                  <span>app</span>
                </div>
                
                {openFolders["backend/app"] && (
                  <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                    {/* core */}
                    <div>
                      <div onClick={() => toggleFolder('backend/app/core')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors">
                        {openFolders["backend/app/core"] ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
                        <Folder className="h-4 w-4 text-cyan-400" />
                        <span>core</span>
                      </div>
                      {openFolders["backend/app/core"] && (
                        <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                          <div onClick={() => setSelectedFile('backend/app/core/database.py')} className={`flex items-center space-x-2 cursor-pointer py-0.5 px-1.5 rounded transition-colors ${selectedFile === 'backend/app/core/database.py' ? 'bg-cyan-500/10 text-cyan-400' : 'hover:text-white'}`}>
                            <FileCode className="h-3.5 w-3.5" />
                            <span>database.py</span>
                          </div>
                        </div>
                      )}
                    </div>
                    {/* models */}
                    <div className="mt-1">
                      <div onClick={() => toggleFolder('backend/app/models')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors">
                        {openFolders["backend/app/models"] ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
                        <Folder className="h-4 w-4 text-cyan-400" />
                        <span>models</span>
                      </div>
                      {openFolders["backend/app/models"] && (
                        <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                          <div onClick={() => setSelectedFile('backend/app/models/core_models.py')} className={`flex items-center space-x-2 cursor-pointer py-0.5 px-1.5 rounded transition-colors ${selectedFile === 'backend/app/models/core_models.py' ? 'bg-cyan-500/10 text-cyan-400' : 'hover:text-white'}`}>
                            <FileCode className="h-3.5 w-3.5" />
                            <span>core_models.py</span>
                          </div>
                        </div>
                      )}
                    </div>

                    <div onClick={() => setSelectedFile('backend/app/main.py')} className={`flex items-center space-x-2 cursor-pointer py-0.5 px-1.5 rounded transition-colors ${selectedFile === 'backend/app/main.py' ? 'bg-cyan-500/10 text-cyan-400' : 'hover:text-white'}`}>
                      <FileCode className="h-3.5 w-3.5" />
                      <span>main.py</span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Frontend */}
          <div>
            <div onClick={() => toggleFolder('frontend')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors py-0.5">
              {openFolders.frontend ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
              <Folder className="h-4 w-4 text-indigo-400" />
              <span>frontend</span>
            </div>
            
            {openFolders.frontend && (
              <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                <div onClick={() => toggleFolder('frontend/src')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors py-0.5">
                  {openFolders["frontend/src"] ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
                  <Folder className="h-4 w-4 text-indigo-400" />
                  <span>src</span>
                </div>
                
                {openFolders["frontend/src"] && (
                  <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                    <div onClick={() => setSelectedFile('frontend/src/App.tsx')} className={`flex items-center space-x-2 cursor-pointer py-0.5 px-1.5 rounded transition-colors ${selectedFile === 'frontend/src/App.tsx' ? 'bg-cyan-500/10 text-cyan-400' : 'hover:text-white'}`}>
                      <FileCode className="h-3.5 w-3.5" />
                      <span>App.tsx</span>
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* MCP Server */}
          <div>
            <div onClick={() => toggleFolder('mcp_server')} className="flex items-center space-x-2 cursor-pointer hover:text-white transition-colors py-0.5">
              {openFolders.mcp_server ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
              <Folder className="h-4 w-4 text-emerald-400" />
              <span>mcp_server</span>
            </div>
            {openFolders.mcp_server && (
              <div className="pl-4 border-l border-slate-800/80 ml-2.5 space-y-1.5 mt-1">
                <div onClick={() => setSelectedFile('mcp_server/server.py')} className={`flex items-center space-x-2 cursor-pointer py-0.5 px-1.5 rounded transition-colors ${selectedFile === 'mcp_server/server.py' ? 'bg-cyan-500/10 text-cyan-400' : 'hover:text-white'}`}>
                  <FileCode className="h-3.5 w-3.5" />
                  <span>server.py</span>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Code Display Area */}
      <div className="md:col-span-3 flex flex-col h-[500px]">
        <div className="flex items-center justify-between border-b border-glassBorder/60 px-4 py-2 bg-slate-950/45">
          <span className="font-mono text-xs text-cyan-400">{selectedFile}</span>
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1 hover:text-white text-slate-400 text-xs px-2.5 py-1.5 rounded border border-white/5 bg-white/5 hover:bg-white/10 transition-all"
          >
            {copied ? (
              <>
                <Check className="h-3 w-3 text-emerald-400" />
                <span className="text-emerald-400">Copied!</span>
              </>
            ) : (
              <>
                <Copy className="h-3 w-3" />
                <span>Copy Code</span>
              </>
            )}
          </button>
        </div>

        <div className="flex-1 p-4 font-mono text-xs text-slate-300 overflow-auto bg-slate-950/80 select-text">
          <pre>
            <code>{MOCK_FILES[selectedFile]?.code || ""}</code>
          </pre>
        </div>
      </div>

    </div>
  );
};
export default CodeViewer;
