from src.llm_wrapper import llm_complete
import json

EDITOR_PROMPT = """
You are Editor Agent. Input: draft_md and verifier_report JSON.
Apply inline editorial edits for clarity and incorporate verifier suggestions:
- Rewrite ambiguous lines (Original -> Suggested)
- Mark unresolved claims with [VERIFY]
Return: edited markdown and changelog JSON.
"""

def edit_draft(draft_md: str, verifier_report: dict) -> dict:
    prompt = EDITOR_PROMPT + "\n\nDRAFT:\n" + draft_md + "\n\nVERIFIER:\n" + json.dumps(verifier_report)
    edited = llm_complete(prompt, temperature=0.2, max_tokens=800)
    return {"edited": edited}