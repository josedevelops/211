from pydantic import BaseModel


class CitizenRequest(BaseModel):
    full_name: str
    address: str
    issue: str
    contact: str


class GatewayResponse(BaseModel):
    correlation_id: str
    status: str
    message: str
