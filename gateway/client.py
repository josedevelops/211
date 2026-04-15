import os
import httpx
from typing import Any, Dict
from utils.logger import get_logger
from exceptions import InvalidLocationAddress, RequestServiceExceptions


logger = get_logger("gateway")


LOCATION_SERVICE_URL = os.getenv("LOCATION_SERVICE_URL")
REQUEST_SERVICE_URL = os.getenv("REQUEST_SERVICE_URL")


async def validate_address(address: str, correlation_id: str) -> Dict[str, Any]:
    """
    Validate an address via location-service
    """
    headers = {
        "X-Correlation-ID": correlation_id,
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                LOCATION_SERVICE_URL,
                json={
                    "address": address,
                    "correlation_id": correlation_id,
                },
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error("Service call failed | error=%s", str(e), exc_info=True)
        raise InvalidLocationAddress()

    except Exception as e:
        logger.error("Unexpected error | error=%s", str(e), exc_info=True)
        raise


async def create_request(payload: Dict[str, Any], user: str) -> Dict[str, Any]:
    """
    Create a request via the request-service.
    """
    headers = {
        "X-User": user,
        "Content-Type": "application/json",
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                REQUEST_SERVICE_URL,
                json=payload,
                headers=headers,
                timeout=10.0,
            )
            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        logger.error("Service call failed | error=%s", str(e), exc_info=True)
        raise RequestServiceExceptions()

    except Exception as e:
        logger.error("Unexpected error | error=%s", str(e), exc_info=True)
        raise
