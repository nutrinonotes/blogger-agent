from src.llm_wrapper import llm_complete
import json

ARCHITECT_PROMPT = """You are the ARCHITECT AGENT for a public-facing, entrepreneurship-focused nuclear blog (audience: curious learners + aspiring entrepreneurs). 
Produce a JSON object containing:
- pillars: an array of 5-7 pillar objects. Each pillar: {
    id: "P1", name: "Short name", description: "1-2 sentence blurb explaining why this pillar matters for entrepreneurs",
    priority: 1-10
  }
- posts: an array of 12-24 post objects. Each post:
  {
    id: "T1",
    pillar_id: "P1",
    title: "Suggested title (<=80 chars)",
    short_blurb: "1-sentence summary",
    target_audience: ["learner","entrepreneur","policy"],               # choose tags
    seo_keyword: "primary SEO keyword phrase",
    secondary_keywords: ["kw1","kw2"],
    estimated_read_time_min: 6,
    research_depth: "low|medium|high",                                # what Research Agent should collect
    learning_objectives: ["objective 1","objective 2"],
    required_sections: ["What it is","Why it matters","Technical primer","Business implications","Action plan"],
    suggested_visuals: [{"type":"static_chart|diagram|animation","purpose":"explain fuel cycle"}],
    suggested_audio_clip_minutes: 5,
    suggested_sources: [{"name":"IAEA primer", "why":"authoritative overview", "preferred_url": "https://..."}],
    priority: 1-10,
    publish_timing: "week-1|week-2|month-1"                         # optional scheduling hint
  }
- editorial_calendar: list of first 12 posts (by id) in publish order
Return strictly valid JSON only (no extra commentary).
"""

def generate_editorial_plan() -> dict:
    # Use json_mode=True to ensure valid JSON and avoid retries
    resp = llm_complete(ARCHITECT_PROMPT, temperature=0.3, max_tokens=800, json_mode=True)
    try:
        data = json.loads(resp)
    except Exception as e:
        print(f"Architect JSON parse failed: {e}")
        data = {}
    return data