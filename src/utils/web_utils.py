import requests
from bs4 import BeautifulSoup

def search_duckduckgo_snippets(query, max_results=8):
    url = "https://html.duckduckgo.com/html/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        # Verify=False to handle potential corporate proxy/SSL issues
        resp = requests.post(url, data={"q": query}, headers=headers, timeout=10, verify=False)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Search error: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []
    for r in soup.select(".result__body")[:max_results]:
        title_el = r.select_one(".result__title")
        link_el = r.select_one("a.result__a")
        snippet_el = r.select_one(".result__snippet")
        
        title = title_el.get_text(strip=True) if title_el else "No Title"
        link = link_el["href"] if link_el else ""
        snippet = snippet_el.get_text(strip=True) if snippet_el else ""
        
        if link:
            results.append({"title":title,"url":link,"snippet":snippet})
    return results