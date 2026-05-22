from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analytics

app = FastAPI(title="Portfolio API", version="1.0.0")
app.include_router(analytics.router)
app.add_middleware(CORSMiddleware, allow_origins=["*"])
