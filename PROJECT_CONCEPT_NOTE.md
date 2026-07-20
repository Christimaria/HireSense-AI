# Project Concept Note: HireSense AI

> **Vibe Coding Masterclass Series — Capstone Project Submission**  
> **Application Name:** HireSense AI — Intelligent Career Readiness & Interview Co-Pilot  
> **Developer:** Student Submission  
> **Live Application URL:** https://hire-sense-ai-delta.vercel.app  
> **Backend API URL:** https://hiresense-ai-backend-ndq3.onrender.com/api/v1  

---

## 1. Executive Summary & Problem Statement

### 1.1 The Challenge
Preparing for technical and HR job interviews is often stressful, fragmented, and lacks real-time, objective feedback. Job candidates consistently encounter three major barriers:
* **Unrealistic Practice:** Static interview prep lists do not simulate dynamic, multi-turn technical conversations.
* **ATS Resume Rejection:** Resumes are frequently filtered out by Automated Tracking Systems (ATS) due to formatting mismatches or missing role-specific keywords.
* **Unstructured Learning Paths:** Candidates lack personalized, week-by-week actionable roadmaps tailored to their specific skill gaps and targeted roles.

### 1.2 The Solution
**HireSense AI** is an end-to-end, next-generation career readiness co-pilot powered by **Google Gemini AI** (`gemini-1.5-flash`). It provides:
1. **Real-time AI Mock Interviews:** Multi-turn practice with progressive token streaming.
2. **ATS Resume Calibration:** Section-by-section auditing and keyword matching.
3. **Holistic Performance Dashboards:** Multi-category scoring across Technical Depth, Communication, and Problem Solving.
4. **Custom Weekly Roadmaps:** Actionable skill-gap learning pathways tailored to candidate timelines.

---

## 2. Target Audience & Primary Use Cases

| Target Audience | Primary Use Case | Key Benefit Received |
| :--- | :--- | :--- |
| **Students & Fresh Graduates** | Preparing for entry-level tech & HR interviews | Instant mock practice without needing human interviewers |
| **Experienced Engineers** | Transitioning into Senior/Lead/Specialized roles | Deep technical metric evaluation and targeted trade-off analysis |
| **Career Switchers** | Up-skilling for software engineering / data roles | Customized week-by-week learning pathway with project milestones |

---

## 3. LLM Model & API Architecture

* **AI SDK:** Official `google-genai` Python SDK (`v2.12.1`)
* **Primary LLM Model:** Google Gemini `gemini-1.5-flash`
* **Streaming Transport:** Server-Sent Events (SSE) streaming via FastAPI `StreamingResponse`
* **Security & Privacy Guarantee:** Zero client-side API key exposure; all credentials stored in server environment variables; zero persistent storage of candidate resumes.

---

## 4. Key Application Features

### Feature 1: Interactive AI Mock Interview Suite
* Dynamic role, experience level, and interview type selection (Technical, Behavioral, HR).
* Multi-turn conversation tracking with real-time SSE token streaming for progressive typing animations.

### Feature 2: Live Answer Evaluation & Grading
* Detailed feedback per question: Score (0.0–10.0), key strengths, identified gaps, and rewritten "Gold Standard" answers.

### Feature 3: Holistic Performance Dashboard
* Session-wide analytics across Technical Depth, Communication Clarity, and Problem Solving.
* Overall readiness grade (e.g. "Industry Ready", "Needs Practice") with actionable next steps.

### Feature 4: Resume ATS Scanner & Calibrator
* Instant plain-text resume auditing against targeted job titles.
* Section scores, ATS readability metrics, weakness identification, and tailoring recommendations.

### Feature 5: Week-by-Week Career Roadmap Generator
* Custom learning path creation matching current candidate skills against target role requirements.
* Hands-on weekly tasks, practical projects, and verification milestones.

---

## 5. Expected Outcomes & User Experience

Candidates experience a responsive web application featuring dark-mode aesthetic styling, micro-animations, and real-time streaming feedback.

* **5x Faster Interview Preparation:** Instant, repeatable practice sessions.
* **Measurable ATS Resume Score Improvements:** Clear formatting and keyword guidance.
* **Actionable Learning Pathways:** Structured weekly tasks eliminate career pivot ambiguity.
