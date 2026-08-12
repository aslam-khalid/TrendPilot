import os
import re
import requests
import streamlit as st
from groq import Groq

# Read securely from Streamlit Cloud Secrets or local environment
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"  # Local fallback model


def call_llm(prompt: str) -> str:
    """Ultra-fast LLM caller using Groq Cloud API with local Ollama fallback."""
    # 1. Cloud Execution via Groq
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5,
                max_tokens=300,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[Groq API Warning]: {str(e)} -> Falling back to local Ollama...")

    # 2. Local Execution via Ollama
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
        res = requests.post(OLLAMA_URL, json=payload, timeout=60)
        res.raise_for_status()
        return res.json().get("response", "").strip()
    except Exception as e:
        return f"Error connecting to LLM: {str(e)}"
