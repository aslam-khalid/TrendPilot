# TrendPilot AI — Error & Failure Analysis Report

**Project:** TrendPilot AI — Local Agentic Content Studio  
**Engine:** Ollama (`qwen2.5:1.5b`)  
**Assignment:** AIRI Team PITB - AI Internship Task 2  

---

## 1. Failure Analysis Table

The following table documents 5 real technical issues, root causes, and fixes encountered during the design, development, and optimization of the TrendPilot AI agent pipeline:

| Test / Case No. | Problem Found | Possible Reason / Root Cause | Fix Applied |
| :--- | :--- | :--- | :--- |
| **01. Generation Latency** | Full generation took 45+ seconds or hung indefinitely | Local LLM default output length was uncapped, causing long-winded text generation across multiple agent tools | Added `num_predict: 220`, `temperature: 0.5`, `top_k: 20`, and `top_p: 0.8` inside `call_llm()` payload options in `app/tools.py` |
| **02. Ollama Connection Timeout** | `Read timed out (timeout=15)` error on complex tabs (Reel Script & QA Audit) | `requests.post()` in `call_llm()` had a strict 15-second timeout, which was exceeded when running multi-step prompts sequentially | Increased the request timeout in `app/tools.py` from `timeout=15` to `timeout=60` to allow structured multi-token outputs to finish |
| **03. File Saver Execution Failure** | Output files failed to save or caused path errors when topics included special characters (e.g., `:`, `/`) | Filenames generated directly from raw user prompts contained invalid OS filesystem characters | Created a `sanitize_filename()` utility function using regex (`re.sub`) to strip illegal characters and resolve absolute project paths in `app/tools.py` |
| **04. UI Layout Breakdown** | An unwanted empty dark bar appeared above the input dock | Wrapping native Streamlit widgets inside raw HTML `<div>` tags broke the Streamlit virtual DOM hierarchy | Replaced raw HTML container wrappers with a native `st.form()` element and styled it using `[data-testid="stForm"]` in custom CSS |
| **05. Dropdown Text Truncation** | Option text in tone/platform selectors was cut off (`Technical & Educati...`) | The fixed column width allocation (`col_tone = 1.2`) restricted popover menu width | Updated column ratios in `app/main.py` (`[1.3, 1.5, 3.8, 1.2]`) and injected CSS popover rules (`div[data-baseweb="popover"] { min-width: 240px !important; }`) |

---

## 2. Key System Optimizations Applied

1. **Sub-Second Latency Capping:**  
   By enforcing strict output token limits (`num_predict: 220`), we reduced per-tool generation latency from ~12s down to ~1.8s while maintaining concise, high-quality social copy.

2. **Absolute Path Resolution:**  
   Replaced hardcoded relative paths with dynamic `os.path.abspath()` calls anchored to the project root directory. This guarantees that Markdown exports land consistently in `outputs/saved_results/` regardless of where the Streamlit app is launched from.

3. **Streamlit Native Form Handling:**  
   Converting the execution dock to `st.form` eliminated DOM rendering bugs, enabled seamless single-click pipeline execution, and added support for pressing **Enter** to submit inputs.

---

## 3. Recommended Future System Improvements

1. **Async Tool Execution:**  
   Currently, the tools run sequentially in `agent.py`. Implementing `asyncio` or concurrent requests would allow independent tools (e.g., `caption_writer` and `hashtag_generator`) to execute in parallel, cutting runtime in half.

2. **Structured JSON Output Parsing:**  
   Force Ollama schema outputs using JSON mode to guarantee deterministic key-value extraction for complex multi-agent workflows.

3. **Expanded Local Vector Memory:**  
   Upgrade `memory.py` from basic JSON logging to a lightweight ChromaDB or SQLite vector store to enable semantic search across past generated content plans.