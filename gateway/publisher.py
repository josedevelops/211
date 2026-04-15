import os
import json
import aio_pika
from utils.logger import get_logger
from exceptions import PublisherException


RABBITMQ_URL = os.getenv("RABBITMQ_URL")
logger = get_logger("Publisher")


async def publish_notification(correlation_id, contact, message):
    logger.info("Starting publisher....")
    try:
        connection = await aio_pika.connect_robust(RABBITMQ_URL)
        channel = await connection.channel()
        data = json.dumps(
            {
                "correlation_id": correlation_id,
                "contact": contact,
                "message": message,
            }
        )
        await channel.default_exchange.publish(
            aio_pika.Message(body=data.encode()), routing_key="notifications.send"
        )
        logger.info("Notification published | correlation_id=%s", correlation_id)
        await connection.close()

    except Exception as e:
        logger.error(
            "Failed to publish | correlation_id=%s | error=%s",
            correlation_id,
            str(e),
            exc_info=True,
        )
        raise PublisherException(str(e))
