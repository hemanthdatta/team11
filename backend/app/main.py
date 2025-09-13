import sys
import os

# Add the parent directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, customers, referrals, dashboard, social, ai_assistant, digital_presence, messaging, ai_image_generator
from app.core.security_utils import SecurityHeadersMiddleware, limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

def create_app():
    app = FastAPI(
        title="Micro-Entrepreneur Growth App",
        description="Backend API for Micro-Entrepreneur Growth App",
        version="0.1.0"
    )
    
    # Add security middleware
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Add CORS middleware - configure based on environment
    import os
    allowed_origins = ["http://localhost:5000", "http://127.0.0.1:5000", "http://0.0.0.0:5000"]
    
    # Add production domain if deployed
    if os.getenv("REPLIT_DOMAIN"):
        allowed_origins.append(f"https://{os.getenv('REPLIT_DOMAIN')}")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=False,  # Disabled for security
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Add rate limiter
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    
    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(customers.router, prefix="/customers", tags=["customers"])
    app.include_router(referrals.router, prefix="/referrals", tags=["referrals"])
    app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
    app.include_router(social.router, prefix="/social", tags=["social"])
    app.include_router(ai_assistant.router, prefix="/ai", tags=["ai"])
    app.include_router(ai_image_generator.router, prefix="/ai", tags=["ai"])
    app.include_router(digital_presence.router, prefix="/digital-presence", tags=["digital-presence"])
    app.include_router(messaging.router, prefix="/messaging", tags=["messaging"])
    
    @app.get("/")
    async def root():
        return {"message": "Micro-Entrepreneur Growth App API"}
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    import os
    host = "0.0.0.0" if os.getenv("PORT") else "127.0.0.1"  # Production vs dev
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host=host, port=port, reload=True)