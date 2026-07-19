import { useState } from 'react';
import { api } from '../services/api';
import { 
  FileText, Sparkles, CheckCircle, AlertTriangle, Lightbulb, 
  RefreshCw, BarChart2, Star, Target, ArrowRight, Loader2 
} from 'lucide-react';

export default function ResumeReview() {
  const [resumeText, setResumeText] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [loading, setLoading] = useState(false);
  const [streamedText, setStreamedText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const characterCount = resumeText.trim().length;
  const isInputValid = characterCount >= 100 && characterCount <= 10000;

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isInputValid) return;

    setLoading(true);
    setError('');
    setResult(null);
    setStreamedText('');

    api.reviewResume(
      resumeText,
      targetRole,
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
    setResumeText('');
    setTargetRole('');
    setResult(null);
    setError('');
    setStreamedText('');
  };

  // Helper to color code scores
  const getScoreColor = (score) => {
    if (score >= 8) return 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20';
    if (score >= 6) return 'text-amber-400 bg-amber-500/10 border-amber-500/20';
    return 'text-rose-400 bg-rose-500/10 border-rose-500/20';
  };

  const getATSColor = (score) => {
    if (score >= 80) return 'text-emerald-400';
    if (score >= 60) return 'text-amber-400';
    return 'text-rose-400';
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-extrabold text-white sm:text-4xl">
          ATS & Content <span className="text-gradient">Resume Reviewer</span>
        </h1>
        <p className="mx-auto mt-2 max-w-xl text-sm text-slate-400">
          Paste your resume text below. Gemini will scan and calibrate its language, formatting, and ATS compatibility.
        </p>
      </div>

      {error && (
        <div className="mb-8 rounded-xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-400 flex items-start space-x-3">
          <AlertTriangle className="h-5 w-5 shrink-0" />
          <div>
            <span className="font-semibold">Analysis Failed:</span> {error}
          </div>
        </div>
      )}

      {/* Main Container */}
      {!loading && !result ? (
        <form onSubmit={handleSubmit} className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/20 p-6 sm:p-8 glass-panel animate-fade-in">
          {/* Target Role */}
          <div>
            <label htmlFor="target-role" className="block text-sm font-semibold text-slate-200 mb-2">
              Target Job Role <span className="text-xs text-slate-500 font-normal">(Optional — helps Gemini tailor suggestions)</span>
            </label>
            <input
              type="text"
              id="target-role"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Senior Full-Stack Engineer"
              maxLength={120}
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 placeholder-slate-600 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 outline-none transition"
            />
          </div>

          {/* Resume Content */}
          <div>
            <label htmlFor="resume-text" className="block text-sm font-semibold text-slate-200 mb-2">
              Resume Plain Text <span className="text-rose-500">*</span>
            </label>
            <textarea
              id="resume-text"
              required
              rows={12}
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste the full text of your resume here (e.g. contact info, professional summary, work experience, skills, education)..."
              className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm font-mono text-slate-300 placeholder-slate-600 focus:border-indigo-500/50 focus:ring-1 focus:ring-indigo-500/30 outline-none transition"
            />
            {/* Character count validator */}
            <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
              <span>Must be between 100 and 10,000 characters.</span>
              <span className={characterCount < 100 || characterCount > 10000 ? 'text-rose-400 font-semibold' : 'text-slate-400'}>
                {characterCount.toLocaleString()} / 10,000 characters
              </span>
            </div>
          </div>

          {/* Submit */}
          <button
            type="submit"
            disabled={!isInputValid}
            className={`w-full flex items-center justify-center space-x-2 rounded-xl py-4 text-sm font-semibold text-white shadow-lg transition duration-200 ${
              isInputValid
                ? 'bg-indigo-600 hover:bg-indigo-500 shadow-indigo-500/25 cursor-pointer'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700/50'
            }`}
          >
            <Sparkles className="h-4 w-4" />
            <span>Analyze Resume</span>
          </button>
        </form>
      ) : loading ? (
        /* Loading & Streaming UI */
        <div className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/30 p-8 glass-panel text-center animate-fade-in">
          <div className="flex flex-col items-center justify-center py-8">
            <Loader2 className="h-10 w-10 text-indigo-500 animate-spin mb-4" />
            <h3 className="font-heading text-lg font-bold text-white mb-2">Analyzing Resume Structure...</h3>
            <p className="text-sm text-slate-400 max-w-sm">
              Gemini is assessing ATS readability, grading content sections, and generating tailoring recommendations.
            </p>
          </div>

          {/* Real-time Streaming compilation view */}
          {streamedText && (
            <div className="text-left">
              <div className="flex items-center justify-between px-4 py-2 bg-slate-950/80 border-t border-x border-slate-800 rounded-t-xl">
                <span className="text-[10px] uppercase font-mono tracking-widest text-slate-500">Gemini Output Stream</span>
                <div className="flex space-x-1.5">
                  <div className="w-2 h-2 rounded-full bg-rose-500" />
                  <div className="w-2 h-2 rounded-full bg-amber-500" />
                  <div className="w-2 h-2 rounded-full bg-emerald-500" />
                </div>
              </div>
              <div className="max-h-48 overflow-y-auto p-4 bg-slate-950 rounded-b-xl border border-slate-800 text-[11px] font-mono text-indigo-300/80 leading-relaxed whitespace-pre-wrap">
                {streamedText}
              </div>
            </div>
          )}
        </div>
      ) : (
        /* Structured Result Viewer */
        <div className="space-y-8 animate-slide-up">
          {/* Main Scorecards */}
          <div className="grid gap-6 sm:grid-cols-2">
            {/* Overall Score */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-6 glass-panel flex items-center justify-between">
              <div>
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">Overall Content Quality</div>
                <div className="text-3xl font-bold font-heading text-white">
                  {result.overall_score.toFixed(1)} <span className="text-slate-600 text-sm">/ 10</span>
                </div>
                <p className="mt-2 text-xs text-slate-400">Holistic rating based on formatting clarity and description impact.</p>
              </div>
              <div className="h-16 w-16 shrink-0 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                <Star className="h-8 w-8 fill-current" />
              </div>
            </div>

            {/* ATS Compatibility */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-6 glass-panel flex items-center justify-between">
              <div>
                <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">ATS Match Score</div>
                <div className="text-3xl font-bold font-heading text-white">
                  <span className={getATSColor(result.ats_score)}>{result.ats_score}%</span>
                </div>
                <p className="mt-2 text-xs text-slate-400">Estimated parsing compatibility based on headers and core keywords.</p>
              </div>
              <div className="h-16 w-16 shrink-0 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                <Target className="h-8 w-8" />
              </div>
            </div>
          </div>

          {/* Section Grade Cards */}
          <div>
            <h3 className="text-lg font-bold text-white mb-4 flex items-center space-x-2">
              <BarChart2 className="h-5 w-5 text-indigo-400" />
              <span>Section Breakdown Grade</span>
            </h3>
            <div className="grid gap-4 sm:grid-cols-2">
              {Object.entries(result.sections).map(([name, detail]) => (
                <div key={name} className="rounded-xl border border-slate-800/80 bg-slate-900/10 p-5 glass-panel">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-semibold capitalize text-slate-200">{name}</span>
                    <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${getScoreColor(detail.score)}`}>
                      {detail.score.toFixed(1)} / 10
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-normal">{detail.feedback}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Strengths, Weaknesses, Recommendations Panels */}
          <div className="grid gap-6 lg:grid-cols-3">
            {/* Strengths */}
            <div className="rounded-xl border border-emerald-500/10 bg-emerald-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-emerald-400 flex items-center space-x-2 mb-4">
                <CheckCircle className="h-5 w-5 shrink-0" />
                <span>Core Strengths</span>
              </h4>
              <ul className="space-y-3">
                {result.strengths.map((str, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-emerald-500 shrink-0 font-bold">•</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Weaknesses */}
            <div className="rounded-xl border border-rose-500/10 bg-rose-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-rose-400 flex items-center space-x-2 mb-4">
                <AlertTriangle className="h-5 w-5 shrink-0" />
                <span>Areas of Concern</span>
              </h4>
              <ul className="space-y-3">
                {result.weaknesses.map((weak, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-rose-500 shrink-0 font-bold">•</span>
                    <span>{weak}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Recommendations */}
            <div className="rounded-xl border border-indigo-500/10 bg-indigo-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-indigo-400 flex items-center space-x-2 mb-4">
                <Lightbulb className="h-5 w-5 shrink-0" />
                <span>ATS Tailoring Steps</span>
              </h4>
              <ul className="space-y-3">
                {result.recommendations.map((rec, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-indigo-400 shrink-0 font-bold">•</span>
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Reset Action */}
          <div className="flex justify-center mt-6">
            <button
              onClick={handleReset}
              className="flex items-center space-x-2 rounded-xl border border-slate-800 bg-slate-900/60 px-6 py-3 text-sm font-semibold text-slate-300 hover:bg-slate-900 hover:text-white transition duration-200"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Analyze Another Resume</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
