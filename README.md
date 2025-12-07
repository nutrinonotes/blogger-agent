# NuclearBlogAgent  
*A multi-agent system for generating high-quality, research-backed, visual-rich, audio-enabled technical blogs.*

---

## 👋 Hi — I’m **Aviran Deshmara**

This repository contains my ongoing work in building an automated, Python-driven agent architecture for writing, verifying, illustrating, and narrating blog posts — starting with nuclear energy, deeptech, and adjacent domains.

I come from a non-nuclear background and I’m learning the field from first principles.  
This project is part of that journey: building tools that can help anyone explore complex topics with clarity, accuracy, and creativity.

---

# 🚀 Project Overview

**NuclearBlogAgent** is a multi-agent framework with these goals:

### 🧠 **1. Architect Agent**  
Creates topic pillars, post outlines, learning paths, and an editorial calendar.

### 🔍 **2. Research Agent**  
Gathers authoritative sources (IAEA, AERB, NPCIL, academic papers, reputable journalism) and extracts structured factual snippets.

### ✍️ **3. Draft Agent**  
Writes the first full draft from the research package, with placeholders for citations, visuals, and animations.

### ✅ **4. Verifier Agent**  
Independently checks factual claims, logical consistency, missing citations, tone, safety, and contradictions.

### 🧹 **5. Editor Agent**  
Improves clarity, flow, voice, and correctness. Applies verifier feedback.

### 🛡️ **6. Compliance Agent**  
Ensures posts avoid sensitive technical instructions or hazardous details — especially important for nuclear topics.

### 🎨 **7. Visuals Agent**  
Generates:  
- Static charts (matplotlib/plotly)  
- Diagrams  
- GIF and MP4 animations (matplotlib / manim)  
- Visual specs for future media

### 🎙️ **8. Audio Agent**  
Produces podcast-ready narration using TTS (OpenAI / ElevenLabs / offline fallback).  
Outputs MP3 + transcript.

### 🌐 **9. Publisher Agent**  
Formats final output for Substack:  
- Markdown + HTML embeds  
- Image/video hosting  
- Audio player embeds  
- SEO metadata

### 📈 **10. Ops/Monitor Agent**  
Tracks performance, recomputes citations, and ensures quality over time.

---

# 🧩 Tech Stack

- **Python 3.11+**  
- **LangChain** for orchestration  
- **OpenAI / web-enabled LLMs** for drafting & verification  
- **matplotlib**, **imageio**, **ffmpeg-python**, **plotly**, **manim** for visuals  
- **ElevenLabs / OpenAI TTS** for audio  
- **boto3** (AWS S3) for hosting media assets  
- **Obsidian** + Git workflow for drafts  
- **Substack** for publishing  

---

# 📚 Goals of This Project

- Build a *repeatable*, *verifiable*, *high-trust* writing pipeline.  
- Make learning nuclear energy accessible to non-experts.  
- Experiment with agents as co-writers, researchers, and editors.  
- Publish posts with visuals, animations, and audio narration.  
- Eventually extend this architecture into broader educational tooling.

This repository will evolve continuously as I refine the workflow, prompts, tooling, and agents.

---

# 🛠️ Project Status

- [x] Repository initialized  
- [x] Identity & platform setup  
- [ ] Architect Agent (in progress)  
- [ ] Research Agent  
- [ ] Draft Agent  
- [ ] Verifier Agent  
- [ ] Editor Agent  
- [ ] Compliance Agent  
- [ ] Visuals Agent  
- [ ] Audio Agent  
- [ ] Publisher Agent  
- [ ] End-to-end pipeline  
- [ ] Automated publishing  
- [ ] First public release  

---

# 🗺️ Roadmap (High-level)

### Phase 1 — Foundation  
- Architect Agent  
- Basic drafting  
- Basic verification  
- Static visuals  
- Audio prototype

### Phase 2 — Automations  
- Structured research ingestion  
- Visual spec language  
- Social/post exports  
- S3 media hosting  
- Enhanced compliance checks

### Phase 3 — Full Pipeline  
- End-to-end automation  
- Multi-format outputs  
- Podcast feed generation  
- Rich animations  
- Improved editorial personalization

---

# 💬 Feedback / Collaboration

If you're exploring similar agent architectures or working in nuclear, deeptech, or AI-driven publishing, I’d love to connect.

You can reach me here on GitHub or via:  
📬 nuclearblog@proton.me

---

# 📝 License  
MIT

---

