# logger.py

import csv
import os

LOG_PATH = os.path.join("data", "sessions.csv")

FIELDS = [
    "player_id",
    "round",
    "age",
    "choice",
    "risk_outcome",
    "knowledge",
    "money",
    "health",
    "happiness",
    "luck",
    "social_count",
    "ending",
]

def save_session(history, ending):
    file_exists = os.path.isfile(LOG_PATH)

    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)

        if not file_exists:
            writer.writeheader()

        for row in history:
            row["ending"] = ending
            writer.writerow(row)

    print(f"\n  Session saved → data/sessions.csv")