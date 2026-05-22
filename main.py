from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analytics

app = FastAPI(title="Portfolio API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(analytics.router)
