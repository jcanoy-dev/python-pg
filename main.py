from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analytics
from workers import WorkerEntrypoint  #

app = FastAPI(title="Portfolio API", version="1.0.0")

# Setup Routing modules
app.include_router(analytics.router)

# Global policies setup
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# ⚠️ ADD THIS CLASS AT THE BOTTOM OF THE FILE
class Default(WorkerEntrypoint):
    async def fetch(self, request, env, ctx): # type: ignore
        return await app.fetch(request, env, ctx) # type: ignore
