from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional

from app.core.dependencies import get_current_wallet, get_db
from app.ml.analyzer import BugAnalyzer
from app.services.blockchain_service import blockchain_service
from app.db.repositories.bug_repository import BugRepository
from app.core.config import settings

router = APIRouter(prefix="/triage", tags=["triage"])
analyzer = BugAnalyzer()


class TriageRequest(BaseModel):
    title: str
    description: str
    steps_to_reproduce: str
    severity: Optional[str] = None
    bug_id: Optional[str] = None


class TriageResponse(BaseModel):
    owasp_category: str
    owasp_confidence: float
    cvss_score: float
    severity: str
    spam_probability: float
    is_spam: bool
    ai_confidence: float
    auto_approved: bool
    requires_human_review: bool
    recommendation: str
    tx_hash: Optional[str] = None


@router.post("/analyze", response_model=TriageResponse)
async def analyze_bug(
    payload: TriageRequest,
    wallet: str = Depends(get_current_wallet),
    db=Depends(get_db),
):
    """
    Run AI triage on a bug report.
    If AI confidence >= threshold and not spam, auto-approve and submit on-chain.
    """
    text = f"{payload.title}\n\n{payload.description}\n\n{payload.steps_to_reproduce}"

    try:
        result = analyzer.analyze(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    owasp_cat = result.get("owasp_category", "Unknown")
    owasp_conf = float(result.get("owasp_confidence", 0.0))
    cvss = float(result.get("cvss_score", 0.0))
    severity = result.get("severity", payload.severity or "low")
    spam_prob = float(result.get("spam_probability", 0.0))
    is_spam = spam_prob > 0.7
    ai_confidence = max(0.0, min(1.0, owasp_conf * (1 - spam_prob)))

    threshold = settings.CONFIDENCE_THRESHOLD_AUTO_APPROVE
    auto_approved = ai_confidence >= threshold and not is_spam
    requires_review = not auto_approved and not is_spam

    tx_hash = None
    if auto_approved and payload.bug_id:
        bug_repo = BugRepository(db)
        bug_repo.update_status(
            payload.bug_id,
            "approved",
            ai_confidence=round(ai_confidence, 4),
            owasp_category=owasp_cat,
            cvss_score=cvss,
            severity=severity,
        )
        tx_hash = blockchain_service.submit_bug_on_chain(
            bug_id=payload.bug_id,
            researcher=wallet,
            ipfs_cid="",
            ai_confidence=int(ai_confidence * 100),
        )
    elif payload.bug_id and not is_spam:
        BugRepository(db).update_status(
            payload.bug_id,
            "human_review",
            ai_confidence=round(ai_confidence, 4),
            owasp_category=owasp_cat,
            cvss_score=cvss,
            severity=severity,
        )
    elif payload.bug_id and is_spam:
        BugRepository(db).update_status(payload.bug_id, "spam")

    if auto_approved:
        recommendation = "✅ Auto-approved. Payment will be released after on-chain confirmation."
    elif is_spam:
        recommendation = "🚫 Detected as spam/duplicate. Please submit genuine, unique vulnerabilities."
    else:
        recommendation = "🔍 Queued for human review. A security engineer will evaluate your report."

    return TriageResponse(
        owasp_category=owasp_cat,
        owasp_confidence=round(owasp_conf, 4),
        cvss_score=round(cvss, 1),
        severity=severity,
        spam_probability=round(spam_prob, 4),
        is_spam=is_spam,
        ai_confidence=round(ai_confidence, 4),
        auto_approved=auto_approved,
        requires_human_review=requires_review,
        recommendation=recommendation,
        tx_hash=tx_hash,
    )


@router.get("/status/{bug_id}")
async def triage_status(bug_id: str, db=Depends(get_db)):
    """Return the current triage status of a bug."""
    bug = BugRepository(db).get_by_id(bug_id)
    if not bug:
        raise HTTPException(status_code=404, detail="Bug not found.")
    return {
        "bug_id": bug_id,
        "status": bug.get("status"),
        "ai_confidence": bug.get("ai_confidence"),
        "owasp_category": bug.get("owasp_category"),
        "cvss_score": bug.get("cvss_score"),
        "severity": bug.get("severity"),
    }
