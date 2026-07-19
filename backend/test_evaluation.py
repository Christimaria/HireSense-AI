"""
HireSense AI — Test script to verify POST /api/v1/evaluation/answer
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


def test_evaluation_stream():
    client = TestClient(app)

    payload = {
        "question": "What is the difference between event.preventDefault() and event.stopPropagation()?",
        "answer": (
            "event.preventDefault() stops the default browser action from happening, like following a link. "
            "event.stopPropagation() stops the event from bubbling up the DOM tree to parent elements."
        ),
        "role": "Frontend",
        "experience_level": "Junior",
        "interview_type": "Technical",
    }

    print("Sending POST /api/v1/evaluation/answer request...")

    # Read streamed lines
    with client.stream("POST", "/api/v1/evaluation/answer", json=payload) as r:
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
    test_evaluation_stream()
