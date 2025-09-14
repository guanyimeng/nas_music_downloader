from datetime import datetime

from fastapi import APIRouter, Response, HTTPException
from pydantic import BaseModel

monitor_router = APIRouter()

class ReadinessResponse(BaseModel):
    utc_dt: datetime

class LivenessResponse(BaseModel):
    status: str

@monitor_router.get(
    "/readiness", 
    summary="Readiness Probe",
    response_model=ReadinessResponse
)
async def readiness_probe(response: Response):
    """
    Readiness probe endpoint to check if the service is ready.
    Returns 200 OK if ready, otherwise 503 Service Unavailable.
    """
    try:
        # Here you can add checks to ensure the service is ready
        # For simplicity, we'll assume it's always ready
        response.status_code = 200
    except Exception:
        raise HTTPException(status_code=503, detail="Service not ready")

    return ReadinessResponse(utc_dt=datetime.utcnow())

@monitor_router.get(
    "/liveness",
    summary="Liveness Probe",
    response_model=LivenessResponse
)
async def liveness_probe(response: Response):
    """
    Liveness probe endpoint to check if the service is alive.
    Returns 200 OK if alive, otherwise 500 Internal Server Error.
    """
    try:
        # Here you can add checks to ensure the service is alive
        # For simplicity, we'll assume it's always alive
        response.status_code = 200
        return {"status": "Success"}
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Service is not alive"
        )