from apscheduler.schedulers.background import BackgroundScheduler

from ..config import settings
from ..db import SessionLocal
from .agent import LeadAgent
from .discovery import LeadDiscoveryEngine

scheduler = BackgroundScheduler()


def scheduled_agent_run():
    db = SessionLocal()
    try:
        agent = LeadAgent(LeadDiscoveryEngine(settings.serpapi_key))
        agent.run(db, query="influencer marketing agency India brand partnerships", max_results=10)
    finally:
        db.close()


def start_scheduler():
    if scheduler.running:
        return
    scheduler.add_job(scheduled_agent_run, "interval", minutes=settings.agent_schedule_minutes, id="lead-agent", replace_existing=True)
    scheduler.start()
