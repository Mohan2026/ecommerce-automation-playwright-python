
import json
from pathlib import Path
from datetime import datetime


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FAILURES_DIR = PROJECT_ROOT / "artifacts" / "failures"


def save_failure_data(
    test_name: str,
    phase: str,
    error_message: str,
    traceback_text: str,
) -> Path:
    """Save actual pytest failure details as a JSON file."""

    FAILURES_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

    failure_data = {
        "test_name": test_name,
        "status": "failed",
        "phase": phase,
        "error_type": "Unknown",
        "error_message": error_message,
        "traceback": traceback_text,
        "application": "SauceDemo",
        "browser": "chromium",
        "timestamp": timestamp,
    }

    failure_path = FAILURES_DIR / f"{test_name}-{timestamp}.json"

    failure_path.write_text(
        json.dumps(failure_data, indent=2),
        encoding="utf-8",
    )

    return failure_path
