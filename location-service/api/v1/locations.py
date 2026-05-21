from client import validate_address
from fastapi import APIRouter, HTTPException, Request
from utils.logger import get_logger
from exceptions import AddressNotFoundException, NominatimServiceException
from schemas import AddressValidationRequest, AddressValidationResponse


logger = get_logger("locations-service")
router = APIRouter(prefix="/validate", tags=["Validate"])


@router.post("/", response_model=AddressValidationResponse, status_code=200)
async def create_location(payload: AddressValidationRequest, request: Request = None):
    trace_id = getattr(request.state, "trace_id", "-") if request else "-"
    try:
        logger.info("POST /locations | trace_id=%s | correlation=%s", trace_id, payload.correlation_id)
        results = await validate_address(payload.address)

        if not results:
            raise AddressNotFoundException(correlation_id=payload.correlation_id)

        result = results[0]

        return AddressValidationResponse(
            correlation_id=payload.correlation_id,
            valid=True,
            address=result.get("display_name", ""),
            district=result.get("address", {}).get("city")
            or result.get("address", {}).get("town")
            or result.get("address", {}).get("county", "Unknown"),
            coordinates={
                "lat": float(result.get("lat", 0)),
                "lng": float(result.get("lon", 0)),
            },
        )
    except AddressNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e.message))

    except NominatimServiceException as e:
        raise HTTPException(status_code=503, detail=str(e.message))
