import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Vendor Discovery",
    page_icon="🤝",
    layout="wide"
)

# =========================
# SAMPLE DATA
# =========================

data = [
    {
        "Supplier": "SmartStock",
        "Category": "Grocery",
        "ReliabilityScore": 96.9,
        "Fulfillment": 98,
        "OnTime": 95,
        "Rating": 4.9,
        "Inventory": 700,
        "PriceScore": 4.8
    },
    {
        "Supplier": "BeveragePro",
        "Category": "Beverages",
        "ReliabilityScore": 92.2,
        "Fulfillment": 95,
        "OnTime": 91,
        "Rating": 4.7,
        "Inventory": 620,
        "PriceScore": 4.5
    },
    {
        "Supplier": "FreshFoods Ltd",
        "Category": "Grocery",
        "ReliabilityScore": 90.6,
        "Fulfillment": 92,
        "OnTime": 90,
        "Rating": 4.0,
        "Inventory": 500,
        "PriceScore": 4.3
    },
    {
        "Supplier": "DairyBest",
        "Category": "Dairy",
        "ReliabilityScore": 90.1,
        "Fulfillment": 91,
        "OnTime": 89,
        "Rating": 4.6,
        "Inventory": 480,
        "PriceScore": 4.2
    },
    {
        "Supplier": "GroceryHub",
        "Category": "Grocery",
        "ReliabilityScore": 89.4,
        "Fulfillment": 90,
        "OnTime": 88,
        "Rating": 4.5,
        "Inventory": 550,
        "PriceScore": 4.4
    }
]

df = pd.DataFrame(data)

# =========================
# STYLES
# =========================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2rem;
}

.page-header{
    background:linear-gradient(
        135deg,
        #4C1D95,
        #7C3AED,
        #A855F7
    );
    padding:40px;
    border-radius:24px;
    color:white;
    margin-bottom:30px;
}

.sup-card{
    background:white;
    border-radius:18px;
    padding:20px;
    border:1px solid #E2E8F0;
}

.sup-name{
    font-size:28px;
    font-weight:800;
    color:#0F172A;
}

.sup-cat{
    margin-top:8px;
    color:#7C3AED;
    font-size:14px;
    font-weight:700;
    letter-spacing:.08em;
}

.score-big{
    font-size:54px;
    font-weight:900;
    color:#2563EB;
    line-height:1;
}

.badge-top{
    background:#DBEAFE;
    color:#1D4ED8;
    padding:8px 14px;
    border-radius:999px;
    font-size:13px;
    font-weight:700;
}

.badge-good{
    background:#DCFCE7;
    color:#166534;
    padding:8px 14px;
    border-radius:999px;
    font-size:13px;
    font-weight:700;
}

.badge-mid{
    background:#FEF3C7;
    color:#92400E;
    padding:8px 14px;
    border-radius:999px;
    font-size:13px;
    font-weight:700;
}

.metric-box{
    background:#F8FAFC;
    border-radius:14px;
    padding:16px;
    text-align:center;
}

.metric-value{
    font-size:24px;
    font-weight:800;
    color:#2563EB;
}

.metric-label{
    margin-top:6px;
    font-size:12px;
    color:#64748B;
}

