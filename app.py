from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# Regional Digital Payments Growth Monitor
# Source: PhonePe Pulse public aggregated data
# ============================================================

st.set_page_config(
    page_title="Regional Payments Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
STATE_CSV = BASE_DIR / "data" / "processed" / "phonepe_state_transactions.csv"
INDIA_CSV = BASE_DIR / "data" / "processed" / "phonepe_india_transactions.csv"

BG = "#090612"
PANEL = "#171128"
PANEL_2 = "#21183A"
PURPLE = "#8B5CF6"
LAVENDER = "#C4B5FD"
TEXT = "#F5F3FF"
MUTED = "#A49ABF"
GRID = "rgba(196,181,253,0.14)"
PALETTE = ["#8B5CF6", "#C4B5FD", "#6D28D9", "#A78BFA", "#DDD6FE"]

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    :root {{
      --bg: {BG}; --panel: {PANEL}; --purple: {PURPLE};
      --lavender: {LAVENDER}; --text: {TEXT}; --muted: {MUTED};
    }}
    html, body, [class*="css"] {{ font-family: Inter, sans-serif; }}
    .stApp {{
      background:
        radial-gradient(ellipse at 8% 0%, rgba(109,40,217,.24), transparent 34%),
        radial-gradient(ellipse at 95% 8%, rgba(139,92,246,.13), transparent 30%),
        {BG};
      color: {TEXT};
    }}
    [data-testid="stHeader"] {{ background: transparent; }}
    .block-container {{ max-width: 1500px; padding-top: 1.5rem; padding-bottom: 3rem; }}
    [data-testid="stSidebar"] {{
      background: linear-gradient(180deg, #171027 0%, #0D0918 100%);
      border-right: 1px solid rgba(167,139,250,.2);
    }}
    [data-testid="stSidebar"] * {{ color: {TEXT}; }}
    h1,h2,h3 {{ color: {TEXT} !important; letter-spacing: -.45px; }}
    p, label, .stCaption {{ color: #D0C8E5; }}
    .hero {{
      padding: 1.55rem 1.7rem; border-radius: 24px; margin-bottom: 1.2rem;
      border: 1px solid rgba(196,181,253,.25);
      background: linear-gradient(120deg, rgba(109,40,217,.27), rgba(23,17,40,.92) 55%, rgba(139,92,246,.12));
      box-shadow: 0 18px 55px rgba(0,0,0,.22);
    }}
    .eyebrow {{ color: {LAVENDER}; text-transform: uppercase; letter-spacing: 2px; font-size: .72rem; font-weight: 700; }}
    .hero h1 {{ font-size: clamp(1.7rem, 3vw, 2.65rem); margin: .45rem 0 .4rem; }}
    .hero p {{ margin: 0; color: #C8BFDE; font-size: .98rem; }}
    .metric-card {{
      padding: 1.05rem 1.15rem; border-radius: 18px; min-height: 122px;
      background: linear-gradient(135deg, rgba(139,92,246,.17), rgba(23,17,40,.93));
      border: 1px solid rgba(167,139,250,.25);
      box-shadow: 0 10px 30px rgba(0,0,0,.15);
    }}
    .metric-label {{ color: {LAVENDER}; font-size: .78rem; font-weight: 600; margin-bottom: .45rem; }}
    .metric-value {{ color: #FFFFFF; font-size: clamp(1.25rem, 2vw, 1.9rem); font-weight: 800; line-height: 1.2; }}
    .metric-note {{ color: {MUTED}; font-size: .72rem; margin-top: .45rem; }}
    .section-title {{ font-size: 1.1rem; font-weight: 750; color: {TEXT}; margin: .8rem 0 .2rem; }}
    .section-sub {{ color: {MUTED}; font-size: .82rem; margin-bottom: .7rem; }}
    div[data-testid="stPlotlyChart"] {{
      background: rgba(23,17,40,.72); border: 1px solid rgba(167,139,250,.18);
      border-radius: 18px; padding: 8px;
    }}
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stMultiSelect"] > div > div {{
      background: #19122C; border-color: #49366F; border-radius: 10px;
    }}
    .note {{
      border-left: 3px solid {PURPLE}; padding: .75rem 1rem; border-radius: 0 10px 10px 0;
      background: rgba(139,92,246,.09); color: #D8D0EA; font-size: .82rem;
    }}
    hr {{ border-color: rgba(167,139,250,.17); }}
    footer {{ visibility: hidden; }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_csv(path_string: str) -> pd.DataFrame:
    frame = pd.read_csv(path_string)
    return frame


def format_count(value) -> str:
    if pd.isna(value):
        return "—"
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:,.2f}B"
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:,.2f}M"
    if abs(value) >= 1_000:
        return f"{value / 1_000:,.1f}K"
    return f"{value:,.0f}"


def style_fig(fig, height=350):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEXT, size=11),
        margin=dict(l=12, r=12, t=28, b=12),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E9D5FF"),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        xaxis=dict(
            gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID,
            tickfont=dict(color=MUTED), title_font=dict(color=MUTED),
        ),
        yaxis=dict(
            gridcolor=GRID, zerolinecolor=GRID, linecolor=GRID,
            tickfont=dict(color=MUTED), title_font=dict(color=MUTED),
        ),
    )
    return fig


# ---- Load real project data; do not silently substitute synthetic demo data ----
if not STATE_CSV.exists():
    st.error("Cleaned state CSV not found.")
    st.code("data/processed/phonepe_state_transactions.csv")
    st.info("Project root ke andar `data/processed/phonepe_state_transactions.csv` file honi chahiye.")
    st.stop()

try:
    raw = load_csv(str(STATE_CSV))
except Exception as exc:
    st.error(f"CSV read nahi ho paayi: {exc}")
    st.stop()

required = {
    "state", "year", "quarter", "transaction_type",
    "payment_instrument", "transaction_count",
}
missing = required - set(raw.columns)
if missing:
    st.error(f"CSV mein required columns missing hain: {', '.join(sorted(missing))}")
    st.stop()

raw["state"] = raw["state"].astype(str).str.strip()
raw["transaction_type"] = raw["transaction_type"].astype(str).str.strip()
for col in ["year", "quarter", "transaction_count"]:
    raw[col] = pd.to_numeric(raw[col], errors="coerce")
raw = raw.dropna(subset=["state", "year", "quarter", "transaction_count"]).copy()
raw["year"] = raw["year"].astype(int)
raw["quarter"] = raw["quarter"].astype(int)
raw["transaction_count"] = raw["transaction_count"].astype("int64")
raw["period"] = raw["year"].astype(str) + " Q" + raw["quarter"].astype(str)
raw["period_order"] = raw["year"] * 10 + raw["quarter"]
raw["state_key"] = raw["state"].str.casefold()

# The state CSV should exclude the India aggregate; protect against accidental inclusion.
state_data = raw[raw["state_key"] != "india"].copy()
if state_data.empty:
    st.error("State-level data empty hai. CSV mein India aggregate ke alawa state records hone chahiye.")
    st.stop()

min_year = int(state_data["year"].min())
max_year = int(state_data["year"].max())
years = sorted(state_data["year"].unique().tolist())
states = sorted(state_data["state"].unique().tolist())
categories = sorted(state_data["transaction_type"].unique().tolist())

# ---- Sidebar filters ----
with st.sidebar:
    st.markdown("## ◈ Payments Intelligence")
    st.caption("PHONEPE PULSE · INDIA")
    st.markdown("---")
    st.markdown("### Filter data")
    selected_years = st.multiselect(
        "Year", years, default=[max_year] if max_year in years else years[-1:]
    )
    selected_states = st.multiselect("States / UTs", states, default=[])
    selected_categories = st.multiselect(
        "Transaction category", categories, default=categories
    )
    st.markdown("---")
    st.markdown("### About this dashboard")
    st.caption("Aggregated PhonePe Pulse transaction counts. Not individual users, payment value in ₹, or all-India UPI totals.")
    st.markdown("---")
    st.caption("Built with Python · Pandas · Plotly · Streamlit")


filtered = state_data.copy()
if selected_years:
    filtered = filtered[filtered["year"].isin(selected_years)]
else:
    filtered = filtered.iloc[0:0]
if selected_states:
    filtered = filtered[filtered["state"].isin(selected_states)]
if selected_categories:
    filtered = filtered[filtered["transaction_type"].isin(selected_categories)]
else:
    filtered = filtered.iloc[0:0]

# ---- Hero ----
st.markdown(
    """
    <div class="hero">
      <div class="eyebrow">Digital Payments · Regional Intelligence</div>
      <h1>Regional Digital Payments Growth Monitor</h1>
      <p>Explore transaction-count patterns across Indian states, quarters and payment categories.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if filtered.empty:
    st.warning("Current filters ke liye data nahi mila. Year aur category filters check karo.")
    st.stop()

# ---- KPI cards ----
total_transactions = filtered["transaction_count"].sum()
state_count = filtered["state"].nunique()
category_count = filtered["transaction_type"].nunique()
period_count = filtered[["year", "quarter"]].drop_duplicates().shape[0]

k1, k2, k3, k4 = st.columns(4)
for col, label, value, note in [
    (k1, "TRANSACTION COUNT", format_count(total_transactions), "Current filters ke hisaab se"),
    (k2, "STATES / UTs", f"{state_count}", "Selected geography"),
    (k3, "CATEGORIES", f"{category_count}", "P2P · Retail · Utility where available"),
    (k4, "QUARTERS", f"{period_count}", "Periods included in selection"),
]:
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)

# ---- Aggregate data for charts ----
quarterly = (
    filtered.groupby(["year", "quarter", "period", "period_order"], as_index=False)
    ["transaction_count"].sum()
    .sort_values("period_order")
)
category_mix = (
    filtered.groupby("transaction_type", as_index=False)["transaction_count"]
    .sum().sort_values("transaction_count", ascending=False)
)
state_rank = (
    filtered.groupby("state", as_index=False)["transaction_count"]
    .sum().sort_values("transaction_count", ascending=True).tail(10)
)

left, right = st.columns([1.55, 1])
with left:
    st.markdown('<div class="section-title">Quarterly transaction trend</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Sum of counts across the currently selected states and categories</div>', unsafe_allow_html=True)
    fig = px.line(
        quarterly, x="period", y="transaction_count", markers=True,
        labels={"period": "Quarter", "transaction_count": "Transaction count"},
        color_discrete_sequence=[LAVENDER],
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=7, color=PURPLE))
    fig.update_yaxes(tickformat="~s")
    st.plotly_chart(style_fig(fig, 365), use_container_width=True)

with right:
    st.markdown('<div class="section-title">Transaction category mix</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Share of transaction counts in the current selection</div>', unsafe_allow_html=True)
    fig = px.pie(
        category_mix, names="transaction_type", values="transaction_count",
        hole=0.68, color_discrete_sequence=PALETTE,
    )
    fig.update_traces(
        textposition="inside", textinfo="percent",
        marker=dict(line=dict(color=BG, width=3)),
        hovertemplate="%{label}<br>Count: %{value:,.0f}<br>Share: %{percent}<extra></extra>",
    )
    fig.update_layout(showlegend=True, annotations=[
        dict(text="Category<br>mix", x=0.5, y=0.5, font=dict(size=15, color=TEXT), showarrow=False)
    ])
    st.plotly_chart(style_fig(fig, 365), use_container_width=True)

left, right = st.columns([1.25, 1])
with left:
    st.markdown('<div class="section-title">Top 10 states / UTs</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ranked by aggregated transaction counts for the selected filters</div>', unsafe_allow_html=True)
    fig = px.bar(
        state_rank, x="transaction_count", y="state", orientation="h",
        labels={"state": "State / UT", "transaction_count": "Transaction count"},
        color="transaction_count", color_continuous_scale=["#C4B5FD", "#8B5CF6", "#6D28D9"],
    )
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(tickformat="~s")
    fig.update_traces(hovertemplate="%{y}<br>Count: %{x:,.0f}<extra></extra>")
    st.plotly_chart(style_fig(fig, 410), use_container_width=True)

with right:
    st.markdown('<div class="section-title">Quarter × category detail</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Explore how category counts vary across quarters</div>', unsafe_allow_html=True)
    heat = filtered.groupby(["period", "transaction_type"], as_index=False)["transaction_count"].sum()
    heat["period"] = pd.Categorical(
        heat["period"],
        categories=quarterly["period"].tolist(),
        ordered=True,
    )
    heat_pivot = heat.pivot(index="transaction_type", columns="period", values="transaction_count").fillna(0)
    fig = px.imshow(
        heat_pivot,
        aspect="auto",
        color_continuous_scale=["#171128", "#6D28D9", "#C4B5FD"],
        labels=dict(x="Quarter", y="Category", color="Count"),
    )
    fig.update_xaxes(tickangle=-45)
    st.plotly_chart(style_fig(fig, 410), use_container_width=True)

# ---- Data table and export ----
st.markdown('<div class="section-title">Explore the data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">Filtered records behind the visuals</div>', unsafe_allow_html=True)
display_cols = [
    "state", "year", "quarter", "transaction_type",
    "payment_instrument", "transaction_count",
]
table = filtered[display_cols].sort_values(
    ["year", "quarter", "state", "transaction_type"]
)
st.dataframe(
    table,
    use_container_width=True,
    hide_index=True,
    column_config={
        "state": st.column_config.TextColumn("State / UT"),
        "year": st.column_config.NumberColumn("Year", format="%d"),
        "quarter": st.column_config.NumberColumn("Quarter", format="%d"),
        "transaction_type": st.column_config.TextColumn("Category"),
        "payment_instrument": st.column_config.TextColumn("Instrument"),
        "transaction_count": st.column_config.NumberColumn("Transaction count", format="%,d"),
    },
)

st.download_button(
    "⬇ Download filtered data (CSV)",
    data=table.to_csv(index=False).encode("utf-8"),
    file_name="phonepe_pulse_filtered_transactions.csv",
    mime="text/csv",
)

st.markdown("---")
st.markdown(
    """
    <div class="note">
      <b>Data note:</b> This dashboard uses public, aggregated PhonePe Pulse data.
      Transaction counts are not rupee transaction value, unique users, active customers,
      or all-India UPI totals. The state-level view excludes the separate India aggregate
      to avoid double counting. Latest periods may be partial, so compare like-for-like
      quarters when assessing growth.
    </div>
    """,
    unsafe_allow_html=True,
)
