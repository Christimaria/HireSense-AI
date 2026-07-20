"""
HireSense AI — Gemini Model Lister Utility Script

Lists all available models accessible with your GEMINI_API_KEY using the
official google-genai SDK, highlights models that support generateContent,
and prints the recommended model ID for GEMINI_MODEL.
"""

import os
import sys
from dotenv import load_dotenv
from google import genai

# Attempt to load .env from backend/.env or root .env
load_dotenv()
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ ERROR: GEMINI_API_KEY environment variable is not set.")
    print("Please set GEMINI_API_KEY in your environment or in backend/.env file.")
    sys.exit(1)

try:
    client = genai.Client(api_key=api_key)
    print("🔍 Querying Google GenAI API for available models...\n")
    
    models_pager = client.models.list()
    models = list(models_pager)
    
    if not models:
        print("⚠️ No models returned by the API.")
        sys.exit(0)

    print(f"{'Model ID':<45} | {'Supports generateContent':<25}")
    print("=" * 75)

    recommended = None
    flash_models = []

    for m in models:
        # Get raw model name (e.g. 'models/gemini-2.5-flash-lite' or 'gemini-1.5-flash')
        raw_name = getattr(m, "name", str(m))
        model_id = raw_name[7:] if raw_name.startswith("models/") else raw_name
        
        # Determine if generateContent is supported
        supported_methods = getattr(m, "supported_generation_methods", None) or getattr(m, "supported_actions", None) or []
        
        supports_gen = False
        if supported_methods:
            supports_gen = any("generateContent" in str(method) for method in supported_methods)
        else:
            # Fallback heuristic for standard text/chat models
            supports_gen = any(k in model_id for k in ["flash", "pro", "gemini"])

        status = "✅ YES" if supports_gen else "❌ No"
        print(f"{model_id:<45} | {status:<25}")

        if supports_gen:
            if "flash" in model_id:
                flash_models.append(model_id)

    print("=" * 75)

    # Pick best recommended model
    if flash_models:
        # Prefer lite / flash model if present
        recommended = flash_models[0]
    elif models:
        recommended = getattr(models[0], "name", str(models[0])).replace("models/", "")

    print(f"\n✨ Recommended GEMINI_MODEL setting for your .env: {recommended}\n")

except Exception as err:
    print(f"❌ Failed to list models: {err}")
    sys.exit(1)
