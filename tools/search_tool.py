import requests
from bs4 import BeautifulSoup


def simple_web_search(query: str):
    """
    Simple demo search tool.
    This does not use Google API.
    It fetches DuckDuckGo HTML search results.
    """

    url = "https://html.duckduckgo.com/html/"
    params = {"q": query}

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.post(url, data=params, headers=headers, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result in soup.select(".result")[:5]:
        title_tag = result.select_one(".result__title")
        snippet_tag = result.select_one(".result__snippet")
        link_tag = result.select_one(".result__url")

        title = title_tag.get_text(" ", strip=True) if title_tag else "No title"
        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else "No snippet"
        link = link_tag.get_text(" ", strip=True) if link_tag else "No link"

        results.append({
            "title": title,
            "snippet": snippet,
            "link": link
        })

    return results
