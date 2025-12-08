from src.llm_wrapper import llm_complete
import json

DRAFT_PROMPT_TEMPLATE = """
You are the Draft Agent. Input: a structured `post_spec` JSON object and a `sources` list (each source has id, title, url, snippet).
Task: produce a clear, audience-aware blog draft in **markdown** using the following constraints:
- Use `post_spec['title']` as the article title.
- Create a short hook (1-3 sentences), then a 3-5 item TOC.
- For each heading in `post_spec['required_sections']`, produce an H2 section with 2-4 paragraphs.
- Insert inline citation anchors where factual claims appear using the format [S#] matching `sources` ids.
- Include a 3-6 step Action Plan section at the end specifically for entrepreneurs when requested.
- For each `suggested_visuals` produce a 1-line visual spec comment under a "Suggested Visuals" section.
- Add 3 comment prompts for readers at the end and a short author bio.
- Return only the markdown content; also output a small JSON metadata blob after the markdown (separated by a JSON fence) with keys: post_id, title, read_time_min, tags, claims (list of strings).
Tone: founder-friendly, curious, slightly playful. Keep jargon explained.
"""


def _build_prompt(post_spec: dict, sources: list) -> str:
    # Normalize inputs
    title = post_spec.get('title', 'Untitled')
    required_sections = post_spec.get('required_sections', [])
    learning_obj = post_spec.get('learning_objectives', [])
    tone = post_spec.get('tone', 'founder-friendly, curious, slightly playful')
    word_limit = post_spec.get('word_limit', 800)

    sources_summary = json.dumps(sources)

    sections_md = "\n".join([f"- {s}" for s in required_sections]) if required_sections else "- (no required sections)"

    prompt = DRAFT_PROMPT_TEMPLATE + "\n\nPOST_SPEC:\n" + json.dumps(post_spec, indent=2) + "\n\nSOURCES:\n" + sources_summary + "\n\nINSTRUCTIONS:\n"
    prompt += f"Write a markdown draft up to {word_limit} words, use the required sections exactly as H2 headings, include inline anchors [S1] etc. when referring to sources. Tone: {tone}."
    prompt += "\nReturn only markdown, then a JSON metadata fence."
    return prompt


def produce_draft(post_spec: dict, sources: list) -> dict:
    """Produce draft from structured post_spec and sources.
    post_spec: dict containing fields described by the Architect output.
    sources: list of {'id','title','url','snippet'}
    Returns: {'draft': markdown_str, 'metadata': {...}}
    """
    prompt = _build_prompt(post_spec, sources)
    draft_md = llm_complete(prompt, temperature=0.25, max_tokens=1400)

    # Try to split markdown and metadata JSON fence if present
    metadata = {}
    # Heuristic: look for a JSON object at end of output
    try:
        # find last occurrence of a JSON object starting on its own line
        last_brace = draft_md.rfind("\n{")
        if last_brace != -1:
            possible_json = draft_md[last_brace+1:].strip()
            # attempt to parse
            metadata = json.loads(possible_json)
            markdown_only = draft_md[:last_brace+1].rstrip()
        else:
            markdown_only = draft_md
    except Exception:
        markdown_only = draft_md
        metadata = {"post_id": post_spec.get('id'), "title": post_spec.get('title')}

    return {"draft": markdown_only, "metadata": metadata}