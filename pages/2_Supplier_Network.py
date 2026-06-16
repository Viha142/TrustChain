
import streamlit as st
import pandas as pd
import plotly.express as px
from textwrap import dedent

st.set_page_config(page_title="Suppliers — VendorVault", page_icon="🤝", layout="wide")

st.markdown(
    dedent(f"""
    <div>

        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px">

            <div>
                <div class="sup-name">{row['Supplier']}</div>
                <div class="sup-cat">📂 {row['Category']}</div>
            </div>

            <div style="text-align:right">
                <div class="score-big">{score:.1f}</div>
                <div style="font-size:11px;color:#94A3B8">
                    Reliability
                </div>

                <span class="badge {badge_class}"
                      style="margin-top:4px;display:inline-block">
                    {badge_label}
                </span>
            </div>

        </div>

        <div style="margin-bottom:12px">

            <div style="
                display:flex;
                justify-content:space-between;
                font-size:12px;
                color:#64748B;
                margin-bottom:4px;
            ">
                <span>Reliability Score</span>
                <span>{score:.1f}/100</span>
            </div>

            <div style="
                background:#E2E8F0;
                border-radius:4px;
                height:8px;
            ">

                <div style="
                    width:{score}%;
                    height:100%;
                    background:linear-gradient(90deg,#7C3AED,#2563EB);
                    border-radius:4px;
                ">
                </div>

            </div>

        </div>

    </div>
    """),
    unsafe_allow_html=True
)

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
                <span class="badge {badge_class}" style="margin-top:4px;display:inline-block">
                    {badge_label}
                </span>
            </div>
        </div>

        <div style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748B;margin-bottom:4px">
                <span>Reliability Score</span>
                <span>{score:.1f}/100</span>
            </div>

            <div style="background:#E2E8F0;border-radius:4px;height:8px;">
                <div style="width:{score}%;height:100%;
                    background:linear-gradient(90deg,#7C3AED,#2563EB);
                    border-radius:4px;">
                </div>
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