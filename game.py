# game.py

import random
import uuid
from colorama import init, Fore, Style

init(autoreset=True)

# ── Stats ──────────────────────────────────────────────
def starting_stats():
    return {
        "knowledge": 30,
        "money":     20,
        "health":    70,
        "happiness": 60,
    }

def clamp(value):
    return max(0, min(100, value))

def apply_changes(stats, changes):
    for key, delta in changes.items():
        stats[key] = clamp(stats[key] + delta)
    return stats

# ── Display ────────────────────────────────────────────
def print_stats(stats, round_num, age):
    print(f"\n{Fore.CYAN}{'─'*40}")
    print(f"  Round {round_num} · Age {age}")
    print(f"{'─'*40}{Style.RESET_ALL}")
    bars = {
        "knowledge": Fore.BLUE,
        "money":     Fore.GREEN,
        "health":    Fore.RED,
        "happiness": Fore.MAGENTA,
    }
    for stat, color in bars.items():
        val = stats[stat]
        filled = int(val / 5)
        bar = "█" * filled + "░" * (20 - filled)
        print(f"  {color}{stat:<12} {bar} {val:>3}{Style.RESET_ALL}")
    print()

# ── Choices ────────────────────────────────────────────
CHOICES = {
    "1": {
        "label": "Study / Learn",
        "effects": {"knowledge": 12, "happiness": -5, "health": -3},
    },
    "2": {
        "label": "Work harder",
        "effects": {"money": 12, "health": -6, "happiness": -4},
    },
    "3": {
        "label": "Rest / Invest in self",
        "effects": {"health": 12, "happiness": 8, "knowledge": 2},
    },
    "4": {
        "label": "Take a risk",
        "effects": "random",
    },
    "5": {
        "label": "Invest socially",
        "effects": {"happiness": 10, "money": -3, "health": 3},
    },
}

RISK_OUTCOMES = [
    {"label": "Big payoff!",       "effects": {"money": 25, "happiness": 15}},
    {"label": "Learned a lesson.", "effects": {"knowledge": 15, "health": -5}},
    {"label": "Nothing happened.", "effects": {"happiness": -5}},
    {"label": "It went badly.",    "effects": {"money": -15, "health": -10}},
]

def take_risk(luck):
    weights = [
        10 + luck,   # big payoff — more likely with high luck
        30,
        30,
        30 - luck,   # bad outcome — less likely with high luck
    ]
    outcome = random.choices(RISK_OUTCOMES, weights=weights, k=1)[0]
    return outcome

def get_choice():
    print(f"{Fore.YELLOW}What do you do this round?{Style.RESET_ALL}")
    for key, choice in CHOICES.items():
        print(f"  [{key}] {choice['label']}")
    while True:
        pick = input("\n  Your choice: ").strip()
        if pick in CHOICES:
            return pick
        print("  Please enter a number between 1 and 5.")

