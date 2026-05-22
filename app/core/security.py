import hashlib
import httpx
from datetime import datetime, timezone
from typing import Tuple
from fastapi import Request

_LOCAL_IPS = {"127.0.0.1", "::1", "unknown_ip"}


def generate_session_id(request: Request) -> str:
    ip = request.client.host if request.client else "unknown_ip"
    user_agent = request.headers.get("user-agent", "unknown_ua")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    raw_signature = f"{ip}-{user_agent}-{today}"
    return hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()


def _get_client_ip(request: Request) -> str | None:
    # Vercel (and most reverse proxies) put the real IP in x-forwarded-for
    forwarded = request.headers.get("x-forwarded-for", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else None


async def _lookup_country(ip: str) -> str:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            res = await client.get(f"http://ip-api.com/json/{ip}?fields=countryCode")
            if res.status_code == 200:
                return res.json().get("countryCode", "UNK").upper()
    except Exception:
        pass
    return "UNK"


async def extract_device_and_country(request: Request) -> Tuple[str, str]:
    ip = _get_client_ip(request)
    country = await _lookup_country(ip) if ip and ip not in _LOCAL_IPS else "UNK"

    user_agent = request.headers.get("user-agent", "").lower()
    if "mobile" in user_agent:
        device = "mobile"
    elif "tablet" in user_agent or "ipad" in user_agent:
        device = "tablet"
    else:
        device = "desktop"

    return country, device
