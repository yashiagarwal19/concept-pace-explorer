"""Epsilon-greedy multi-armed bandit: picks the teaching format.
Mostly shows the best-performing format, sometimes explores the others."""
import random

FORMATS = ["picture", "audio", "story"]
EPSILON = 0.2  # 20% of the time, try a random format

def reward(correct, ms, hints):
    """0 if wrong. If right: higher for faster answers, small penalty per hint."""
    if not correct:
        return 0.0
    speed = max(0.3, 1 - ms / 20000)
    return round(speed * (1 - 0.1 * min(hints, 3)), 3)

def choose(rows):
    avg = {r["fmt"]: r["avg_reward"] for r in rows}
    untried = [f for f in FORMATS if f not in avg]
    if untried:
        return random.choice(untried)
    if random.random() < EPSILON:
        return random.choice(FORMATS)
    return max(FORMATS, key=lambda f: avg[f])
