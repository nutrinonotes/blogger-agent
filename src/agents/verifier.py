from src.llm_wrapper import llm_complete
import re, json
from src.utils.web_utils import search_duckduckgo_snippets

VERIFIER_PROMPT = """
You are Verifier Agent. Input: draft markdown. Task:
1) Extract numbered factual claims.
2) For each claim perform web search and return status: Verified/Unverified/Contradicted with 1 URL and 1-sentence evidence.
3) Identify high-risk safety phrases (operational instructions). Flag as safety_high.
Return JSON: {{claims:[{{id, claim, status, url, evidence}}], safety_flags:[], score:0-100}}.
"""

def verify_with_search(draft_md: str) -> dict:
    # Step 1: extract candidate factual sentences (naive)
    sentences = re.split(r'\n+', draft_md)
    claims = []
    for idx, s in enumerate(sentences):
        s_strip = s.strip()
        if len(s_strip) < 30: 
            continue
        # naive: treat sentences with numbers or org names as factual candidates
        if any(tok.isdigit() for tok in s_strip.split()) or "NPCIL" in s_strip or "AERB" in s_strip or "SMR" in s_strip:
            # search
            snippets = search_duckduckgo_snippets(s_strip, max_results=2)
            status="Unverified"
            url=""
            evidence=""
            if snippets:
                status="Plausible"
                url=snippets[0]["url"]
                evidence=snippets[0]["snippet"]
            claims.append({"id": f"C{idx+1}", "claim": s_strip, "status": status, "url": url, "evidence": evidence})
    # safety scan
    safety_flags=[]
    if "build a reactor" in draft_md.lower() or "how to make" in draft_md.lower():
        safety_flags.append({"reason":"contains explicit build instructions", "level":"high"})
    score = 80 - len([c for c in claims if c["status"]!="Plausible"]) * 5
    return {"claims":claims, "safety_flags":safety_flags, "score": max(0,min(100,score))}