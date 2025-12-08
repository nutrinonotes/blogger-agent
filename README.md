# NuclearBlogAgent  
*A multi-agent system for generating high-quality, research-backed, visual-rich, audio-enabled technical blogs.*

---

## 🚀 Project Overview

**NuclearBlogAgent** is an automated, Python-driven agent architecture for writing, verifying, illustrating, and narrating blog posts. It orchestrates specialized AI agents to take a topic from concept to published artifact.

### 🤖 The Agent Team

1.  **Architect Agent**: Creates topic pillars and editorial calendars.
2.  **Research Agent**: Scrapes and summarizes authoritative sources (duckduckgo, academic snippets).
3.  **Draft Agent**: Writes full blog drafts with citation placeholders.
4.  **Verifier Agent**: Checks facts against web sources and flags safety issues.
5.  **Editor Agent**: Refines tone, clarity, and incorporates verifier feedback.
6.  **Visuals Agent**: Generates charts (Matplotlib) and animations (MP4/GIF).
7.  **Audio Agent**: Synthesizes podcast narration (ElevenLabs/OpenAI TTS).
8.  **Publisher Agent**: Formats final Markdown for platforms like Substack.

---

## 🛠️ Installation & Usage

### 1. Prerequisites
- Python 3.10+
- OpenAI API Key
- (Optional) ElevenLabs API Key for high-quality audio

### 2. Setup
Clone the repository and install dependencies:
```bash
git clone https://github.com/nutrinonotes/blogger-agent.git
cd blogger-agent
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=sk-your-key-here
ELEVENLABS_API_KEY=your-key-here  # Optional
```

### 4. Run the Pipeline
To generate a blog post about "Two Agents":
```bash
python -m src.agents.orchestrator
```

The system will:
1.  Research the topic.
2.  Draft content.
3.  Verify facts.
4.  Edit the post.
5.  Generate visuals (Charts & GIFs).
6.  Save outputs to `workspace/`.

### 5. Verify System Health
Run the included check script to verify all dependencies and imports:
```bash
python check_system.py
```

---

## 🧩 Tech Stack

-   **LangChain / OpenAI client**: LLM orchestration.
-   **BeautifulSoup**: Web research.
-   **Matplotlib / ImageIO**: Visuals and animations.
-   **ElevenLabs**: Audio synthesis.
-   **DuckDuckGo**: Search backend.

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.

Copyright (c) 2025 Aviran Deshmara
