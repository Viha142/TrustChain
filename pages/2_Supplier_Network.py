import streamlit as st
import pandas as pd
import plotly.express as px

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Suppliers — VendorVault",
    page_icon="🤝",
    layout="wide"
)

# ─────────────────────────────────────────────────────────────
# CUSTOM STYLES
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.stApp {
    background: linear-gradient(
        135deg,
        #F0F4FF 0%,
        #F8FAFF 50%,
        #EEF2FF 100%
    );
}

section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #0F172A 0%,
        #1E1B4B 50%,
        #1E3A5F 100%
    ) !important;
}

section[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

.page-header {
    background: linear-gradient(
        135deg,
        #4C1D95 0%,
        #7C3AED 60%,
        #A855F7 100%
    );
    border-radius: 18px;
    padding: 30px 36px;
    color: white;
    margin-bottom: 28px;
}

.sup-card {
    background: white;
    border-radius: 14px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 2px 14px rgba(0,0,0,0.06);
}

.sup-name {
    font-size: 18px;
    font-weight: 800;
    color: #0F172A;
}

.sup-cat {
    font-size: 12px;
    font-weight: 700;
    color: #7C3AED;
    text-transform: uppercase;
    letter-spacing: .05em;
}

.score-big {
    font-size: 30px;
    font-weight: 800;
    color: #2563EB;
}

.metric-box {
    background: #F8FAFF;
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}

.metric-title {
    font-size: 11px;
    color: #94A3B8;
}

.metric-value {
    font-size: 20px;
    font-weight: 800;
}

.divider {
    height: 1px;
    background: linear-gradient(
        90deg,
        transparent,
        #CBD5E1,
        transparent
    );
    margin: 24px 0;
}

.rank-card {
    background: white;
    border-radius: 12px;
    padding: 14px;
    margin-bottom: 10px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 1px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("## 🏪 VendorVault AI")

    st.page_link("app.py", label="🏠 Dashboard")
    st.page_link("pages/1_Inventory_Management.py", label="📦 Inventory")
    st.page_link("pages/2_Supplier_Network.py", label="🤝 Supplier Network")
    st.page_link("pages/3_AI_Assistant.py", label="🤖 AI Assistant")
    st.page_link("pages/4_Analytics.py", label="📊 Analytics")
    st.page_link("pages/5_Contracts_Trust.py", label="📋 Contracts & Trust")

    st.markdown("---")

    if st.button("🔄 Refresh", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ─────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_suppliers():

    try:
        df = pd.read_csv("data/suppliers.csv")

        required_columns = [
            "Supplier",
            "Category",
            "Fulfillment",
            "OnTime",
            "PriceScore",
            "Inventory",
            "Rating"
        ]

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        return df

    except Exception as e:

        st.error(f"Error loading supplier data: {e}")

        return pd.DataFrame(
            columns=[
                "Supplier",
                "Category",
                "Fulfillment",
                "OnTime",
                "PriceScore",
                "Inventory",
                "Rating"
            ]
        )

# ─────────────────────────────────────────────────────────────
# RELIABILITY SCORE
# ─────────────────────────────────────────────────────────────
def calculate_reliability(row):

    fulfillment = float(row["Fulfillment"])
    ontime = float(row["OnTime"])
    rating = float(row["Rating"])
    price = float(row["PriceScore"])

    score = (
        fulfillment * 0.4
        + ontime * 0.3
        + (rating * 20) * 0.2
        + (price * 20) * 0.1
    )

    return round(score, 1)

# ─────────────────────────────────────────────────────────────
# LOAD DATAFRAME
# ─────────────────────────────────────────────────────────────
suppliers = load_suppliers()

if suppliers.empty:
    st.error("No supplier data available.")
    st.stop()

suppliers["ReliabilityScore"] = suppliers.apply(
    calculate_reliability,
    axis=1
)

suppliers_sorted = suppliers.sort_values(
    by="ReliabilityScore",
    ascending=False
).reset_index(drop=True)

# ─────────────────────────────────────────────────────────────
# PAGE HEADER
# ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">

    <div style="
        font-size:13px;
        opacity:.8;
        text-transform:uppercase;
        letter-spacing:.1em;
        margin-bottom:6px;
    ">
        SUPPLIER NETWORK
    </div>

    <div style="
        font-size:34px;
        font-weight:800;
    ">
        🤝 Vendor Discovery
    </div>

    <div style="
        opacity:.88;
        margin-top:6px;
        font-size:15px;
    ">
        Search, filter and rank all verified suppliers in your procurement ecosystem.
    </div>

</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# FILTERS
# ─────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([2, 1.5, 1.5])

with col1:
    search = st.text_input(
        "🔍 Search Suppliers",
        placeholder="Search supplier name..."
    )

with col2:
    categories = ["All"] + sorted(
        suppliers["Category"].dropna().unique().tolist()
    )

    selected_category = st.selectbox(
        "📂 Category",
        categories
    )

with col3:
    sort_option = st.selectbox(
        "↕️ Sort By",
        [
            "Reliability Score",
            "Rating",
            "Fulfillment",
            "Inventory"
        ]
    )

# ─────────────────────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────────────────────
filtered = suppliers.copy()

if search:
    filtered = filtered[
        filtered["Supplier"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if selected_category != "All":
    filtered = filtered[
        filtered["Category"] == selected_category
    ]

sort_mapping = {
    "Reliability Score": "ReliabilityScore",
    "Rating": "Rating",
    "Fulfillment": "Fulfillment",
    "Inventory": "Inventory"
}

filtered = filtered.sort_values(
    by=sort_mapping[sort_option],
    ascending=False
).reset_index(drop=True)

st.markdown(f"### Showing {len(filtered)} Supplier(s)")

st.markdown(
    "<div class='divider'></div>",
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────────────────────────────────────
left_col, right_col = st.columns([2, 1], gap="large")

# ─────────────────────────────────────────────────────────────
# SUPPLIER CARDS
# ─────────────────────────────────────────────────────────────
with left_col:

    st.markdown("## 🗂️ Supplier Cards")

    for index, row in filtered.iterrows():

        score = row["ReliabilityScore"]

        if score >= 90:
            badge = "⭐ Top Vendor"
        elif score >= 80:
            badge = "✅ Reliable"
        else:
            badge = "📋 Average"

    st.markdown(f"""
<div class="rank-card">

    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:8px;
    ">

        <div>
            <span style="font-size:15px">
                {medal}
            </span>

            <span style="
                font-weight:700;
                margin-left:6px;
                color:#0F172A;
            ">
                {row['Supplier']}
            </span>
        </div>

        <div style="
            font-weight:800;
            color:#2563EB;
        ">
            {row['ReliabilityScore']}
        </div>

    </div>

    <div style="
        background:#E2E8F0;
        border-radius:4px;
        height:6px;
        overflow:hidden;
    ">

        <div style="
            width:{min(int(row['ReliabilityScore']),100)}%;
            height:100%;
            background:linear-gradient(
                90deg,
                #2563EB,
                #7C3AED
            );
        "></div>

    </div>

    <div style="
        margin-top:6px;
        font-size:11px;
        color:#94A3B8;
    ">
        {row['Category']} · ⭐ {row['Rating']}
    </div>

</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
m4, m5 = st.columns(2)

with m1:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value" style="color:#2563EB">
                        {row['Fulfillment']}%
                    </div>
                    <div class="metric-title">
                        Fulfillment
                    </div>
                </div>
                """, unsafe_allow_html=True)
with m2:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value" style="color:#7C3AED">
                        {row['OnTime']}%
                    </div>
                    <div class="metric-title">
                        On-Time
                    </div>
                </div>
                """, unsafe_allow_html=True)

with m3:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value" style="color:#06B6D4">
                        ⭐ {row['Rating']}
                    </div>
                    <div class="metric-title">
                        Rating
                    </div>
                </div>
                """, unsafe_allow_html=True)

with m4:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value" style="color:#059669">
                        {row['Inventory']}
                    </div>
                    <div class="metric-title">
                        Inventory
                    </div>
                </div>
                """, unsafe_allow_html=True)

with m5:
                st.markdown(f"""
                <div class="metric-box">
                    <div class="metric-value" style="color:#D97706">
                        {row['PriceScore']}
                    </div>
                    <div class="metric-title">
                        Price Score
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# RANKING PANEL
# ─────────────────────────────────────────────────────────────
with right_col:

    st.markdown("## 🏆 Top Suppliers")

    top_suppliers = suppliers_sorted.head(10)

    for i, row in top_suppliers.iterrows():

        if i == 0:
            medal = "🥇"
        elif i == 1:
            medal = "🥈"
        elif i == 2:
            medal = "🥉"
        else:
            medal = f"#{i + 1}"

        st.markdown(f"""
        <div class="rank-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:8px;
            ">

                <div>
                    <span style="font-size:15px">
                        {medal}
                    </span>

                    <span style="
                        font-weight:700;
                        margin-left:6px;
                        color:#0F172A;
                    ">
                        {row['Supplier']}
                    </span>
                </div>

                <div style="
                    font-weight:800;
                    color:#2563EB;
                ">
                    {row['ReliabilityScore']}
                </div>

            </div>

            <div style="
                background:#E2E8F0;
                border-radius:4px;
                height:6px;
                overflow:hidden;
            ">

                <div style="
                    width:{min(int(row['ReliabilityScore']),100)}%;
                    height:100%;
                    background:linear-gradient(
                        90deg,
                        #2563EB,
                        #7C3AED
                    );
                "></div>

            </div>

            <div style="
                margin-top:6px;
                font-size:11px;
                color:#94A3B8;
            ">
                {row['Category']} · ⭐ {row['Rating']}
            </div>

        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div class='divider'></div>",
        unsafe_allow_html=True
    )

    # DOWNLOAD BUTTON
    csv = suppliers_sorted.to_csv(index=False)

    st.download_button(
        label="⬇️ Export Supplier Data",
        data=csv,
        file_name="suppliers.csv",
        mime="text/csv",
        use_container_width=True
    )

# ─────────────────────────────────────────────────────────────
# ANALYTICS SECTION
# ─────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("## 📊 Supplier Analytics")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:

    fig = px.bar(
        suppliers_sorted.head(10),
        x="Supplier",
        y="ReliabilityScore",
        color="ReliabilityScore",
        title="Top Supplier Reliability Scores"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with chart_col2:

    fig2 = px.pie(
        suppliers,
        names="Category",
        title="Supplier Category Distribution"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )