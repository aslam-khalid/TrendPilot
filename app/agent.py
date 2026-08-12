import sys
import os

# Add project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.tools import (
    trend_idea_generator,
    caption_writer,
    hashtag_generator,
    reel_script_generator,
    content_reviewer,
    file_saver_tool
)
from app.memory import save_to_memory


class TrendPilotAgent:
    def __init__(self, log_callback=None):
        self.log = log_callback if log_callback else print

    def run(self, topic: str, platform: str, tone: str) -> dict:
        self.log(f"[Agent]: Starting task for '{topic}'...")

        self.log("[Tool Called]: Trend Idea Generator")
        angles = trend_idea_generator(topic)

        self.log("[Tool Called]: Caption Writer")
        caption = caption_writer(topic, platform, tone, angles)

        self.log("[Tool Called]: Hashtag Generator")
        hashtags = hashtag_generator(topic, platform)

        self.log("[Tool Called]: Reel Script Generator")
        script = reel_script_generator(topic)

        self.log("[Tool Called]: Content Reviewer Tool")
        raw_output = f"{caption}\n\nHashtags:\n{hashtags}\n\nScript:\n{script}"
        review = content_reviewer(raw_output)

        result_data = {
            "topic": topic,
            "platform": platform,
            "tone": tone,
            "angles": angles,
            "caption": caption,
            "hashtags": hashtags,
            "script": script,
            "review": review
        }

        self.log("[Tool Called]: File Saver Tool")
        # Sanitize filename and fallback if empty
        safe_filename = "".join(c for c in topic if c.isalnum() or c in (' ', '_', '-')).strip().replace(" ", "_").lower()
        if not safe_filename:
            safe_filename = "campaign_output"

        filepath = file_saver_tool(result_data, safe_filename)
        result_data["saved_file"] = filepath

        self.log("[Tool Called]: Simple Memory Tool")
        save_to_memory({"topic": topic, "platform": platform, "file": filepath})

        self.log("[Agent]: Finished successfully!")
        return result_data
