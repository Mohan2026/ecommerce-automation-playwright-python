
import json
from pathlib import Path

failure_file = Path(__file__).parent / "sample_failure.json"

with failure_file.open("r", encoding="utf-8") as file:
    failure_data = json.load(file)

print("Test name:", failure_data["test_name"])
print("Status:", failure_data["status"])
print("Error:", failure_data["error_message"])
print("Expected:", failure_data["expected"])
print("Actual:", failure_data["actual"])
