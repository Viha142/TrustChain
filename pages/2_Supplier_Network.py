
import pandas as pd
import plotly.express as px

import streamlit as st

st.set_page_config(
    page_title="Vendor Discovery",
    layout="wide"
)

# ---------------- PAGE STYLE ---------------- #

st.markdown("""
<style>

.stApp {
    background: #F5F7FB;
}

/* REMOVE CODE BLOCK LOOK */
code {
    background: transparent !important;
    color: inherit !important;
}

pre {
    background: transparent !important;
    border: none !important;
}

/* Supplier Card */
.supplier-card {
    background: white;
    border-radius: 24px;
    padding: 28px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    margin-bottom: 20px;
}

/* Supplier Name */
.sup-name {
    font-size: 28px;
    font-weight: 800;
    color: #0F172A;
}

/* Category */
.sup-cat {
    margin-top: 8px;
    font-size: 14px;
    color: #7C3AED;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
}

/* Big Score */
.score-big {
    font-size: 54px;
    font-weight: 900;
    color: #2563EB;
    line-height: 1;
}

/* Small Label */
.score-label {
    color: #94A3B8;
    font-size: 14px;
    margin-top: 6px;
}

/* Badge */
.badge {
    margin-top: 14px;
    display: inline-block;
    background: #DBEAFE;
    color: #1D4ED8;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 700;
}

/* Metric Box */
.metric-box {
    background: #F8FAFF;
    border-radius: 16px;
    padding: 16px;
    text-align: center;
}

/* Metric Number */
.metric-number {
    font-size: 26px;
    font-weight: 900;
}

/* Metric Label */
.metric-label {
    margin-top: 4px;
    font-size: 12px;
    color: #94A3B8;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HERO SECTION ---------------- #

st.markdown("""
<div style="
    background:linear-gradient(135deg,#4C1D95,#7C3AED,#A855F7);
    padding:50px;
    border-radius:30px;
    color:white;
    margin-bottom:40px;
">

    <div style="
        font-size:13px;
        opacity:.85;
        letter-spacing:.15em;
        text-transform:uppercase;
        margin-bottom:10px;
        font-weight:700;
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

# ---------------- FILTERS ---------------- #

col1, col2, col3 = st.columns(3)

with col1:
    search = st.text_input("🔍 Search suppliers", placeholder="Search...")

with col2:
    category = st.selectbox(
        "📁 Category",
        ["All", "Grocery", "Beverages", "Dairy"]
    )

with col3:
    sort = st.selectbox(
        "↕️ Sort by",
        ["Reliability Score", "Rating"]
    )

# ---------------- DATA ---------------- #

suppliers = [
    {
        "name": "SmartStock",
        "category": "GROCERY",
        "score": 96.9,
        "fulfillment": "98%",
        "delivery": "95%",
        "rating": "4.9",
        "orders": "700+"
    }
]

# ---------------- LAYOUT ---------------- #

left, right = st.columns([2.2, 1])

# ---------------- LEFT SIDE ---------------- #

with left:

    st.markdown("""
    <h1 style="
        font-size:48px;
        font-weight:900;
        color:#1E293B;
        margin-bottom:25px;
    ">
        🗂️ Supplier Cards
    </h1>
    """, unsafe_allow_html=True)

    for s in suppliers:

        if search:
            if search.lower() not in s["name"].lower():
                continue

        html = f"""
        <div class="supplier-card">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:flex-start;
                margin-bottom:24px;
            ">

                <div>

                    <div class="sup-name">
                        {s["name"]}
                    </div>

                    <div class="sup-cat">
                        📁 {s["category"]}
                    </div>

                </div>

                <div style="text-align:right">

                    <div class="score-big">
                        {s["score"]}
                    </div>

                    <div class="score-label">
                        Reliability
                    </div>

                    <div class="badge">
                        ⭐ Top Vendor
                    </div>

                </div>

            </div>

            <div style="margin-bottom:18px;">

                <div style="
                    display:flex;
                    justify-content:space-between;
                    font-size:13px;
                    color:#64748B;
                    margin-bottom:6px;
                ">
                    <span>Reliability Score</span>
                    <span>{s["score"]}/100</span>
                </div>

                <div style="
                    background:#E2E8F0;
                    border-radius:999px;
                    height:10px;
                    overflow:hidden;
                ">

                    <div style="
                        width:{s["score"]}%;
                        height:100%;
                        background:linear-gradient(90deg,#7C3AED,#2563EB);
                    ">
                    </div>

                </div>

            </div>

            <div style="
                display:grid;
                grid-template-columns:1fr 1fr 1fr 1fr;
                gap:14px;
            ">

                <div class="metric-box">
                    <div class="metric-number" style="color:#2563EB;">
                        {s["fulfillment"]}
                    </div>
                    <div class="metric-label">
                        Fulfillment
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-number" style="color:#7C3AED;">
                        {s["delivery"]}
                    </div>
                    <div class="metric-label">
                        On-Time
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-number" style="color:#06B6D4;">
                        ⭐ {s["rating"]}
                    </div>
                    <div class="metric-label">
                        Rating
                    </div>
                </div>

                <div class="metric-box">
                    <div class="metric-number" style="color:#059669;">
                        {s["orders"]}
                    </div>
                    <div class="metric-label">
                        Orders
                    </div>
                </div>

            </div>

        </div>
        """

        st.markdown(html, unsafe_allow_html=True)

# ---------------- RIGHT SIDE ---------------- #

with right:

    st.markdown("""
    <h1 style="
        font-size:48px;
        font-weight:900;
        color:#1E293B;
        margin-bottom:25px;
    ">
        🏆 Master Ranking
    </h1>
    """, unsafe_allow_html=True)

    rankings = [
        ("🥇", "SmartStock", 96.9, "Grocery", "4.9"),
        ("🥈", "BeveragePro", 92.2, "Beverages", "4.7"),
        ("🥉", "FreshFoods Ltd", 90.6, "Grocery", "4.0"),
    ]

    for medal, name, score, cat, rating in rankings:

        st.markdown(f"""
        <div style="
            background:white;
            border-radius:20px;
            padding:20px;
            margin-bottom:16px;
            border:1px solid #E2E8F0;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:10px;
            ">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                    font-weight:800;
                    color:#0F172A;
                    font-size:22px;
                ">
                    <span>{medal}</span>
                    <span>{name}</span>
                </div>

                <div style="
                    font-size:28px;
                    font-weight:900;
                    color:#2563EB;
                ">
                    {score}
                </div>

            </div>

            <div style="
                height:8px;
                background:#E2E8F0;
                border-radius:999px;
                overflow:hidden;
                margin-bottom:10px;
            ">

                <div style="
                    width:{score}%;
                    height:100%;
                    background:linear-gradient(90deg,#2563EB,#9333EA);
                ">
                </div>

            </div>

            <div style="
                color:#94A3B8;
                font-size:14px;
            ">
                {cat} · ⭐{rating}
            </div>

        </div>
        """, unsafe_allow_html=True)