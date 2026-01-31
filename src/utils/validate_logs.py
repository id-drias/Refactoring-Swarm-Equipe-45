import json
import os


def validate_logs(filepath: str = "logs/experiment_data.json") -> bool:
    if not os.path.exists(filepath):
        print(f"Missing log file: {filepath}")
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        logs = json.load(f)

    for i, entry in enumerate(logs, start=1):
        top_level_required = ["agent", "model", "action", "status", "details"]
        for field in top_level_required:
            if field not in entry:
                print(f"Entry {i}: Missing field '{field}'")
                return False

        details = entry.get("details", {})
        for field in ["input_prompt", "output_response"]:
            if field not in details or not details.get(field):
                print(f"Entry {i}: Missing or empty details['{field}']")
                return False

    print("Logs are valid ✅")
    return True


if __name__ == "__main__":
    validate_logs()
