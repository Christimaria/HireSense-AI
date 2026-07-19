import { useState } from 'react';
import { api } from '../services/api';
import { 
  Compass, Map, Target, AlertTriangle, Layers, BookOpen, 
  Calendar, Award, CheckSquare, Sparkles, RefreshCw, Loader2, ExternalLink
} from 'lucide-react';

export default function Roadmap() {
  const [skillsInput, setSkillsInput] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [timeline, setTimeline] = useState('3 months');
  const [loading, setLoading] = useState(false);
  const [streamedText, setStreamedText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!skillsInput.trim() || !targetRole.trim() || !timeline.trim()) {
      setError('All fields are required.');
      return;
    }

    // Split skills by comma and clean up whitespace
    const skillsArray = skillsInput
      .split(',')
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    if (skillsArray.length === 0) {
      setError('Please list at least one current skill.');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);
    setStreamedText('');

    api.generateRoadmap(
      skillsArray,
      targetRole,
      timeline,
      // onChunk
      (chunk) => {
        setStreamedText((prev) => prev + chunk);
      },
      // onResult
      (finalResult) => {
        setResult(finalResult);
        setLoading(false);
      },
      // onError
      (errMessage) => {
        setError(errMessage);
        setLoading(false);
      }
    );
  };

  const handleReset = () => {
    setSkillsInput('');
    setTargetRole('');
    setTimeline('3 months');
    setResult(null);
    setError('');
    setStreamedText('');
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-extrabold text-white sm:text-4xl">
          AI Career <span className="text-gradient">Preparation Roadmap</span>
        </h1>
        <p className="mx-auto mt-2 max-w-xl text-sm text-slate-400">
          Enter your current skill set, target tech role, and study timeline to receive a custom week-by-week transition blueprint.
        </p>
      </div>

      {error && (
        <div className="mb-8 rounded-xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-400 flex items-start space-x-3">
          <AlertTriangle className="h-5 w-5 shrink-0" />
          <div>{error}</div>
        </div>
      )}

      {/* SETUP FORM */}
      {!loading && !result ? (
        <form onSubmit={handleSubmit} className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/20 p-6 sm:p-8 glass-panel animate-fade-in">
          {/* Target Role & Timeline */}
          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <label htmlFor="target-role" className="block text-sm font-semibold text-slate-200 mb-2">
                Target Role <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                id="target-role"
                required
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                placeholder="e.g. Backend Developer"
                maxLength={120}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 placeholder-slate-600 focus:border-indigo-500/50 outline-none transition"
              />
            </div>

            <div>
              <label htmlFor="timeline" className="block text-sm font-semibold text-slate-200 mb-2">
                Prep Timeline <span className="text-rose-500">*</span>
              </label>
              <input
                type="text"
                id="timeline"
                required
                value={timeline}
                onChange={(e) => setTimeline(e.target.value)}
                placeholder="e.g. 8 weeks, 3 months"
                maxLength={60}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 placeholder-slate-600 focus:border-indigo-500/50 outline-none transition"
              />
            </div>
          </div>

          {/* Current Skills */}
          <div>
            <label htmlFor="current-skills" className="block text-sm font-semibold text-slate-200 mb-2">
              Your Current Skills <span className="text-rose-500">*</span> <span className="text-xs text-slate-500 font-normal">(Comma-separated)</span>
            </label>
            <textarea
              id="current-skills"
              required
              rows={4}
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              placeholder="e.g. HTML, CSS, JavaScript, Basic Git, React basics"
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 placeholder-slate-600 focus:border-indigo-500/50 outline-none transition"
            />
            <p className="mt-1 text-xs text-slate-500">
              List the tools, programming languages, or databases you already know to bypass repeated content.
            </p>
          </div>

          <button
            type="submit"
            className="w-full flex items-center justify-center space-x-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 py-4 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition duration-200 cursor-pointer"
          >
            <Sparkles className="h-4 w-4" />
            <span>Generate Career Roadmap</span>
          </button>
        </form>
      ) : loading ? (
        /* LOADING / STREAMING STATE */
        <div className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/30 p-8 glass-panel text-center animate-fade-in">
          <div className="flex flex-col items-center justify-center py-8">
            <Loader2 className="h-10 w-10 text-indigo-500 animate-spin mb-4" />
            <h3 className="font-heading text-lg font-bold text-white mb-2">Assembling Career Roadmap...</h3>
            <p className="text-sm text-slate-400 max-w-sm">
              Gemini is auditing your current skills against standard requirements for {targetRole} and building a custom schedule.
            </p>
          </div>

          {streamedText && (
            <div className="text-left">
              <div className="flex items-center justify-between px-4 py-2 bg-slate-950/80 border-t border-x border-slate-800 rounded-t-xl">
                <span className="text-[10px] uppercase font-mono tracking-widest text-slate-500">Roadmap Stream Buffer</span>
                <div className="flex space-x-1.5">
                  <div className="w-2.5 h-2.5 rounded-full bg-indigo-500/40 animate-pulse" />
                </div>
              </div>
              <div className="max-h-48 overflow-y-auto p-4 bg-slate-950 rounded-b-xl border border-slate-800 text-[11px] font-mono text-cyan-300/80 leading-relaxed whitespace-pre-wrap">
                {streamedText}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* ROADMAP DISPLAY */
        <div className="space-y-10 animate-slide-up">
          {/* Header Summary */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Target Profile</div>
              <h2 className="text-2xl font-bold font-heading text-white mt-1">{targetRole}</h2>
            </div>
            <div className="flex items-center space-x-2 text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-4 py-2 rounded-xl text-sm font-semibold self-start md:self-auto">
              <Calendar className="h-4 w-4" />
              <span>{timeline} Roadmap</span>
            </div>
          </div>

          {/* Skill Gaps Diagnostics */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/20 p-6 glass-panel">
            <h3 className="text-sm font-bold uppercase tracking-wider text-rose-400 flex items-center space-x-2 mb-4">
              <AlertTriangle className="h-5 w-5" />
              <span>Identified Skill Gaps</span>
            </h3>
            <div className="flex flex-wrap gap-2">
              {result.skill_gaps.map((gap, idx) => (
                <span 
                  key={idx} 
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-500/10 border border-rose-500/20 text-rose-300"
                >
                  {gap}
                </span>
              ))}
            </div>
          </div>

          {/* Week-by-Week timeline plan */}
          <div>
            <h3 className="text-lg font-bold text-white mb-6 flex items-center space-x-2">
              <Layers className="h-5 w-5 text-indigo-400" />
              <span>Weekly Syllabus & Tasks</span>
            </h3>
            
            <div className="relative border-l border-slate-800 ml-4 space-y-8">
              {result.weekly_roadmap.map((weekItem) => (
                <div key={weekItem.week} className="relative pl-8">
                  {/* Timeline bullet dot */}
                  <span className="absolute -left-3 top-1 flex h-6 w-6 items-center justify-center rounded-full bg-slate-950 border border-indigo-500 text-[10px] font-bold text-indigo-400">
                    {weekItem.week}
                  </span>

                  <div className="rounded-xl border border-slate-800 bg-slate-900/10 p-5 glass-panel">
                    <h4 className="font-heading font-semibold text-slate-100 text-base mb-3">
                      Week {weekItem.week}: {weekItem.focus}
                    </h4>

                    <div className="grid gap-6 md:grid-cols-2 mt-4">
                      {/* Check topics to learn */}
                      <div className="space-y-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Topics to Cover</span>
                        <ul className="space-y-2">
                          {weekItem.topics.map((topic, i) => (
                            <li key={i} className="text-xs text-slate-300 flex items-start space-x-2 leading-relaxed">
                              <CheckSquare className="h-4 w-4 shrink-0 text-indigo-500/70" />
                              <span>{topic}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Practical tasks */}
                      <div className="space-y-2">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 block mb-1">Hands-on Sandbox Projects</span>
                        <ul className="space-y-2">
                          {weekItem.tasks.map((task, i) => (
                            <li key={i} className="text-xs text-slate-300 flex items-start space-x-2 leading-relaxed">
                              <Map className="h-4 w-4 shrink-0 text-cyan-500/70" />
                              <span>{task}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Milestones & Resources */}
          <div className="grid gap-6 md:grid-cols-2">
            {/* Milestones check */}
            <div className="rounded-xl border border-slate-800 bg-slate-900/20 p-6 glass-panel">
              <h3 className="font-heading text-sm font-bold uppercase tracking-wider text-indigo-400 flex items-center space-x-2 mb-4">
                <Award className="h-5 w-5" />
                <span>Roadmap Milestones</span>
              </h3>
              <div className="space-y-4">
                {result.milestones.map((mil, idx) => (
                  <div key={idx} className="border-b border-slate-850 pb-3 last:border-b-0 last:pb-0">
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-0.5 rounded bg-indigo-500/10 text-indigo-300 text-[10px] font-bold">
                        Week {mil.week_number} Check
                      </span>
                      <h4 className="text-xs font-bold text-slate-200">{mil.title}</h4>
                    </div>
                    <p className="text-xs text-slate-400 mt-1.5 leading-relaxed">{mil.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Recommended Learning Resources */}
            <div className="rounded-xl border border-slate-800 bg-slate-900/20 p-6 glass-panel">
              <h3 className="font-heading text-sm font-bold uppercase tracking-wider text-cyan-400 flex items-center space-x-2 mb-4">
                <BookOpen className="h-5 w-5" />
                <span>Reference Material & URLs</span>
              </h3>
              <div className="space-y-4">
                {result.learning_resources.map((res, idx) => (
                  <div key={idx} className="border-b border-slate-850 pb-3 last:border-b-0 last:pb-0">
                    <div className="flex items-start justify-between">
                      <div>
                        <h4 className="text-xs font-bold text-slate-200">{res.title}</h4>
                        <span className="inline-block mt-0.5 text-[9px] uppercase font-semibold text-cyan-400 bg-cyan-500/10 border border-cyan-500/20 px-1.5 py-0.2 rounded">
                          {res.type}
                        </span>
                      </div>
                      {res.url && (
                        <a 
                          href={res.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="text-slate-500 hover:text-indigo-400"
                        >
                          <ExternalLink className="h-3.5 w-3.5" />
                        </a>
                      )}
                    </div>
                    <p className="text-xs text-slate-400 mt-2 leading-relaxed">{res.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Reset Action */}
          <div className="flex justify-center mt-6">
            <button
              onClick={handleReset}
              className="flex items-center space-x-2 rounded-xl border border-slate-800 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-300 hover:bg-slate-900 hover:text-white transition duration-200"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Create Another Career Roadmap</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
