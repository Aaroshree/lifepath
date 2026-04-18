# LifePath

A choice-driven life simulation game built in Python, where every decision
compounds over time — and every playthrough generates a dataset for analysis.

## What it is
You play from age 18 to 40 across 14 rounds, choosing between studying,
working, resting, taking risks, and investing socially. Four stats track
your progress: knowledge, money, health, and happiness. Hidden mechanics
like burnout, luck, and momentum shape the outcomes.

## What makes it a data science project
Every run logs to CSV. After enough playthroughs the data reveals patterns —
which stats predict your ending, how choices compound, and what the most
likely outcome is if you play randomly.

## Tech stack
- Python 3.13
- pandas, matplotlib, scikit-learn, colorama
- Jupyter Notebook

## How to run
pip install pandas matplotlib scikit-learn colorama
python game.py

## Analysis so far
- Decision tree trained on round 7 stats to predict ending
- Feature importance: health (0.39) > money (0.35) > happiness (0.26)
- Knowledge is irrelevant at the halfway point — behavior matters more

## Endings (10 total)
Balanced Developer, Burnout Genius, The Grinder, The Quiet Life,
Perpetual Student, Accidental Millionaire, Late Bloomer,
Social Butterfly, Crisis Recovery, The Regret
