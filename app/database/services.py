from typing import Any
from app.schemas.analytics import AnalyticsPayload

def run_d1_analytics_pipeline(db: Any, session_id: str, country: str, device: str, payload: AnalyticsPayload):
    try:
        db.prepare("""
            INSERT INTO visitor_sessions (session_id, country_code, device_type)
            VALUES (?, ?, ?)
            ON CONFLICT(session_id) DO UPDATE SET last_seen_at = CURRENT_TIMESTAMP;
        """).bind(session_id, country, device).run()

        db.prepare("""
            INSERT INTO page_views (session_id, page_path, referrer)
            VALUES (?, ?, ?);
        """).bind(session_id, payload.page_path, payload.referrer or "direct").run()

        db.prepare("""
            INSERT INTO page_aggregates (page_path, total_views)
            VALUES (?, 1)
            ON CONFLICT(page_path) DO UPDATE SET total_views = total_views + 1, last_updated = CURRENT_TIMESTAMP;
        """).bind(payload.page_path).run()

        if payload.event_category and payload.event_action:
            db.prepare("""
                INSERT INTO event_logs (session_id, event_category, event_action, label)
                VALUES (?, ?, ?, ?);
            """).bind(session_id, payload.event_category, payload.event_action, payload.event_label).run()

        print(f"Analytics pipeline logged for session: {session_id[:8]}...")

    except Exception as e:
        print(f"D1 analytics pipeline failed: {e}")
