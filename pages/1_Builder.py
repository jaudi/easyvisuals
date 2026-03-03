import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import random
import io
import base64
from pathlib import Path
from datetime import datetime, timedelta

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable,
)

# ── Color themes ──────────────────────────────────────────────────────────────
THEMES = {
    "Corporate Blue": {
        "plotly_template": "plotly_white",
        "color_sequence": ["#003f88", "#0066cc", "#3399ff", "#66b2ff", "#99ccff", "#cce5ff"],
        "primary": "#003f88",
        "accent": "#0066cc",
        "pdf_header_bg": colors.HexColor("#003f88"),
        "pdf_accent": colors.HexColor("#0066cc"),
        "pdf_row_alt": colors.HexColor("#EAF1FB"),
    },
    "Executive Dark": {
        "plotly_template": "plotly_dark",
        "color_sequence": ["#C9A84C", "#E8C97A", "#F5E2A8", "#A07830", "#6B4F1A", "#3D2C0A"],
        "primary": "#1a1a2e",
        "accent": "#C9A84C",
        "pdf_header_bg": colors.HexColor("#1a1a2e"),
        "pdf_accent": colors.HexColor("#C9A84C"),
        "pdf_row_alt": colors.HexColor("#F5F0E8"),
    },
    "Modern Teal": {
        "plotly_template": "plotly_white",
        "color_sequence": ["#007C77", "#00B4AE", "#44D4CE", "#88EAE6", "#00544F", "#003330"],
        "primary": "#007C77",
        "accent": "#00B4AE",
        "pdf_header_bg": colors.HexColor("#007C77"),
        "pdf_accent": colors.HexColor("#00B4AE"),
        "pdf_row_alt": colors.HexColor("#E6F7F7"),
    },
    "Slate & Crimson": {
        "plotly_template": "plotly_white",
        "color_sequence": ["#2F4F6F", "#C0392B", "#5D8AA8", "#E74C3C", "#1A3A52", "#922B21"],
        "primary": "#2F4F6F",
        "accent": "#C0392B",
        "pdf_header_bg": colors.HexColor("#2F4F6F"),
        "pdf_accent": colors.HexColor("#C0392B"),
        "pdf_row_alt": colors.HexColor("#F2F5F8"),
    },
    "Sunset": {
        "plotly_template": "plotly_white",
        "color_sequence": ["#FF6B35", "#F7C59F", "#EFEFD0", "#004E89", "#1A936F", "#88D498"],
        "primary": "#FF6B35",
        "accent": "#004E89",
        "pdf_header_bg": colors.HexColor("#FF6B35"),
        "pdf_accent": colors.HexColor("#004E89"),
        "pdf_row_alt": colors.HexColor("#FFF5F0"),
    },
}

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Builder · EasyVisuals", page_icon="🔨", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; }
        h2 { font-size: 1.25rem !important; color: #333;
             border-bottom: 2px solid #eee; padding-bottom: 6px; margin-top: 1.5rem; }
        .ev-caption { color: #888; font-size: 0.88rem; margin-top: -6px; margin-bottom: 1rem; }
        .stButton > button[kind="primary"] { border-radius: 8px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

st.title("🔨 Visual Builder")
st.markdown('<p class="ev-caption">Define columns · Preview dummy data · Upload file · Generate chart · Export PDF</p>', unsafe_allow_html=True)

# ── Step 1: Define columns ────────────────────────────────────────────────────
st.header("Step 1 — Define your columns")

num_cols = st.number_input("How many columns?", min_value=1, max_value=20, value=2, step=1)

col_names, col_types = [], []
grid = st.columns(min(int(num_cols), 4))
for i in range(int(num_cols)):
    with grid[i % len(grid)]:
        name = st.text_input(f"Column {i+1} name", key=f"col_name_{i}", placeholder=f"column_{i+1}")
        dtype = st.selectbox("Type", ["Number", "Text", "Date"], key=f"col_type_{i}")
        col_names.append(name.strip() if name.strip() else f"column_{i+1}")
        col_types.append(dtype)

# ── Step 2: Dummy preview ─────────────────────────────────────────────────────
st.header("Step 2 — Dummy data preview")
st.caption("Your file must contain these exact column names.")

DUMMY_ROWS = 8
text_samples = ["Alpha", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta"]
_date_start = datetime(2023, 1, 1)

dummy = {}
for name, dtype in zip(col_names, col_types):
    if dtype == "Number":
        dummy[name] = np.round(np.random.uniform(10, 1000, DUMMY_ROWS), 2).tolist()
    elif dtype == "Date":
        dummy[name] = [
            (_date_start + timedelta(days=random.randint(0, 730))).strftime("%Y-%m-%d")
            for _ in range(DUMMY_ROWS)
        ]
    else:
        dummy[name] = [random.choice(text_samples) for _ in range(DUMMY_ROWS)]

st.dataframe(pd.DataFrame(dummy), use_container_width=True)

# ── Step 3: Upload ────────────────────────────────────────────────────────────
st.header("Step 3 — Upload your data")

uploaded_file = st.file_uploader(
    "Upload CSV or Excel (.csv, .xlsx, .xls)",
    type=["csv", "xlsx", "xls"],
)

df = None
if uploaded_file is not None:
    try:
        df = (
            pd.read_csv(uploaded_file)
            if uploaded_file.name.endswith(".csv")
            else pd.read_excel(uploaded_file)
        )
        missing = [c for c in col_names if c not in df.columns]
        if missing:
            st.error(f"Missing columns: **{', '.join(missing)}**")
            st.info(f"Columns in file: {', '.join(df.columns.tolist())}")
            df = None
        else:
            df = df[col_names].copy()
            for name, dtype in zip(col_names, col_types):
                if dtype == "Number":
                    df[name] = pd.to_numeric(df[name], errors="coerce")
                elif dtype == "Date":
                    df[name] = pd.to_datetime(df[name], errors="coerce")
            st.success(f"Loaded — {len(df):,} rows · {len(df.columns)} columns")
            st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Could not read file: {e}")

# ── Step 4: Chart config ──────────────────────────────────────────────────────
if df is not None:
    st.header("Step 4 — Configure your chart")

    numeric_cols = [n for n, t in zip(col_names, col_types) if t == "Number"]
    date_cols    = [n for n, t in zip(col_names, col_types) if t == "Date"]
    text_cols    = [n for n, t in zip(col_names, col_types) if t == "Text"]

    # Suggest line chart when dates are present
    default_chart = "Line" if date_cols else "Bar"
    chart_options = ["Bar", "Line", "Area", "Scatter", "Pie", "Histogram", "Heatmap"]

    cfg1, cfg2, cfg3 = st.columns([2, 2, 1])
    with cfg1:
        chart_type = st.selectbox("Chart type", chart_options,
                                  index=chart_options.index(default_chart))
    with cfg2:
        theme_name = st.selectbox("Color theme", list(THEMES.keys()))
    with cfg3:
        smooth_lines = st.checkbox("Smooth lines", value=True) if chart_type in ["Line", "Area"] else False

    theme = THEMES[theme_name]
    report_title = st.text_input("Report title (for PDF)", value="Data Visualization Report")

    # Columns eligible for X axis (all types)
    x_eligible = col_names
    # Auto-place date col first in X options if present
    if date_cols:
        x_eligible = date_cols + [c for c in col_names if c not in date_cols]

    x_col = y_col = color_col = names_col = values_col = hist_col = None
    bins = 20

    if chart_type in ["Bar", "Line", "Area", "Scatter"]:
        c1, c2, c3 = st.columns(3)
        with c1:
            x_col = st.selectbox("X axis", x_eligible, key="x")
        with c2:
            y_col = st.selectbox("Y axis", numeric_cols if numeric_cols else col_names, key="y")
        with c3:
            cc = st.selectbox("Color by (optional)", ["None"] + col_names, key="color")
            color_col = None if cc == "None" else cc

    elif chart_type == "Pie":
        c1, c2 = st.columns(2)
        with c1:
            names_col = st.selectbox("Labels column", col_names, key="pie_names")
        with c2:
            values_col = st.selectbox("Values column", numeric_cols if numeric_cols else col_names, key="pie_values")

    elif chart_type == "Histogram":
        c1, c2 = st.columns(2)
        with c1:
            hist_col = st.selectbox("Column", numeric_cols if numeric_cols else col_names, key="hist")
        with c2:
            bins = st.slider("Bins", 5, 100, 20)

    elif chart_type == "Heatmap":
        if len(numeric_cols) < 2:
            st.warning("Heatmap needs at least 2 numeric columns.")

    # ── Step 5: Generate & Export ─────────────────────────────────────────────
    st.header("Step 5 — Generate & Export")

    if st.button("Generate Chart", type="primary", use_container_width=True):
        try:
            line_shape = "spline" if smooth_lines else "linear"

            common = dict(
                template=theme["plotly_template"],
                color_discrete_sequence=theme["color_sequence"],
            )

            # ── Build main chart ───────────────────────────────────────────
            if chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col, color=color_col,
                             title=f"{y_col} by {x_col}", **common)
                fig.update_traces(
                    marker_line_width=0,
                    opacity=0.88,
                )

            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col, color=color_col,
                              title=f"{y_col} over {x_col}",
                              line_shape=line_shape, markers=True, **common)
                fig.update_traces(
                    line=dict(width=3),
                    marker=dict(size=7, line=dict(width=2, color="white")),
                )

            elif chart_type == "Area":
                fig = px.area(df, x=x_col, y=y_col, color=color_col,
                              title=f"{y_col} over {x_col}",
                              line_shape=line_shape, **common)
                fig.update_traces(
                    line=dict(width=2.5),
                    opacity=0.75,
                )

            elif chart_type == "Scatter":
                fig = px.scatter(df, x=x_col, y=y_col, color=color_col,
                                 title=f"{y_col} vs {x_col}",
                                 trendline="ols" if numeric_cols else None,
                                 **common)
                fig.update_traces(
                    marker=dict(size=10, opacity=0.8,
                                line=dict(width=1, color="white")),
                )

            elif chart_type == "Pie":
                fig = px.pie(df, names=names_col, values=values_col,
                             title=f"{values_col} distribution",
                             color_discrete_sequence=theme["color_sequence"],
                             template=theme["plotly_template"],
                             hole=0.35)
                fig.update_traces(
                    textposition="outside",
                    textinfo="percent+label",
                    marker=dict(line=dict(color="white", width=2)),
                )

            elif chart_type == "Histogram":
                fig = px.histogram(df, x=hist_col, nbins=bins,
                                   title=f"Distribution of {hist_col}", **common)
                fig.update_traces(marker_line_width=0, opacity=0.85)

            elif chart_type == "Heatmap":
                corr = df[numeric_cols].corr()
                fig = px.imshow(corr, text_auto=".2f", title="Correlation Heatmap",
                                color_continuous_scale="RdBu_r",
                                template=theme["plotly_template"],
                                zmin=-1, zmax=1)

            # ── Shared layout polish ───────────────────────────────────────
            is_dark = "dark" in theme["plotly_template"]
            bg = "#16213e" if is_dark else "white"
            plot_bg = "#1a1a2e" if is_dark else "rgba(248,249,252,1)"
            grid_color = "rgba(255,255,255,0.08)" if is_dark else "rgba(0,0,0,0.06)"

            fig.update_layout(
                height=520,
                font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=13),
                title_font=dict(size=20, family="Inter, Segoe UI, Arial, sans-serif",
                                color=theme["primary"]),
                title_x=0.01,
                paper_bgcolor=bg,
                plot_bgcolor=plot_bg,
                margin=dict(t=70, b=55, l=55, r=30),
                legend=dict(
                    bgcolor="rgba(255,255,255,0.9)" if not is_dark else "rgba(30,30,50,0.9)",
                    bordercolor="rgba(0,0,0,0.08)",
                    borderwidth=1,
                    font=dict(size=12),
                ),
                hoverlabel=dict(
                    bgcolor="white" if not is_dark else "#2a2a4e",
                    bordercolor="rgba(0,0,0,0.1)",
                    font_size=13,
                    font_family="Inter, Arial, sans-serif",
                ),
                bargap=0.25,
            )

            if chart_type not in ["Pie", "Heatmap"]:
                fig.update_xaxes(
                    showgrid=False,
                    showline=True,
                    linecolor="rgba(0,0,0,0.12)" if not is_dark else "rgba(255,255,255,0.1)",
                    tickfont=dict(size=11),
                    title_font=dict(size=13),
                    zeroline=False,
                )
                fig.update_yaxes(
                    gridcolor=grid_color,
                    showline=False,
                    tickfont=dict(size=11),
                    title_font=dict(size=13),
                    zeroline=False,
                )

            st.plotly_chart(fig, use_container_width=True)

            # ── Supplementary charts ───────────────────────────────────────
            supp_layout = dict(
                height=380,
                font=dict(family="Inter, Segoe UI, Arial, sans-serif", size=12),
                paper_bgcolor=bg,
                plot_bgcolor=plot_bg,
                margin=dict(t=55, b=45, l=45, r=20),
                hoverlabel=dict(bgcolor="white" if not is_dark else "#2a2a4e",
                                font_size=12),
                bargap=0.25,
            )
            supp_figs = []

            if numeric_cols:
                fig2 = px.histogram(df, x=numeric_cols[0], nbins=20,
                                    title=f"Distribution — {numeric_cols[0]}", **common)
                fig2.update_traces(marker_line_width=0, opacity=0.85)
                fig2.update_layout(
                    title_font=dict(size=15, color=theme["primary"]),
                    **supp_layout,
                )
                fig2.update_xaxes(showgrid=False, showline=True,
                                  linecolor="rgba(0,0,0,0.12)")
                fig2.update_yaxes(gridcolor=grid_color, showline=False)
                supp_figs.append(fig2)

            if len(numeric_cols) >= 2:
                fig3 = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1],
                                  title=f"{numeric_cols[1]} vs {numeric_cols[0]}", **common)
                fig3.update_traces(marker=dict(size=9, opacity=0.8,
                                               line=dict(width=1, color="white")))
                fig3.update_layout(
                    title_font=dict(size=15, color=theme["primary"]),
                    **supp_layout,
                )
                fig3.update_xaxes(showgrid=False, showline=True,
                                  linecolor="rgba(0,0,0,0.12)")
                fig3.update_yaxes(gridcolor=grid_color, showline=False)
                supp_figs.append(fig3)
            elif text_cols and numeric_cols:
                fig3 = px.bar(df, x=text_cols[0], y=numeric_cols[0],
                              title=f"{numeric_cols[0]} by {text_cols[0]}", **common)
                fig3.update_traces(marker_line_width=0, opacity=0.88)
                fig3.update_layout(
                    title_font=dict(size=15, color=theme["primary"]),
                    **supp_layout,
                )
                fig3.update_xaxes(showgrid=False, showline=True,
                                  linecolor="rgba(0,0,0,0.12)")
                fig3.update_yaxes(gridcolor=grid_color, showline=False)
                supp_figs.append(fig3)

            if supp_figs:
                supp_cols = st.columns(len(supp_figs))
                for sc, sf in zip(supp_cols, supp_figs):
                    with sc:
                        st.plotly_chart(sf, use_container_width=True)

            # ── PDF export ────────────────────────────────────────────────
            st.subheader("Export")

            all_chart_bytes = [fig.to_image(format="png", width=900, height=480, scale=2)]
            for sf in supp_figs:
                all_chart_bytes.append(sf.to_image(format="png", width=900, height=480, scale=2))

            def build_pdf(title, df, chart_bytes_list, theme, chart_type):
                buf = io.BytesIO()
                doc = SimpleDocTemplate(
                    buf, pagesize=A4,
                    leftMargin=2*cm, rightMargin=2*cm,
                    topMargin=1.5*cm, bottomMargin=2*cm,
                )
                W = A4[0] - 4*cm

                header_style = ParagraphStyle(
                    "header", fontName="Helvetica-Bold", fontSize=22,
                    textColor=colors.white, alignment=TA_LEFT,
                )
                sub_style = ParagraphStyle(
                    "sub", fontName="Helvetica", fontSize=10,
                    textColor=colors.HexColor("#ccddee"), alignment=TA_LEFT,
                )
                section_style = ParagraphStyle(
                    "section", fontName="Helvetica-Bold", fontSize=12,
                    textColor=theme["primary"], spaceBefore=14, spaceAfter=4,
                )
                footer_style = ParagraphStyle(
                    "footer", fontName="Helvetica", fontSize=8,
                    textColor=colors.HexColor("#999999"), alignment=TA_CENTER,
                )

                story = []

                # Header banner
                header_table = Table(
                    [[Paragraph("EasyVisuals", header_style),
                      Paragraph(title, header_style),
                      Paragraph(f"Generated\n{datetime.now().strftime('%B %d, %Y')}", sub_style)]],
                    colWidths=[W * 0.22, W * 0.50, W * 0.28],
                )
                header_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, -1), theme["pdf_header_bg"]),
                    ("TOPPADDING",    (0, 0), (-1, -1), 16),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
                    ("LEFTPADDING",   (0, 0), (-1, -1), 14),
                    ("RIGHTPADDING",  (0, 0), (-1, -1), 14),
                    ("VALIGN",  (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN",   (2, 0), (2, 0),  "RIGHT"),
                ]))
                story.append(header_table)
                story.append(Spacer(1, 0.4*cm))
                story.append(HRFlowable(width="100%", thickness=3,
                                        color=theme["pdf_accent"], spaceAfter=8))

                # Summary
                summary_data = [
                    ["Rows", "Columns", "Chart Type", "Theme"],
                    [f"{len(df):,}", str(len(df.columns)), chart_type, theme_name],
                ]
                summary_table = Table(summary_data, colWidths=[W/4]*4)
                summary_table.setStyle(TableStyle([
                    ("BACKGROUND", (0, 0), (-1, 0), theme["pdf_accent"]),
                    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE",   (0, 0), (-1, -1), 10),
                    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING",    (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                    ("BACKGROUND", (0, 1), (-1, 1), theme["pdf_row_alt"]),
                    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
                ]))
                story.append(summary_table)
                story.append(Spacer(1, 0.3*cm))

                # Charts
                story.append(Paragraph("Visualizations", section_style))
                story.append(HRFlowable(width="100%", thickness=1,
                                        color=colors.HexColor("#DDDDDD"), spaceAfter=6))
                for cb in chart_bytes_list:
                    img = Image(io.BytesIO(cb), width=W, height=W * 0.53)
                    story.append(img)
                    story.append(Spacer(1, 0.3*cm))

                # Data table
                story.append(Paragraph("Data Preview (first 20 rows)", section_style))
                story.append(HRFlowable(width="100%", thickness=1,
                                        color=colors.HexColor("#DDDDDD"), spaceAfter=6))

                preview = df.head(20).copy()
                table_data = [list(preview.columns)] + preview.astype(str).values.tolist()
                col_w = W / len(preview.columns)
                data_table = Table(table_data, colWidths=[col_w]*len(preview.columns), repeatRows=1)

                row_styles = [
                    ("BACKGROUND", (0, 0), (-1, 0), theme["pdf_header_bg"]),
                    ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
                    ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE",   (0, 0), (-1, -1), 8),
                    ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
                    ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
                    ("TOPPADDING",    (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#DDDDDD")),
                ]
                for row_i in range(1, len(table_data)):
                    if row_i % 2 == 0:
                        row_styles.append(
                            ("BACKGROUND", (0, row_i), (-1, row_i), theme["pdf_row_alt"])
                        )
                data_table.setStyle(TableStyle(row_styles))
                story.append(data_table)

                story.append(Spacer(1, 0.6*cm))
                story.append(HRFlowable(width="100%", thickness=1,
                                        color=colors.HexColor("#DDDDDD"), spaceAfter=4))
                story.append(Paragraph("Generated by EasyVisuals · Confidential", footer_style))

                doc.build(story)
                buf.seek(0)
                return buf

            pdf_buf = build_pdf(report_title, df, all_chart_bytes, theme, chart_type)

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "📄 Download PDF Report",
                    pdf_buf,
                    file_name=f"{report_title.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )
            with col_b:
                csv = df.to_csv(index=False)
                st.download_button(
                    "⬇️ Download CSV",
                    csv,
                    file_name="easyvisuals_data.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

        except Exception as e:
            st.error(f"Error generating chart: {e}")
