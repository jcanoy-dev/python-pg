from typing import Any
from fastapi import APIRouter, Depends, Request, BackgroundTasks

from app.database.d1_client import get_d1_client
from app.schemas.analytics import AnalyticsPayload
from app.core.security import generate_session_id, extract_device_and_country
from app.database.services import run_d1_analytics_pipeline

router = APIRouter(prefix="/api/analytics", tags=["Analytics Collection"])

@router.post("", status_code=202)
async def track_visit(
    payload: AnalyticsPayload,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Any = Depends(get_d1_client)
):
    session_id = generate_session_id(request)
    country, device = extract_device_and_country(request)
    
    # Pass the function and ALL its parameters to the background worker pool
    background_tasks.add_task(
        run_d1_analytics_pipeline, 
        db, 
        session_id, 
        country, 
        device, 
        payload
    )
    
    # Immediately drops the client browser connection with a 202 Accepted status
    return {"status": "accepted"}
