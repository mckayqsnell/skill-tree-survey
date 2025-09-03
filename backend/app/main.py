"""
FastAPI main application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config.settings import get_settings
from app.database.connection import init_db
from app.seeders.seeder import Seeder, get_db
from app.routes import questions, sessions, responses, admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    
    Args:
        app: FastAPI application
    """
    # Startup
    print("Starting up...")
    
    # Initialize database
    init_db()
    
    # Run seeder if enabled
    if settings.SEED_ON_STARTUP:
        db = next(get_db())
        try:
            seeder = Seeder(db)
            seeder.seed_database()
        finally:
            db.close()
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(questions.router, prefix=settings.API_PREFIX)
app.include_router(sessions.router, prefix=settings.API_PREFIX)
app.include_router(responses.router, prefix=settings.API_PREFIX)
app.include_router(admin.router, prefix=settings.API_PREFIX)


@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    
    Returns:
        Dict: Application status
    """
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    
    Returns:
        Dict: Health status
    """
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )