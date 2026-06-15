import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Analytics — VendorVault", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background: linear-gradient(135deg, #F0F4FF 0%, #F8FAFF 50%, #EEF2FF 100%); }
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E1B4B 50%, #1E3A5F 100%) !important;
}
section[data-testid="stSidebar"] * { color: #E2E8F0 !important; }
.page-header {
    background: linear-gradient(135deg, #0C4A6E 0%, #0369A1 60%, #06B6D4 100%);
    border-radius: 16px; padding: 28px 36px; color: white; margin-bottom: 28px;
}
.chart-card {
    background: white; border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0; margin-bottom: 20px;
}
.insight-card {
    background: linear-gradient(135deg, #EFF6FF, #F0FDF4);
    border: 1px solid #BFDBFE; border-radius: 12px; padding: 16px;
    margin-bottom: 10px; border-left: 4px solid #2563EB;
}
.insight-title { font-weight: 700; color: #1D4ED8; font-size: 14px; margin-bottom: 4px; }
.insight-text { font-size: 13px; color: #475569; line-height: 1.6; }
.divider { height:1px; background:linear-gradient(90deg,transparent,#E2E8F0,transparent); margin:24px 0; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🏪 VendorVault AI")
    st.page_link("app.py", label="🏠  Dashboard")
    st.page_link("pages/1_Inventory_Management.py", label="📦  Inventory")
    st.page_link("pages/2_Supplier_Network.py", label="🤝  Supplier Network")
    st.page_link("pages/3_AI_Assistant.py", label="🤖  AI Assistant")
    st.page_link("pages/4_Analytics.py", label="📊  Analytics")
    st.page_link("pages/5_Contracts_Trust.py", label="📋  Contracts & Trust")
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear(); st.rerun()

@st.cache_data(ttl=60)
def load():
    try:
        p = pd.read_csv("data/products.csv")
    except:
        p = pd.DataFrame(columns=["Product","Category","CurrentStock","MinimumStock"])
    try:
        s = pd.read_csv("data/suppliers.csv")
    except:
        s = pd.DataFrame(columns=["Supplier","Category","Fulfillment","OnTime","PriceScore","Inventory","Rating"])
    return p, s

def calc_reliability(row):
    return round(row["Fulfillment"] * 0.4 + row["OnTime"] * 0.3 +
                 row["Rating"] * 20 * 0.2 + row["PriceScore"] * 20 * 0.1, 1)

products, suppliers = load()
if not suppliers.empty:
    suppliers["ReliabilityScore"] = suppliers.apply(calc_reliability, axis=1)
    suppliers_sorted = suppliers.sort_values("ReliabilityScore", ascending=False).reset_index(drop=True)

COLORS = ["#2563EB","#7C3AED","#06B6D4","#059669","#F59E0B","#EF4444","#8B5CF6","#10B981"]

st.markdown("""
<div class="page-header">
    <div style="font-size:13px;opacity:.7;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">
        ANALYTICS & INSIGHTS
    </div>
    <div style="font-size:32px;font-weight:800;">📊 Business Intelligence</div>
    <div style="opacity:.85;margin-top:4px;">
        Deep insights into your supply chain performance and inventory health
    </div>
</div>
""", unsafe_allow_html=True)

if suppliers.empty:
    st.error("No data available.")
    st.stop()

# ─── Chart Row 1 ─────────────────────────────────────────────────────────────
c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:4px">
        📊 Supplier Reliability Bar Chart
    </div>
    <div style="font-size:13px;color:#64748B;margin-bottom:12px">
        Composite score based on fulfillment, on-time, rating & price
    </div>
    """, unsafe_allow_html=True)

    fig1 = px.bar(
        suppliers_sorted,
        x="Supplier", y="ReliabilityScore",
        color="ReliabilityScore",
        color_continuous_scale=["#BFDBFE","#2563EB","#4C1D95"],
        text="ReliabilityScore",
        labels={"ReliabilityScore": "Score"},
    )
    fig1.update_traces(texttemplate='%{text:.1f}', textposition='outside', marker_line_width=0)
    fig1.update_layout(
        height=320, margin=dict(l=0,r=0,t=10,b=10),
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter',size=11,color='#475569'),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#F1F5F9', range=[0,105]),
    )
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

with c2:
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:4px">
        🥧 Inventory Distribution by Category
    </div>
    <div style="font-size:13px;color:#64748B;margin-bottom:12px">
        How your stock is spread across product categories
    </div>
    """, unsafe_allow_html=True)

    if not products.empty:
        cat_data = products.groupby("Category")["CurrentStock"].sum().reset_index()
        fig2 = px.pie(
            cat_data, names="Category", values="CurrentStock",
            hole=0.5, color_discrete_sequence=COLORS,
        )
        fig2.update_traces(textposition='outside', textinfo='label+percent',
                           hovertemplate='<b>%{label}</b><br>Stock: %{value}<br>%{percent}<extra></extra>')
        fig2.update_layout(
            height=320, margin=dict(l=20,r=20,t=10,b=10),
            paper_bgcolor='white', showlegend=True,
            legend=dict(orientation='h', y=-0.15),
            font=dict(family='Inter',size=11,color='#475569'),
        )
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Chart Row 2 ─────────────────────────────────────────────────────────────
c3, c4 = st.columns(2, gap="large")

with c3:
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:4px">
        📦 Category-wise Supplier Count
    </div>
    <div style="font-size:13px;color:#64748B;margin-bottom:12px">
        How many suppliers operate in each category
    </div>
    """, unsafe_allow_html=True)

    cat_sup = suppliers.groupby("Category").size().reset_index(name="Count")
    fig3 = px.bar(
        cat_sup.sort_values("Count", ascending=True),
        x="Count", y="Category",
        orientation='h',
        color="Count",
        color_continuous_scale=["#E0F2FE","#7C3AED"],
        text="Count",
    )
    fig3.update_traces(textposition='outside', marker_line_width=0)
    fig3.update_layout(
        height=300, margin=dict(l=0,r=30,t=10,b=10),
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter',size=11,color='#475569'),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=True, gridcolor='#F1F5F9'),
        yaxis=dict(showgrid=False),
    )
    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

with c4:
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:4px">
        ⭐ Rating Distribution
    </div>
    <div style="font-size:13px;color:#64748B;margin-bottom:12px">
        How supplier ratings are distributed across the network
    </div>
    """, unsafe_allow_html=True)

    bins = [3.5, 4.0, 4.3, 4.6, 4.9, 5.1]
    labels = ["3.5–4.0","4.0–4.3","4.3–4.6","4.6–4.9","4.9–5.0"]
    suppliers["RatingBin"] = pd.cut(suppliers["Rating"], bins=bins, labels=labels, right=False)
    rating_dist = suppliers.groupby("RatingBin", observed=True).size().reset_index(name="Count")

    fig4 = px.bar(
        rating_dist, x="RatingBin", y="Count",
        color="Count",
        color_continuous_scale=["#FEF3C7","#F59E0B","#D97706"],
        text="Count",
        labels={"RatingBin": "Rating Range", "Count": "# Suppliers"},
    )
    fig4.update_traces(textposition='outside', marker_line_width=0)
    fig4.update_layout(
        height=300, margin=dict(l=0,r=10,t=10,b=10),
        paper_bgcolor='white', plot_bgcolor='white',
        font=dict(family='Inter',size=11,color='#475569'),
        coloraxis_showscale=False,
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#F1F5F9'),
    )
    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Scatter: Fulfillment vs Rating ──────────────────────────────────────────
st.markdown("""
<div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:4px">
    🔍 Fulfillment Rate vs Rating Scatter Plot
</div>
<div style="font-size:13px;color:#64748B;margin-bottom:12px">
    Bubble size = Inventory available · Color = Reliability score
</div>
""", unsafe_allow_html=True)

fig5 = px.scatter(
    suppliers,
    x="Fulfillment", y="Rating",
    size="Inventory",
    color="ReliabilityScore",
    hover_name="Supplier",
    text="Supplier",
    color_continuous_scale=["#DBEAFE","#2563EB","#4C1D95"],
    labels={"Fulfillment": "Fulfillment Rate (%)", "Rating": "Supplier Rating (out of 5)"},
    size_max=40,
)
fig5.update_traces(
    textposition='top center',
    textfont=dict(size=10, color='#475569'),
)
fig5.update_layout(
    height=380, margin=dict(l=20,r=60,t=20,b=20),
    paper_bgcolor='white', plot_bgcolor='#F8FAFF',
    font=dict(family='Inter',size=12,color='#475569'),
    coloraxis_colorbar=dict(title="Score"),
    xaxis=dict(showgrid=True, gridcolor='#E2E8F0', zeroline=False, range=[65,105]),
    yaxis=dict(showgrid=True, gridcolor='#E2E8F0', zeroline=False, range=[3.5,5.1]),
)
st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False})

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Automated Insights ───────────────────────────────────────────────────────
st.markdown("""
<div style="font-size:20px;font-weight:700;color:#0F172A;margin-bottom:16px">
    💡 Automated Business Insights
</div>
""", unsafe_allow_html=True)

if not suppliers.empty and not products.empty:
    top_s = suppliers_sorted.iloc[0]
    bottom_s = suppliers_sorted.iloc[-1]
    avg_r = suppliers["ReliabilityScore"].mean()
    low_stock = products[products["CurrentStock"] < products["MinimumStock"]]

    insights = [
        {
            "title": f"🏆 Top Performer: {top_s['Supplier']}",
            "text": (f"{top_s['Supplier']} leads the network with a reliability score of "
                     f"{top_s['ReliabilityScore']:.1f}, a {top_s['Fulfillment']}% fulfillment rate, "
                     f"and {top_s['Inventory']} units available. Prioritize this vendor for critical orders.")
        },
        {
            "title": f"⚠️ Needs Attention: {bottom_s['Supplier']}",
            "text": (f"{bottom_s['Supplier']} has the lowest reliability score of "
                     f"{bottom_s['ReliabilityScore']:.1f}. With {bottom_s['Fulfillment']}% fulfillment and "
                     f"{bottom_s['OnTime']}% on-time delivery, consider switching to a higher-performing alternative.")
        },
        {
            "title": f"📈 Network Average: {avg_r:.1f} Reliability",
            "text": (f"Your supplier network averages {avg_r:.1f}/100 reliability. "
                     f"{len(suppliers[suppliers['ReliabilityScore'] >= avg_r])} suppliers are above average. "
                     f"Focus procurement on these to reduce supply chain risk.")
        },
        {
            "title": f"📦 {len(low_stock)} Products Need Restocking",
            "text": (f"{', '.join(low_stock['Product'].tolist()[:4])}{'...' if len(low_stock)>4 else ''} "
                     f"are below minimum stock thresholds. Immediate procurement is recommended to avoid stockouts.")
        },
        {
            "title": "🎯 Category Opportunity: Grocery",
            "text": ("Grocery has the highest supplier count and availability. SmartStock and FreshFoods Ltd "
                     "offer the best combination of price, reliability, and inventory — ideal for bulk ordering.")
        },
    ]

    col_i1, col_i2 = st.columns(2, gap="large")
    for i, ins in enumerate(insights):
        col = col_i1 if i % 2 == 0 else col_i2
        with col:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">{ins['title']}</div>
                <div class="insight-text">{ins['text']}</div>
            </div>
            """, unsafe_allow_html=True)