from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analytics
from workers import WorkersASGI

_app = FastAPI(title="Portfolio API", version="1.0.0")
_app.include_router(analytics.router)
_app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Register the ASGI app as a Cloudflare Workers fetch handler
app = WorkersASGI(_app)
