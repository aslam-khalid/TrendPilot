import os
import re
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"  # Lightweight 1.5B model for ultra-fast generation


def call_llm(prompt: str) -> str:
    """Optimized LLM caller with strict output limits for sub-second speeds."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 220,
            "temperature": 0.5,
            "top_k": 20,
            "top_p": 0.8
        }
    }
    try:
        # Increased timeout from 15s to 60s
        res = requests.post(OLLAMA_URL, json=payload, timeout=60)
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except Exception as e:
        return f"Error connecting to Ollama: {str(e)}"


# --- TOOL DEFINITIONS ---


def trend_idea_generator(topic: str) -> str:
    prompt = f"Act as a viral strategist. Provide 3 short, catchy content angles for: '{topic}'."
    return call_llm(prompt)


def caption_writer(topic: str, platform: str, tone: str, angle: str) -> str:
    prompt = f"Write a concise {platform} caption for '{topic}' with a {tone} tone. Angle: {angle}. Keep it short and impactful."
    return call_llm(prompt)


def hashtag_generator(topic: str, platform: str) -> str:
    prompt = f"Generate 8 relevant hashtags for a {platform} post about '{topic}'. Output ONLY the hashtags."
    return call_llm(prompt)


def reel_script_generator(topic: str) -> str:
    prompt = f"Write a short 30-sec video script for '{topic}'. Include: Hook, Body, Visual Cue, and CTA."
    return call_llm(prompt)


def content_reviewer(content: str) -> str:
    prompt = f"Review this content briefly. Check tone, clarity, and give 2 short recommendations:\n\n{content}"
    return call_llm(prompt)


def sanitize_filename(name: str) -> str:
    """Removes invalid characters to safely create filesystem names."""
    name = re.sub(r"[^\w\s-]", "", name).strip().lower()
    return re.sub(r"[-\s]+", "_", name)


def file_saver_tool(data: dict, filename: str = "") -> str:
    # Resolve absolute path to guarantee files save inside project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "outputs", "saved_results")
    os.makedirs(target_dir, exist_ok=True)

    # Determine safe filename from input parameter or topic dict
    raw_name = filename or data.get("topic", "campaign_output")
    safe_name = sanitize_filename(raw_name) or "campaign_output"
    filepath = os.path.join(target_dir, f"{safe_name}.md")

    content = f"# TrendPilot Content Plan: {data.get('topic')}\n\n"
    content += (
        f"**Platform:** {data.get('platform')} | **Tone:** {data.get('tone')}\n\n"
    )
    content += f"## 💡 Content Angles\n{data.get('angles')}\n\n"
    content += f"## ✍️ Caption\n{data.get('caption')}\n\n"
    content += f"## #️⃣ Hashtags\n{data.get('hashtags')}\n\n"
    content += f"## 🎬 Reel Script\n{data.get('script')}\n\n"
    content += f"## 🔍 Reviewer Feedback\n{data.get('review')}\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[FileSaver]: Saved file to {filepath}")
    return filepath