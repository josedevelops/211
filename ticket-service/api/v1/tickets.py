from fastapi import APIRouter, HTTPException, Request
from utils.logger import get_logger
from schemas import TicketCreate, TicketResponse
from services import TicketService
from exceptions import DuplicateCorrelationIdException

logger = get_logger("ticket-service")
router = APIRouter(prefix="/tickets", tags=["Tickets"])
service = TicketService()


@router.post("/", response_model=TicketResponse, status_code=202)
async def create_ticket(payload: TicketCreate, request: Request = None):
    trace_id = getattr(request.state, "trace_id", "-") if request else "-"
    try:
        logger.info("POST /tickets | trace_id=%s | correlation=%s", trace_id, payload.correlation_id)
        result = service.create_ticket(payload)
        return TicketResponse(
            correlation_id=result.correlation_id,
            status=result.status.value,
            priority=result.priority.value,
        )
    except DuplicateCorrelationIdException as e:
        raise HTTPException(status_code=409, detail=str(e.message))


@router.get("/{correlation_id}", response_model=TicketResponse, status_code=200)
async def get_by_correlation_id(correlation_id: str):
    logger.info("GET /tickets/%s", correlation_id)
    result = service.get_by_correlation_id(correlation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse(
        correlation_id=result.correlation_id,
        status=result.status.value,
        priority=result.priority.value,
    )


@router.get("/", response_model=list[TicketResponse], status_code=200)
async def get_all_requests():
    logger.info("Get /tickets | Fectching all")
    results = service.get_all()
    return [
        TicketResponse(
            correlation_id=r.correlation_id,
            status=r.status.value,
            priority=r.priority.value,
        )
        for r in results
    ]


@router.patch(
    "/{correlation_id}/status", response_model=TicketResponse, status_code=200
)
async def update_request_status(correlation_id: str, status: str):
    logger.info(
        "PATCH /tickets | correlation_id=%s | status=%s", correlation_id, status
    )
    result = service.update_status(correlation_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return TicketResponse(
        correlation_id=result.correlation_id,
        status=result.status.value,
        priority=result.priority.value,
    )
