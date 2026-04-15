from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from utils.logger import get_logger
from api.v1.requests import router as request_router

logger = get_logger("gateway")


# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Gateway service starting up...")
    yield
    logger.info("Gateway service shutting down...")


# FastAPI App
app = FastAPI(lifespan=lifespan, redirect_slashes=False)
app.include_router(request_router, prefix="/api/v1")


# Custom Exception
class GatewayException(Exception):
    """Custom exception for gateway-level errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


# Global Exception Handlers
@app.exception_handler(GatewayException)
async def gateway_exception_handler(request: Request, exc: GatewayException):
    logger.error("GatewayException occurred: %s", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Gateway error",
            "request_id": request.headers.get("X-Request-ID"),
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "request_id": request.headers.get("X-Request-ID"),
        },
    )


# Health Endpoint
@app.get("/health")
async def health():
    try:
        logger.info("Health check invoked")
        return {"status": "ok"}
    except Exception as exc:
        logger.error("Health check failure: %s", exc)
        raise GatewayException("Health check failed", status_code=500)
