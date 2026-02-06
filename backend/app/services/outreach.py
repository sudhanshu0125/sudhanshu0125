from datetime import datetime


def generate_outreach_message(company_name: str, notes: str) -> str:
    return (
        f"Hi {company_name} team,\n\n"
        "I am reaching out from InfluencersPlace, where brands and agencies launch performance-driven influencer campaigns. "
        f"We noticed your fit: {notes[:180]}.\n\n"
        "Would you be open to a quick call to discuss partnership opportunities?\n\n"
        f"Sent by AI Agent on {datetime.utcnow().isoformat()} UTC"
    )
