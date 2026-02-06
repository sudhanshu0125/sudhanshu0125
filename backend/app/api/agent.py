from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config import settings
from ..db import get_db
from ..models import User
from ..schemas import AgentRunRequest, LeadOut
from ..security import get_current_user
from ..services.agent import LeadAgent
from ..services.discovery import LeadDiscoveryEngine

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run", response_model=list[LeadOut])
def run_agent(
    payload: AgentRunRequest,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    engine = LeadDiscoveryEngine(settings.serpapi_key)
    agent = LeadAgent(engine)
    return agent.run(db, query=payload.query, max_results=payload.max_results)
