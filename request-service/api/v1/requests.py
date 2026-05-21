from fastapi import APIRouter, HTTPException, Request
from utils.logger import get_logger
from schemas import ServiceRequestCreate, ServiceRequestResponse
from services import RequestService
from exceptions import DuplicateCorrelationIdException

logger = get_logger("request-service")
router = APIRouter(prefix="/requests", tags=["Requests"])
service = RequestService()


@router.post("/", response_model=ServiceRequestResponse, status_code=202)
async def create_request(payload: ServiceRequestCreate, request: Request = None):
    trace_id = getattr(request.state, "trace_id", "-") if request else "-"
    try:
        logger.info("POST /requests | trace_id=%s | correlation_id=%s", trace_id, payload.correlation_id)
        result = await service.create_request(payload)
        return ServiceRequestResponse(
            correlation_id=result.correlation_id,
            status=result.status.value,
        )
    except DuplicateCorrelationIdException as e:
        raise HTTPException(status_code=409, detail=str(e.message))


@router.get("/{correlation_id}", response_model=ServiceRequestResponse, status_code=200)
async def get_by_correlation_id(correlation_id: str):
    logger.info("GET /requests/%s", correlation_id)
    result = service.get_by_correlation_id(correlation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Request not found")
    return ServiceRequestResponse(
        correlation_id=result.correlation_id,
        status=result.status.value,
    )


@router.get("/", response_model=list[ServiceRequestResponse], status_code=200)
async def get_all_requests():
    logger.info("GET /requests | Fetching all")
    results = service.get_all()
    return [
        ServiceRequestResponse(
            correlation_id=r.correlation_id,
            status=r.status.value,
        )
        for r in results
    ]


@router.patch(
    "/{correlation_id}/status", response_model=ServiceRequestResponse, status_code=200
)
async def update_request_status(correlation_id: str, status: str):
    logger.info(
        "PATCH /requests | correlation_id=%s | status=%s", correlation_id, status
    )
    result = service.update_status(correlation_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Request not found")
    return ServiceRequestResponse(
        correlation_id=result.correlation_id,
        status=result.status.value,
    )
