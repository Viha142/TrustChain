import streamlit as st
import pandas as pd
import plotly.express as px
from textwrap import dedent

st.set_page_config(page_title="Suppliers — VendorVault", page_icon="🤝", layout="wide")

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
    background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 60%, #A855F7 100%);
    border-radius: 16px; padding: 28px 36px; color: white; margin-bottom: 28px;
}
.sup-card {
    background: white; border-radius: 14px; padding: 20px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0; margin-bottom: 14px;
    transition: all 0.2s;
    border-left: 5px solid #7C3AED;
}
.sup-card:hover {
    box-shadow: 0 6px 28px rgba(124,58,237,0.15);
    transform: translateY(-2px);
}
.sup-card.top { border-left-color: #2563EB; }
.sup-name { font-size: 17px; font-weight: 800; color: #1E293B; margin-bottom: 4px; }
.sup-cat { font-size: 12px; color: #7C3AED; font-weight: 600; text-transform: uppercase;
    letter-spacing: .06em; }
.stat-row { display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; }
.stat-chip {
    background: #F1F5F9; border-radius: 8px; padding: 6px 12px;
    font-size: 12px; color: #475569; font-weight: 600;
}
.badge { display:inline-block; padding:4px 12px; border-radius:20px;
    font-size:11px; font-weight:700; }
.badge-top { background:#DBEAFE; color:#1D4ED8; }
.badge-good { background:#D1FAE5; color:#065F46; }
.badge-avg { background:#FEF3C7; color:#92400E; }
.score-big { font-size: 28px; font-weight: 800; color: #2563EB; }
.divider { height:1px; background:linear-gradient(90deg,transparent,#E2E8F0,transparent); margin:24px 0; }
.rank-table-header {
    display:grid; grid-template-columns: 40px 1fr 80px 80px 80px 80px 80px;
    gap:8px; padding:10px 16px;
    background: linear-gradient(135deg, #EFF6FF, #F5F3FF);
    border-radius:10px 10px 0 0;
    font-size:11px; font-weight:700; color:#475569; text-transform:uppercase;
    letter-spacing:.06em;
}
.rank-table-row {
    display:grid; grid-template-columns: 40px 1fr 80px 80px 80px 80px 80px;
    gap:8px; padding:12px 16px;
    border-bottom: 1px solid #F1F5F9; font-size:13px; color:#334155;
    background: white;
}
.rank-table-row:last-child { border-radius: 0 0 10px 10px; border-bottom:none; }
.rank-table-row:hover { background:#F8FAFF; }
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
        return pd.read_csv("data/suppliers.csv")
    except:
        return pd.DataFrame(columns=["Supplier","Category","Fulfillment","OnTime","PriceScore","Inventory","Rating"])

def calc_reliability(row):
    return round(row["Fulfillment"] * 0.4 + row["OnTime"] * 0.3 +
                 row["Rating"] * 20 * 0.2 + row["PriceScore"] * 20 * 0.1, 1)

suppliers = load()
if not suppliers.empty:
    suppliers["ReliabilityScore"] = suppliers.apply(calc_reliability, axis=1)
    suppliers_sorted = suppliers.sort_values("ReliabilityScore", ascending=False).reset_index(drop=True)

st.markdown("""
<div class="page-header">
    <div style="font-size:13px;opacity:.7;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">
        SUPPLIER NETWORK
    </div>
    <div style="font-size:32px;font-weight:800;">🤝 Vendor Discovery</div>
    <div style="opacity:.85;margin-top:4px;">
        Search, filter and rank all verified suppliers in your procurement network
    </div>
</div>
""", unsafe_allow_html=True)

if suppliers.empty:
    st.error("No supplier data found.")
    st.stop()

# ─── Search + Filter ──────────────────────────────────────────────────────────
col_s, col_f, col_sort = st.columns([2, 1.5, 1.5])
with col_s:
    search = st.text_input("🔍 Search suppliers", placeholder="e.g. FreshFoods, Dairy...")
with col_f:
    cats = ["All"] + sorted(suppliers["Category"].unique().tolist())
    cat_filter = st.selectbox("📂 Category", cats)
with col_sort:
    sort_by = st.selectbox("↕️ Sort by", ["Reliability Score", "Rating", "Fulfillment", "Inventory"])

# Apply filters
filtered = suppliers.copy()
if search:
    filtered = filtered[filtered["Supplier"].str.contains(search, case=False, na=False)]
if cat_filter != "All":
    filtered = filtered[filtered["Category"] == cat_filter]

sort_map = {
    "Reliability Score": "ReliabilityScore",
    "Rating": "Rating",
    "Fulfillment": "Fulfillment",
    "Inventory": "Inventory",
}
filtered = filtered.sort_values(sort_map[sort_by], ascending=False).reset_index(drop=True)

st.markdown(f"**Showing {len(filtered)} supplier(s)**")
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Supplier Cards ───────────────────────────────────────────────────────────
col_cards, col_ranking = st.columns([2, 1], gap="large")

with col_cards:
    st.markdown("#### 🗂️ Supplier Cards")
    for rank_idx, (_, row) in enumerate(filtered.iterrows()):
        is_top = rank_idx == 0 and cat_filter == "All" and not search
        score = row["ReliabilityScore"]
        badge_class = "badge-top" if score >= 90 else ("badge-good" if score >= 80 else "badge-avg")
        badge_label = "⭐ Top Vendor" if score >= 90 else ("✅ Reliable" if score >= 80 else "📋 Average")
        bar_w = min(100, int(score))

        with st.expander(f"{'🏆 ' if is_top else ''}{row['Supplier']} — Score: {score:.1f}", expanded=rank_idx==0):
            st.markdown(dedent(f"""
<div>
                <div style="display:flex;justify-content:space-between;align-items:start;margin-bottom:12px">
                    <div>
                        <div class="sup-name">{row['Supplier']}</div>
                        <div class="sup-cat">📂 {row['Category']}</div>
                    </div>
                    <div style="text-align:right">
                        <div class="score-big">{score:.1f}</div>
                        <div style="font-size:11px;color:#94A3B8">Reliability</div>
                        <span class="badge {badge_class}" style="margin-top:4px;display:inline-block">{badge_label}</span>
                    </div>
                </div>

                <div style="margin-bottom:12px">
                    <div style="display:flex;justify-content:space-between;
                         font-size:12px;color:#64748B;margin-bottom:4px">
                        <span>Reliability Score</span><span>{score:.1f}/100</span>
                    </div>
                    <div style="background:#E2E8F0;border-radius:4px;height:8px;">
                        <div style="width:{bar_w}%;height:100%;
                             background:linear-gradient(90deg,#7C3AED,#2563EB);border-radius:4px;"></div>
                    </div>
                </div>

                <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin-top:10px">
                    <div style="background:#F8FAFF;border-radius:10px;padding:12px;text-align:center">
                        <div style="font-size:20px;font-weight:800;color:#2563EB">{row['Fulfillment']}%</div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px">Fulfillment</div>
                    </div>
                    <div style="background:#F8FAFF;border-radius:10px;padding:12px;text-align:center">
                        <div style="font-size:20px;font-weight:800;color:#7C3AED">{row['OnTime']}%</div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px">On-Time</div>
                    </div>
                    <div style="background:#F8FAFF;border-radius:10px;padding:12px;text-align:center">
                        <div style="font-size:20px;font-weight:800;color:#06B6D4">⭐{row['Rating']}</div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px">Rating</div>
                    </div>
                    <div style="background:#F8FAFF;border-radius:10px;padding:12px;text-align:center">
                        <div style="font-size:20px;font-weight:800;color:#059669">{row['Inventory']}</div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px">Units Avail.</div>
                    </div>
                    <div style="background:#F8FAFF;border-radius:10px;padding:12px;text-align:center">
                        <div style="font-size:20px;font-weight:800;color:#D97706">{row['PriceScore']}</div>
                        <div style="font-size:11px;color:#94A3B8;margin-top:2px">Price Score</div>
                    </div>
                </div>
            </div>
"""), unsafe_allow_html=True)

with col_ranking:
    st.markdown("#### 🏆 Master Ranking")
    for i, (_, row) in enumerate(suppliers_sorted.head(10).iterrows()):
        medal = ["🥇","🥈","🥉"][i] if i < 3 else f"#{i+1}"
        bar = min(100, int(row["ReliabilityScore"]))
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:12px 14px;
             margin-bottom:8px;box-shadow:0 1px 8px rgba(0,0,0,0.05);
             border:1px solid #E2E8F0;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <div>
                    <span style="font-size:14px">{medal}</span>
                    <span style="font-weight:700;font-size:13px;color:#0F172A;margin-left:4px">
                        {row['Supplier']}
                    </span>
                </div>
                <span style="font-weight:800;font-size:14px;color:#2563EB">{row['ReliabilityScore']:.1f}</span>
            </div>
            <div style="background:#E2E8F0;border-radius:3px;height:5px;">
                <div style="width:{bar}%;height:100%;
                     background:{'linear-gradient(90deg,#F59E0B,#EF4444)' if i==0 else 'linear-gradient(90deg,#2563EB,#7C3AED)'};
                     border-radius:3px;"></div>
            </div>
            <div style="font-size:11px;color:#94A3B8;margin-top:4px">
                {row['Category']} · ⭐{row['Rating']}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    csv = suppliers_sorted.to_csv(index=False)
    st.download_button("⬇️ Export Supplier Data", csv, "suppliers.csv", "text/csv",
                       use_container_width=True)