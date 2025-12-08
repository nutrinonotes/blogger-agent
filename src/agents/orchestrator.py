import os
import logging
from src.agents.architect import generate_editorial_plan
from src.agents.research import collect_sources
from src.agents.draft import produce_draft
from src.agents.verifier import verify_with_search
from src.agents.editor import edit_draft
from src.agents.visuals import render_static_chart, render_animation
from src.agents.audio import synthesize_tts_elevenlabs
from src.agents.publisher import compose_substack_markdown, export_manifest
from src.utils.io import ensure_dir, write_json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_pipeline(seed_title, slug="post1"):
    logger.info("Architecting (optional)...")
    # (Optionally) call architect; skipping for single run.

    logger.info("Researching...")
    sources = collect_sources(seed_title)
    write_json(f"workspace/{slug}/sources.json", sources)

    logger.info("Drafting...")
    draft_obj = produce_draft(seed_title, sources)
    draft_md = draft_obj["draft"]
    with open(f"workspace/{slug}/draft.md","w",encoding="utf-8") as f:
        f.write(draft_md)

    logger.info("Verifying...")
    verifier_report = verify_with_search(draft_md)
    write_json(f"workspace/{slug}/verifier.json", verifier_report)

    logger.info("Editing...")
    edited = edit_draft(draft_md, verifier_report)
    final_md = edited.get("edited", draft_md)
    with open(f"workspace/{slug}/final.md","w",encoding="utf-8") as f:
        f.write(final_md)

    logger.info("Rendering visuals...")
    fig = render_static_chart(f"workspace/{slug}/visuals/figure1.png")
    mp4, gif = render_animation(f"workspace/{slug}/visuals/anim.mp4", f"workspace/{slug}/visuals/anim.gif")
    
    # --- Audio step: make it optional for local testing ---
    skip_audio = os.getenv("SKIP_AUDIO", "false").lower() in ("1","true","yes")
    eleven_api = os.getenv("ELEVENLABS_API_KEY", "")  # from src.config or env

    audio_path = None
    if skip_audio or not eleven_api:
        logger.warning("Skipping audio generation (SKIP_AUDIO or no ELEVENLABS_API_KEY).")
    else:
        logger.info("Generating audio (TTS)...")
        audio_dir = f"workspace/{slug}/audio"
        ensure_dir(audio_dir)
        audio_path = f"{audio_dir}/podcast.mp3"
        synthesize_tts_elevenlabs(final_md[:4000], audio_path)

    logger.info("Publishing (export)...")
    audio_url = f"https://storage.example/{slug}/podcast.mp3"  # replace with S3 upload flow
    visuals_urls = [fig]
    md = compose_substack_markdown(final_md, visuals_urls, audio_url, seed_title)
    out = export_manifest(slug, md)
    logger.info(f"Done. Exported: {out}")
    return out

if __name__ == "__main__":
    run_pipeline("How I’m Building Two Agents to Write Better Blogs", slug="two-agents")