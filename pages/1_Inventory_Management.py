import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Inventory — VendorVault", page_icon="📦", layout="wide")

# ─── Shared CSS ────────────────────────────────────────────────────────────────
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
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 60%, #06B6D4 100%);
    border-radius: 16px; padding: 28px 36px; color: white; margin-bottom: 28px;
}
.card {
    background: white; border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06); border: 1px solid #E2E8F0;
    margin-bottom: 16px;
}
.stock-good { color: #059669; font-weight: 700; }
.stock-low { color: #D97706; font-weight: 700; }
.stock-critical { color: #DC2626; font-weight: 700; }
.badge { display:inline-block; padding:3px 10px; border-radius:20px;
    font-size:11px; font-weight:700; text-transform:uppercase; }
.badge-green { background:#D1FAE5; color:#065F46; }
.badge-yellow { background:#FEF3C7; color:#92400E; }
.badge-red { background:#FEE2E2; color:#991B1B; }
.rec-box {
    background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
    border: 2px solid #BFDBFE; border-radius: 14px; padding: 20px;
}
.divider { height:1px; background:linear-gradient(90deg,transparent,#E2E8F0,transparent); margin:24px 0; }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar nav ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏪 VendorVault AI")
    st.page_link("app.py", label="🏠  Dashboard")
    st.page_link("pages/1_Inventory_Management.py", label="📦  Inventory")
    st.page_link("pages/2_Supplier_Network.py", label="🤝  Supplier Network")
    st.page_link("pages/3_AI_Assistant.py", label="🤖  AI Assistant")
    st.page_link("pages/4_Analytics.py", label="📊  Analytics")
    st.page_link("pages/5_Contracts_Trust.py", label="📋  Contracts & Trust")
    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ─── Data ─────────────────────────────────────────────────────────────────────
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
    return (row["Fulfillment"] * 0.4 + row["OnTime"] * 0.3 +
            row["Rating"] * 20 * 0.2 + row["PriceScore"] * 20 * 0.1)

products, suppliers = load()

if not products.empty:
    products["StockPct"] = (products["CurrentStock"] / products["MinimumStock"] * 100).round(1)
    products["Status"] = products["StockPct"].apply(
        lambda x: "Critical" if x < 50 else ("Low" if x < 100 else "OK"))

if not suppliers.empty:
    suppliers["ReliabilityScore"] = suppliers.apply(calc_reliability, axis=1).round(1)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div style="font-size:13px;opacity:.7;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">
        INVENTORY MANAGEMENT
    </div>
    <div style="font-size:32px;font-weight:800;">📦 Stock Monitor</div>
    <div style="opacity:.85;margin-top:4px;">
        Track product levels, spot shortages, and find the right supplier instantly
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Row ──────────────────────────────────────────────────────────────────
if not products.empty:
    total = len(products)
    ok = len(products[products["Status"] == "OK"])
    low = len(products[products["Status"] == "Low"])
    critical = len(products[products["Status"] == "Critical"])
    health = int(ok / total * 100) if total else 0

    c1, c2, c3, c4 = st.columns(4)
    for col, label, val, icon, color in [
        (c1, "Total Products", total, "📦", "#2563EB"),
        (c2, "In Stock (OK)", ok, "✅", "#059669"),
        (c3, "Low Stock", low, "🟡", "#D97706"),
        (c4, "Critical", critical, "🔴", "#DC2626"),
    ]:
        with col:
            st.markdown(f"""
            <div class="card" style="border-top:4px solid {color};text-align:center;">
                <div style="font-size:28px;margin-bottom:6px">{icon}</div>
                <div style="font-size:11px;color:#94A3B8;text-transform:uppercase;
                     letter-spacing:.08em;margin-bottom:4px">{label}</div>
                <div style="font-size:34px;font-weight:800;color:{color}">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── Gauge ─────────────────────────────────────────────────────────────────
    col_gauge, col_table = st.columns([1, 2], gap="large")

    with col_gauge:
        st.markdown("**📈 Overall Stock Health**")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=health,
            title={'text': "Stock Health %", 'font': {'size': 14, 'color': '#475569', 'family': 'Inter'}},
            delta={'reference': 80, 'increasing': {'color': '#059669'}, 'decreasing': {'color': '#DC2626'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#94A3B8'},
                'bar': {'color': "#2563EB", 'thickness': 0.25},
                'bgcolor': "white",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': '#FEE2E2'},
                    {'range': [40, 70], 'color': '#FEF3C7'},
                    {'range': [70, 100], 'color': '#D1FAE5'},
                ],
                'threshold': {
                    'line': {'color': "#7C3AED", 'width': 3},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig_gauge.update_layout(
            height=280, margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='white', font=dict(family='Inter', color='#475569')
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        status_label = "Excellent" if health >= 80 else ("Fair" if health >= 50 else "Poor")
        status_color = "#059669" if health >= 80 else ("#D97706" if health >= 50 else "#DC2626")
        st.markdown(f"""
        <div style="text-align:center;padding:14px;background:#F8FAFF;border-radius:10px;
             border:1px solid #E2E8F0;">
            <div style="color:{status_color};font-weight:700;font-size:18px">{status_label}</div>
            <div style="color:#64748B;font-size:13px;margin-top:4px">
                {ok} of {total} products at healthy stock levels
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_table:
        st.markdown("**📋 Full Inventory Table**")

        # Filter
        cat_filter = st.selectbox("Filter by Category",
            ["All"] + list(products["Category"].unique()), key="inv_cat")
        status_filter = st.selectbox("Filter by Status",
            ["All", "OK", "Low", "Critical"], key="inv_status")

        df_view = products.copy()
        if cat_filter != "All":
            df_view = df_view[df_view["Category"] == cat_filter]
        if status_filter != "All":
            df_view = df_view[df_view["Status"] == status_filter]

        def highlight_status(val):
            if val == "Critical":
                return "background-color:#FEE2E2;color:#991B1B;font-weight:700"
            elif val == "Low":
                return "background-color:#FEF3C7;color:#92400E;font-weight:700"
            return "background-color:#D1FAE5;color:#065F46;font-weight:700"

        styled = df_view.style.map(highlight_status, subset=["Status"])
        st.dataframe(styled, use_container_width=True, hide_index=True, height=260)

        # CSV download
        csv = df_view.to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv, "inventory.csv", "text/csv")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── Find Suppliers ────────────────────────────────────────────────────────
    st.markdown("### 🔍 Find Suppliers for Low-Stock Products")

    low_products = products[products["Status"] != "OK"]

    if len(low_products) == 0:
        st.success("✅ All products are well-stocked. No supplier search needed!")
    else:
        selected_product = st.selectbox(
            "Select a low-stock product to find suppliers:",
            low_products["Product"].tolist(),
            key="find_sup"
        )

        if st.button("🔍 Find Best Suppliers", type="primary", use_container_width=False):
            prod_row = products[products["Product"] == selected_product].iloc[0]
            prod_cat = prod_row["Category"]

            matching = suppliers[suppliers["Category"] == prod_cat].copy()

            if matching.empty:
                st.warning(f"No suppliers found for category: {prod_cat}")
            else:
                matching = matching.sort_values(
                    ["ReliabilityScore", "Rating", "Inventory"],
                    ascending=[False, False, False]
                ).reset_index(drop=True)

                best = matching.iloc[0]
                st.markdown(f"""
                <div class="rec-box">
                    <div style="font-size:13px;color:#7C3AED;font-weight:700;
                         text-transform:uppercase;letter-spacing:.08em;margin-bottom:10px">
                        🏆 Top Recommendation
                    </div>
                    <div style="font-size:22px;font-weight:800;color:#1D4ED8;margin-bottom:8px">
                        {best['Supplier']}
                    </div>
                    <div style="font-size:14px;color:#475569;line-height:1.7">
                        ✅ <b>Reason:</b> Highest reliability score of <b>{best['ReliabilityScore']:.1f}</b>,
                        with a <b>{best['Fulfillment']}%</b> fulfillment rate,
                        <b>{best['Inventory']}</b> units available, and a customer rating of
                        <b>⭐ {best['Rating']}</b>.<br>
                        Recommended for restocking <b>{selected_product}</b>
                        (current: {int(prod_row['CurrentStock'])} / min: {int(prod_row['MinimumStock'])} units).
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.markdown("**All matching suppliers (ranked):**")
                for rank, (_, row) in enumerate(matching.iterrows()):
                    medal = ["🥇","🥈","🥉"][rank] if rank < 3 else f"#{rank+1}"
                    st.markdown(f"""
                    <div class="card" style="display:flex;align-items:center;gap:16px;padding:16px 20px;">
                        <div style="font-size:22px">{medal}</div>
                        <div style="flex:1">
                            <div style="font-weight:700;color:#0F172A">{row['Supplier']}</div>
                            <div style="font-size:12px;color:#64748B;margin-top:2px">
                                Fulfillment: {row['Fulfillment']}% &nbsp;|&nbsp;
                                On-time: {row['OnTime']}% &nbsp;|&nbsp;
                                Rating: ⭐{row['Rating']} &nbsp;|&nbsp;
                                Stock: {row['Inventory']} units
                            </div>
                        </div>
                        <div style="font-size:22px;font-weight:800;color:#2563EB">
                            {row['ReliabilityScore']:.0f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

else:
    st.error("⚠️ No product data found. Make sure `data/products.csv` exists.")