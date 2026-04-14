from schemas import NotificationEvent
from utils.logger import get_logger

logger = get_logger("notification-service")


def send_notifications(event: NotificationEvent) -> None:
    logger.info(
        "SMS sent | contact=%s | message=%s | correlation_id=%s",
        event.contact,
        event.message,
        event.correlation_id,
    )
    return None
