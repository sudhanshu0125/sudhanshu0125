from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Lead, User
from ..schemas import OutreachRequest
from ..security import get_current_user
from ..services.outreach import generate_outreach_message

router = APIRouter(prefix="/outreach", tags=["outreach"])


@router.post("/trigger")
def trigger_outreach(payload: OutreachRequest, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == payload.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    lead.outreach_state = f"queued:{payload.channel}"
    db.add(lead)
    db.commit()

    return {
        "lead_id": lead.id,
        "channel": payload.channel,
        "message_preview": payload.message or generate_outreach_message(lead.company_name, lead.notes or "Relevant lead"),
        "state": lead.outreach_state,
    }
