import os, json
from datetime import datetime

def compose_substack_markdown(final_md:str, visuals:list, audio_url:str, title:str):
    md = f"# {title}\n\n*Published {datetime.utcnow().date()}*\n\n"
    md += final_md + "\n\n"
    # embed visuals
    for v in visuals:
        md += f"\n\n![figure]({v})\n"
    if audio_url:
        md += f"\n\n<audio controls src=\"{audio_url}\"></audio>\n"
    md += "\n\n---\n*Author: Aviran Deshmara*\n"
    return md

def export_manifest(slug, md, out_dir="out"):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{slug}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
    return path