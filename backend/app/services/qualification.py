from dataclasses import dataclass


RELEVANT_KEYWORDS = {
    "influencer",
    "brand",
    "creator",
    "ugc",
    "social media",
    "talent",
    "marketing agency",
    "campaign",
}


@dataclass
class QualificationResult:
    score: float
    status: str
    industry_relevance: float
    company_size_score: float
    online_authority: float
    activity_level: float
    decision_maker_probability: float


def qualify_lead(company_name: str, role: str | None, notes: str, website: str | None, linkedin_url: str | None) -> QualificationResult:
    haystack = f"{company_name} {role or ''} {notes} {website or ''} {linkedin_url or ''}".lower()

    industry_relevance = min(100.0, sum(14 for kw in RELEVANT_KEYWORDS if kw in haystack))
    company_size_score = 70.0 if "agency" in haystack else 55.0 if "consult" in haystack else 40.0
    online_authority = 80.0 if website and linkedin_url else 60.0 if website or linkedin_url else 25.0
    activity_level = 75.0 if "2024" in haystack or "2025" in haystack or "active" in haystack else 50.0
    decision_maker_probability = 85.0 if role and any(k in role.lower() for k in ["founder", "director", "head", "manager"]) else 55.0

    score = (
        industry_relevance * 0.30
        + company_size_score * 0.10
        + online_authority * 0.20
        + activity_level * 0.15
        + decision_maker_probability * 0.25
    )

    status = "Hot" if score >= 75 else "Warm" if score >= 55 else "Cold"

    return QualificationResult(
        score=round(score, 2),
        status=status,
        industry_relevance=industry_relevance,
        company_size_score=company_size_score,
        online_authority=online_authority,
        activity_level=activity_level,
        decision_maker_probability=decision_maker_probability,
    )
