import requests
import logging
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from src.utils.web_utils import search_duckduckgo_snippets

logger = logging.getLogger(__name__)

def collect_sources(seed_title: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Collect search results for a given title using DuckDuckGo snippets.
    
    Args:
        seed_title: The search query or title.
        max_results: Max number of snippets to return.
        
    Returns:
        List of dictionaries with id, title, url, snippet, etc.
    """
    try:
        snippets = search_duckduckgo_snippets(seed_title, max_results=max_results)
    except Exception as e:
        logger.error(f"Failed to search for {seed_title}: {e}")
        return []

    # snippets: list of {title, url, snippet}
    # convert to sources.json compatible format
    sources = []
    for i,s in enumerate(snippets):
        sources.append({
            "id": f"S{i+1}", 
            "title": s.get("title", ""), 
            "url": s.get("url", ""), 
            "snippet": s.get("snippet", ""), 
            "confidence": "medium"
        })
    return sources