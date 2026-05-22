from typing import Any
from app.schemas.analytics import AnalyticsPayload

def run_d1_analytics_pipeline(db: Any, session_id: str, country: str, device: str, payload: AnalyticsPayload):
    try:
        with db.cursor() as cur:
            cur.execute("""
                INSERT INTO visitor_sessions (session_id, country_code, device_type)
                VALUES (%s, %s, %s)
                ON CONFLICT (session_id) DO UPDATE SET last_seen_at = CURRENT_TIMESTAMP;
            """, [session_id, country, device])

            cur.execute("""
                INSERT INTO page_views (session_id, page_path, referrer)
                VALUES (%s, %s, %s);
            """, [session_id, payload.page_path, payload.referrer or "direct"])

            cur.execute("""
                INSERT INTO page_aggregates (page_path, total_views)
                VALUES (%s, 1)
                ON CONFLICT (page_path) DO UPDATE SET total_views = page_aggregates.total_views + 1, last_updated = CURRENT_TIMESTAMP;
            """, [payload.page_path])

            if payload.event_category and payload.event_action:
                cur.execute("""
                    INSERT INTO event_logs (session_id, event_category, event_action, label)
                    VALUES (%s, %s, %s, %s);
                """, [session_id, payload.event_category, payload.event_action, payload.event_label])

        db.commit()
        print(f"Analytics pipeline logged for session: {session_id[:8]}...")

    except Exception as e:
        db.rollback()
        print(f"Analytics pipeline failed: {e}")
    finally:
        db.close()
