
import argparse
import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from ai_analyzer.prompts import FAILURE_ANALYSIS_PROMPT
from ai_analyzer.analysis_schema import FailureAnalysis


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_FAILURE_FILE = PROJECT_ROOT / "ai_analyzer" / "sample_failure.json"

load_dotenv(PROJECT_ROOT / ".env")


def analyze_failure(failure_file: Path) -> FailureAnalysis:
    """Analyze a pytest failure using the OpenAI API."""

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY not found. Check your environment configuration."
        )

    with failure_file.open("r", encoding="utf-8") as file:
        failure_data = json.load(file)

    client = OpenAI()

    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=FAILURE_ANALYSIS_PROMPT,
        input=json.dumps(failure_data, indent=2),
        text_format=FailureAnalysis,
    )

    analysis = response.output_parsed

    if analysis is None:
        raise RuntimeError("The AI did not return a parsed analysis.")

    return analysis


def save_analysis(
    analysis: FailureAnalysis,
    failure_file: Path,
) -> Path:
    """Save the structured AI analysis as a JSON file."""

    output_dir = PROJECT_ROOT / "artifacts" / "ai-analysis"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{failure_file.stem}-analysis.json"

    output_file.write_text(
        analysis.model_dump_json(indent=2),
        encoding="utf-8",
    )

    return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyze a pytest failure using AI."
    )

    parser.add_argument(
        "--file",
        type=Path,
        default=DEFAULT_FAILURE_FILE,
        help="Path to the failure JSON file.",
    )

    args = parser.parse_args()
    failure_file = args.file.resolve()

    if not failure_file.is_file():
        raise FileNotFoundError(
            f"Failure JSON file not found: {failure_file}"
        )

    analysis = analyze_failure(failure_file)

    saved_path = save_analysis(analysis, failure_file)

    print("\n========== AI TEST FAILURE ANALYSIS ==========\n")
    print(analysis.model_dump_json(indent=2))
    print(f"\nAI analysis saved to: {saved_path}")
