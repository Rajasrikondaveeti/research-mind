import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind · AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

STEPS = ["search", "reader", "writer", "critic"]

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    color: #e8e4dc;
}

.stApp {
    background: #0a0a0f;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
}

/* ── Hide default streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3rem 0 2rem;
    position: relative;
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.live-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #50c878;
    box-shadow: 0 0 0 rgba(80,200,120,0.6);
    animation: pulse 1.8s infinite;
}
@keyframes pulse {
    0%   { box-shadow: 0 0 0 0 rgba(80,200,120,0.55); }
    70%  { box-shadow: 0 0 0 8px rgba(80,200,120,0); }
    100% { box-shadow: 0 0 0 0 rgba(80,200,120,0); }
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.03em;
    color: #f0ebe0;
    margin: 0 0 1rem;
}
.hero h1 span {
    color: #ff8c32;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #a09890;
    max-width: 520px;
    margin: 0 auto;
    line-height: 1.65;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
    margin: 2rem 0;
}

/* ── Input card ── */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,140,50,0.15);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.2rem;
    backdrop-filter: blur(8px);
}

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] div[data-baseweb="input"] {
    background: #18181b !important;
    border: 1px solid rgba(255,140,50,0.25) !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input {
    background: #18181b !important;
    color: #f0ebe0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
    -webkit-text-fill-color: #f0ebe0 !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: #706860 !important;
    opacity: 1 !important;
}
[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
    border-color: #ff8c32 !important;
    box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
}
[data-testid="stTextInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: #ff8c32 !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
    color: #0a0a0f !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.7rem 2.2rem !important;
    cursor: pointer !important;
    transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
    box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
    opacity: 0.95 !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}
.stButton > button:disabled {
    opacity: 0.5 !important;
    transform: none !important;
    cursor: not-allowed !important;
}

/* ── Overall progress bar ── */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #ff8c32, #ff5a1a) !important;
}

/* ── Pipeline step cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card.active {
    border-color: rgba(255,140,50,0.4);
    background: rgba(255,140,50,0.05);
}
.step-card.done {
    border-color: rgba(80,200,120,0.3);
    background: rgba(80,200,120,0.03);
}
.step-card.failed {
    border-color: rgba(240,80,80,0.4);
    background: rgba(240,80,80,0.05);
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    border-radius: 14px 0 0 14px;
    background: rgba(255,255,255,0.05);
    transition: background 0.3s;
}
.step-card.active::before { background: #ff8c32; }
.step-card.done::before   { background: #50c878; }
.step-card.failed::before { background: #f05050; }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    margin-bottom: 0.3rem;
}
.step-icon { font-size: 1.1rem; }
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    font-weight: 500;
    letter-spacing: 0.15em;
    color: #ff8c32;
    opacity: 0.7;
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #f0ebe0;
}
.step-status {
    margin-left: auto;
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
}
.status-waiting  { color: #555; }
.status-running  { color: #ff8c32; }
.status-done     { color: #50c878; }
.status-failed   { color: #f05050; }

/* ── Result panels ── */
.result-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    margin-top: 1rem;
    margin-bottom: 1.5rem;
}
.result-panel-title {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #ff8c32;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.result-content {
    font-size: 0.92rem;
    line-height: 1.8;
    color: #cdc8bf;
    white-space: pre-wrap;
    font-family: 'DM Sans', sans-serif;
}

/* ── Report & feedback panels ── */
.report-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,140,50,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.feedback-panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(80,200,120,0.2);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    margin-top: 1rem;
}
.panel-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
    padding-bottom: 0.7rem;
}
.panel-label.orange {
    color: #ff8c32;
    border-bottom: 1px solid rgba(255,140,50,0.15);
}
.panel-label.green {
    color: #50c878;
    border-bottom: 1px solid rgba(80,200,120,0.15);
}

/* ── Progress text ── */
.stSpinner > div { color: #ff8c32 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    letter-spacing: 0.05em !important;
    color: #a09890 !important;
}
.stTabs [aria-selected="true"] { color: #ff8c32 !important; }

/* ── Expander ── */
details summary {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #a09890 !important;
    letter-spacing: 0.1em !important;
    cursor: pointer;
}

/* ── Section heading ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #f0ebe0;
    margin: 2rem 0 1rem;
}

/* ── Typography fix for Streamlit markdown ── */
.stMarkdown p, .stMarkdown li {
    line-height: 1.7 !important;
    color: #d4d4d8;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #f0ebe0;
}

/* ── Toast-style notice ── */
.notice {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #605850;
    text-align: center;
    margin-top: 3rem;
    letter-spacing: 0.08em;
}
</style>
""", unsafe_allow_html=True)


# ── Helper: render a step card ────────────────────────────────────────────────
STEP_META = {
    "search": ("01", "🔍", "Search Agent", "Gathers recent web information"),
    "reader": ("02", "📄", "Reader Agent", "Scrapes & extracts deep content"),
    "writer": ("03", "✍️", "Writer Chain", "Drafts the full research report"),
    "critic": ("04", "🧐", "Critic Chain", "Reviews & scores the report"),
}


def step_card(step: str, state: str):
    num, icon, title, desc = STEP_META[step]
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done":    ("✓ DONE",   "status-done"),
        "failed":  ("✕ FAILED", "status-failed"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done", "failed": "failed"}.get(state, "")
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-icon">{icon}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        <div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
defaults = {"results": {}, "running": False, "done": False, "error": None, "start_time": None}
for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ── Hero ──────────────────────────────────────────────────────────────────────
eyebrow = (
    '<span class="live-dot"></span> Pipeline running'
    if st.session_state.running
    else "Multi-Agent AI System"
)
st.markdown(f"""
<div class="hero">
    <div class="hero-eyebrow">{eyebrow}</div>
    <h1>Research<span>Mind</span></h1>
    <p class="hero-sub">
        Four specialized AI agents collaborate — searching, scraping, writing,
        and critiquing — to deliver a polished research report on any topic.
    </p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Layout: input left, pipeline right ───────────────────────────────────────
col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])

