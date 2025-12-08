from src.agents.architect import generate_editorial_plan
from src.agents.research import collect_sources
from src.agents.draft import produce_draft
from src.agents.verifier import verify_with_search
from src.agents.editor import edit_draft
from src.agents.visuals import render_static_chart, render_animation
from src.agents.audio import synthesize_tts_elevenlabs
from src.agents.publisher import compose_substack_markdown, export_manifest
from src.utils.io import ensure_dir, write_json, read_json
import os

def run_pipeline(seed_title=None, slug="post1"):
    print("Loading architect plan (if available)...")
    plan = None
    architect_paths = ["architect_output.json", "workspace/architect_output.json"]

    for p in architect_paths:
        if os.path.exists(p):
            try:
                plan = read_json(p)
                print(f"Loaded architect plan from {p}")
                break
            except Exception:
                plan = None

    # Determine post_spec
    post_spec = None
    if plan:
        # If seed_title provided, try to match by title
        if seed_title:
            for post in plan.get('posts', []):
                if post.get('title') and seed_title.lower() in post.get('title','').lower():
                    post_spec = post
                    break
        # fallback: pick first id in editorial_calendar
        if not post_spec:
            first_id = None
            cal = plan.get('editorial_calendar') or []
            if cal:
                first_id = cal[0]
            else:
                # pick first post object
                posts = plan.get('posts', [])
                if posts:
                    first_id = posts[0].get('id')
            if first_id:
                for post in plan.get('posts', []):
                    if post.get('id') == first_id:
                        post_spec = post
                        break

    print("Researching...")
    # Use post_spec title for search if available, else use seed_title
    research_query = None
    if post_spec and post_spec.get('title'):
        research_query = post_spec.get('title')
    elif seed_title:
        research_query = seed_title
    else:
        research_query = "nuclear energy basics"

    sources = collect_sources(research_query)
    write_json(f"workspace/{slug}/sources.json", sources)

    print("Drafting...")
    # If we have a post_spec, pass it; else pass a minimal spec with title
    if post_spec:
        ensure_dir(f"workspace/{slug}")
        draft_obj = produce_draft(post_spec, sources)
    else:
        minimal_spec = {"id":"ad-hoc","title": research_query, "required_sections":["Introduction","Main","Conclusion"]}
        draft_obj = produce_draft(minimal_spec, sources)

    draft_md = draft_obj.get("draft")
    metadata = draft_obj.get("metadata", {})
    ensure_dir(f"workspace/{slug}")
    with open(f"workspace/{slug}/draft.md","w",encoding="utf-8") as f:
        f.write(draft_md)

    print("Verifying...")
    verifier_report = verify_with_search(draft_md)
    write_json(f"workspace/{slug}/verifier.json", verifier_report)

    print("Editing...")
    edited = edit_draft(draft_md, verifier_report)
    final_md = edited.get("edited", draft_md)
    ensure_dir(f"workspace/{slug}")
    with open(f"workspace/{slug}/final.md","w",encoding="utf-8") as f:
        f.write(final_md)

    print("Rendering visuals...")
    fig = render_static_chart(f"workspace/{slug}/visuals/figure1.png")
    # guard animation if ffmpeg not available
    try:
        mp4, gif = render_animation(f"workspace/{slug}/visuals/anim.mp4", f"workspace/{slug}/visuals/anim.gif")
    except Exception as e:
        print("Animation skipped (ffmpeg may be missing):", e)
        mp4, gif = None, None

    # Optional audio step - will error if ELEVENLABS_API_KEY not set; orchestrator will skip if not present
    print("Generating audio (TTS)...")
    audio_path = None
    skip_audio = os.getenv("SKIP_AUDIO", "false").lower() in ("1","true","yes")
    if not skip_audio and os.getenv("ELEVENLABS_API_KEY"):
        try:
            audio_dir = f"workspace/{slug}/audio"
            ensure_dir(audio_dir)
            audio_path = f"{audio_dir}/podcast.mp3"
            synthesize_tts_elevenlabs(final_md[:4000], audio_path)
        except Exception as e:
            print("Audio generation failed or skipped:", e)
            audio_path = None
    else:
        print("Skipping audio generation (SKIP_AUDIO or ELEVENLABS_API_KEY not set).")

    print("Publishing (export)...")
    # For local testing we won't upload to S3. Use local path or None.
    audio_url = audio_path
    visuals_urls = [fig] if fig else []
    title = post_spec.get('title') if post_spec else research_query
    md = compose_substack_markdown(final_md, visuals_urls, audio_url, title)
    out = export_manifest(slug, md)
    print("Done. Exported:", out)
    return out

if __name__ == "__main__":
    run_pipeline("How I’m Building Two Agents to Write Better Blogs", slug="two-agents")