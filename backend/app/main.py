from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import agent, auth, leads, outreach
from .config import settings
from .db import Base, engine
from .services.scheduler import start_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(leads.router, prefix="/api")
app.include_router(agent.router, prefix="/api")
app.include_router(outreach.router, prefix="/api")


@app.on_event("startup")
def startup_event():
    start_scheduler()


@app.get("/health")
def health():
    return {"status": "ok"}
