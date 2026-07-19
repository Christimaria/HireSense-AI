import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Menu, X, BrainCircuit, FileText, Bot, Compass, Home } from 'lucide-react';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { name: 'Home', path: '/', icon: Home },
    { name: 'Resume Review', path: '/resume', icon: FileText },
    { name: 'Mock Interview', path: '/interview', icon: Bot },
    { name: 'Career Roadmap', path: '/roadmap', icon: Compass },
  ];

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          {/* Logo Section */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2 group">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-indigo-600 text-white shadow-lg shadow-indigo-500/30 group-hover:bg-indigo-500 transition-colors duration-200">
                <BrainCircuit className="h-6 w-6 animate-pulse-slow" />
              </div>
              <span className="font-heading text-xl font-bold tracking-tight text-white">
                HireSense<span className="text-indigo-400">AI</span>
              </span>
            </Link>
          </div>

          {/* Desktop Nav Items */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-center space-x-1">
              {navItems.map((item) => {
                const Icon = item.icon;
                const active = isActive(item.path);
                return (
                  <Link
                    key={item.name}
                    to={item.path}
                    className={`flex items-center space-x-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 ${
                      active
                        ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20'
                        : 'text-slate-400 hover:text-slate-100 hover:bg-slate-900/60'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setIsOpen(!isOpen)}
              type="button"
              className="inline-flex items-center justify-center rounded-lg p-2 text-slate-400 hover:bg-slate-900 hover:text-white focus:outline-none"
              aria-controls="mobile-menu"
              aria-expanded={isOpen}
            >
              <span className="sr-only">Open main menu</span>
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden border-b border-slate-800 bg-slate-950/95" id="mobile-menu">
          <div className="space-y-1 px-2 pb-3 pt-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = isActive(item.path);
              return (
                <Link
                  key={item.name}
                  to={item.path}
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center space-x-3 rounded-lg px-3 py-2.5 text-base font-medium transition-colors ${
                    active
                      ? 'bg-indigo-600/10 text-indigo-400 border-l-2 border-indigo-500'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-white'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              );
            })}
          </div>
        </div>
      )}
    </nav>
  );
}
