CREATE TABLE IF NOT EXISTS visitor_sessions (
    id          BIGSERIAL PRIMARY KEY,
    session_id  TEXT        NOT NULL UNIQUE,
    country_code TEXT,
    device_type TEXT,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS page_views (
    id          BIGSERIAL PRIMARY KEY,
    session_id  TEXT        NOT NULL REFERENCES visitor_sessions(session_id),
    page_path   TEXT        NOT NULL,
    referrer    TEXT        NOT NULL DEFAULT 'direct',
    viewed_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS page_aggregates (
    page_path   TEXT        PRIMARY KEY,
    total_views BIGINT      NOT NULL DEFAULT 0,
    last_updated TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS event_logs (
    id              BIGSERIAL PRIMARY KEY,
    session_id      TEXT        NOT NULL REFERENCES visitor_sessions(session_id),
    event_category  TEXT        NOT NULL,
    event_action    TEXT        NOT NULL,
    label           TEXT,
    logged_at       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
