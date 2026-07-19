import { useState } from 'react';
import { api } from '../services/api';
import { 
  Bot, Award, ChevronRight, MessageSquare, AlertTriangle, 
  HelpCircle, Send, CheckCircle, RefreshCw, Star, Play, 
  BookOpen, Sparkles, AlertCircle, TrendingUp, Compass, Loader2
} from 'lucide-react';

export default function Interview() {
  // Session Stages: 'SETUP' | 'QUESTION_STREAMING' | 'WAITING_FOR_ANSWER' | 'EVALUATING_ANSWER' | 'EVALUATION_RESULT' | 'DASHBOARD_STREAMING' | 'DASHBOARD_RESULT'
  const [stage, setStage] = useState('SETUP');

  // Configuration State
  const [role, setRole] = useState('Software Engineer');
  const [experienceLevel, setExperienceLevel] = useState('Junior');
  const [interviewType, setInterviewType] = useState('Technical');
  const [totalQuestions, setTotalQuestions] = useState(5);

  // Active Session State
  const [currentQuestionNumber, setCurrentQuestionNumber] = useState(1);
  const [activeQuestion, setActiveQuestion] = useState('');
  const [candidateAnswer, setCandidateAnswer] = useState('');
  const [activeEvaluation, setActiveEvaluation] = useState(null);
  const [conversationHistory, setConversationHistory] = useState([]); // Array of { question, answer }
  const [streamedText, setStreamedText] = useState(''); // Raw stream logger
  const [error, setError] = useState('');

  // Dashboard Result State
  const [dashboardResult, setDashboardResult] = useState(null);

  // Setup options matching backend enums
  const roles = [
    'Software Engineer', 'Frontend', 'Backend', 'Full Stack', 
    'Data Analyst', 'Data Scientist', 'AI Engineer', 'DevOps', 
    'Cybersecurity', 'HR'
  ];
  const experienceLevels = ['Fresher', 'Junior', 'Mid', 'Senior'];
  const interviewTypes = ['Technical', 'Behavioral', 'HR'];

  // Start interview - trigger first question
  const handleStartInterview = () => {
    setError('');
    setStage('QUESTION_STREAMING');
    setActiveQuestion('');
    setCandidateAnswer('');
    setConversationHistory([]);
    setCurrentQuestionNumber(1);
    fetchNextQuestion(1, []);
  };

  // Fetch next question from AI
  const fetchNextQuestion = (qNumber, history) => {
    setStage('QUESTION_STREAMING');
    setActiveQuestion('');
    setStreamedText('');
    setError('');

    const payload = {
      role,
      experience_level: experienceLevel,
      interview_type: interviewType,
      question_number: qNumber,
      total_questions: totalQuestions,
      conversation_history: history
    };

    api.getInterviewQuestion(
      payload,
      // onChunk
      (chunk) => {
        setActiveQuestion((prev) => prev + chunk);
      },
      // onError
      (errMessage) => {
        setError(errMessage);
        setStage('WAITING_FOR_ANSWER'); // fallback so they can retry or reset
      }
    );
  };

  // Submit Answer for evaluation
  const handleSubmitAnswer = (e) => {
    e.preventDefault();
    if (!candidateAnswer.trim() || candidateAnswer.trim().length < 10) {
      setError('Please provide a slightly more detailed response (minimum 10 characters).');
      return;
    }

    setError('');
    setStage('EVALUATING_ANSWER');
    setStreamedText('');
    setActiveEvaluation(null);

    const payload = {
      question: activeQuestion,
      answer: candidateAnswer,
      role,
      experience_level: experienceLevel,
      interview_type: interviewType
    };

    api.evaluateAnswer(
      payload,
      // onChunk
      (chunk) => {
        setStreamedText((prev) => prev + chunk);
      },
      // onResult
      (result) => {
        setActiveEvaluation(result);
        setStage('EVALUATION_RESULT');
      },
      // onError
      (errMessage) => {
        setError(errMessage);
        setStage('WAITING_FOR_ANSWER'); // Fallback
      }
    );
  };

  // Move to next question or complete interview
  const handleNextStep = () => {
    // Save current Q&A turn to history
    const updatedHistory = [
      ...conversationHistory,
      { question: activeQuestion, answer: candidateAnswer }
    ];
    setConversationHistory(updatedHistory);
    setCandidateAnswer('');
    setActiveEvaluation(null);

    if (currentQuestionNumber < totalQuestions) {
      const nextNum = currentQuestionNumber + 1;
      setCurrentQuestionNumber(nextNum);
      fetchNextQuestion(nextNum, updatedHistory);
    } else {
      // Trigger dashboard generation
      generateFinalDashboard(updatedHistory);
    }
  };

  // Generate holistic performance dashboard
  const generateFinalDashboard = (history) => {
    setStage('DASHBOARD_STREAMING');
    setStreamedText('');
    setDashboardResult(null);
    setError('');

    const payload = {
      role,
      experience_level: experienceLevel,
      interview_type: interviewType,
      session_turns: history
    };

    api.generateDashboard(
      payload,
      // onChunk
      (chunk) => {
        setStreamedText((prev) => prev + chunk);
      },
      // onResult
      (result) => {
        setDashboardResult(result);
        setStage('DASHBOARD_RESULT');
      },
      // onError
      (errMessage) => {
        setError(errMessage);
        setStage('EVALUATION_RESULT'); // fallback
      }
    );
  };

  // Reset interview session
  const handleReset = () => {
    setStage('SETUP');
    setConversationHistory([]);
    setActiveQuestion('');
    setCandidateAnswer('');
    setActiveEvaluation(null);
    setDashboardResult(null);
    setStreamedText('');
    setError('');
  };

  return (
    <div className="mx-auto max-w-4xl px-4 py-12 sm:px-6 lg:px-8">
      {/* Page Title */}
      <div className="mb-10 text-center">
        <h1 className="text-3xl font-extrabold text-white sm:text-4xl">
          Conversational <span className="text-gradient">Mock Interview</span>
        </h1>
        <p className="mx-auto mt-2 max-w-xl text-sm text-slate-400">
          Tailored to your career path. Receive immediate score breakdowns, detailed model answers, and a holistic readiness dashboard.
        </p>
      </div>

      {error && (
        <div className="mb-6 rounded-xl border border-rose-500/20 bg-rose-500/10 p-4 text-sm text-rose-400 flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 shrink-0" />
          <div>{error}</div>
        </div>
      )}

      {/* STAGE 1: SETUP FORM */}
      {stage === 'SETUP' && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 sm:p-8 glass-panel animate-fade-in">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center space-x-2">
            <Bot className="h-5 w-5 text-indigo-400" />
            <span>Configure Interview Settings</span>
          </h2>

          <div className="grid gap-6 sm:grid-cols-2">
            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Target Job Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 focus:border-indigo-500/50 outline-none transition"
              >
                {roles.map((r) => (
                  <option key={r} value={r}>{r}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Seniority / Experience Level</label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 focus:border-indigo-500/50 outline-none transition"
              >
                {experienceLevels.map((lvl) => (
                  <option key={lvl} value={lvl}>{lvl}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Interview Domain</label>
              <select
                value={interviewType}
                onChange={(e) => setInterviewType(e.target.value)}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 focus:border-indigo-500/50 outline-none transition"
              >
                {interviewTypes.map((t) => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">Total Questions</label>
              <select
                value={totalQuestions}
                onChange={(e) => setTotalQuestions(Number(e.target.value))}
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-100 focus:border-indigo-500/50 outline-none transition"
              >
                <option value={3}>3 Questions (Fast Run)</option>
                <option value={5}>5 Questions (Standard)</option>
                <option value={10}>10 Questions (Complete Practice)</option>
              </select>
            </div>
          </div>

          <button
            onClick={handleStartInterview}
            className="w-full mt-8 flex items-center justify-center space-x-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 py-4 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition duration-200 cursor-pointer"
          >
            <Play className="h-4 w-4 fill-current" />
            <span>Launch Mock Session</span>
          </button>
        </div>
      )}

      {/* STAGE 2: QUESTION STREAMING */}
      {stage === 'QUESTION_STREAMING' && (
        <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-8 glass-panel text-center animate-fade-in">
          <div className="flex flex-col items-center justify-center py-10">
            <Loader2 className="h-10 w-10 text-indigo-500 animate-spin mb-4" />
            <h3 className="font-heading text-lg font-bold text-white mb-2">
              Generating Question {currentQuestionNumber} of {totalQuestions}
            </h3>
            <p className="text-sm text-slate-400 max-w-sm mb-6">
              Tailoring technical question with context to role {role} ({experienceLevel} level).
            </p>
          </div>

          {activeQuestion && (
            <div className="text-left bg-slate-950 p-6 rounded-xl border border-slate-800 text-slate-200 font-medium leading-relaxed shadow-inner">
              <span className="text-[10px] text-indigo-400 uppercase font-mono block mb-2">Incoming Question</span>
              <p className="whitespace-pre-wrap">{activeQuestion}</p>
            </div>
          )}
        </div>
      )}

      {/* STAGE 3: WAITING FOR ANSWER */}
      {stage === 'WAITING_FOR_ANSWER' && (
        <div className="space-y-6 animate-fade-in">
          {/* Question card */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel">
            <div className="flex items-center justify-between text-xs text-indigo-400 font-mono mb-4 uppercase tracking-wider">
              <span>Question {currentQuestionNumber} of {totalQuestions}</span>
              <span className="px-2 py-0.5 rounded bg-slate-950 border border-slate-850">{interviewType} Round</span>
            </div>
            <p className="text-base font-semibold text-white leading-relaxed">{activeQuestion}</p>
          </div>

          {/* Answer box */}
          <form onSubmit={handleSubmitAnswer} className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel space-y-4">
            <div>
              <label htmlFor="candidate-answer" className="block text-sm font-semibold text-slate-200 mb-2">
                Your Answer
              </label>
              <textarea
                id="candidate-answer"
                required
                rows={8}
                value={candidateAnswer}
                onChange={(e) => setCandidateAnswer(e.target.value)}
                placeholder="Type your structured answer here. Include your technical rationale, examples, or frameworks you'd refer to..."
                className="w-full rounded-xl border border-slate-800 bg-slate-950 px-4 py-3 text-sm text-slate-300 placeholder-slate-600 focus:border-indigo-500/50 outline-none transition"
              />
              <div className="mt-1 flex items-center justify-between text-xs text-slate-500">
                <span>Minimum 10 characters. Tip: Be structured (Star method).</span>
                <span>{candidateAnswer.length} chars</span>
              </div>
            </div>

            <button
              type="submit"
              className="w-full flex items-center justify-center space-x-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 py-3.5 text-sm font-semibold text-white shadow-lg transition duration-200 cursor-pointer"
            >
              <Send className="h-4 w-4" />
              <span>Submit Answer for Review</span>
            </button>
          </form>
        </div>
      )}

      {/* STAGE 4: EVALUATING ANSWER */}
      {stage === 'EVALUATING_ANSWER' && (
        <div className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/30 p-8 glass-panel text-center animate-fade-in">
          <div className="flex flex-col items-center justify-center py-8">
            <Loader2 className="h-10 w-10 text-indigo-500 animate-spin mb-4" />
            <h3 className="font-heading text-lg font-bold text-white mb-2">Evaluating Answer Details...</h3>
            <p className="text-sm text-slate-400 max-w-sm">
              Gemini is assessing your answer metrics, finding code/system concept gaps, and scoring relevance.
            </p>
          </div>

          {streamedText && (
            <div className="text-left bg-slate-950 rounded-xl border border-slate-800">
              <div className="px-4 py-2 border-b border-slate-800 text-[10px] uppercase font-mono tracking-widest text-slate-500 flex justify-between items-center">
                <span>Evaluation Feed Stream</span>
                <span className="animate-pulse text-indigo-400">Live Compilation</span>
              </div>
              <div className="max-h-40 overflow-y-auto p-4 text-[11px] font-mono text-purple-300 leading-relaxed whitespace-pre-wrap">
                {streamedText}
              </div>
            </div>
          )}
        </div>
      )}

      {/* STAGE 5: EVALUATION RESULT */}
      {stage === 'EVALUATION_RESULT' && activeEvaluation && (
        <div className="space-y-6 animate-slide-up">
          {/* Question Summary */}
          <div className="rounded-xl border border-slate-800 bg-slate-950 p-5">
            <span className="text-[10px] text-indigo-400 font-mono uppercase tracking-wider block mb-1">Question</span>
            <p className="text-sm text-slate-300 font-medium">{activeQuestion}</p>
          </div>

          {/* Score & Highlights */}
          <div className="grid gap-6 md:grid-cols-3">
            {/* Score Card */}
            <div className="rounded-xl border border-slate-800 bg-slate-900/20 p-5 glass-panel flex flex-col justify-between">
              <div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500">Answer Score</span>
                <div className="text-4xl font-bold font-heading text-white mt-1">
                  {activeEvaluation.score.toFixed(1)} <span className="text-slate-600 text-xs">/ 10</span>
                </div>
              </div>
              <div className="mt-4 flex items-center space-x-1.5 text-xs text-indigo-400 font-semibold">
                <Star className="h-4 w-4 fill-current" />
                <span>Immediate Feedback Grade</span>
              </div>
            </div>

            {/* Strengths Card */}
            <div className="rounded-xl border border-emerald-500/10 bg-emerald-500/5 p-5 glass-panel md:col-span-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 flex items-center space-x-1.5 mb-3">
                <CheckCircle className="h-4 w-4" />
                <span>Good Details Highlighted</span>
              </h4>
              <ul className="space-y-2">
                {activeEvaluation.strengths.map((str, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-1.5">
                    <span className="text-emerald-500 shrink-0 font-bold">•</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="grid gap-6 md:grid-cols-2">
            {/* Weaknesses Card */}
            <div className="rounded-xl border border-rose-500/10 bg-rose-500/5 p-5 glass-panel">
              <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 flex items-center space-x-1.5 mb-3">
                <AlertTriangle className="h-4 w-4" />
                <span>Inaccuracies or Gaps</span>
              </h4>
              <ul className="space-y-2">
                {activeEvaluation.weaknesses.map((weak, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-1.5">
                    <span className="text-rose-500 shrink-0 font-bold">•</span>
                    <span>{weak}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Tips Card */}
            <div className="rounded-xl border border-indigo-500/10 bg-indigo-500/5 p-5 glass-panel">
              <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-400 flex items-center space-x-1.5 mb-3">
                <BookOpen className="h-4 w-4" />
                <span>Preparation Tips</span>
              </h4>
              <ul className="space-y-2">
                {activeEvaluation.tips.map((tip, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-1.5">
                    <span className="text-indigo-400 shrink-0 font-bold">•</span>
                    <span>{tip}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Model Answer (Expanded by default for high readability) */}
          <div className="rounded-xl border border-slate-800 bg-slate-900/30 p-5 glass-panel">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200 flex items-center space-x-1.5 mb-3">
              <Sparkles className="h-4 w-4 text-amber-400" />
              <span>Model Answer Blueprint</span>
            </h4>
            <div className="bg-slate-950 p-4 rounded-lg border border-slate-850 text-xs font-mono text-slate-300 leading-relaxed whitespace-pre-wrap">
              {activeEvaluation.improved_answer}
            </div>
          </div>

          {/* Proceed Button */}
          <button
            onClick={handleNextStep}
            className="w-full flex items-center justify-center space-x-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 py-4 text-sm font-semibold text-white shadow-lg transition duration-200 cursor-pointer"
          >
            <span>
              {currentQuestionNumber < totalQuestions 
                ? `Proceed to Question ${currentQuestionNumber + 1}` 
                : 'Finish & Generate Platform Dashboard'}
            </span>
            <ChevronRight className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* STAGE 6: DASHBOARD STREAMING */}
      {stage === 'DASHBOARD_STREAMING' && (
        <div className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900/30 p-8 glass-panel text-center animate-fade-in">
          <div className="flex flex-col items-center justify-center py-8">
            <Loader2 className="h-10 w-10 text-indigo-500 animate-spin mb-4" />
            <h3 className="font-heading text-lg font-bold text-white mb-2">Analyzing Session Performance...</h3>
            <p className="text-sm text-slate-400 max-w-sm">
              Gemini is evaluating your total answers, scoring specific skill sectors, and grading overall readiness.
            </p>
          </div>

          {streamedText && (
            <div className="text-left bg-slate-950 rounded-xl border border-slate-800">
              <div className="px-4 py-2 border-b border-slate-800 text-[10px] uppercase font-mono tracking-widest text-slate-500 flex justify-between items-center">
                <span>Dashboard Data Stream</span>
                <span className="animate-pulse text-indigo-400 font-bold">Assembling Metrics</span>
              </div>
              <div className="max-h-40 overflow-y-auto p-4 text-[11px] font-mono text-cyan-300 leading-relaxed whitespace-pre-wrap">
                {streamedText}
              </div>
            </div>
          )}
        </div>
      )}

      {/* STAGE 7: DASHBOARD RESULT */}
      {stage === 'DASHBOARD_RESULT' && dashboardResult && (
        <div className="space-y-8 animate-slide-up">
          {/* Top banner scores */}
          <div className="grid gap-6 sm:grid-cols-3">
            {/* Overall Score */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel flex flex-col justify-between">
              <div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500">Holistic Score</span>
                <div className="text-4xl font-extrabold font-heading text-white mt-1">
                  {dashboardResult.overall_score.toFixed(1)} <span className="text-slate-600 text-xs">/ 10</span>
                </div>
              </div>
              <span className="mt-4 text-xs text-indigo-400 font-medium">Platform Session Score</span>
            </div>

            {/* Performance Grade */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel flex flex-col justify-between">
              <div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500">Performance Grade</span>
                <div className="text-4xl font-extrabold font-heading text-emerald-400 mt-1">
                  {dashboardResult.performance_grade}
                </div>
              </div>
              <span className="mt-4 text-xs text-slate-400">Preparation grade tier</span>
            </div>

            {/* Readiness assessment */}
            <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel flex flex-col justify-between sm:col-span-1">
              <div>
                <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500">Readiness Assessment</span>
                <div className="text-sm font-semibold text-slate-200 mt-2 leading-snug">
                  {dashboardResult.interview_readiness}
                </div>
              </div>
              <span className="mt-4 text-xs text-cyan-400 font-semibold flex items-center space-x-1">
                <TrendingUp className="h-3.5 w-3.5" />
                <span>Holistic readiness level</span>
              </span>
            </div>
          </div>

          {/* Category Scores breakdown */}
          <div className="rounded-2xl border border-slate-800 bg-slate-900/20 p-6 glass-panel">
            <h3 className="font-heading text-base font-bold text-white mb-6 flex items-center space-x-2">
              <Award className="h-5 w-5 text-indigo-400" />
              <span>Skill Categories Performance</span>
            </h3>
            <div className="grid gap-4 sm:grid-cols-2">
              {Object.entries(dashboardResult.category_scores).map(([category, rating]) => (
                <div key={category} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs font-semibold text-slate-300 capitalize">
                    <span>{category}</span>
                    <span>{rating.toFixed(1)} / 10</span>
                  </div>
                  <div className="h-2 w-full rounded-full bg-slate-950 overflow-hidden border border-slate-850">
                    <div 
                      className="h-full bg-gradient-to-r from-indigo-500 to-indigo-600 rounded-full" 
                      style={{ width: `${rating * 10}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Strengths & Weaknesses */}
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-xl border border-emerald-500/10 bg-emerald-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-emerald-400 flex items-center space-x-2 mb-4">
                <CheckCircle className="h-5 w-5" />
                <span>Session Strengths</span>
              </h4>
              <ul className="space-y-3">
                {dashboardResult.strengths.map((str, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-emerald-500 shrink-0 font-bold">•</span>
                    <span>{str}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-xl border border-rose-500/10 bg-rose-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-rose-400 flex items-center space-x-2 mb-4">
                <AlertTriangle className="h-5 w-5" />
                <span>Demonstrated Gaps</span>
              </h4>
              <ul className="space-y-3">
                {dashboardResult.weaknesses.map((weak, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-rose-500 shrink-0 font-bold">•</span>
                    <span>{weak}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Improvement topics and actions */}
          <div className="grid gap-6 md:grid-cols-2">
            <div className="rounded-xl border border-indigo-500/10 bg-indigo-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-indigo-400 flex items-center space-x-2 mb-4">
                <Compass className="h-5 w-5" />
                <span>Key Improvement Areas</span>
              </h4>
              <ul className="space-y-3">
                {dashboardResult.improvement_areas.map((area, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-indigo-400 shrink-0 font-bold">•</span>
                    <span>{area}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-xl border border-cyan-500/10 bg-cyan-500/5 p-6 glass-panel">
              <h4 className="font-heading font-bold text-cyan-400 flex items-center space-x-2 mb-4">
                <TrendingUp className="h-5 w-5" />
                <span>Next Preparation Steps</span>
              </h4>
              <ul className="space-y-3">
                {dashboardResult.next_steps.map((step, idx) => (
                  <li key={idx} className="text-xs text-slate-300 leading-relaxed flex items-start space-x-2">
                    <span className="text-cyan-400 shrink-0 font-bold">•</span>
                    <span>{step}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Actions */}
          <div className="flex justify-center pt-4">
            <button
              onClick={handleReset}
              className="flex items-center space-x-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/25 transition duration-200 cursor-pointer"
            >
              <RefreshCw className="h-4 w-4" />
              <span>Launch a New Session</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
