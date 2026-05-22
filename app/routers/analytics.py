from typing import Any
from fastapi import APIRouter, Depends, Request, BackgroundTasks

from app.database.db_client import get_db_client
from app.schemas.analytics import AnalyticsPayload
from app.core.security import generate_session_id, extract_device_and_country
from app.database.services import run_d1_analytics_pipeline

router = APIRouter(prefix="/api/analytics", tags=["Analytics Collection"])

@router.post("", status_code=202)
async def track_visit(
    payload: AnalyticsPayload,
    request: Request,
    background_tasks: BackgroundTasks,
    db: Any = Depends(get_db_client)
):
    session_id = generate_session_id(request)
    country, device = extract_device_and_country(request)

    background_tasks.add_task(
        run_d1_analytics_pipeline,
        db,
        session_id,
        country,
        device,
        payload
    )

    return {"status": "accepted"}
