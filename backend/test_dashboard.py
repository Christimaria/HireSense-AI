"""
HireSense AI — Test script to verify POST /api/v1/evaluation/dashboard
"""

import sys
import os
from fastapi.testclient import TestClient

# Add current folder to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load env variables
from dotenv import load_dotenv
load_dotenv()

from app.main import app


def test_dashboard_stream():
    client = TestClient(app)

    payload = {
        "role": "Frontend",
        "experience_level": "Junior",
        "interview_type": "Technical",
        "session_turns": [
            {
                "question": "Explain event delegation in JavaScript.",
                "answer": (
                    "Event delegation attaches a single event listener to a parent element rather than attaching "
                    "listeners to individual children. The event bubbles up from child to parent, triggering the parent listener."
                ),
            },
            {
                "question": "What is the difference between event.preventDefault() and event.stopPropagation()?",
                "answer": (
                    "preventDefault stops default browser behavior like following a link. "
                    "stopPropagation stops event bubbling to parent DOM elements."
                ),
            },
            {
                "question": "How do you optimize page load performance for a heavy React application?",
                "answer": (
                    "Use lazy loading with Suspense, code splitting with Dynamic imports, "
                    "optimize image sizes, and avoid inline arrow functions in render if possible."
                ),
            },
        ],
    }

    print("Sending POST /api/v1/evaluation/dashboard request...")

    # Read streamed lines
    with client.stream("POST", "/api/v1/evaluation/dashboard", json=payload) as r:
        if r.status_code != 200:
            print(f"Error: status code {r.status_code}")
            print(r.text)
            sys.exit(1)

        print("Response received, streaming SSE events:")
        print("=" * 60)
        for line in r.iter_lines():
            if line:
                print(line)
        print("=" * 60)


if __name__ == "__main__":
    test_dashboard_stream()
