"""
Test script for the /analyze-report endpoint
"""

import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"
ANALYZE_ENDPOINT = f"{BASE_URL}/api/v1/analyze-report"

# Test cases
test_cases = [
    {
        "name": "SQL Injection - High Priority",
        "data": {
            "bug_title": "SQL Injection in Login Form",
            "bug_description": "The login form is vulnerable to SQL injection attacks. By entering a single quote in the username field, the application returns a database error revealing the SQL query structure. This allows an attacker to bypass authentication and potentially access sensitive data.",
            "steps_to_reproduce": "1. Navigate to /login\n2. Enter ' OR '1'='1 in username field\n3. Enter any password\n4. Click submit\n5. Observe SQL error message and successful login"
        }
    },
    {
        "name": "XSS Vulnerability - High Priority",
        "data": {
            "bug_title": "Stored XSS in Comment Section",
            "bug_description": "The application does not properly sanitize user input in the comment section, allowing attackers to inject malicious JavaScript code. When other users view the comments, the script executes in their browser, potentially stealing session cookies or performing actions on their behalf.",
            "steps_to_reproduce": "1. Navigate to /posts/123\n2. Enter <script>alert(document.cookie)</script> in comment field\n3. Submit comment\n4. Reload page\n5. Observe JavaScript execution"
        }
    },
    {
        "name": "Broken Access Control - Medium",
        "data": {
            "bug_title": "Unauthorized Access to Admin Panel",
            "bug_description": "Regular users can access the admin panel by directly navigating to /admin without proper authorization checks. This allows privilege escalation.",
            "steps_to_reproduce": "1. Login as regular user\n2. Navigate to /admin\n3. Access granted without admin role verification"
        }
    },
    {
        "name": "Spam Report - Should be Rejected",
        "data": {
            "bug_title": "test",
            "bug_description": "hello this is a test",
            "steps_to_reproduce": "testing testing"
        }
    },
    {
        "name": "Low Quality Report - Needs Review",
        "data": {
            "bug_title": "Bug in the system",
            "bug_description": "There is a bug when I click the button. It doesn't work properly.",
            "steps_to_reproduce": "Click the button and see the error"
        }
    }
]

def test_analyze_endpoint():
    """Test the analyze-report endpoint"""
    print("=" * 80)
    print("Testing /analyze-report Endpoint")
    print("=" * 80)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test Case {i}: {test_case['name']}")
        print("=" * 80)
        
        try:
            response = requests.post(
                ANALYZE_ENDPOINT,
                json=test_case['data'],
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"\n✅ Status: {result['status']}")
                print(f"📊 Confidence Score: {result['confidence_score']}/100")
                print(f"\n🔍 OWASP Category:")
                print(f"   Code: {result['owasp_category']['code']}")
                print(f"   Name: {result['owasp_category']['name']}")
                print(f"   Confidence: {result['owasp_category']['confidence']:.2f}%")
                print(f"   Keywords: {', '.join(result['owasp_category']['matched_keywords'][:3])}")
                
                print(f"\n⚠️  Severity:")
                print(f"   Level: {result['severity']['level'].upper()}")
                print(f"   CVSS Score: {result['severity']['cvss_score']}/100")
                
                print(f"\n🚫 Spam Detection:")
                print(f"   Is Spam: {result['spam_detection']['is_spam']}")
                print(f"   Spam Score: {result['spam_detection']['spam_score']:.2f}%")
                
                print(f"\n📝 Text Quality:")
                print(f"   Score: {result['text_quality']['score']:.2f}/100")
                print(f"   Assessment: {result['text_quality']['assessment'].upper()}")
                
                print(f"\n😊 Sentiment:")
                print(f"   Label: {result['sentiment']['label']}")
                print(f"   Score: {result['sentiment']['score']:.3f}")
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the backend is running on http://localhost:8000")
            return
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    print(f"\n{'=' * 80}")
    print("Testing Complete!")
    print("=" * 80)

def test_health_endpoint():
    """Test the health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print(f"✅ Health Check: {response.json()}")
        else:
            print(f"❌ Health Check Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_owasp_categories():
    """Test the OWASP categories endpoint"""
    print("\n📚 Testing OWASP Categories Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/owasp-categories")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total Categories: {data['total']}")
            for cat in data['categories'][:3]:
                print(f"   - {cat['code']}: {cat['name']} ({cat['keyword_count']} keywords)")
        else:
            print(f"❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    # Test health first
    test_health_endpoint()
    
    # Test OWASP categories
    test_owasp_categories()
    
    # Test main analysis endpoint
    test_analyze_endpoint()
