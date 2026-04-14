from pydantic import BaseModel


class NotificationEvent(BaseModel):
    contact: str
    message: str
    correlation_id: str
