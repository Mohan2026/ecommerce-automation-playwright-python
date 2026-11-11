
import csv
import os
import re
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load local environment variables without overriding CI secrets
load_dotenv(PROJECT_ROOT / ".env", override=False)


def resolve_env_variable(value: str) -> str:
    """Replace ${VARIABLE_NAME} with its environment value."""

    pattern = r"^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$"
    match = re.fullmatch(pattern, value)

    if not match:
        return value

    variable_name = match.group(1)
    secret = os.getenv(variable_name)

    if secret is None:
        raise ValueError(
            f"Missing environment variable: {variable_name}"
        )

    return secret


def load_csv(file_path: str) -> list[dict[str, str]]:
    """Read CSV test data and resolve environment references."""

    path = PROJECT_ROOT / file_path

    if not path.is_file():
        raise FileNotFoundError(f"CSV file not found: {path}")

    with path.open(
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("CSV file has no header.")

        test_data = []

        for row in reader:
            resolved_row = {
                key: resolve_env_variable(value or "")
                for key, value in row.items()
                if key is not None
            }

            test_data.append(resolved_row)

    return test_data
