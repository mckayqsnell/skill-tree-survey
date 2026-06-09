"""
FastAPI main application entry point.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.connection import init_db, reset_db
from app.routes import admin, categories, questions, responses, sessions
from app.seeders.seeder import Seeder, get_db

logger = settings.logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.

    Args:
        app: FastAPI application
    """
    # Startup
    logger.info(
        "Starting up",
        app_version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )

    # Check if database reset is requested
    if settings.RESET_DATABASE:
        logger.warning("RESET_DATABASE enabled - resetting database and reseeding")
        # Reset database (drop all tables and recreate)
        reset_db()

        # Run seeder to populate with initial data
        db = next(get_db())
        try:
            seeder = Seeder(db)
            count = seeder.seed_database()
            logger.info("Database reset complete", base_questions_seeded=count)
        finally:
            db.close()
    else:
        # Normal startup - just ensure tables exist
        init_db()

        # Try to seed if database is empty (backward compatibility)
        db = next(get_db())
        try:
            seeder = Seeder(db)
            if seeder.is_database_empty():
                logger.info("Database is empty, seeding with initial data")
                seeder.seed_database()

            # Clean up Pokemon from category orders if it exists
            from app.dao.factory import DAOFactory

            dao_factory = DAOFactory(db)
            category_dao = dao_factory.get_category_dao()

            # Check if Pokemon exists and delete it
            pokemon_category = category_dao.get_by_category("Pokemon")
            if pokemon_category:
                logger.info("Removing Pokemon from category orders")
                category_dao.delete("Pokemon")
        except Exception:
            # uvicorn --workers N runs this lifespan in every worker process;
            # whichever worker loses the seed/cleanup race must not die on the
            # SQLite write conflict — the winner already did the work.
            logger.warning(
                "Startup seed/cleanup skipped (another worker likely won the race)",
                exc_info=True,
            )
        finally:
            db.close()

    yield

    # Shutdown
    logger.info("Shutting down")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
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
app.include_router(categories.router, prefix=settings.API_PREFIX)
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
        "status": "healthy",
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

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)
