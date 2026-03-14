"""
FastAPI Backend Entry Point
Anti-Gravity Bug Bounty Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Import routers
from app.api.routes import analysis

# Import ML models loader (to be created)
# from app.ml.model_loader import load_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events
    """
    # Startup: Load AI/ML models
    print("🚀 Loading AI/ML models...")
    # Pre-load the analyzer to download the model
    from app.ml.analyzer import get_analyzer
    analyzer = get_analyzer()
    print("✅ Models loaded successfully")
    
    yield
    
    # Shutdown: Cleanup
    print("👋 Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title="Anti-Gravity Bug Bounty API",
    description="AI-driven decentralized bug bounty platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8501",  # Streamlit demo
        # Add production domains here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "service": "anti-gravity-bug-bounty",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """
    API root endpoint
    """
    return {
        "message": "Anti-Gravity Bug Bounty Platform API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "analyze_report": "/api/v1/analyze-report",
            "owasp_categories": "/api/v1/owasp-categories"
        }
    }

# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["AI Analysis"])

# Future routers (uncomment when created)
# app.include_router(bugs.router, prefix="/api/v1/bugs", tags=["Bug Reports"])
# app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
# app.include_router(reputation.router, prefix="/api/v1/reputation", tags=["Reputation"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