.rank-card{
    background:white;
    border-radius:18px;
    padding:18px;
    margin-bottom:14px;
    border:1px solid #E2E8F0;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.markdown("""
<div class="page-header">

    <div style="
        font-size:13px;
        opacity:.85;
        letter-spacing:.15em;
        text-transform:uppercase;
        margin-bottom:10px;
    ">
        Supplier Network
    </div>

    <div style="
        font-size:56px;
        font-weight:900;
        line-height:1.1;
    ">
        🤝 Vendor Discovery
    </div>

    <div style="
        margin-top:14px;
        font-size:20px;
        opacity:.92;
    ">
        Search, filter and rank all verified suppliers in your procurement network
    </div>

</div>
""", unsafe_allow_html=True)

# =========================
# FILTERS
# =========================

c1, c2, c3 = st.columns(3)

with c1:
    search = st.text_input(
        "🔍 Search suppliers",
        placeholder="Search..."
    )

with c2:
    category = st.selectbox(
        "📂 Category",
        ["All"] + list(df["Category"].unique())
    )

with c3:
    sort_by = st.selectbox(
        "↕️ Sort by",
        [
            "Reliability Score",
            "Rating",
            "Fulfillment"
        ]
    )

# =========================
# FILTER LOGIC
# =========================

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["Supplier"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]

if sort_by == "Reliability Score":
    filtered_df = filtered_df.sort_values(
        by="ReliabilityScore",
        ascending=False
    )

elif sort_by == "Rating":
    filtered_df = filtered_df.sort_values(
        by="Rating",
        ascending=False
    )

elif sort_by == "Fulfillment":
    filtered_df = filtered_df.sort_values(
        by="Fulfillment",
        ascending=False
    )

st.markdown(
    f"### Showing {len(filtered_df)} supplier(s)"
)

st.divider()

# =========================
# LAYOUT
# =========================

left_col, right_col = st.columns([2.2, 1])

# =========================
# SUPPLIER CARDS
# =========================

with left_col:

    st.markdown("## 🗂️ Supplier Cards")

    if filtered_df.empty:

        st.warning("No suppliers found.")

    else:

        for idx, row in filtered_df.iterrows():

            score = float(row["ReliabilityScore"])
            bar_width = min(int(score), 100)

            if score >= 95:
                badge = "⭐ Top Vendor"
                badge_class = "badge-top"

            elif score >= 90:
                badge = "✅ Trusted"
                badge_class = "badge-good"

            else:
                badge = "⚠️ Average"
                badge_class = "badge-mid"

            with st.expander(
                f"{row['Supplier']} — Score: {score:.1f}",
                expanded=(idx == 0)
            ):

                st.markdown(f"""
                <div class="sup-card">

                    <div style="
                        display:flex;
                        justify-content:space-between;
                        align-items:flex-start;
                        margin-bottom:20px;
                    ">

                        <div>

                            <div class="sup-name">
                                {row['Supplier']}
                            </div>

                            <div class="sup-cat">
                                📂 {row['Category'].upper()}
                            </div>

                        </div>

                        <div style="text-align:right">

                            <div class="score-big">
                                {score:.1f}
                            </div>

                            <div style="
                                color:#94A3B8;
                                font-size:13px;
                                margin-top:4px;
                            ">
                                Reliability
                            </div>

                            <div style="margin-top:12px">
                                <span class="{badge_class}">
                                    {badge}
                                </span>
                            </div>

                        </div>

                    </div>

                    <div style="margin-bottom:20px">

                        <div style="
                            display:flex;
                            justify-content:space-between;
                            margin-bottom:6px;
                            color:#64748B;
                            font-size:13px;
                        ">
                            <span>Reliability Score</span>
                            <span>{score:.1f}/100</span>
                        </div>

                        <div style="
                            background:#E2E8F0;
                            border-radius:999px;
                            height:10px;
                            overflow:hidden;
                        ">

                            <div style="
                                width:{bar_width}%;
                                height:100%;
                                background:linear-gradient(
                                    90deg,
                                    #7C3AED,
                                    #2563EB
                                );
                            "></div>

                        </div>

                    </div>

                    <div style="
                        display:grid;
                        grid-template-columns:1fr 1fr 1fr;
                        gap:12px;
                    ">

                        <div class="metric-box">
                            <div class="metric-value">
                                {row['Fulfillment']}%
                            </div>

                            <div class="metric-label">
                                Fulfillment
                            </div>
                        </div>

                        <div class="metric-box">
                            <div class="metric-value">
                                {row['OnTime']}%
                            </div>

                            <div class="metric-label">
                                On-Time
                            </div>
                        </div>

                        <div class="metric-box">
                            <div class="metric-value">
                                ⭐ {row['Rating']}
                            </div>

                            <div class="metric-label">
                                Rating
                            </div>
                        </div>

                    </div>

                </div>
                """, unsafe_allow_html=True)

# =========================
# MASTER RANKING
# =========================

with right_col:

    st.markdown("## 🏆 Master Ranking")

    rank_df = df.sort_values(
        by="ReliabilityScore",
        ascending=False
    )

    medals = ["🥇", "🥈", "🥉"]

    for idx, row in rank_df.iterrows():

        score = row["ReliabilityScore"]

        if idx < 3:
            medal = medals[idx]
        else:
            medal = f"#{idx+1}"

        st.markdown(f"""
        <div class="rank-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:8px;
            ">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:8px;
                    font-weight:800;
                    color:#0F172A;
                    font-size:18px;
                ">
                    <span>{medal}</span>
                    <span>{row['Supplier']}</span>
                </div>

                <div style="
                    font-weight:900;
                    color:#2563EB;
                    font-size:18px;
                ">
                    {score:.1f}
                </div>

            </div>

            <div style="
                background:#E2E8F0;
                border-radius:999px;
                height:8px;
                overflow:hidden;
                margin-bottom:8px;
            ">

                <div style="
                    width:{int(score)}%;
                    height:100%;
                    background:linear-gradient(
                        90deg,
                        #2563EB,
                        #7C3AED
                    );
                "></div>

            </div>

            <div style="
                color:#94A3B8;
                font-size:13px;
            ">
                {row['Category']} · ⭐ {row['Rating']}
            </div>

        </div>
        """, unsafe_allow_html=True)