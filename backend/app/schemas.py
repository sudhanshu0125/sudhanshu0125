from datetime import datetime

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LeadBase(BaseModel):
    name: str | None = None
    company_name: str
    role: str | None = None
    email: str | None = None
    phone: str | None = None
    whatsapp: str | None = None
    linkedin_url: str | None = None
    website: str | None = None
    location: str | None = None
    notes: str | None = None


class LeadCreate(LeadBase):
    source: str = "manual"


class LeadUpdate(BaseModel):
    status: str | None = None
    approved: bool | None = None
    notes: str | None = None
    outreach_state: str | None = None


class LeadOut(LeadBase):
    id: int
    source: str
    score: float
    status: str
    approved: bool
    outreach_state: str
    created_at: datetime

    class Config:
        from_attributes = True


class AgentRunRequest(BaseModel):
    query: str = "influencer marketing agencies india brand partnerships"
    max_results: int = 20


class OutreachRequest(BaseModel):
    lead_id: int
    channel: str = "email"
    message: str
