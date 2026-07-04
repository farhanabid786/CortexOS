import React from 'react';
import { Link } from 'react-router-dom';
import { Layers, Terminal, ArrowRight, Brain, Zap } from 'lucide-react';
import Navbar from '../components/Navbar';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-darkBg text-slate-100">
      <Navbar />

      {/* Hero Section */}
      <header className="relative flex-1 flex flex-col justify-center items-center text-center px-6 py-20 overflow-hidden">
        {/* Glow backdrop circles */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 animate-pulse-slow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl -z-10 animate-pulse-slow"></div>

        <div className="max-w-4xl space-y-6">
          <div className="inline-flex items-center space-x-2 bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider mb-2">
            <Zap className="h-3.5 w-3.5" />
            <span>Autonomous Multi-Agent AI Platform</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight leading-none bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
            Build Software Blueprints <br />
            <span className="bg-gradient-to-r from-cyan-400 to-indigo-500 bg-clip-text text-transparent">With 10 Collaborating Agents</span>
          </h1>

          <p className="text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Translate natural language requirements into complete production-ready architectures, REST APIs, database schemas, and deployment guides automatically.
          </p>

          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4 pt-6">
            <Link
              to="/login"
              className="w-full sm:w-auto bg-gradient-to-r from-cyan-400 to-indigo-500 hover:from-cyan-500 hover:to-indigo-600 text-slate-950 font-bold px-8 py-3.5 rounded-xl flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 shadow-lg shadow-cyan-500/20"
            >
              <span>Get Started Free</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
            <a
              href="#agents"
              className="w-full sm:w-auto bg-white/5 border border-white/10 hover:bg-white/10 text-slate-300 hover:text-white font-semibold px-8 py-3.5 rounded-xl transition-all flex items-center justify-center"
            >
              Learn More
            </a>
          </div>
        </div>
      </header>

      {/* Agents section */}
      <section id="agents" className="py-20 px-6 md:px-12 max-w-7xl mx-auto space-y-12 border-t border-glassBorder/40">
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <h2 className="text-3xl font-bold text-white">The Cortex Multi-Agent Grid</h2>
          <p className="text-slate-400 text-sm">
            Ten specialized virtual engineers collaborating sequentially, passing structured JSON specifications downstream to review, audit, and build your application.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="glass-card p-6 space-y-3">
            <div className="text-cyan-400 bg-cyan-400/10 p-2.5 rounded-xl w-fit"><Brain className="h-6 w-6" /></div>
            <h3 className="font-bold text-white text-lg">1. Requirements & Product</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Requirement Analyst checks injection security and maps functional modules. Product Manager details agile stories, priorities, and success metrics.
            </p>
          </div>

          <div className="glass-card p-6 space-y-3">
            <div className="text-indigo-400 bg-indigo-400/10 p-2.5 rounded-xl w-fit"><Layers className="h-6 w-6" /></div>
            <h3 className="font-bold text-white text-lg">2. Architecture & Database</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Software Architect sets structures and stack parameters. Database Engineer compiles ERD models, key constraints, and relational tables.
            </p>
          </div>

          <div className="glass-card p-6 space-y-3">
            <div className="text-emerald-400 bg-emerald-400/10 p-2.5 rounded-xl w-fit"><Terminal className="h-6 w-6" /></div>
            <h3 className="font-bold text-white text-lg">3. Engineering & Security</h3>
            <p className="text-slate-400 text-xs leading-relaxed">
              Backend and Frontend engineers generate route paths, endpoints, and component tree trees. Security Analyst reviews threats (STRIDE audit).
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-glassBorder/40 py-8 text-center text-xs text-slate-500 mt-auto">
        &copy; {new Date().getFullYear()} CortexOS. All rights reserved. Capstone Project.
      </footer>
    </div>
  );
};
export default LandingPage;
