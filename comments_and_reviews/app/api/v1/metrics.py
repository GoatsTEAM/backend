from fastapi import APIRouter, Response
from prometheus_client import generate_latest

router = APIRouter()


@router.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
