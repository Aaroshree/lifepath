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

## Project structure
lifepath/
├── game.py            ← game logic, stat system, ending classifier
├── logger.py          ← saves every run to data/sessions.csv
├── data/
│   └── sessions.csv   ← grows with every playthrough
└── analysis/
└── explore.ipynb  ← all analysis and models

## Dataset schema
| Column | Description |
|--------|-------------|
| player_id | Unique ID per run |
| round | Round number (1–14) |
| age | Player age (18–31) |
| choice | Choice made that round |
| risk_outcome | Outcome if risk was taken |
| knowledge | Stat snapshot |
| money | Stat snapshot |
| health | Stat snapshot |
| happiness | Stat snapshot |
| luck | Hidden luck value |
| social_count | Cumulative social investments |
| ending | Final ending label |

## Analysis completed

### 1. Decision tree — predicting ending from round 7 stats
Trained a decision tree classifier on midgame stats to predict final ending.
- Health is the #1 predictor at round 7 (importance: 0.39)
- Money is second (0.35), happiness third (0.26)
- Knowledge scored 0.00 — behavior patterns matter more than knowledge at midgame

### 2. Logistic regression — what drives each ending
Trained a multiclass logistic regression model and visualized coefficients
as a heatmap to show which stats push toward which endings.

### 3. K-means clustering — player archetypes
Clustered all 11 runs into 4 groups based on final stat shape.

| Cluster | Endings | Stat profile |
|---------|---------|--------------|
| 0 | Balanced Developer | High across all stats |
| 1 | The Grinder, The Regret | High money, near-zero health and happiness |
| 2 | The Quiet Life | Zero money, maximum happiness and health |
| 3 | Burnout Genius | Maximum knowledge, zero health |

Key finding: The Regret and The Grinder share the same stat shape —
same life trajectory, different severity.

## Endings (10 total)
| Ending | Condition |
|--------|-----------|
| Balanced Developer | All stats >= 55 |
| Burnout Genius | Knowledge >= 85, Health <= 30 |
| The Grinder | Money >= 70, Happiness <= 35 |
| The Quiet Life | Health + Happiness >= 150, Money <= 40 |
| Perpetual Student | Knowledge >= 80, Money <= 35 |
| Accidental Millionaire | Money >= 85, 3+ risk wins |
| Late Bloomer | All stats <= 50 by round 10, then 2+ risk wins |
| Social Butterfly | 4+ social rounds, Happiness >= 60 |
| Crisis Recovery | 2+ burnouts survived, final Health >= 60 |
| The Regret | Any stat <= 20 at end |

## Next steps
- [ ] Monte Carlo simulation — 10,000 random games to map ending probabilities
- [ ] Play more runs to improve model generalization
- [ ] Add more ending variety through mixed strategies