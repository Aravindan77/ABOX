"""
Reputation Engine - Calculates trust scores for bug hunters.

Trust Score Formula (0-100):
  base = 50
  + acceptance_rate_bonus  (up to +30)
  + volume_bonus           (up to +10)
  + severity_bonus         (up to +10)
  - spam_penalty           (up to -20)
  - inactivity_decay       (up to -10)
"""
from typing import List
import math


# Severity weights
SEVERITY_WEIGHTS = {
    "critical": 5.0,
    "high": 3.0,
    "medium": 1.5,
    "low": 0.5,
    "informational": 0.1,
}


def calculate_trust_score(
    total_submissions: int,
    accepted: int,
    rejected: int,
    severities: List[str] | None = None,
    spam_flags: int = 0,
    days_since_last_submission: int = 0,
) -> float:
    """Calculate a researcher trust score between 0 and 100."""
    base = 50.0
    severities = severities or []

    # 1. Acceptance rate bonus (+0 to +30)
    if total_submissions > 0:
        rate = accepted / total_submissions
        acceptance_bonus = rate * 30
    else:
        acceptance_bonus = 0

    # 2. Volume bonus – logarithmic (+0 to +10)
    volume_bonus = min(10, math.log1p(accepted) * 2.5) if accepted > 0 else 0

    # 3. Severity bonus – weighted quality (+0 to +10)
    severity_score = sum(SEVERITY_WEIGHTS.get(s.lower(), 0) for s in severities)
    severity_bonus = min(10, severity_score * 0.5)

    # 4. Spam penalty (-0 to -20)
    spam_penalty = min(20, spam_flags * 4)

    # 5. Inactivity decay (-0 to -10)
    if days_since_last_submission > 180:
        inactivity_penalty = min(10, (days_since_last_submission - 180) / 36)
    else:
        inactivity_penalty = 0

    score = (
        base
        + acceptance_bonus
        + volume_bonus
        + severity_bonus
        - spam_penalty
        - inactivity_penalty
    )
    return round(max(0.0, min(100.0, score)), 2)


def get_trust_tier(score: float) -> dict:
    """Return the tier name, label, and colour for a trust score."""
    if score >= 85:
        return {"tier": "elite", "label": "Elite Hunter", "color": "#FFD700"}
    elif score >= 70:
        return {"tier": "expert", "label": "Expert", "color": "#C0C0C0"}
    elif score >= 50:
        return {"tier": "trusted", "label": "Trusted", "color": "#00D4FF"}
    elif score >= 30:
        return {"tier": "novice", "label": "Novice", "color": "#A0A0A0"}
    else:
        return {"tier": "unverified", "label": "Unverified", "color": "#FF4444"}


def recalculate_for_user(user: dict, bug_history: List[dict]) -> float:
    """
    Given a user dict and their full bug history, recompute and return
    their updated trust score.
    """
    from datetime import datetime, timezone

    accepted = [b for b in bug_history if b.get("status") == "approved"]
    rejected = [b for b in bug_history if b.get("status") == "rejected"]
    spam = [b for b in bug_history if b.get("status") == "spam"]

    severities = [b.get("severity", "low") for b in accepted]

    # Days since last submission
    days_inactive = 0
    if bug_history:
        latest_str = max(b.get("created_at", "") for b in bug_history)
        if latest_str:
            try:
                latest = datetime.fromisoformat(latest_str.replace("Z", "+00:00"))
                days_inactive = (datetime.now(timezone.utc) - latest).days
            except Exception:
                pass

    return calculate_trust_score(
        total_submissions=len(bug_history),
        accepted=len(accepted),
        rejected=len(rejected),
        severities=severities,
        spam_flags=len(spam),
        days_since_last_submission=days_inactive,
    )
