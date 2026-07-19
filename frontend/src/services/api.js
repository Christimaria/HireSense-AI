/**
 * HireSense AI — Frontend API Service Layer
 * 
 * Provides functions to connect to backend FastAPI endpoints.
 * Handles Server-Sent Events (SSE) streaming for POST requests.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * Core helper to consume POST SSE streams.
 * 
 * @param {string} endpoint - API path relative to API_BASE_URL (e.g. '/resume/review')
 * @param {object} payload - JSON request body
 * @param {function} onChunk - Callback for intermediate text chunks
 * @param {function} onResult - Callback for final structured JSON object (if available)
 * @param {function} onError - Callback for errors
 */
export async function streamPost(endpoint, payload, onChunk, onResult, onError) {
  try {
    const url = `${API_BASE_URL}${endpoint}`;
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      let errorMessage = `Server error: ${response.status}`;
      try {
        const errorJson = await response.json();
        errorMessage = errorJson.detail || errorMessage;
      } catch (e) {
        // Fallback if not JSON
      }
      throw new Error(errorMessage);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buffer = '';

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      // Decode and add to buffer
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');

      // Keep the last partial line in buffer
      buffer = lines.pop() || '';

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;

        if (trimmed.startsWith('data: ')) {
          const dataStr = trimmed.slice(6).trim();

          if (dataStr === '[DONE]') {
            continue; // End of stream
          }

          try {
            const parsed = JSON.parse(dataStr);
            if (parsed.type === 'chunk') {
              if (onChunk) onChunk(parsed.content);
            } else if (parsed.type === 'result') {
              if (onResult) onResult(parsed.content);
            } else if (parsed.type === 'error') {
              throw new Error(parsed.content);
            }
          } catch (err) {
            console.error('Failed to parse SSE line:', err, trimmed);
          }
        }
      }
    }
  } catch (error) {
    console.error(`Error streaming from ${endpoint}:`, error);
    if (onError) {
      onError(error.message || 'An unexpected connection error occurred.');
    }
  }
}

/**
 * Service methods mapped directly to backend endpoints
 */
export const api = {
  /**
   * Reviews a resume (returns structured analysis: overall score, ATS score, section scores, strengths, recommendations)
   */
  reviewResume: (resumeText, targetRole, onChunk, onResult, onError) => {
    return streamPost(
      '/resume/review',
      { resume_text: resumeText, target_role: targetRole || null },
      onChunk,
      onResult,
      onError
    );
  },

  /**
   * Generates next interview question (returns raw text question stream)
   */
  getInterviewQuestion: (config, onChunk, onError) => {
    // Config matches InterviewQuestionRequest: role, experience_level, interview_type, question_number, total_questions, conversation_history
    return streamPost(
      '/interview/question',
      config,
      onChunk,
      null, // This endpoint only streams text chunks
      onError
    );
  },

  /**
   * Evaluates individual answer (returns evaluation result: score, strengths, weaknesses, improved answer, tips)
   */
  evaluateAnswer: (payload, onChunk, onResult, onError) => {
    // Payload matches EvaluationRequest: question, answer, role, experience_level, interview_type
    return streamPost(
      '/evaluation/answer',
      payload,
      onChunk,
      onResult,
      onError
    );
  },

  /**
   * Generates final dashboard assessment (returns dashboard details: grade, overall score, strengths, weaknesses, next steps, readiness, category scores)
   */
  generateDashboard: (payload, onChunk, onResult, onError) => {
    // Payload matches DashboardRequest: role, experience_level, interview_type, session_turns
    return streamPost(
      '/evaluation/dashboard',
      payload,
      onChunk,
      onResult,
      onError
    );
  },

  /**
   * Generates customized career roadmap (returns roadmap details: weekly plan, skill gaps, learning resources, milestones)
   */
  generateRoadmap: (skills, targetRole, timeline, onChunk, onResult, onError) => {
    return streamPost(
      '/roadmap/generate',
      { current_skills: skills, target_role: targetRole, timeline },
      onChunk,
      onResult,
      onError
    );
  }
};
