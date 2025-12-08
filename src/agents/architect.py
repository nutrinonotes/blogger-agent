from src.llm_wrapper import llm_complete
import json

ARCHITECT_PROMPT = """You are the ARCHITECT AGENT for a nuclear entrepreneurship blog.
Produce a JSON with:
- pillars: list of 5 pillars {name, short_blurb}
- posts: 12 upcoming post objects {title, blurb, depth(low|medium|high), priority(1-10), keywords:[...]}
Return JSON only.
"""

def generate_editorial_plan() -> dict:
    resp = llm_complete(ARCHITECT_PROMPT, temperature=0.3, max_tokens=800)
    # attempt to parse; if LLM returns text, try to extract JSON substring
    try:
        data = json.loads(resp)
    except Exception:
        # fallback: ask LLM to only return JSON
        resp2 = llm_complete(ARCHITECT_PROMPT+"\nReturn only valid JSON.", temperature=0.1)
        data = json.loads(resp2)
    return data