import os
import aio_pika
import json
from schemas import NotificationEvent
from notifier import send_notifications
from utils.logger import get_logger


RABBITMQ_URL = os.getenv("RABBITMQ_URL")

logger = get_logger("notification-service")


async def start_consumer():
    logger.info("Starting connection...")

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("notifications.send")
    logger.info("Consumer listening | queue=notifications.send")

    async for message in queue:
        async with message.process():
            body = message.body.decode()
            data = json.loads(body)
            event = NotificationEvent(**data)
            logger.info("Message received | correlation_id=%s", event.correlation_id)
            send_notifications(event)
