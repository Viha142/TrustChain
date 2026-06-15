import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VendorVault AI",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Hide default Streamlit header */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main background */
.stApp {
    background: linear-gradient(135deg, #F0F4FF 0%, #F8FAFF 50%, #EEF2FF 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E1B4B 50%, #1E3A5F 100%) !important;
    border-right: none;
}
section[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    color: #CBD5E1 !important;
}

/* KPI Cards */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 24px rgba(37,99,235,0.08);
    border: 1px solid rgba(37,99,235,0.08);
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
    overflow: hidden;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(37,99,235,0.15);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
}
.kpi-blue::before { background: linear-gradient(90deg, #2563EB, #3B82F6); }
.kpi-purple::before { background: linear-gradient(90deg, #7C3AED, #A855F7); }
.kpi-cyan::before { background: linear-gradient(90deg, #06B6D4, #22D3EE); }
.kpi-green::before { background: linear-gradient(90deg, #059669, #10B981); }
.kpi-red::before { background: linear-gradient(90deg, #DC2626, #EF4444); }

.kpi-label {
    font-size: 12px;
    font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
}
.kpi-value {
    font-size: 36px;
    font-weight: 800;
    color: #0F172A;
    line-height: 1;
    margin-bottom: 6px;
}
.kpi-sub {
    font-size: 13px;
    color: #64748B;
    font-weight: 500;
}
.kpi-icon {
    font-size: 28px;
    margin-bottom: 12px;
}

/* Section headers */
.section-header {
    font-size: 20px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 14px;
    color: #64748B;
    margin-bottom: 20px;
}

/* Supplier cards */
.supplier-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0;
    margin-bottom: 12px;
    transition: all 0.2s;
}
.supplier-card:hover {
    box-shadow: 0 6px 24px rgba(37,99,235,0.12);
    border-color: #BFDBFE;
    transform: translateY(-1px);
}

/* Badge */
.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.badge-blue { background: #DBEAFE; color: #1D4ED8; }
.badge-green { background: #D1FAE5; color: #065F46; }
.badge-red { background: #FEE2E2; color: #991B1B; }
.badge-yellow { background: #FEF3C7; color: #92400E; }
.badge-purple { background: #EDE9FE; color: #5B21B6; }

/* Hero */
.hero-section {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 40%, #7C3AED 100%);
    border-radius: 20px;
    padding: 40px 48px;
    color: white;
    margin-bottom: 32px;
    position: relative;
    overflow: hidden;
}
.hero-section::after {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 8px;
    line-height: 1.1;
}
.hero-sub {
    font-size: 18px;
    opacity: 0.85;
    font-weight: 400;
}
.hero-date {
    font-size: 13px;
    opacity: 0.6;
    margin-top: 16px;
    font-weight: 500;
}

/* Chart card */
.chart-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0;
    margin-bottom: 24px;
}

/* Alert card */
.alert-card {
    background: linear-gradient(135deg, #FFF7ED, #FEF3C7);
    border: 1px solid #FDE68A;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.alert-critical {
    background: linear-gradient(135deg, #FFF1F2, #FFE4E6);
    border-color: #FECDD3;
}

/* Divider */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
    margin: 28px 0;
}

/* Recommendation card */
.rec-card {
    background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
    border: 1px solid #BFDBFE;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}
.rec-supplier {
    font-size: 16px;
    font-weight: 700;
    color: #1D4ED8;
    margin-bottom: 4px;
}
.rec-detail {
    font-size: 13px;
    color: #475569;
    line-height: 1.6;
}

/* Metric delta */
.metric-up { color: #059669; font-weight: 600; }
.metric-down { color: #DC2626; font-weight: 600; }

/* Sidebar logo */
.sidebar-logo {
    padding: 20px 16px 24px;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 16px;
}
.sidebar-logo-title {
    font-size: 20px;
    font-weight: 800;
    color: white;
}
.sidebar-logo-sub {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 2px;
}
</style>
""", unsafe_allow_html=True)

# ─── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_data():
    try:
        products = pd.read_csv("data/products.csv")
    except FileNotFoundError:
        products = pd.DataFrame(columns=["Product","Category","CurrentStock","MinimumStock"])

    try:
        suppliers = pd.read_csv("data/suppliers.csv")
    except FileNotFoundError:
        suppliers = pd.DataFrame(columns=["Supplier","Category","Fulfillment","OnTime","PriceScore","Inventory","Rating"])

    try:
        ratings = pd.read_csv("data/ratings.csv")
    except FileNotFoundError:
        ratings = pd.DataFrame(columns=["Supplier","Stars","Comment"])

    return products, suppliers, ratings

# ─── Reliability Score Formula ─────────────────────────────────────────────────
def calc_reliability(row):
    return (row["Fulfillment"] * 0.4 +
            row["OnTime"] * 0.3 +
            row["Rating"] * 20 * 0.2 +
            row["PriceScore"] * 20 * 0.1)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div style="font-size:28px; margin-bottom:6px;">🏪</div>
        <div class="sidebar-logo-title">VendorVault AI</div>
        <div class="sidebar-logo-sub">Smart Procurement Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

   

    # Dark mode toggle
    dark = st.toggle("🌙 Dark Mode", value=False)

    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown(f"""
    <div style='margin-top:24px; padding:16px; background:rgba(255,255,255,0.06);
         border-radius:12px; border:1px solid rgba(255,255,255,0.1)'>
        <div style='font-size:11px; color:#94A3B8; text-transform:uppercase;
             letter-spacing:0.08em; margin-bottom:6px;'>Session</div>
        <div style='font-size:12px; color:#CBD5E1;'>📅 {datetime.now().strftime("%d %b %Y")}</div>
        <div style='font-size:12px; color:#CBD5E1; margin-top:4px;'>🕐 {datetime.now().strftime("%I:%M %p")}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── Load Data ─────────────────────────────────────────────────────────────────
products, suppliers, ratings = load_data()

# Compute reliability scores
if not suppliers.empty:
    suppliers["ReliabilityScore"] = suppliers.apply(calc_reliability, axis=1).round(1)
    suppliers_sorted = suppliers.sort_values("ReliabilityScore", ascending=False)

# Low stock
if not products.empty:
    low_stock = products[products["CurrentStock"] < products["MinimumStock"]]
    critical = products[products["CurrentStock"] < products["MinimumStock"] * 0.5]

# ─── Hero Section ─────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-section">
    <div style="font-size:13px; opacity:0.65; font-weight:500; margin-bottom:8px; text-transform:uppercase; letter-spacing:0.1em;">
        PROCUREMENT DASHBOARD
    </div>
    <div class="hero-title">🏪 VendorVault AI</div>
    <div class="hero-sub">Helping small retailers source smarter, faster, and more reliably</div>
    <div class="hero-date">📅 {datetime.now().strftime("%A, %d %B %Y")}</div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Cards ────────────────────────────────────────────────────────────────
total_products = len(products) if not products.empty else 0
active_suppliers = len(suppliers) if not suppliers.empty else 0
low_stock_count = len(low_stock) if not products.empty else 0
avg_rating = suppliers["Rating"].mean() if not suppliers.empty else 0
avg_reliability = suppliers["ReliabilityScore"].mean() if not suppliers.empty else 0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-icon">📦</div>
        <div class="kpi-label">Total Products</div>
        <div class="kpi-value">{total_products}</div>
        <div class="kpi-sub">Across all categories</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card kpi-purple">
        <div class="kpi-icon">🤝</div>
        <div class="kpi-label">Active Suppliers</div>
        <div class="kpi-value">{active_suppliers}</div>
        <div class="kpi-sub">Verified vendor network</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    color = "kpi-red" if low_stock_count > 3 else "kpi-yellow"
    st.markdown(f"""
    <div class="kpi-card {color}">
        <div class="kpi-icon">⚠️</div>
        <div class="kpi-label">Low Stock Alerts</div>
        <div class="kpi-value">{low_stock_count}</div>
        <div class="kpi-sub">Products need restocking</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card kpi-green">
        <div class="kpi-icon">⭐</div>
        <div class="kpi-label">Avg Supplier Rating</div>
        <div class="kpi-value">{avg_rating:.1f}</div>
        <div class="kpi-sub">Out of 5.0 across network</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Charts Row ───────────────────────────────────────────────────────────────
col_chart, col_recs = st.columns([3, 2], gap="large")

with col_chart:
    st.markdown("""
    <div class="section-header">📊 Supplier Reliability Comparison</div>
    <div class="section-sub">Composite score based on fulfillment, on-time delivery, rating & price</div>
    """, unsafe_allow_html=True)

    if not suppliers.empty:
        colors_bar = ["#2563EB" if i == 0 else "#93C5FD" for i in range(len(suppliers_sorted))]
        fig = go.Figure(go.Bar(
            x=suppliers_sorted["ReliabilityScore"],
            y=suppliers_sorted["Supplier"],
            orientation='h',
            marker=dict(
                color=colors_bar,
                line=dict(width=0),
            ),
            text=suppliers_sorted["ReliabilityScore"].apply(lambda x: f"{x:.1f}"),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<extra></extra>'
        ))
        fig.update_layout(
            height=340,
            margin=dict(l=0, r=40, t=10, b=10),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(family='Inter', size=12, color='#475569'),
            xaxis=dict(
                range=[0, 105],
                showgrid=True,
                gridcolor='#F1F5F9',
                zeroline=False,
                ticksuffix=''
            ),
            yaxis=dict(showgrid=False, autorange='reversed'),
            bargap=0.3,
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_recs:
    st.markdown("""
    <div class="section-header">🎯 Today's Procurement Picks</div>
    <div class="section-sub">Top recommended suppliers right now</div>
    """, unsafe_allow_html=True)

    if not suppliers.empty:
        top3 = suppliers_sorted.head(3)
        badges = ["🥇 Best Match", "🥈 Strong Pick", "🥉 Solid Option"]
        badge_colors = ["badge-blue", "badge-green", "badge-purple"]

        for idx, (_, row) in enumerate(top3.iterrows()):
            stock_pct = min(100, int(row["Inventory"] / 10))
            st.markdown(f"""
            <div class="rec-card">
                <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:10px;">
                    <div class="rec-supplier">{row['Supplier']}</div>
                    <span class="badge {badge_colors[idx]}">{badges[idx]}</span>
                </div>
                <div class="rec-detail">
                    📦 <b>{row['Category']}</b> &nbsp;|&nbsp;
                    ⭐ <b>{row['Rating']}</b> rating &nbsp;|&nbsp;
                    🎯 <b>{row['ReliabilityScore']:.0f}</b> score
                </div>
                <div class="rec-detail" style="margin-top:6px;">
                    📊 Fulfillment: <b>{row['Fulfillment']}%</b> &nbsp;|&nbsp;
                    🚚 On-time: <b>{row['OnTime']}%</b>
                </div>
                <div style="margin-top:10px; background:#E2E8F0; border-radius:4px; height:6px; overflow:hidden;">
                    <div style="width:{stock_pct}%; height:100%;
                         background:linear-gradient(90deg,#2563EB,#7C3AED);
                         border-radius:4px;"></div>
                </div>
                <div style="font-size:11px; color:#94A3B8; margin-top:4px;">
                    Inventory: {row['Inventory']} units available
                </div>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Low Stock Alerts ─────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">🚨 Low Stock Alerts</div>
<div class="section-sub">Products below minimum threshold — immediate action recommended</div>
""", unsafe_allow_html=True)

if not products.empty and len(low_stock) > 0:
    alert_cols = st.columns(min(4, len(low_stock)))
    for i, (_, row) in enumerate(low_stock.head(8).iterrows()):
        pct = int(row["CurrentStock"] / row["MinimumStock"] * 100)
        is_critical = pct < 50
        with alert_cols[i % 4]:
            bg = "#FFF1F2" if is_critical else "#FFFBEB"
            border = "#FECDD3" if is_critical else "#FDE68A"
            label = "🔴 CRITICAL" if is_critical else "🟡 LOW"
            label_color = "#991B1B" if is_critical else "#92400E"
            st.markdown(f"""
            <div style="background:{bg}; border:1px solid {border}; border-radius:12px;
                 padding:16px; margin-bottom:12px; text-align:center;">
                <div style="font-size:22px; margin-bottom:6px;">📉</div>
                <div style="font-weight:700; font-size:14px; color:#0F172A;">{row['Product']}</div>
                <div style="font-size:12px; color:#64748B; margin:4px 0;">{row['Category']}</div>
                <div style="font-size:24px; font-weight:800; color:#DC2626; margin:8px 0;">
                    {row['CurrentStock']}
                </div>
                <div style="font-size:11px; color:#94A3B8;">of {row['MinimumStock']} min units</div>
                <div style="margin-top:8px; background:#E2E8F0; border-radius:4px; height:5px;">
                    <div style="width:{pct}%; height:100%;
                         background:{'#EF4444' if is_critical else '#F59E0B'};
                         border-radius:4px;"></div>
                </div>
                <div style="margin-top:8px;">
                    <span style="background:{border}; color:{label_color}; padding:2px 10px;
                         border-radius:20px; font-size:10px; font-weight:700;">{label}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.success("✅ All products are sufficiently stocked! No alerts at this time.")

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Inventory Donut + Supplier Scatter ───────────────────────────────────────
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div class="section-header">🗂️ Category Distribution</div>
    <div class="section-sub">Products grouped by category</div>
    """, unsafe_allow_html=True)

    if not products.empty:
        cat_data = products.groupby("Category")["CurrentStock"].sum().reset_index()
        fig2 = px.pie(
            cat_data,
            names="Category",
            values="CurrentStock",
            hole=0.55,
            color_discrete_sequence=["#2563EB","#7C3AED","#06B6D4","#059669","#F59E0B","#EF4444"],
        )
        fig2.update_traces(textposition='outside', textinfo='label+percent')
        fig2.update_layout(
            height=300,
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='white',
            showlegend=False,
            font=dict(family='Inter', size=12, color='#475569'),
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

with c2:
    st.markdown("""
    <div class="section-header">🔍 Fulfillment vs Rating</div>
    <div class="section-sub">Supplier quality scatter view</div>
    """, unsafe_allow_html=True)

    if not suppliers.empty:
        fig3 = px.scatter(
            suppliers,
            x="Fulfillment",
            y="Rating",
            size="Inventory",
            color="ReliabilityScore",
            hover_name="Supplier",
            color_continuous_scale=["#DBEAFE","#2563EB","#4C1D95"],
            labels={"Fulfillment": "Fulfillment Rate (%)", "Rating": "Supplier Rating"},
            size_max=30,
        )
        fig3.update_layout(
            height=300,
            margin=dict(l=0, r=10, t=10, b=10),
            paper_bgcolor='white',
            plot_bgcolor='#F8FAFF',
            font=dict(family='Inter', size=12, color='#475569'),
            coloraxis_showscale=False,
        )
        fig3.update_xaxes(showgrid=True, gridcolor='#E2E8F0', zeroline=False)
        fig3.update_yaxes(showgrid=True, gridcolor='#E2E8F0', zeroline=False)
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:32px 0 16px; color:#94A3B8; font-size:13px;">
    🏪 <b>VendorVault AI</b> · Built for kirana stores & small retailers
    · Powered by AI procurement intelligence
</div>
""", unsafe_allow_html=True)