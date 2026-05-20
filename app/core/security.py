import hashlib
from datetime import datetime, timezone
from typing import Tuple  
from fastapi import Request

def generate_session_id(request: Request) -> str:
    """
    Creates an anonymous daily session hash unique to the user.
    Changes every midnight so users can never be tracked across multiple days.
    """
    # 1. Grab client network identifiers safely
    ip = request.client.host if request.client else "unknown_ip"
    user_agent = request.headers.get("user-agent", "unknown_ua")
    
    # 2. Get current date string acting as a rolling security salt
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # 3. Concatenate and generate a non-reversible cryptographic SHA-256 hash
    raw_signature = f"{ip}-{user_agent}-{today}"
    return hashlib.sha256(raw_signature.encode("utf-8")).hexdigest()



def extract_device_and_country(request: Request) -> Tuple[str, str]:
    """
    Extracts geographic data and identifies client form-factors.
    Leverages native Cloudflare geographic geolocation proxy headers if available.
    """
    # Cloudflare proxies automatically inject 'cf-ipcountry' header for free!
    country = request.headers.get("cf-ipcountry", "UNK").upper()
    
    # Simple user-agent parser to classify device profiles
    user_agent = request.headers.get("user-agent", "").lower()
    
    if "mobile" in user_agent:
        device = "mobile"
    elif "tablet" in user_agent or "ipad" in user_agent:
        device = "tablet"
    else:
        device = "desktop"
        
    return country, device
