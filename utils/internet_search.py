import requests
from bs4 import BeautifulSoup


def search_web(query: str, max_results: int = 5):
    """
    Free web search using DuckDuckGo HTML scraping.
    Returns list of dicts: [{title, url, snippet}, ...]
    """
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
    except Exception:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    results = []

    for res in soup.select(".result")[:max_results]:
        a = res.select_one(".result__a")
        snippet = res.select_one(".result__snippet")

        if not a:
            continue

        results.append({
            "title": a.get_text(strip=True),
            "url": a.get("href", ""),
            "snippet": snippet.get_text(strip=True) if snippet else ""
        })

    return results