# ── Main game loop ─────────────────────────────────────
def play_game():
    print(f"\n{Fore.MAGENTA}{'═'*40}")
    print("       W E L C O M E  T O  L I F E P A T H")
    print(f"{'═'*40}{Style.RESET_ALL}")
    print("\nYou are 18. The choices you make will shape your life.\n")

    stats        = starting_stats()
    history      = []
    player_id    = str(uuid.uuid4())[:8]
    luck         = 0
    consecutive  = {"choice": None, "count": 0}
    social_count = 0

    ROUNDS = 14

    for round_num in range(1, ROUNDS + 1):
        age = 18 + round_num - 1
        print_stats(stats, round_num, age)
        pick = get_choice()
        choice = CHOICES[pick]

        # momentum tracking
        if consecutive["choice"] == pick:
            consecutive["count"] += 1
        else:
            consecutive["choice"] = pick
            consecutive["count"] = 1

        # apply effects
        risk_label = ""
        if choice["effects"] == "random":
            outcome = take_risk(luck)
            risk_label = outcome["label"]
            print(f"\n  {Fore.YELLOW}Risk outcome: {outcome['label']}{Style.RESET_ALL}")
            apply_changes(stats, outcome["effects"])
        else:
            effects = choice["effects"].copy()
            # momentum bonus/penalty
            if consecutive["count"] == 2:
                effects = {k: int(v * 1.1) for k, v in effects.items()}
            elif consecutive["count"] >= 4:
                effects = {k: int(v * 0.8) for k, v in effects.items()}
            apply_changes(stats, effects)

        # update hidden luck from happiness
        luck = max(0, min(20, stats["happiness"] // 5))

        # social count for network modifier
        if pick == "5":
            social_count += 1

        # burnout check
        if consecutive["choice"] in ("1", "2") and consecutive["count"] >= 3:
            print(f"\n  {Fore.RED}⚠ Burnout! You've pushed too hard. Forced rest.{Style.RESET_ALL}")
            apply_changes(stats, {"health": -15, "happiness": -10})
            consecutive["count"] = 1
            history[-1]["risk_outcome"] = "Burnout"

        # log the round
        history.append({
            "player_id":    player_id,
            "round":        round_num,
            "age":          age,
            "choice":       choice["label"],
            "risk_outcome": risk_label,
            "knowledge":    stats["knowledge"],
            "money":        stats["money"],
            "health":       stats["health"],
            "happiness":    stats["happiness"],
            "luck":         luck,
            "social_count": social_count,
        })

    return stats, history, player_id, social_count
# ── Ending classifier ──────────────────────────────────
def classify_ending(stats, history, social_count):
    k = stats["knowledge"]
    m = stats["money"]
    h = stats["health"]
    hp = stats["happiness"]

    risk_wins = sum(
        1 for row in history
        if row["risk_outcome"] == "Big payoff!"
    )

    burnout_count = sum(
        1 for row in history
        if "Burnout" in row.get("risk_outcome", "")
    )

    if k >= 85 and h <= 30:
        return "Burnout Genius"
    if m >= 85 and risk_wins >= 3:
        return "Accidental Millionaire"
    if k >= 80 and m <= 35:
        return "Perpetual Student"
    if m >= 70 and hp <= 35:
        return "The Grinder"
    if h + hp >= 150 and m <= 40:
        return "The Quiet Life"
    if social_count >= 4 and hp >= 60:
        return "Social Butterfly"
    if burnout_count >= 2 and h >= 60:
        return "Crisis Recovery"
    if all(stats[s] <= 50 for s in stats) and risk_wins >= 2:
        return "Late Bloomer"
    if any(stats[s] <= 20 for s in stats):
        return "The Regret"
    return "Balanced Developer"


def print_ending(ending, stats, player_id):
    messages = {
        "Burnout Genius":        "You achieved greatness — at a cost.",
        "Accidental Millionaire":"The risks paid off. Not everyone gets this lucky.",
        "Perpetual Student":     "You know everything. Except how to cash in.",
        "The Grinder":           "Rich, exhausted, and wondering what it was all for.",
        "The Quiet Life":        "Not glamorous. But genuinely happy. Rarer than it sounds.",
        "Social Butterfly":      "Your network carried you further than your stats did.",
        "Crisis Recovery":       "You broke down and rebuilt. That takes real strength.",
        "Late Bloomer":          "Slow start, bold finish. The best kind of story.",
        "The Regret":            "Some paths close. The question is what you do next.",
        "Balanced Developer":    "Steady, capable, grounded. Most people never get here.",
    }

    print(f"\n{Fore.MAGENTA}{'═'*40}")
    print(f"  YOUR ENDING: {ending}")
    print(f"{'═'*40}{Style.RESET_ALL}")
    print(f"\n  {messages[ending]}")
    print(f"\n  Final stats:")
    for stat, val in stats.items():
        print(f"    {stat:<12} {val}")
    print(f"\n  Player ID: {player_id}")
    print(f"{Fore.CYAN}{'─'*40}{Style.RESET_ALL}\n")


# ── Entry point ────────────────────────────────────────
if __name__ == "__main__":
    from logger import save_session

    stats, history, player_id, social_count = play_game()
    ending = classify_ending(stats, history, social_count)
    print_ending(ending, stats, player_id)
    save_session(history, ending)