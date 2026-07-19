import { Link } from 'react-router-dom';
import { FileText, Bot, Compass, ArrowRight, CheckCircle, Award, Sparkles } from 'lucide-react';

export default function Home() {
  const features = [
    {
      title: 'Resume Review',
      description: 'Upload your resume for real-time ATS optimization scoring, section-by-section analysis, strengths, weaknesses, and actionable feedback.',
      path: '/resume',
      icon: FileText,
      color: 'from-blue-500/20 to-indigo-500/20 hover:border-indigo-500/40 text-indigo-400',
      tag: 'ATS Optimization',
    },
    {
      title: 'Mock Interview',
      description: 'Engage in a live, streaming, conversational Q&A mock interview tailored to your role. Get scores, tips, and comprehensive model answers for each turn.',
      path: '/interview',
      icon: Bot,
      color: 'from-violet-500/20 to-purple-500/20 hover:border-purple-500/40 text-purple-400',
      tag: 'Interactive Q&A',
    },
    {
      title: 'Career Roadmap',
      description: 'Bridge your skill gaps. Enter your current stack and target role to generate a custom, weekly learning path with resource links and checkpoints.',
      path: '/roadmap',
      icon: Compass,
      color: 'from-cyan-500/20 to-blue-500/20 hover:border-cyan-500/40 text-cyan-400',
      tag: 'Skills Mapping',
    },
  ];

  return (
    <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="text-center relative">
        {/* Glow decoration */}
        <div className="absolute left-1/2 top-0 -z-10 h-72 w-72 -translate-x-1/2 rounded-full bg-indigo-500/10 blur-[120px]" />
        
        <div className="inline-flex items-center space-x-1.5 rounded-full border border-indigo-500/30 bg-indigo-500/10 px-3 py-1.5 text-xs font-semibold text-indigo-300 mb-6 animate-pulse-slow">
          <Sparkles className="h-3.5 w-3.5" />
          <span>Next-Generation Career Readiness Co-Pilot</span>
        </div>

        <h1 className="text-4xl font-extrabold tracking-tight sm:text-6xl text-white mb-6">
          Supercharge Your Career Preparation <br />
          <span className="text-gradient">Powered by Gemini AI</span>
        </h1>
        
        <p className="mx-auto max-w-2xl text-lg text-slate-400 leading-relaxed mb-10">
          Get institutional-grade interview practice, precise resume ATS feedback, and a tailored learning roadmap to land your dream tech job.
        </p>

        <div className="flex justify-center space-x-4">
          <Link
            to="/interview"
            className="flex items-center space-x-2 rounded-xl bg-indigo-600 px-6 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 hover:bg-indigo-500 transition duration-200"
          >
            <span>Start Mock Interview</span>
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link
            to="/resume"
            className="flex items-center space-x-2 rounded-xl border border-slate-800 bg-slate-900/60 px-6 py-3.5 text-sm font-semibold text-slate-300 hover:bg-slate-900 hover:text-white transition duration-200"
          >
            <span>Review Resume</span>
          </Link>
        </div>
      </div>

      {/* Feature Section */}
      <div className="mt-24">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
            Choose Your Preparation Path
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-base text-slate-500">
            A comprehensive suite of intelligence tools designed to assess and elevate your skills.
          </p>
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          {features.map((feat) => {
            const Icon = feat.icon;
            return (
              <div
                key={feat.title}
                className={`flex flex-col justify-between rounded-2xl border border-slate-800 bg-slate-900/30 p-8 glass-panel-hover`}
              >
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <div className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-slate-900 border border-slate-800 text-indigo-400 shadow-md">
                      <Icon className="h-6 w-6" />
                    </div>
                    <span className="inline-flex items-center rounded-full bg-indigo-500/10 px-2.5 py-0.5 text-xs font-medium text-indigo-300">
                      {feat.tag}
                    </span>
                  </div>
                  <h3 className="font-heading text-xl font-bold text-white mb-3">
                    {feat.title}
                  </h3>
                  <p className="text-sm text-slate-400 leading-relaxed mb-6">
                    {feat.description}
                  </p>
                </div>
                <Link
                  to={feat.path}
                  className="flex items-center space-x-1.5 text-sm font-semibold text-indigo-400 hover:text-indigo-300 group"
                >
                  <span>Explore Module</span>
                  <ArrowRight className="h-4 w-4 transform group-hover:translate-x-1 transition-transform" />
                </Link>
              </div>
            );
          })}
        </div>
      </div>

      {/* Stats/Benefits Section */}
      <div className="mt-28 rounded-3xl border border-slate-800 bg-slate-900/20 p-8 sm:p-12 relative overflow-hidden glass-panel">
        <div className="absolute -left-1/4 -top-1/4 -z-10 h-64 w-64 rounded-full bg-purple-500/5 blur-[80px]" />
        <div className="grid gap-8 md:grid-cols-3">
          <div className="flex items-start space-x-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-indigo-500/10 text-indigo-400">
              <CheckCircle className="h-5 w-5" />
            </div>
            <div>
              <h4 className="font-heading font-semibold text-white">Stateless & Secure</h4>
              <p className="mt-1 text-xs text-slate-500 leading-normal">
                No database or retention. Your resume text, answers, and data remain strictly yours, deleted after your session.
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-purple-500/10 text-purple-400">
              <Bot className="h-5 w-5" />
            </div>
            <div>
              <h4 className="font-heading font-semibold text-white">Interactive Streaming UI</h4>
              <p className="mt-1 text-xs text-slate-500 leading-normal">
                Powered by Gemini. Experience fast streaming outputs, typing animations, and immediate feedback loop.
              </p>
            </div>
          </div>
          <div className="flex items-start space-x-4">
            <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-cyan-500/10 text-cyan-400">
              <Award className="h-5 w-5" />
            </div>
            <div>
              <h4 className="font-heading font-semibold text-white">ATS Calibration</h4>
              <p className="mt-1 text-xs text-slate-500 leading-normal">
                Optimize your applications for automated systems using standard recruitment keyword models.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
