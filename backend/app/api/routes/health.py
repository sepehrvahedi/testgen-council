"""
Health check and configuration endpoints
"""

from datetime import datetime

from fastapi import APIRouter
from loguru import logger

from app.config import config
from app.models.responses import HealthResponse, ConfigResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the service is running and return configuration info"
)
async def health_check():
    """
    Health check endpoint

    Returns service status and basic configuration information
    """
    try:
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            models_available=len(config.LLM_MODELS),
            roles_available=len(config.ROLES)
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            version="1.0.0",
            timestamp=datetime.utcnow(),
            models_available=0,
            roles_available=0
        )


@router.get(
    "/config",
    response_model=ConfigResponse,
    summary="Get Configuration",
    description="Get available models, roles, and clustering methods"
)
async def get_config():
    """
    Get system configuration

    Returns:
        ConfigResponse: Available models, roles, and clustering methods
    """
    try:
        return ConfigResponse(
            models=config.get_models_info(),
            roles=config.get_roles_info(),
            clustering_methods=config.get_clustering_methods_info(),
            test_categories=config.TEST_CATEGORIES
        )
    except Exception as e:
        logger.error(f"Failed to get config: {e}")
        raise
