from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models import Lead
from .discovery import LeadDiscoveryEngine
from .extraction import enrich_from_website
from .qualification import qualify_lead


class LeadAgent:
    def __init__(self, discovery_engine: LeadDiscoveryEngine):
        self.discovery = discovery_engine

    def run(self, db: Session, query: str, max_results: int = 20) -> list[Lead]:
        candidates = self.discovery.discover(query=query, max_results=max_results)
        saved: list[Lead] = []

        for candidate in candidates:
            if self._is_duplicate(db, candidate.company_name, candidate.website, candidate.linkedin_url):
                continue

            enrichment = {}
            if candidate.website:
                try:
                    enrichment = enrich_from_website(candidate.website)
                except Exception:
                    enrichment = {}

            notes = candidate.notes
            if enrichment.get("notes_extra"):
                notes = f"{notes}. {enrichment['notes_extra']}"

            result = qualify_lead(
                company_name=candidate.company_name,
                role=None,
                notes=notes,
                website=candidate.website,
                linkedin_url=candidate.linkedin_url,
            )

            lead = Lead(
                company_name=candidate.company_name,
                website=candidate.website,
                linkedin_url=candidate.linkedin_url,
                notes=notes,
                email=enrichment.get("email"),
                phone=enrichment.get("phone"),
                source=candidate.source,
                score=result.score,
                status=result.status,
                industry_relevance=result.industry_relevance,
                company_size_score=result.company_size_score,
                online_authority=result.online_authority,
                activity_level=result.activity_level,
                decision_maker_probability=result.decision_maker_probability,
            )
            db.add(lead)
            saved.append(lead)

        db.commit()
        for item in saved:
            db.refresh(item)
        return saved

    @staticmethod
    def _is_duplicate(db: Session, company_name: str, website: str | None, linkedin_url: str | None) -> bool:
        query = db.query(Lead).filter(Lead.company_name == company_name)
        if website or linkedin_url:
            query = query.filter(or_(Lead.website == website, Lead.linkedin_url == linkedin_url))
        return db.query(query.exists()).scalar()
