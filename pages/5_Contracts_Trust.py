import streamlit as st
import pandas as pd
from datetime import datetime
import random
import string

st.set_page_config(page_title="Contracts & Trust — VendorVault", page_icon="📋", layout="wide")

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
    background: linear-gradient(135deg, #7C2D12 0%, #EA580C 60%, #F59E0B 100%);
    border-radius: 16px; padding: 28px 36px; color: white; margin-bottom: 28px;
}
.form-card {
    background: white; border-radius: 14px; padding: 28px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    border: 1px solid #E2E8F0; margin-bottom: 20px;
}
.leader-row {
    display: flex; align-items: center; padding: 14px 16px;
    background: white; border-radius: 10px; margin-bottom: 8px;
    box-shadow: 0 1px 8px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;
    transition: all 0.2s;
}
.leader-row:hover {
    box-shadow: 0 4px 16px rgba(37,99,235,0.1);
    transform: translateX(2px);
}
.contract-box {
    background: linear-gradient(135deg, #F0FDF4, #ECFDF5);
    border: 2px solid #A7F3D0; border-radius: 14px; padding: 24px;
    margin-top: 16px; font-family: 'Courier New', monospace;
}
.contract-line { margin-bottom: 8px; font-size: 13px; color: #065F46; }
.star-display { color: #F59E0B; font-size: 20px; }
.divider { height:1px; background:linear-gradient(90deg,transparent,#E2E8F0,transparent); margin:24px 0; }
.badge { display:inline-block; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700; }
.badge-gold { background:#FEF3C7; color:#92400E; }
.badge-silver { background:#F1F5F9; color:#475569; }
.badge-bronze { background:#FEF9EE; color:#92400E; }
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

@st.cache_data(ttl=30)
def load():
    try:
        s = pd.read_csv("data/suppliers.csv")
    except:
        s = pd.DataFrame(columns=["Supplier","Category","Fulfillment","OnTime","PriceScore","Inventory","Rating"])
    try:
        r = pd.read_csv("data/ratings.csv")
    except:
        r = pd.DataFrame(columns=["Supplier","Stars","Comment"])
    return s, r

def calc_reliability(row):
    return round(row["Fulfillment"] * 0.4 + row["OnTime"] * 0.3 +
                 row["Rating"] * 20 * 0.2 + row["PriceScore"] * 20 * 0.1, 1)

suppliers, ratings = load()
if not suppliers.empty:
    suppliers["ReliabilityScore"] = suppliers.apply(calc_reliability, axis=1)

st.markdown("""
<div class="page-header">
    <div style="font-size:13px;opacity:.7;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">
        CONTRACTS & TRUST
    </div>
    <div style="font-size:32px;font-weight:800;">📋 Vendor Trust Center</div>
    <div style="opacity:.85;margin-top:4px;">
        Rate deliveries, build trust scores, and manage supplier contracts
    </div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

# ─── Left: Rating Form ─────────────────────────────────────────────────────────
with col_left:
    st.markdown("""
    <div style="font-size:18px;font-weight:700;color:#0F172A;margin-bottom:16px">
        ⭐ Rate a Delivery
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        if suppliers.empty:
            st.error("No supplier data found.")
        else:
            supplier_names = suppliers["Supplier"].tolist()

            with st.form("rating_form", clear_on_submit=True):
                selected_supplier = st.selectbox("🏭 Select Supplier", supplier_names)
                stars = st.slider("⭐ Rating (1–5 stars)", 1, 5, 4,
                                  help="1 = Poor, 5 = Excellent")

                # Visual star display
                star_str = "⭐" * stars + "☆" * (5 - stars)
                st.markdown(f"<div class='star-display'>{star_str}</div>", unsafe_allow_html=True)

                comment = st.text_area("💬 Your Comment",
                    placeholder="Share your experience with this supplier...",
                    height=100)

                submitted = st.form_submit_button("✅ Submit Rating", type="primary",
                                                   use_container_width=True)

                if submitted:
                    if not comment.strip():
                        st.warning("Please add a comment before submitting.")
                    else:
                        # Save to ratings.csv
                        new_rating = pd.DataFrame([{
                            "Supplier": selected_supplier,
                            "Stars": stars,
                            "Comment": comment.strip()
                        }])
                        try:
                            existing = pd.read_csv("data/ratings.csv")
                            updated = pd.concat([existing, new_rating], ignore_index=True)
                        except:
                            updated = new_rating

                        updated.to_csv("data/ratings.csv", index=False)
                        st.cache_data.clear()

                        # Recalculate average and update suppliers.csv
                        try:
                            avg = updated[updated["Supplier"] == selected_supplier]["Stars"].mean()
                            sup_df = pd.read_csv("data/suppliers.csv")
                            sup_df.loc[sup_df["Supplier"] == selected_supplier, "Rating"] = round(avg / 5 * 5, 2)
                            sup_df.to_csv("data/suppliers.csv", index=False)
                        except:
                            pass

                        st.success(f"✅ Rating submitted for **{selected_supplier}**! {'⭐' * stars}")
                        st.balloons()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── Recent Reviews ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:16px;font-weight:700;color:#0F172A;margin-bottom:12px">
        💬 Recent Reviews
    </div>
    """, unsafe_allow_html=True)

    if ratings.empty:
        st.info("No reviews yet. Be the first to rate a supplier!")
    else:
        for _, review in ratings.tail(5).iloc[::-1].iterrows():
            star_count = int(review.get("Stars", 0))
            stars_display = "⭐" * star_count + "☆" * max(0, 5 - star_count)
            st.markdown(f"""
            <div style="background:white;border-radius:10px;padding:14px 16px;
                 margin-bottom:8px;box-shadow:0 1px 8px rgba(0,0,0,0.05);
                 border:1px solid #E2E8F0;border-left:3px solid #F59E0B;">
                <div style="display:flex;justify-content:space-between;margin-bottom:6px">
                    <span style="font-weight:700;color:#0F172A">{review['Supplier']}</span>
                    <span style="font-size:14px">{stars_display}</span>
                </div>
                <div style="font-size:13px;color:#475569;font-style:italic">
                    "{review['Comment']}"
                </div>
            </div>
            """, unsafe_allow_html=True)

# ─── Right: Leaderboard + Contracts ───────────────────────────────────────────
with col_right:
    st.markdown("""
    <div style="font-size:18px;font-weight:700;color:#0F172A;margin-bottom:16px">
        🏆 Most Trusted Suppliers
    </div>
    """, unsafe_allow_html=True)

    if not suppliers.empty:
        leaderboard = suppliers.sort_values("Rating", ascending=False).reset_index(drop=True)
        medals = ["🥇","🥈","🥉"] + [f"#{i+4}" for i in range(10)]
        badge_classes = ["badge-gold","badge-silver","badge-bronze"] + ["badge-silver"]*10

        for i, (_, row) in enumerate(leaderboard.iterrows()):
            stars_count = round(row["Rating"])
            stars_vis = "⭐" * stars_count + "☆" * max(0, 5 - stars_count)
            trust_width = int(row["Rating"] / 5 * 100)
            st.markdown(f"""
            <div class="leader-row">
                <div style="font-size:20px;width:36px;flex-shrink:0">{medals[i]}</div>
                <div style="flex:1;margin:0 12px">
                    <div style="font-weight:700;color:#0F172A;font-size:14px">{row['Supplier']}</div>
                    <div style="font-size:11px;color:#94A3B8;margin-top:2px">{row['Category']}</div>
                    <div style="background:#E2E8F0;border-radius:3px;height:4px;margin-top:6px;">
                        <div style="width:{trust_width}%;height:100%;
                             background:linear-gradient(90deg,#F59E0B,#EF4444);border-radius:3px;"></div>
                    </div>
                </div>
                <div style="text-align:right;flex-shrink:0">
                    <div style="font-size:16px;font-weight:800;color:#D97706">{row['Rating']:.1f}</div>
                    <div style="font-size:10px;color:#94A3B8">/ 5.0</div>
                    <div style="font-size:12px">{stars_vis[:5]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # ─── Contract Generator ────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:18px;font-weight:700;color:#0F172A;margin-bottom:12px">
        📄 Generate Supplier Contract
    </div>
    """, unsafe_allow_html=True)

    gen_supplier = st.selectbox("Select supplier for contract",
        suppliers["Supplier"].tolist() if not suppliers.empty else ["—"],
        key="contract_sup")

    if st.button("⚡ Generate Contract", type="primary", use_container_width=True):
        if not suppliers.empty:
            sup_row = suppliers[suppliers["Supplier"] == gen_supplier].iloc[0]
            contract_id = "VV-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
            today = datetime.now().strftime("%d %B %Y")
            reliability = sup_row.get("ReliabilityScore", calc_reliability(sup_row))
            valid_until = "31 December 2026"

            st.markdown(f"""
            <div class="contract-box">
                <div style="text-align:center;margin-bottom:16px">
                    <div style="font-size:16px;font-weight:800;color:#065F46;letter-spacing:.1em">
                        ✦ VENDORVAULT SUPPLIER AGREEMENT ✦
                    </div>
                    <div style="font-size:11px;color:#6B7280;margin-top:4px">OFFICIAL PROCUREMENT CONTRACT</div>
                </div>
                <div class="contract-line">CONTRACT ID: <b>{contract_id}</b></div>
                <div class="contract-line">DATE ISSUED: <b>{today}</b></div>
                <div class="contract-line">VALID UNTIL: <b>{valid_until}</b></div>
                <div class="contract-line">STATUS: <b>✅ ACTIVE</b></div>
                <hr style="border-color:#A7F3D0;margin:12px 0">
                <div class="contract-line">VENDOR: <b>{gen_supplier}</b></div>
                <div class="contract-line">CATEGORY: <b>{sup_row['Category']}</b></div>
                <div class="contract-line">RELIABILITY SCORE: <b>{reliability:.1f} / 100</b></div>
                <div class="contract-line">FULFILLMENT COMMITMENT: <b>{sup_row['Fulfillment']}%</b></div>
                <div class="contract-line">ON-TIME DELIVERY SLA: <b>{sup_row['OnTime']}%</b></div>
                <div class="contract-line">CURRENT RATING: <b>⭐ {sup_row['Rating']} / 5.0</b></div>
                <div class="contract-line">INVENTORY COMMITMENT: <b>{sup_row['Inventory']} units/month</b></div>
                <hr style="border-color:#A7F3D0;margin:12px 0">
                <div class="contract-line" style="font-size:11px;color:#6B7280">
                    This contract is auto-generated by VendorVault AI and is subject to
                    manual review and signing before becoming legally binding.
                    Both parties agree to the stated fulfillment and delivery commitments.
                </div>
                <div style="text-align:center;margin-top:14px;font-size:12px;color:#059669;font-weight:700">
                    🔐 Digitally Signed · VendorVault AI Platform
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.success(f"✅ Contract `{contract_id}` generated for **{gen_supplier}**!")

            # Downloadable text version
            contract_text = f"""VENDORVAULT SUPPLIER AGREEMENT
================================
Contract ID: {contract_id}
Date: {today}
Valid Until: {valid_until}
Status: ACTIVE

Vendor: {gen_supplier}
Category: {sup_row['Category']}
Reliability Score: {reliability:.1f}/100
Fulfillment Commitment: {sup_row['Fulfillment']}%
On-Time Delivery SLA: {sup_row['OnTime']}%
Rating: {sup_row['Rating']}/5.0
Inventory Commitment: {sup_row['Inventory']} units/month

Auto-generated by VendorVault AI.
"""
            st.download_button(
                "⬇️ Download Contract (.txt)",
                contract_text,
                f"contract_{contract_id}.txt",
                "text/plain",
                use_container_width=True,
            )