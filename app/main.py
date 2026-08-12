import sys
import os
import streamlit as st
import time

from .agent import TrendPilotAgent

# --- 1. PAGE SETUP (Must be the FIRST Streamlit command) ---
st.set_page_config(
    page_title="TrendPilot AI | Campaign Studio Pro",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. EXECUTIVE SaaS CUSTOM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #07090e;
        color: #e2e8f0;
    }

    [data-testid="stSidebar"] {
        background-color: #0c0e15;
        border-right: 1px solid #1a1e2b;
    }

    /* Top Navigation Header */
    .top-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 16px;
        border-bottom: 1px solid #1a1e2b;
        margin-bottom: 25px;
    }
    .header-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffffff;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .header-badge {
        background: rgba(52, 211, 153, 0.1);
        border: 1px solid rgba(52, 211, 153, 0.3);
        color: #34d399;
        font-size: 0.72rem;
        padding: 3px 10px;
        border-radius: 99px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* User Prompt Card */
    .user-request-card {
        background: #121622;
        border: 1px solid #1d2334;
        border-radius: 12px;
        padding: 18px 22px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .user-prompt-text {
        font-size: 0.95rem;
        color: #e2e8f0;
        font-weight: 500;
        margin-bottom: 12px;
    }
    .prompt-meta-pill {
        display: inline-block;
        background: #1a2130;
        border: 1px solid #293348;
        color: #94a3b8;
        font-size: 0.75rem;
        padding: 3px 10px;
        border-radius: 6px;
        margin-right: 8px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* PIPELINE VISUALIZER CARD */
    .pipeline-card {
        background: #0d111a;
        border: 1px solid #1e2638;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .pipeline-title {
        font-size: 0.75rem;
        font-weight: 700;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 12px;
    }
    .pipeline-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 8px;
    }
    .pipeline-step {
        background: #141a26;
        border: 1px solid #232d42;
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 0.75rem;
        color: #cbd5e1;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .pipeline-step.active {
        border-color: #a855f7;
        background: rgba(168, 85, 247, 0.08);
        color: #c084fc;
    }

    /* Main Result Container */
    .agent-card {
        background: #0f131d;
        border: 1px solid #1e2638;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    .agent-meta-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 18px;
        padding-bottom: 12px;
        border-bottom: 1px solid #1a202c;
    }

    /* Hasthag Box Terminal Code Style */
    .hashtag-container {
        background: #121824;
        border: 1px solid #202a3d;
        border-radius: 10px;
        padding: 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.88rem;
        color: #38bdf8;
        line-height: 1.8;
    }

    /* Native Streamlit Form Bottom Dock Override */
    [data-testid="stForm"] {
        background: #111520 !important;
        border: 1px solid #202738 !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5) !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #171c2b !important;
        border-color: #262e42 !important;
        color: white !important;
        border-radius: 8px !important;
        font-size: 0.82rem !important;
    }

    .stTextInput input {
        background-color: #171c2b !important;
        border: 1px solid #262e42 !important;
        color: white !important;
        font-size: 0.92rem !important;
        border-radius: 8px !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #a855f7 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 8px 20px !important;
        border-radius: 8px !important;
        width: 100%;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        opacity: 0.9 !important;
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- 4. SIDEBAR PANEL ---
with st.sidebar:
    st.markdown("""
        <div style="display:flex; align-items:center; gap:10px; margin-bottom: 25px;">
            <div style="background: linear-gradient(135deg, #a855f7, #6366f1); width: 34px; height: 34px; border-radius: 8px; display:flex; align-items:center; justify-content:center; font-size:16px; font-weight:bold; color:white;">🔮</div>
            <div>
                <div style="font-weight: 700; font-size: 1.05rem; color: #fff;">TrendPilot AI</div>
                <div style="display:flex; gap:6px; align-items:center; margin-top:2px;">
                    <span style="color:#34d399; font-size:0.65rem; background:rgba(52,211,153,0.1); padding:1px 6px; border-radius:4px;">Engine Active</span>
                    <span style="color:#64748b; font-size:0.68rem;">Pro v2.4</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🛠️ **Active Sub-Agents**")
    st.markdown("""
    - `1. Trend Discovery Engine`
    - `2. Content Copywriter`
    - `3. Hashtag Strategist`
    - `4. Video Script Writer`
    - `5. QA & Compliance Auditor`
    - `6. Markdown File Exporter`
    """)

    st.divider()

    st.markdown("""
        <div style="font-size: 0.7rem; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:8px;">System Telemetry</div>
        <div style="background:#10141f; border:1px solid #1a202c; border-radius:10px; padding:12px; font-family:'JetBrains Mono', monospace; font-size:0.75rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>Model:</span> <span style="color:#34d399;">qwen2.5:1.5b</span></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:4px;"><span>Hardware:</span> <span style="color:#34d399;">Apple Metal</span></div>
            <div style="display:flex; justify-content:space-between;"><span>Latency:</span> <span style="color:#34d399;">Sub-2s</span></div>
        </div>
    """, unsafe_allow_html=True)

# --- 5. TOP HEADER ---
st.markdown("""
    <div class="top-header">
        <div class="header-title">
            Campaign Studio
            <span class="header-badge">• Agent Pipeline Active</span>
        </div>
        <div style="display:flex; align-items:center; gap:16px; font-size:0.85rem; color:#94a3b8;">
            <span>Drafts</span>
            <span>Templates</span>
            <span style="background:#1e2638; color:#e2e8f0; padding:6px 14px; border-radius:8px; border:1px solid #2d374e;">Export Workspace</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 6. CHAT FEED CANVAS ---
if not st.session_state.chat_history:
    st.markdown("""
        <div style="text-align: center; padding: 80px 20px; color: #64748b;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">✨</div>
            <div style="font-size: 1.15rem; font-weight: 600; color: #f8fafc;">Enter a project topic to trigger the multi-agent pipeline</div>
            <div style="font-size: 0.85rem; margin-top: 6px;">Watch the sub-agents orchestrate trend analysis, writing, and QA review in real time.</div>
        </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"""
            <div class="user-request-card">
                <div class="user-prompt-text">📌 Campaign Topic: "{msg['topic']}"</div>
                <div>
                    <span class="prompt-meta-pill">Target Platform: {msg['platform']}</span>
                    <span class="prompt-meta-pill">Persona Tone: {msg['tone']}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        res = msg["data"]
        
        # PIPELINE EXPLANATION CARD
        st.markdown(f"""
            <div class="pipeline-card">
                <div class="pipeline-title">⚡ Multi-Agent Execution Pipeline Breakdown</div>
                <div class="pipeline-grid">
                    <div class="pipeline-step active">1. Trend Discovery</div>
                    <div class="pipeline-step active">2. Caption Writer</div>
                    <div class="pipeline-step active">3. Hashtag Strategy</div>
                    <div class="pipeline-step active">4. Script Blueprint</div>
                    <div class="pipeline-step active">5. QA Compliance</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # MAIN AGENT OUTPUT CONTAINER
        st.markdown(f"""
            <div class="agent-card">
                <div class="agent-meta-header">
                    <div style="font-size:0.88rem; font-weight:600; color:#a855f7;">🔮 TrendPilot Content Blueprint</div>
                    <div style="font-size:0.75rem; color:#34d399; font-family:'JetBrains Mono';">✓ Output Saved: {res.get('saved_file')}</div>
                </div>
        """, unsafe_allow_html=True)

        t1, t2, t3, t4 = st.tabs(["📝 Main Caption & Angles", "🎬 Video Reel Script", "🏷️ Hashtag Stack", "🔍 QA Audit Report"])

        with t1:
            st.markdown("#### **Generated Caption**")
            st.markdown(res.get('caption'))
            st.markdown("---")
            st.markdown("#### **Viral Angles Analyzed**")
            st.markdown(res.get('angles'))

        with t2:
            st.markdown(res.get('script'))

        with t3:
            st.markdown(f"""
                <div class="hashtag-container">
                    {res.get('hashtags')}
                </div>
            """, unsafe_allow_html=True)

        with t4:
            st.markdown(res.get('review'))

        st.markdown("</div>", unsafe_allow_html=True)

# --- 7. FLOATING BOTTOM CONTROL DOCK (FORM BASED) ---
st.write("")
st.write("")

with st.form("campaign_dock_form", border=False):
    col_platform, col_tone, col_text, col_submit = st.columns([1.2, 1.2, 4, 1.2], gap="small")
    
    with col_platform:
        platform_sel = st.selectbox("Platform", ["LinkedIn", "Instagram Reels", "YouTube Shorts", "X / Twitter"], label_visibility="collapsed")
    
    with col_tone:
        tone_sel = st.selectbox("Tone Persona", ["Technical & Educational", "Energetic & Professional", "Motivational", "Humorous"], label_visibility="collapsed")
        
    with col_text:
        topic_input = st.text_input("Topic", placeholder="Type your campaign topic here...", label_visibility="collapsed")
        
    with col_submit:
        run_pipeline = st.form_submit_button("Generate ✨", use_container_width=True)

# --- 8. EXECUTION CONTROLLER ---
if run_pipeline and topic_input:
    msg_id = int(time.time())
    
    st.session_state.chat_history.append({
        "id": msg_id,
        "role": "user",
        "topic": topic_input,
        "platform": platform_sel,
        "tone": tone_sel
    })

    log_spot = st.empty()
    logs = []

    def stream_callback(msg):
        logs.append(msg)
        log_spot.caption(f"⚡ Pipeline Step: {logs[-1]}")

    agent = TrendPilotAgent(log_callback=stream_callback)
    
    with st.spinner("🤖 Multi-agent system executing workflow..."):
        agent_output = agent.run(topic_input, platform_sel, tone_sel)

    st.session_state.chat_history.append({
        "id": msg_id + 1,
        "role": "agent",
        "data": agent_output
    })

    log_spot.empty()
    st.rerun()
