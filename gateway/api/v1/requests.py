import uuid
from fastapi import APIRouter, HTTPException, Header
from utils.logger import get_logger
from schemas import CitizenRequest, GatewayResponse
from auth import verify_token
from client import validate_address, create_request
from publisher import publish_notification
from exceptions import (
    InvalidLocationAddress,
    RequestServiceExceptions,
    PublisherException,
)

logger = get_logger("gateway")
router = APIRouter(prefix="/requests", tags=["Requests"])


@router.post("/", response_model=GatewayResponse, status_code=202)
async def submit_request(payload: CitizenRequest, authorization: str = Header(None)):
    # Step 1 - verify token
    user = verify_token(authorization)

    # Step 2 - generate correlation_id
    correlation_id = str(uuid.uuid4())

    # Step 3 - validate address
    location = await validate_address(payload.address, correlation_id)

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
    await create_request(request_payload, user["user_id"])

    # Step 5 - publish notification
    await publish_notification(
        correlation_id=correlation_id,
        contact=payload.contact,
        message=f"Your request {correlation_id} has been received",
    )

    # Step 6 - return response
    return GatewayResponse(
        correlation_id=correlation_id,
        status="pending",
        message="Your request has been received and is being processed",
    )
