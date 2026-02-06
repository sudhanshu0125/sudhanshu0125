from dataclasses import dataclass
from urllib.parse import quote_plus

import httpx
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential

from .cache import cache


@dataclass
class DiscoveryCandidate:
    company_name: str
    website: str | None
    linkedin_url: str | None
    notes: str
    source: str = "google"


class LeadDiscoveryEngine:
    def __init__(self, serpapi_key: str | None = None):
        self.serpapi_key = serpapi_key

    def discover(self, query: str, max_results: int = 20) -> list[DiscoveryCandidate]:
        return cache.get_or_set(f"discover:{query}:{max_results}", 1800, lambda: self._discover_uncached(query, max_results))

    def _discover_uncached(self, query: str, max_results: int) -> list[DiscoveryCandidate]:
        if self.serpapi_key:
            return self._serpapi_search(query, max_results)
        return self._duckduckgo_search(query, max_results)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=6))
    def _duckduckgo_search(self, query: str, max_results: int) -> list[DiscoveryCandidate]:
        url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
        with httpx.Client(timeout=15) as client:
            response = client.get(url, follow_redirects=True)
            response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        candidates: list[DiscoveryCandidate] = []
        for result in soup.select(".result")[:max_results]:
            title = result.select_one(".result__title")
            link = result.select_one("a.result__a")
            snippet = result.select_one(".result__snippet")
            if not link:
                continue
            text = (title.get_text(" ", strip=True) if title else "Unknown company").split("|")[0].strip()
            href = link.get("href", "")
            lowered = href.lower()
            linkedin_url = href if "linkedin.com" in lowered else None
            website = None if linkedin_url else href
            candidates.append(
                DiscoveryCandidate(
                    company_name=text[:255],
                    website=website,
                    linkedin_url=linkedin_url,
                    notes=snippet.get_text(" ", strip=True) if snippet else "Potential lead discovered via web search",
                )
            )
        return candidates

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=6))
    def _serpapi_search(self, query: str, max_results: int) -> list[DiscoveryCandidate]:
        with httpx.Client(timeout=15) as client:
            response = client.get(
                "https://serpapi.com/search.json",
                params={"q": query, "engine": "google", "api_key": self.serpapi_key, "num": max_results},
            )
            response.raise_for_status()
            data = response.json()

        candidates: list[DiscoveryCandidate] = []
        for row in data.get("organic_results", [])[:max_results]:
            link = row.get("link")
            if not link:
                continue
            company_name = (row.get("title") or "Unknown company").split("|")[0][:255]
            lowered = link.lower()
            linkedin_url = link if "linkedin.com" in lowered else None
            website = None if linkedin_url else link
            candidates.append(
                DiscoveryCandidate(
                    company_name=company_name,
                    website=website,
                    linkedin_url=linkedin_url,
                    notes=row.get("snippet", "Potential lead discovered via Google/SerpAPI"),
                    source="serpapi",
                )
            )
        return candidates
