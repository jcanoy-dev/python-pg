from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analytics
from workers import WorkerEntrypoint, Response
import asyncio
from urllib.parse import urlparse

_api = FastAPI(title="Portfolio API", version="1.0.0")
_api.include_router(analytics.router)
_api.add_middleware(CORSMiddleware, allow_origins=["*"])


class Default(WorkerEntrypoint):
    async def fetch(self, request: Any) -> Any:
        url = str(request.url)
        parsed = urlparse(url)

        try:
            headers = [
                (k.lower().encode("latin-1"), v.encode("latin-1"))
                for k, v in request.headers
            ]
        except Exception:
            headers = []

        scope: dict[str, Any] = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": request.method.upper(),
            "headers": headers,
            "path": parsed.path or "/",
            "query_string": (parsed.query or "").encode("latin-1"),
            "root_path": "",
            "server": (parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80)),
            "scheme": parsed.scheme,
        }

        try:
            body = bytes(await request.arrayBuffer())
        except Exception:
            body = b""

        body_sent = False

        async def receive() -> Any:
            nonlocal body_sent
            if not body_sent:
                body_sent = True
                return {"type": "http.request", "body": body, "more_body": False}
            await asyncio.sleep(3600)
            return {"type": "http.disconnect"}

        status_code = 200
        resp_headers: dict[str, str] = {}
        resp_body = bytearray()

        async def send(message: Any) -> None:
            nonlocal status_code, resp_headers
            if message["type"] == "http.response.start":
                status_code = message["status"]
                resp_headers = {
                    k.decode("latin-1"): v.decode("latin-1")
                    for k, v in message.get("headers", [])
                }
            elif message["type"] == "http.response.body":
                resp_body.extend(message.get("body", b""))

        await _api(scope, receive, send)
        return Response(bytes(resp_body), status=status_code, headers=resp_headers)
