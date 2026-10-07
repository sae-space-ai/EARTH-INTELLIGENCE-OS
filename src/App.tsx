import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Globe, LayoutDashboard, BookOpen, GitBranch, Shield, Zap,
  Database, Radio, Server, FileText, Map, Cpu, ChevronRight,
  Activity, AlertTriangle, CheckCircle2, Clock, Satellite,
  Eye, Brain, Target, Link2, Lock, Menu, X
} from 'lucide-react';
import { Dashboard } from './pages/Dashboard';
import { ArchitecturePage } from './pages/Architecture';
import { DomainsPage } from './pages/Domains';
import { EventsPage } from './pages/Events';
import { APIPage } from './pages/API';
import { ADRsPage } from './pages/ADRs';
import { RoadmapPage } from './pages/Roadmap';
import { SecurityPage } from './pages/Security';
import { PipelinePage } from './pages/Pipeline';
import { KnowledgePage } from './pages/Knowledge';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  color: string;
}

const navItems: NavItem[] = [
  { id: 'dashboard', label: 'Control Room', icon: <LayoutDashboard size={18} />, color: '#00d4ff' },
  { id: 'architecture', label: 'Architecture', icon: <GitBranch size={18} />, color: '#00ff88' },
  { id: 'domains', label: 'Domains', icon: <Globe size={18} />, color: '#a855f7' },
  { id: 'pipeline', label: 'Pipeline', icon: <Activity size={18} />, color: '#ff6b35' },
  { id: 'events', label: 'Event Bus', icon: <Radio size={18} />, color: '#ffd700' },
  { id: 'knowledge', label: 'Knowledge', icon: <Brain size={18} />, color: '#06b6d4' },
  { id: 'api', label: 'API', icon: <Server size={18} />, color: '#00d4ff' },
  { id: 'adrs', label: 'ADRs', icon: <BookOpen size={18} />, color: '#00ff88' },
  { id: 'security', label: 'Security', icon: <Shield size={18} />, color: '#ff3366' },
  { id: 'roadmap', label: 'Roadmap', icon: <Map size={18} />, color: '#a855f7' },
];

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => setCurrentTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const renderPage = () => {
    switch (activePage) {
      case 'dashboard': return <Dashboard />;
      case 'architecture': return <ArchitecturePage />;
      case 'domains': return <DomainsPage />;
      case 'pipeline': return <PipelinePage />;
      case 'events': return <EventsPage />;
      case 'knowledge': return <KnowledgePage />;
      case 'api': return <APIPage />;
      case 'adrs': return <ADRsPage />;
      case 'security': return <SecurityPage />;
      case 'roadmap': return <RoadmapPage />;
      default: return <Dashboard />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden bg-earth-900">
      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ width: sidebarOpen ? 240 : 64 }}
        className="relative flex flex-col border-r border-earth-600/50 bg-earth-800/80 backdrop-blur-sm z-20"
      >
        {/* Logo */}
        <div className="flex items-center gap-3 p-4 border-b border-earth-600/50">
          <div className="relative flex-shrink-0">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-neon-blue to-neon-green flex items-center justify-center">
              <Globe size={18} className="text-earth-900" />
            </div>
            <div className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-neon-green rounded-full animate-pulse-glow" />
          </div>
          <AnimatePresence>
            {sidebarOpen && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                className="overflow-hidden"
              >
                <h1 className="text-sm font-bold text-white whitespace-nowrap">EARTH INTELLIGENCE</h1>
                <p className="text-[10px] text-neon-blue font-mono">OS v0.1.0 — Phase 0</p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-2 space-y-1 overflow-y-auto">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-all duration-200 group
                ${activePage === item.id
                  ? 'bg-earth-600/50 text-white'
                  : 'text-earth-300 hover:bg-earth-700/50 hover:text-white'
                }`}
            >
              <span style={{ color: activePage === item.id ? item.color : undefined }}>
                {item.icon}
              </span>
              <AnimatePresence>
                {sidebarOpen && (
                  <motion.span
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="whitespace-nowrap"
                  >
                    {item.label}
                  </motion.span>
                )}
              </AnimatePresence>
              {activePage === item.id && sidebarOpen && (
                <motion.div
                  layoutId="activeIndicator"
                  className="ml-auto w-1.5 h-1.5 rounded-full"
                  style={{ backgroundColor: item.color }}
                />
              )}
            </button>
          ))}
        </nav>

        {/* Status bar */}
        <div className="p-3 border-t border-earth-600/50">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 rounded-full bg-neon-green animate-pulse-glow" />
            {sidebarOpen && (
              <span className="text-[10px] text-earth-400 font-mono">
                SYSTEM OPERATIONAL
              </span>
            )}
          </div>
        </div>

        {/* Toggle */}
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full bg-earth-700 border border-earth-600 flex items-center justify-center text-earth-400 hover:text-white hover:bg-earth-600 transition-colors z-30"
        >
          {sidebarOpen ? <ChevronRight size={12} /> : <Menu size={12} />}
        </button>
      </motion.aside>

      {/* Main content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="flex items-center justify-between px-6 py-3 border-b border-earth-600/50 bg-earth-800/50 backdrop-blur-sm">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-white">
              {navItems.find(n => n.id === activePage)?.label || 'Control Room'}
            </h2>
            <span className="px-2 py-0.5 text-[10px] font-mono rounded-full bg-neon-blue/10 text-neon-blue border border-neon-blue/20">
              PHASE 0
            </span>
          </div>
          <div className="flex items-center gap-4 text-xs text-earth-400 font-mono">
            <span className="flex items-center gap-1.5">
              <Clock size={12} />
              {currentTime.toISOString().replace('T', ' ').slice(0, 19)} UTC
            </span>
            <span className="flex items-center gap-1.5">
              <div className="w-1.5 h-1.5 rounded-full bg-neon-green" />
              ALL SYSTEMS NOMINAL
            </span>
          </div>
        </header>

        {/* Page content */}
        <div className="flex-1 overflow-y-auto grid-bg">
          <AnimatePresence mode="wait">
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="p-6"
            >
              {renderPage()}
            </motion.div>
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
