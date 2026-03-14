"""
OWASP Top 10 Keyword Mapping
Used for bug report classification
"""

OWASP_CATEGORIES = {
    "A01:2021": {
        "name": "Broken Access Control",
        "keywords": [
            "unauthorized", "access control", "privilege", "escalation", "bypass",
            "authentication bypass", "authorization", "forbidden", "admin panel",
            "restricted", "permission", "role", "IDOR", "insecure direct object",
            "path traversal", "directory traversal", "forced browsing"
        ]
    },
    "A02:2021": {
        "name": "Cryptographic Failures",
        "keywords": [
            "encryption", "decrypt", "hash", "password", "plaintext", "weak cipher",
            "ssl", "tls", "certificate", "crypto", "sensitive data", "exposed",
            "hardcoded", "key", "token", "secret", "md5", "sha1", "base64"
        ]
    },
    "A03:2021": {
        "name": "Injection",
        "keywords": [
            "sql injection", "sqli", "xss", "cross-site scripting", "command injection",
            "code injection", "ldap", "xpath", "nosql", "orm", "query", "payload",
            "script", "eval", "exec", "shell", "os command", "blind sql", "union select"
        ]
    },
    "A04:2021": {
        "name": "Insecure Design",
        "keywords": [
            "design flaw", "architecture", "threat model", "security pattern",
            "business logic", "workflow", "rate limit", "brute force", "enumeration",
            "predictable", "sequential", "missing validation", "insecure default"
        ]
    },
    "A05:2021": {
        "name": "Security Misconfiguration",
        "keywords": [
            "misconfiguration", "default", "debug", "error message", "stack trace",
            "verbose", "directory listing", "unnecessary", "outdated", "unpatched",
            "cors", "headers", "security headers", "x-frame-options", "csp",
            "content security policy", "exposed", "configuration"
        ]
    },
    "A06:2021": {
        "name": "Vulnerable and Outdated Components",
        "keywords": [
            "outdated", "vulnerable", "dependency", "library", "framework", "cve",
            "version", "old", "unmaintained", "deprecated", "third-party",
            "component", "package", "npm", "maven", "composer"
        ]
    },
    "A07:2021": {
        "name": "Identification and Authentication Failures",
        "keywords": [
            "authentication", "session", "cookie", "jwt", "token", "login", "logout",
            "password reset", "credential", "brute force", "session fixation",
            "session hijacking", "weak password", "multi-factor", "2fa", "mfa",
            "remember me", "account takeover"
        ]
    },
    "A08:2021": {
        "name": "Software and Data Integrity Failures",
        "keywords": [
            "integrity", "deserialization", "untrusted", "ci/cd", "pipeline",
            "auto-update", "plugin", "unsigned", "verification", "checksum",
            "tamper", "modification", "supply chain", "dependency confusion"
        ]
    },
    "A09:2021": {
        "name": "Security Logging and Monitoring Failures",
        "keywords": [
            "logging", "monitoring", "audit", "log", "event", "alert", "detection",
            "incident", "forensic", "trace", "tracking", "accountability",
            "no logging", "insufficient logging", "missing logs"
        ]
    },
    "A10:2021": {
        "name": "Server-Side Request Forgery (SSRF)",
        "keywords": [
            "ssrf", "server-side request", "internal", "localhost", "127.0.0.1",
            "metadata", "cloud", "aws", "azure", "gcp", "169.254.169.254",
            "url fetch", "webhook", "redirect", "open redirect"
        ]
    }
}

# Severity indicators for CVSS scoring
SEVERITY_KEYWORDS = {
    "critical": [
        "remote code execution", "rce", "arbitrary code", "system compromise",
        "root access", "admin access", "database access", "full control"
    ],
    "high": [
        "authentication bypass", "sql injection", "command injection",
        "privilege escalation", "sensitive data", "account takeover"
    ],
    "medium": [
        "xss", "csrf", "information disclosure", "session", "cookie",
        "weak encryption", "missing validation"
    ],
    "low": [
        "verbose error", "information leakage", "missing header",
        "autocomplete", "clickjacking", "cache"
    ]
}

# Spam indicators
SPAM_INDICATORS = [
    "test", "testing", "hello", "hi", "sample", "example",
    "asdf", "qwerty", "lorem ipsum", "placeholder",
    "xxx", "aaa", "bbb", "ccc"
]

def get_all_keywords():
    """Get all OWASP keywords as a flat list"""
    keywords = []
    for category in OWASP_CATEGORIES.values():
        keywords.extend(category["keywords"])
    return keywords

def get_category_by_code(code: str):
    """Get category details by OWASP code"""
    return OWASP_CATEGORIES.get(code, None)
