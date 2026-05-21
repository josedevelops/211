import uuid
from fastapi import APIRouter, HTTPException, Header, Request
from utils.logger import get_logger
from schemas import CitizenRequest, GatewayResponse
from auth import verify_token
from client import validate_address, create_request
from exceptions import (
    InvalidLocationAddress,
    RequestServiceExceptions,
)

logger = get_logger("gateway")
router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("/", response_model=GatewayResponse, status_code=202)
async def submit_request(
    payload: CitizenRequest, authorization: str = Header(None), request: Request = None
):
    # Step 1 - verify token
    user = verify_token(authorization)

    # Step 2 - generate correlation_id
    correlation_id = str(uuid.uuid4())
    trace_id = getattr(request.state, "trace_id", "-") if request else "-"
    logger.info(
        "Request received | trace_id=%s | correlation_id=%s", trace_id, correlation_id
    )

    # Step 3 - validate address
    location = await validate_address(payload.address, correlation_id, trace_id)

    # Step 4 - build request payload and create request
    request_payload = {
        "correlation_id": correlation_id,
        "user_id": user["user_id"],
        "full_name": payload.full_name,
        "address": location["address"],
        "district": location["district"],
        "coordinates": location["coordinates"],
        "issue": payload.issue,
        "contact": payload.contact,
    }
    await create_request(request_payload, user["user_id"], trace_id)

    # Step 5 - publish notification

    # Step 6 - return response
    return GatewayResponse(
        correlation_id=correlation_id,
        status="pending",
        message="Your request has been received and is being processed",
    )
