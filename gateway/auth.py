import jwt
import os
from utils.logger import get_logger
from exceptions import InvalidTokenException

logger = get_logger("gateway")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")


def verify_token(token: str) -> dict:
    # TODO: implement full JWT validation
    # For now return a mock user
    # payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

    logger.info("Token verified | stub mode")

    return {"user_id": "usr-123", "role": "citizen"}
