# Portfolio Analytics API

A lightweight analytics engine built with FastAPI, deployed on Vercel, and backed by a Neon (serverless PostgreSQL) database. Tracks visitor sessions, page views, and custom events for a portfolio site.

## Stack

- **FastAPI** — API framework
- **Neon** — serverless PostgreSQL
- **psycopg2** — database driver
- **Vercel** — deployment

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/analytics` | Track a page view or custom event |

### Request Body

```json
{
  "page_path": "/projects/chat-app",
  "referrer": "github.com",
  "event_category": "button_click",
  "event_action": "download_resume",
  "event_label": "English CV PDF"
}
```

- `page_path` — required
- `referrer`, `event_category`, `event_action`, `event_label` — optional

### Response

```json
{ "status": "accepted" }
```

## Database Schema

Run `scripts/create_tables.sql` in the Neon SQL Editor to set up the required tables:

- `visitor_sessions` — one row per anonymous daily session
- `page_views` — one row per page visit
- `page_aggregates` — running totals per page path
- `event_logs` — custom events (clicks, downloads, etc.)

## Setup

1. Clone the repo and create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate       # Windows
pip install -e .
```

2. Copy `.env` and set your Neon connection string:

```
DATABASE_URL=postgresql://...
```

3. Run the table setup SQL in the Neon dashboard (`scripts/create_tables.sql`).

4. Start the dev server:

```bash
uvicorn main:app --reload
```

## Deployment

Deployed via Vercel using `@vercel/python`. Set `DATABASE_URL` as an environment variable in the Vercel project settings.