with col_input:
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        key="topic_input",
        label_visibility="visible",
        disabled=st.session_state.running,
    )
    run_btn = st.button(
        "⚡  Run Research Pipeline",
        use_container_width=True,
        disabled=st.session_state.running,
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Example chips
    examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
    chip_html = "".join(
        f'<span style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);'
        f'border-radius:6px;padding:0.25rem 0.7rem;font-size:0.75rem;color:#a09890;'
        f'font-family:\'DM Sans\',sans-serif;cursor:default;">{ex}</span>'
        for ex in examples
    )
    st.markdown(f"""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;align-items:center;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
        {chip_html}
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.error:
        st.error(f"⚠️ Pipeline failed: {st.session_state.error}")

with col_pipeline:
    st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)

    r = st.session_state.results
    completed = [k for k in STEPS if k in r]
    st.progress(len(completed) / len(STEPS))

    def step_state(step: str) -> str:
        if step in r:
            return "done"
        if st.session_state.error and not st.session_state.running:
            next_pending = next((s for s in STEPS if s not in r), None)
            if step == next_pending:
                return "failed"
        if st.session_state.running:
            next_pending = next((s for s in STEPS if s not in r), None)
            return "running" if step == next_pending else "waiting"
        return "waiting"

    for step in STEPS:
        step_card(step, step_state(step))

    if st.session_state.done and st.session_state.start_time:
        elapsed = time.time() - st.session_state.start_time
        st.caption(f"Completed in {elapsed:.1f}s")


# ── Kick off a run ────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.error = None
        st.session_state.start_time = time.time()
        st.rerun()


# ── Run pipeline: one step per rerun, so the pipeline cards animate live ──────
if st.session_state.running and not st.session_state.done:
    r = st.session_state.results
    topic_val = st.session_state.topic_input
    next_step = next((s for s in STEPS if s not in r), None)

    try:
        if next_step == "search":
            with st.spinner("🔍  Search Agent is working…"):
                search_agent = build_search_agent()
                sr = search_agent.invoke({
                    "messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]
                })
                r["search"] = sr["messages"][-1].content

        elif next_step == "reader":
            with st.spinner("📄  Reader Agent is scraping top resources…"):
                reader_agent = build_reader_agent()
                rr = reader_agent.invoke({
                    "messages": [("user",
                        f"Based on the following search results about '{topic_val}', "
                        f"pick the most relevant URL and scrape it for deeper content.\n\n"
                        f"Search Results:\n{r['search'][:800]}"
                    )]
                })
                r["reader"] = rr["messages"][-1].content

        elif next_step == "writer":
            with st.spinner("✍️  Writer is drafting the report…"):
                research_combined = (
                    f"SEARCH RESULTS:\n{r['search']}\n\n"
                    f"DETAILED SCRAPED CONTENT:\n{r['reader']}"
                )
                r["writer"] = writer_chain.invoke({
                    "topic": topic_val,
                    "research": research_combined
                })

        elif next_step == "critic":
            with st.spinner("🧐  Critic is reviewing the report…"):
                r["critic"] = critic_chain.invoke({"report": r["writer"]})
            st.session_state.running = False
            st.session_state.done = True

        st.session_state.results = dict(r)

    except Exception as e:
        st.session_state.error = str(e)
        st.session_state.running = False
        st.session_state.done = False

    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)

    tab_labels = []
    if "writer" in r: tab_labels.append("📝 Report")
    if "critic" in r: tab_labels.append("🧐 Critique")
    if "search" in r: tab_labels.append("🔍 Search Results")
    if "reader" in r: tab_labels.append("📄 Scraped Content")

    tabs = st.tabs(tab_labels)
    idx = 0

    if "writer" in r:
        with tabs[idx]:
            st.markdown('<div class="report-panel">', unsafe_allow_html=True)
            st.markdown(r["writer"])
            st.markdown("</div>", unsafe_allow_html=True)
            st.download_button(
                label="⬇  Download Report (.md)",
                data=r["writer"],
                file_name=f"research_report_{int(time.time())}.md",
                mime="text/markdown",
            )
        idx += 1

    if "critic" in r:
        with tabs[idx]:
            st.markdown('<div class="feedback-panel">', unsafe_allow_html=True)
            st.markdown(r["critic"])
            st.markdown("</div>", unsafe_allow_html=True)
        idx += 1

    if "search" in r:
        with tabs[idx]:
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Search Agent Output</div>'
                        f'<div class="result-content">{r["search"]}</div></div>', unsafe_allow_html=True)
        idx += 1

    if "reader" in r:
        with tabs[idx]:
            st.markdown(f'<div class="result-panel"><div class="result-panel-title">Reader Agent Output</div>'
                        f'<div class="result-content">{r["reader"]}</div></div>', unsafe_allow_html=True)
        idx += 1


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="notice">
    ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
</div>
""", unsafe_allow_html=True)
