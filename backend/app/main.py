"""
Main FastAPI application entry point for Intelligent Test Council
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.config import settings, config
from app.api.routes import test_generation, health


# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO" if not settings.DEBUG else "DEBUG"
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for the application"""
    # Startup
    logger.info("🚀 Starting Intelligent Test Council Backend")
    logger.info(f"📊 Models configured: {len(config.LLM_MODELS)}")
    logger.info(f"🎭 Roles configured: {len(config.ROLES)}")
    logger.info(f"🔧 Debug mode: {settings.DEBUG}")

    yield

    # Shutdown
    logger.info("👋 Shutting down Intelligent Test Council Backend")


# Create FastAPI application
app = FastAPI(
    title="Intelligent Test Council API",
    description="Multi-Agent LLM System for Intelligent Test Generation with Role-Based Prompting and Hybrid Clustering",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
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
app.include_router(
    health.router,
    prefix="/api/v1",
    tags=["Health"]
)

app.include_router(
    test_generation.router,
    prefix="/api/v1",
    tags=["Test Generation"]
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Intelligent Test Council API",
        "version": "1.0.0",
        "description": "Multi-Agent LLM System for Test Generation",
        "docs": "/api/docs" if settings.DEBUG else None,
        "health": "/api/v1/health",
        "endpoints": {
            "generate_tests": "/api/v1/generate-tests",
            "config": "/api/v1/config"
        }
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
