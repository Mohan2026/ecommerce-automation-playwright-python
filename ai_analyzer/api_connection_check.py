
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENAI_API_KEY was not found. Check your project's .env file."
    )

client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-6-luna",
        input="Reply with exactly: API connection successful.",
        max_output_tokens=30,
    )

    print("API request successful.")
    print("Model response:", response.output_text)

except Exception as error:
    print(f"API request failed: {type(error).__name__}: {error}")
