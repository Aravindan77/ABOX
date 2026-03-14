"""
API Routes for Bug Report Analysis
"""

from fastapi import APIRouter, HTTPException, status
from app.models.analysis import BugReportInput, BugReportAnalysis
from app.ml.analyzer import get_analyzer
import time

router = APIRouter()


@router.post(
    "/analyze-report",
    response_model=BugReportAnalysis,
    status_code=status.HTTP_200_OK,
    summary="Analyze Bug Report",
    description="""
    Analyze a bug report using AI/NLP to:
    - Classify against OWASP Top 10
    - Calculate confidence score (0-100)
    - Detect spam
    - Assess severity
    - Determine priority status
    
    **Status Logic:**
    - `REJECTED_SPAM`: Confidence < 40 or detected as spam
    - `NEEDS_REVIEW`: Confidence 40-80
    - `HIGH_PRIORITY`: Confidence > 80
    """
)
async def analyze_bug_report(report: BugReportInput):
    """
    Analyze a bug report and return classification results
    
    **Input:**
    - bug_title: Title of the bug report (5-500 chars)
    - bug_description: Detailed description (min 20 chars)
    - steps_to_reproduce: Reproduction steps (min 10 chars)
    
    **Output:**
    - status: REJECTED_SPAM | NEEDS_REVIEW | HIGH_PRIORITY
    - confidence_score: 0-100
    - owasp_category: Classification with matched keywords
    - severity: Level and CVSS score
    - spam_detection: Spam probability
    - text_quality: Quality assessment
    - sentiment: Sentiment analysis
    """
    try:
        # Get the analyzer instance
        analyzer = get_analyzer()
        
        # Track analysis time
        start_time = time.time()
        
        # Perform analysis
        result = analyzer.analyze_report(
            bug_title=report.bug_title,
            bug_description=report.bug_description,
            steps_to_reproduce=report.steps_to_reproduce
        )
        
        # Calculate processing time
        processing_time = round((time.time() - start_time) * 1000, 2)  # ms
        
        # Log the analysis (in production, use proper logging)
        print(f"✅ Analysis complete in {processing_time}ms - Status: {result['status']}, Confidence: {result['confidence_score']}")
        
        return BugReportAnalysis(**result)
        
    except Exception as e:
        print(f"❌ Analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get(
    "/owasp-categories",
    summary="Get OWASP Top 10 Categories",
    description="Returns the list of OWASP Top 10 2021 categories used for classification"
)
async def get_owasp_categories():
    """
    Get all OWASP Top 10 categories
    """
    from app.ml.owasp_keywords import OWASP_CATEGORIES
    
    categories = []
    for code, data in OWASP_CATEGORIES.items():
        categories.append({
            "code": code,
            "name": data["name"],
            "keyword_count": len(data["keywords"])
        })
    
    return {
        "total": len(categories),
        "categories": categories
    }


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the analysis service is running"
)
async def health_check():
    """
    Health check endpoint for the analysis service
    """
    try:
        analyzer = get_analyzer()
        has_sentiment = analyzer.sentiment_analyzer is not None
        
        return {
            "status": "healthy",
            "service": "bug-report-analyzer",
            "sentiment_model_loaded": has_sentiment,
            "owasp_categories": 10
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }
