import re

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_fixed

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{3,5}\)?[\s-]?)?\d{3,5}[\s-]?\d{4,6}")


@retry(stop=stop_after_attempt(2), wait=wait_fixed(1))
def enrich_from_website(url: str | None) -> dict:
    if not url:
        return {}

    with httpx.Client(timeout=10) as client:
        response = client.get(url, follow_redirects=True)
        response.raise_for_status()

    text = response.text[:200_000]
    soup = BeautifulSoup(text, "html.parser")
    content = soup.get_text(" ", strip=True)
    emails = EMAIL_RE.findall(content)
    phones = PHONE_RE.findall(content)

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "notes_extra": f"Website title: {(soup.title.string if soup.title else 'N/A')[:120]}",
    }
