"""
Pydantic models for bug report analysis
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class BugReportInput(BaseModel):
    """Input model for bug report analysis"""
    bug_title: str = Field(..., min_length=5, max_length=500, description="Bug report title")
    bug_description: str = Field(..., min_length=20, description="Detailed bug description")
    steps_to_reproduce: str = Field(..., min_length=10, description="Steps to reproduce the bug")
    
    class Config:
        json_schema_extra = {
            "example": {
                "bug_title": "SQL Injection in Login Form",
                "bug_description": "The login form is vulnerable to SQL injection attacks. By entering a single quote in the username field, the application returns a database error revealing the SQL query structure.",
                "steps_to_reproduce": "1. Navigate to /login\n2. Enter ' OR '1'='1 in username field\n3. Enter any password\n4. Click submit\n5. Observe SQL error message"
            }
        }


class OWASPCategory(BaseModel):
    """OWASP classification result"""
    code: str = Field(..., description="OWASP category code (e.g., A03:2021)")
    name: str = Field(..., description="OWASP category name")
    confidence: float = Field(..., ge=0, le=100, description="Classification confidence (0-100)")
    matched_keywords: List[str] = Field(default=[], description="Keywords that matched")


class SeverityInfo(BaseModel):
    """Severity assessment"""
    level: str = Field(..., description="Severity level: critical, high, medium, low")
    cvss_score: int = Field(..., ge=0, le=100, description="CVSS score (0-100)")


class SpamDetection(BaseModel):
    """Spam detection result"""
    is_spam: bool = Field(..., description="Whether the report is spam")
    spam_score: float = Field(..., ge=0, le=100, description="Spam probability (0-100)")


class TextQuality(BaseModel):
    """Text quality assessment"""
    score: float = Field(..., ge=0, le=100, description="Quality score (0-100)")
    assessment: str = Field(..., description="Quality level: high, medium, low")


class SentimentInfo(BaseModel):
    """Sentiment analysis result"""
    label: str = Field(..., description="Sentiment label (POSITIVE, NEGATIVE, NEUTRAL)")
    score: float = Field(..., ge=0, le=1, description="Sentiment confidence (0-1)")


class BugReportAnalysis(BaseModel):
    """Complete bug report analysis result"""
    status: str = Field(..., description="Report status: REJECTED_SPAM, NEEDS_REVIEW, HIGH_PRIORITY")
    confidence_score: int = Field(..., ge=0, le=100, description="Overall confidence score (0-100)")
    owasp_category: OWASPCategory
    severity: SeverityInfo
    spam_detection: SpamDetection
    text_quality: TextQuality
    sentiment: SentimentInfo
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "HIGH_PRIORITY",
                "confidence_score": 85,
                "owasp_category": {
                    "code": "A03:2021",
                    "name": "Injection",
                    "confidence": 92.5,
                    "matched_keywords": ["sql injection", "query", "database"]
                },
                "severity": {
                    "level": "high",
                    "cvss_score": 75
                },
                "spam_detection": {
                    "is_spam": False,
                    "spam_score": 10.0
                },
                "text_quality": {
                    "score": 85.0,
                    "assessment": "high"
                },
                "sentiment": {
                    "label": "NEGATIVE",
                    "score": 0.95
                }
            }
        }
