from fastapi import APIRouter, Depends, HTTPException
from app.core.dependencies import get_current_wallet, get_optional_wallet, get_db
from app.db.repositories.user_repository import UserRepository
from app.db.repositories.bug_repository import BugRepository
from app.services.reputation_engine import (
    recalculate_for_user,
    get_trust_tier,
    calculate_trust_score,
)

router = APIRouter(prefix="/reputation", tags=["reputation"])


@router.get("/me")
async def my_reputation(wallet: str = Depends(get_current_wallet), db=Depends(get_db)):
    """Return the calling wallet's full reputation profile."""
    user_repo = UserRepository(db)
    bug_repo = BugRepository(db)

    user = user_repo.get_by_wallet(wallet)
    if not user:
        user = user_repo.create_or_update(wallet)

    history = bug_repo.list_by_researcher(wallet, limit=200)
    score = recalculate_for_user(user, history)
    user_repo.update_trust_score(wallet, score)

    tier = get_trust_tier(score)
    accepted = [b for b in history if b.get("status") == "approved"]
    rejected = [b for b in history if b.get("status") == "rejected"]

    return {
        "wallet_address": wallet,
        "trust_score": score,
        "tier": tier,
        "stats": {
            "total_submissions": len(history),
            "accepted": len(accepted),
            "rejected": len(rejected),
            "acceptance_rate": round(len(accepted) / len(history), 3) if history else 0,
            "total_earned_matic": user.get("total_earned_matic", 0),
        },
        "recent_bugs": history[:5],
    }


@router.get("/profile/{wallet_address}")
async def get_profile(wallet_address: str, db=Depends(get_db)):
    """Public profile for any wallet address."""
    user_repo = UserRepository(db)
    user = user_repo.get_by_wallet(wallet_address)
    if not user:
        raise HTTPException(status_code=404, detail="Researcher not found.")

    tier = get_trust_tier(user.get("trust_score", 50))
    return {
        "wallet_address": wallet_address,
        "trust_score": user.get("trust_score", 50),
        "tier": tier,
        "total_submissions": user.get("total_submissions", 0),
        "accepted_submissions": user.get("accepted_submissions", 0),
        "total_earned_matic": user.get("total_earned_matic", 0),
    }


@router.get("/leaderboard")
async def leaderboard(limit: int = 20, db=Depends(get_db)):
    """Top researchers ranked by trust score."""
    user_repo = UserRepository(db)
    leaders = user_repo.leaderboard(limit=limit)
    ranked = []
    for i, user in enumerate(leaders, start=1):
        tier = get_trust_tier(user.get("trust_score", 50))
        ranked.append({
            "rank": i,
            "wallet_address": user["wallet_address"],
            "trust_score": user["trust_score"],
            "tier": tier["label"],
            "tier_color": tier["color"],
            "accepted_submissions": user.get("accepted_submissions", 0),
            "total_earned_matic": user.get("total_earned_matic", 0),
        })
    return {"leaderboard": ranked}
