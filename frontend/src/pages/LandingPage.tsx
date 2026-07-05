import React from 'react';
import { Link } from 'react-router-dom';
import { Layers, Terminal, ArrowRight, Brain, Zap } from 'lucide-react';
import Navbar from '../components/Navbar';
import TextType from '../components/TextType';

export const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col bg-lightBg dark:bg-darkBg text-slate-800 dark:text-slate-100 transition-colors duration-300">
      <Navbar />

      {/* Hero Section */}
      <header className="relative flex-1 flex flex-col justify-center items-center text-center px-6 py-20 overflow-hidden">
        {/* Glow backdrop circles */}
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 animate-pulse-slow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl -z-10 animate-pulse-slow"></div>

        <div className="max-w-4xl space-y-6">
          <div className="inline-flex items-center space-x-2 bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 border border-cyan-500/20 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider mb-2">
            <Zap className="h-3.5 w-3.5 animate-pulse" />
            <span>Autonomous Multi-Agent AI Platform</span><br />
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight leading-none bg-gradient-to-r from-slate-900 via-slate-800 to-slate-600 dark:from-white dark:via-slate-100 dark:to-slate-400 bg-clip-text text-transparent pb-1">
            Build Software Blueprints <br />
            <span className="bg-gradient-to-r from-cyan-500 to-indigo-600 dark:from-cyan-400 dark:to-indigo-500 bg-clip-text text-transparent">
              <TextType
                as="span"
                text={["With 10 Collaborating Agents", "With Multi-Agent Workflow", "With Autonomous AI Teams"]}
                typingSpeed={60}
                pauseDuration={2500}
                showCursor={true}
                cursorCharacter="|"
                cursorClassName="text-cyan-600 dark:text-cyan-400 font-normal ml-1"
              />
            </span>
          </h1>
          <br />
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Translate natural language requirements into complete production-ready architectures, REST APIs, database schemas, and deployment guides automatically.
          </p>
          <br />
          <div className="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4 pt-6">
            <Link
              to="/login"
              className="w-full sm:w-auto bg-gradient-to-r from-cyan-500 to-indigo-600 dark:from-cyan-400 dark:to-indigo-500 hover:from-cyan-600 hover:to-indigo-700 dark:hover:from-cyan-500 dark:hover:to-indigo-600 text-slate-950 dark:text-slate-955 font-bold px-8 py-3.5 rounded-xl flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5 shadow-lg shadow-cyan-500/20"
            >
              <span>Get Started Free</span>
              <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a
              href="#agents"
              className="w-full sm:w-auto bg-slate-900/5 dark:bg-white/5 border border-slate-900/10 dark:border-white/10 hover:bg-slate-900/10 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300 hover:text-slate-900 dark:hover:text-white font-semibold px-8 py-3.5 rounded-xl transition-all transform hover:-translate-y-0.5 hover:shadow-md flex items-center justify-center"
            >
              Learn More
            </a>
          </div>
        </div>
      </header>

      {/* Agents section */}
      <section id="agents" className="py-20 px-6 md:px-12 max-w-7xl mx-auto space-y-12 border-t border-slate-200 dark:border-glassBorder/40">
        <div className="text-center max-w-2xl mx-auto space-y-3">
          <h2 className="text-3xl font-bold text-slate-900 dark:text-white">The Cortex Multi-Agent Grid</h2>
          <p className="text-slate-500 dark:text-slate-400 text-sm">
            Ten specialized virtual engineers collaborating sequentially, passing structured JSON specifications downstream to review, audit, and build your application.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="group glass-card p-6 space-y-3">
            <div className="text-cyan-600 dark:text-cyan-400 bg-cyan-500/10 p-2.5 rounded-xl w-fit transform group-hover:scale-110 transition-transform duration-300"><Brain className="h-6 w-6" /></div>
            <h3 className="font-bold text-slate-900 dark:text-white text-lg group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">1. Requirements & Product</h3>
            <p className="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">
              Requirement Analyst checks injection security and maps functional modules. Product Manager details agile stories, priorities, and success metrics.
            </p>
          </div>

          <div className="group glass-card p-6 space-y-3">
            <div className="text-indigo-600 dark:text-indigo-400 bg-indigo-500/10 p-2.5 rounded-xl w-fit transform group-hover:scale-110 transition-transform duration-300"><Layers className="h-6 w-6" /></div>
            <h3 className="font-bold text-slate-900 dark:text-white text-lg group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">2. Architecture & Database</h3>
            <p className="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">
              Software Architect sets structures and stack parameters. Database Engineer compiles ERD models, key constraints, and relational tables.
            </p>
          </div>

          <div className="group glass-card p-6 space-y-3">
            <div className="text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 p-2.5 rounded-xl w-fit transform group-hover:scale-110 transition-transform duration-300"><Terminal className="h-6 w-6" /></div>
            <h3 className="font-bold text-slate-900 dark:text-white text-lg group-hover:text-cyan-600 dark:group-hover:text-cyan-400 transition-colors">3. Engineering & Security</h3>
            <p className="text-slate-600 dark:text-slate-400 text-xs leading-relaxed">
              Backend and Frontend engineers generate route paths, endpoints, and component tree trees. Security Analyst reviews threats (STRIDE audit).
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-200 dark:border-glassBorder/40 py-8 text-center text-xs text-slate-500 mt-auto">
        &copy; {new Date().getFullYear()} CortexOS. All rights reserved. Capstone Project.
      </footer>
    </div>
  );
};
export default LandingPage;
