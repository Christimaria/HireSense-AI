import { BrainCircuit, Heart } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="mt-auto border-t border-slate-800 bg-slate-950/40 py-8">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          <div className="flex items-center space-x-2">
            <BrainCircuit className="h-5 w-5 text-indigo-500" />
            <span className="font-heading text-sm font-semibold tracking-tight text-white">
              HireSense<span className="text-indigo-400">AI</span>
            </span>
          </div>
          <p className="text-center text-xs text-slate-500 md:text-left">
            &copy; {new Date().getFullYear()} HireSense AI. All rights reserved. Made with{' '}
            <Heart className="inline-block h-3 w-3 text-red-500 fill-current" /> using React + Gemini API.
          </p>
          <div className="flex space-x-4 text-xs text-slate-500">
            <span className="hover:text-indigo-400 cursor-default">Privacy</span>
            <span className="hover:text-indigo-400 cursor-default">Terms</span>
            <span className="hover:text-indigo-400 cursor-default">Support</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
