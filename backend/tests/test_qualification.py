from app.services.qualification import qualify_lead


def test_qualification_hot_for_relevant_agency():
    result = qualify_lead(
        company_name="Top Influencer Marketing Agency",
        role="Founder",
        notes="Active influencer campaigns in 2025 for creator economy",
        website="https://example.com",
        linkedin_url="https://linkedin.com/company/example",
    )
    assert result.score > 70
    assert result.status in {"Hot", "Warm"}
