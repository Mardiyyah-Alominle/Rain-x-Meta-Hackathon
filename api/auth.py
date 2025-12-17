from fastapi import HTTPException, status, Request
from config import Config


def verify_api_key(request: Request):
    """Verify API key for admin endpoints"""
    api_key = request.headers.get("X-API-Key")
    expected_key = Config.ADMIN_API_KEY

    if not expected_key:
        # If no API key is configured, skip authentication (for development)
        return

    if not api_key or api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )
