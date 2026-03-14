"""
Bug Report Analyzer
Uses NLP and keyword matching for OWASP classification
"""

from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import numpy as np

# transformers/torch are optional — fall back to rule-based sentiment if not installed
try:
    from transformers import pipeline as hf_pipeline
    _TRANSFORMERS_AVAILABLE = True
except ImportError:
    hf_pipeline = None  # type: ignore
    _TRANSFORMERS_AVAILABLE = False
    print("ℹ️  transformers not installed — using rule-based sentiment fallback")

from app.ml.owasp_keywords import (
    OWASP_CATEGORIES,
    SEVERITY_KEYWORDS,
    SPAM_INDICATORS
)


class BugReportAnalyzer:
    """
    Analyzes bug reports using NLP and keyword matching
    """
    
    def __init__(self):
        """Initialize the analyzer with a lightweight sentiment model"""
        self.sentiment_analyzer = None
        if _TRANSFORMERS_AVAILABLE and hf_pipeline is not None:
            try:
                self.sentiment_analyzer = hf_pipeline(
                    "sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english",
                    device=-1  # CPU
                )
                print("✅ Sentiment analyzer loaded (DistilBERT)")
            except Exception as e:
                print(f"⚠️  Could not load DistilBERT: {e} — using rule-based fallback")
        else:
            print("ℹ️  Using rule-based sentiment analysis (no torch required)")
    
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s\-_]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def detect_spam(self, title: str, description: str, steps: str) -> Tuple[bool, float]:
        """
        Detect if the report is spam
        Returns: (is_spam, spam_score)
        """
        combined_text = f"{title} {description} {steps}".lower()
        
        # Check for spam indicators
        spam_count = 0
        for indicator in SPAM_INDICATORS:
            if indicator in combined_text:
                spam_count += 1
        
        # Check text length (too short is suspicious)
        total_length = len(combined_text.strip())
        if total_length < 50:
            spam_count += 2
        
        # Check for repeated characters (e.g., "aaaaaaa")
        if re.search(r'(.)\1{5,}', combined_text):
            spam_count += 2
        
        # Check if description is missing
        if not description or len(description.strip()) < 20:
            spam_count += 1
        
        # Calculate spam score (0-100)
        spam_score = min(spam_count * 15, 100)
        is_spam = spam_score > 50
        
        return is_spam, spam_score
    
    def match_owasp_category(self, text: str) -> Dict[str, any]:
        """
        Match text against OWASP Top 10 categories
        Returns the best matching category with confidence
        """
        text = self.preprocess_text(text)
        
        # Count keyword matches for each category
        category_scores = {}
        
        for code, category_data in OWASP_CATEGORIES.items():
            keywords = category_data["keywords"]
            matches = 0
            matched_keywords = []
            
            for keyword in keywords:
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text):
                    matches += 1
                    matched_keywords.append(keyword)
            
            if matches > 0:
                category_scores[code] = {
                    "name": category_data["name"],
                    "matches": matches,
                    "matched_keywords": matched_keywords
                }
        
        # If no matches, return unknown
        if not category_scores:
            return {
                "code": "UNKNOWN",
                "name": "Unknown Category",
                "confidence": 0,
                "matched_keywords": []
            }
        
        # Get the category with most matches
        best_category = max(category_scores.items(), key=lambda x: x[1]["matches"])
        code = best_category[0]
        data = best_category[1]
        
        # Calculate confidence based on number of matches
        # More matches = higher confidence
        max_possible_matches = len(OWASP_CATEGORIES[code]["keywords"])
        confidence = min((data["matches"] / max_possible_matches) * 100, 100)
        
        # Boost confidence if multiple keywords matched
        if data["matches"] >= 3:
            confidence = min(confidence * 1.2, 100)
        
        return {
            "code": code,
            "name": data["name"],
            "confidence": round(confidence, 2),
            "matched_keywords": data["matched_keywords"][:5]  # Top 5
        }
    
    def calculate_severity(self, text: str) -> Tuple[str, int]:
        """
        Calculate severity based on keywords
        Returns: (severity_level, cvss_score)
        """
        text = self.preprocess_text(text)
        
        # Check for severity keywords
        severity_matches = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        for severity, keywords in SEVERITY_KEYWORDS.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text):
                    severity_matches[severity] += 1
        
        # Determine severity based on matches
        if severity_matches["critical"] > 0:
            return "critical", 90
        elif severity_matches["high"] > 0:
            return "high", 75
        elif severity_matches["medium"] > 0:
            return "medium", 50
        elif severity_matches["low"] > 0:
            return "low", 30
        else:
            return "medium", 50  # Default
    
    def analyze_sentiment(self, text: str) -> Dict[str, any]:
        """
        Analyze sentiment of the text
        Returns sentiment label and score
        """
        if not self.sentiment_analyzer or not text:
            return {"label": "NEUTRAL", "score": 0.5}
        
        try:
            # Truncate text if too long (model limit is 512 tokens)
            text = text[:2000]
            result = self.sentiment_analyzer(text)[0]
            return result
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return {"label": "NEUTRAL", "score": 0.5}
    
    def calculate_confidence_score(
        self,
        owasp_confidence: float,
        text_quality: float,
        spam_score: float,
        sentiment_score: float
    ) -> int:
        """
        Calculate overall confidence score (0-100)
        
        Factors:
        - OWASP match confidence (40%)
        - Text quality (30%)
        - Spam score (20% - inverse)
        - Sentiment (10%)
        """
        # Weighted average
        confidence = (
            owasp_confidence * 0.4 +
            text_quality * 0.3 +
            (100 - spam_score) * 0.2 +
            sentiment_score * 100 * 0.1
        )
        
        return int(round(confidence))
    
    def assess_text_quality(self, title: str, description: str, steps: str) -> float:
        """
        Assess the quality of the bug report text
        Returns score 0-100
        """
        score = 0
        
        # Title quality (max 20 points)
        if title and len(title) > 10:
            score += 20
        elif title and len(title) > 5:
            score += 10
        
        # Description quality (max 40 points)
        if description:
            desc_length = len(description)
            if desc_length > 200:
                score += 40
            elif desc_length > 100:
                score += 30
            elif desc_length > 50:
                score += 20
            else:
                score += 10
        
        # Steps to reproduce (max 30 points)
        if steps:
            steps_length = len(steps)
            # Check for numbered steps
            has_numbers = bool(re.search(r'\d+[\.\)]\s', steps))
            
            if steps_length > 100 and has_numbers:
                score += 30
            elif steps_length > 50:
                score += 20
            else:
                score += 10
        
        # Technical terms bonus (max 10 points)
        combined = f"{title} {description} {steps}".lower()
        technical_terms = ['api', 'endpoint', 'parameter', 'request', 'response',
                          'header', 'cookie', 'token', 'authentication', 'authorization']
        tech_count = sum(1 for term in technical_terms if term in combined)
        score += min(tech_count * 2, 10)
        
        return min(score, 100)
    
    def analyze_report(
        self,
        bug_title: str,
        bug_description: str,
        steps_to_reproduce: str
    ) -> Dict[str, any]:
        """
        Main analysis function
        Returns comprehensive analysis results
        """
        # Combine all text for analysis
        combined_text = f"{bug_title} {bug_description} {steps_to_reproduce}"
        
        # 1. Spam detection
        is_spam, spam_score = self.detect_spam(bug_title, bug_description, steps_to_reproduce)
        
        # 2. OWASP classification
        owasp_result = self.match_owasp_category(combined_text)
        
        # 3. Severity calculation
        severity, cvss_score = self.calculate_severity(combined_text)
        
        # 4. Text quality assessment
        text_quality = self.assess_text_quality(bug_title, bug_description, steps_to_reproduce)
        
        # 5. Sentiment analysis
        sentiment = self.analyze_sentiment(bug_description)
        
        # 6. Calculate overall confidence
        confidence_score = self.calculate_confidence_score(
            owasp_result["confidence"],
            text_quality,
            spam_score,
            sentiment["score"]
        )
        
        # 7. Determine status
        if is_spam or confidence_score < 40:
            status = "REJECTED_SPAM"
        elif confidence_score > 80:
            status = "HIGH_PRIORITY"
        else:
            status = "NEEDS_REVIEW"
        
        return {
            "status": status,
            "confidence_score": confidence_score,
            "owasp_category": {
                "code": owasp_result["code"],
                "name": owasp_result["name"],
                "confidence": owasp_result["confidence"],
                "matched_keywords": owasp_result["matched_keywords"]
            },
            "severity": {
                "level": severity,
                "cvss_score": cvss_score
            },
            "spam_detection": {
                "is_spam": is_spam,
                "spam_score": spam_score
            },
            "text_quality": {
                "score": text_quality,
                "assessment": "high" if text_quality > 70 else "medium" if text_quality > 40 else "low"
            },
            "sentiment": {
                "label": sentiment["label"],
                "score": round(sentiment["score"], 3)
            }
        }


# Global analyzer instance (loaded once)
_analyzer_instance = None

def get_analyzer() -> BugReportAnalyzer:
    """Get or create the global analyzer instance"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = BugReportAnalyzer()
    return _analyzer_instance
