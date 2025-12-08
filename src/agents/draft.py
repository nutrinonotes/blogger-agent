from src.llm_wrapper import llm_complete
import json

DRAFT_PROMPT_TEMPLATE = """
You are Draft Agent: write a clear 800-word blog draft for readers: curious learners + aspiring entrepreneurs.
Input Title: {title}
Input sources: {sources}
Structure: Hook, TOC bullets, H2 sections, Action Plan (3-6 steps), Suggested visuals, 3 comment prompts, short author bio.
Cite sources inline using [S#].
Write in active voice, slight playful line, and keep jargon explained.
Return markdown only and a JSON metadata block at the end.
"""

def produce_draft(title: str, sources: list) -> dict:
    sources_str = json.dumps(sources)
    prompt = DRAFT_PROMPT_TEMPLATE.format(title=title, sources=sources_str)
    draft_md = llm_complete(prompt, temperature=0.25, max_tokens=1200)
    # Try to split markdown and metadata if provided
    return {"draft": draft_md}