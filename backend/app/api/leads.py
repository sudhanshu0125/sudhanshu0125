from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Lead, User
from ..schemas import LeadCreate, LeadOut, LeadUpdate
from ..security import get_current_user

router = APIRouter(prefix="/leads", tags=["leads"])


@router.get("/", response_model=list[LeadOut])
def list_leads(
    status: str | None = None,
    q: str | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Lead)
    if status:
        query = query.filter(Lead.status == status)
    if q:
        query = query.filter(Lead.company_name.ilike(f"%{q}%"))
    return query.order_by(Lead.score.desc(), Lead.created_at.desc()).limit(500).all()


@router.post("/", response_model=LeadOut)
def create_lead(payload: LeadCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    lead = Lead(**payload.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.patch("/{lead_id}", response_model=LeadOut)
def update_lead(lead_id: int, payload: LeadUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(lead, key, value)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
