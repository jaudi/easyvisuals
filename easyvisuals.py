import streamlit as st

st.set_page_config(page_title="EasyVisuals", page_icon="📊", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 2rem; max-width: 960px; }
        .hero-title { font-size: 3rem; font-weight: 800; color: #003f88; line-height: 1.15; }
        .hero-sub   { font-size: 1.2rem; color: #555; margin-top: 0.5rem; margin-bottom: 2rem; }
        .feature-box {
            background: #f7f9fc;
            border-left: 4px solid #0066cc;
            border-radius: 6px;
            padding: 1.1rem 1.3rem;
            height: 100%;
        }
        .feature-box h4 { margin: 0 0 0.4rem 0; color: #003f88; font-size: 1rem; }
        .feature-box p  { margin: 0; color: #555; font-size: 0.9rem; }
        .step-num { font-size: 2rem; font-weight: 800; color: #0066cc; }
        .divider  { border: none; border-top: 2px solid #eee; margin: 2rem 0; }
        .badge {
            display: inline-block;
            background: #e8f1fb;
            color: #003f88;
            font-size: 0.78rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            margin-right: 6px;
            margin-bottom: 6px;
        }
    </style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">📊 EasyVisuals</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-sub">Visual analytics for everyone — '
    'pay per <strong>solution</strong>, not per user.</div>',
    unsafe_allow_html=True,
)

st.page_link("pages/1_Builder.py", label="→ Launch the Builder", icon="🔨")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Problem / Solution ────────────────────────────────────────────────────────
st.markdown("## The problem with Power BI")
col_l, col_r = st.columns(2, gap="large")

with col_l:
    st.markdown("""
    **Power BI charges per user — every viewer pays.**

    A team of 50 people all needing to view the same dashboard?
    That's 50 licences, even if you only built one report.

    Costs spiral fast for growing teams, and small businesses
    are often priced out entirely.
    """)

with col_r:
    st.markdown("""
    **EasyVisuals charges per solution.**

    Build a dashboard once. Share it with your entire company,
    your clients, your partners — at no extra cost.

    We believe access to good data visuals should not depend
    on how many people need to see them.
    """)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Features ─────────────────────────────────────────────────────────────────
st.markdown("## What you can do")

f1, f2, f3, f4 = st.columns(4, gap="small")

features = [
    ("🧱", "Define your schema",
     "Specify columns — text, numbers, or dates — and preview dummy data instantly."),
    ("📂", "Upload your data",
     "Drop in a CSV or Excel file. We validate it against your schema automatically."),
    ("📈", "Build beautiful charts",
     "Bar, line, scatter, pie, histogram, heatmap — with professional color themes."),
    ("📄", "Export to PDF",
     "Download a polished PDF report ready to share with clients or stakeholders."),
]

for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
    with col:
        st.markdown(
            f'<div class="feature-box"><h4>{icon} {title}</h4><p>{desc}</p></div>',
            unsafe_allow_html=True,
        )

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("## How it works")

s1, s2, s3, s4 = st.columns(4, gap="medium")
steps = [
    ("1", "Define columns", "Name your columns and pick their type: Number, Text, or Date."),
    ("2", "Upload your file", "Upload CSV or Excel with the same column names."),
    ("3", "Configure chart", "Choose chart type, axes, color theme, and report title."),
    ("4", "Export", "Generate the chart and download a branded PDF report."),
]
for col, (num, title, desc) in zip([s1, s2, s3, s4], steps):
    with col:
        st.markdown(f'<div class="step-num">{num}</div>', unsafe_allow_html=True)
        st.markdown(f"**{title}**")
        st.caption(desc)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Tech stack badges ─────────────────────────────────────────────────────────
st.markdown("## Built with")
st.markdown(
    '<span class="badge">Python</span>'
    '<span class="badge">Streamlit</span>'
    '<span class="badge">Plotly</span>'
    '<span class="badge">ReportLab</span>'
    '<span class="badge">Pandas</span>',
    unsafe_allow_html=True,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.caption("EasyVisuals · Open source · MIT License · github.com/jaudi/easyvisuals")
