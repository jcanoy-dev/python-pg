from cloudflare import Cloudflare
from app.core.config import settings
from app.schemas.analytics import AnalyticsPayload

def run_d1_analytics_pipeline(
    db: Cloudflare, 
    session_id: str, 
    country: str, 
    device: str, 
    payload: AnalyticsPayload
):
    """
    Executes raw SQL mutations sequentially on your remote D1 instance.
    Since Cloudflare's standard .query API executes one statement per network call,
    we run them one by one.
    """
    try:
        # 1. Ensure the user session exists
        db.d1.database.query(
            account_id=settings.CLOUDFLARE_ACCOUNT_ID,
            database_id=settings.D1_DATABASE_ID,
            sql="""
                INSERT INTO visitor_sessions (session_id, country_code, device_type) 
                VALUES (?, ?, ?)
                ON CONFLICT(session_id) DO UPDATE SET last_seen_at = CURRENT_TIMESTAMP;
            """,
            params=[session_id, country, device]
        )

        # 2. Log the unique page hit
        db.d1.database.query(
            account_id=settings.CLOUDFLARE_ACCOUNT_ID,
            database_id=settings.D1_DATABASE_ID,
            sql="""
                INSERT INTO page_views (session_id, page_path, referrer) 
                VALUES (?, ?, ?);
            """,
            params=[session_id, payload.page_path, payload.referrer or 'direct']
        )

        # 3. Update your quick-read aggregate total metrics cache
        db.d1.database.query(
            account_id=settings.CLOUDFLARE_ACCOUNT_ID,
            database_id=settings.D1_DATABASE_ID,
            sql="""
                INSERT INTO page_aggregates (page_path, total_views) 
                VALUES (?, 1) 
                ON CONFLICT(page_path) DO UPDATE SET total_views = total_views + 1, last_updated = CURRENT_TIMESTAMP;
            """,
            params=[payload.page_path]
        )

        # 4. Optional: If your frontend submitted a custom user click interaction event
        if payload.event_category and payload.event_action:
            db.d1.database.query(
                account_id=settings.CLOUDFLARE_ACCOUNT_ID,
                database_id=settings.D1_DATABASE_ID,
                sql="""
                    INSERT INTO event_logs (session_id, event_category, event_action, label) 
                    VALUES (?, ?, ?, ?);
                """,
                params=[session_id, payload.event_category, payload.event_action, payload.event_label]
            )

        print(f"🎉 Successfully logged analytics pipeline for session: {session_id[:8]}...")

    except Exception as e:
        # Crucial for background tasks because exceptions here do not reach the client browser
        print(f"❌ Background D1 Analytics Pipeline Failed: {e}")
