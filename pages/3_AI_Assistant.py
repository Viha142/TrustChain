import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="AI Assistant — VendorVault", page_icon="🤖", layout="wide")

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
    background: linear-gradient(135deg, #064E3B 0%, #059669 60%, #06B6D4 100%);
    border-radius: 16px; padding: 28px 36px; color: white; margin-bottom: 28px;
}
.chat-bubble-user {
    background: linear-gradient(135deg, #2563EB, #7C3AED);
    color: white; border-radius: 16px 16px 4px 16px;
    padding: 12px 18px; margin: 8px 0 8px 20%;
    font-size: 14px; line-height: 1.6; box-shadow: 0 2px 12px rgba(37,99,235,0.3);
}
.chat-bubble-ai {
    background: white; color: #1E293B;
    border-radius: 16px 16px 16px 4px; padding: 16px 20px;
    margin: 8px 20% 8px 0; font-size: 14px; line-height: 1.7;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #E2E8F0; border-left: 4px solid #059669;
}
.ai-avatar {
    background: linear-gradient(135deg, #059669, #06B6D4);
    border-radius: 50%; width: 32px; height: 32px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 16px; margin-right: 8px; vertical-align: middle;
}
.quick-prompt {
    background: white; border: 1px solid #BFDBFE; border-radius: 10px;
    padding: 10px 14px; margin-bottom: 8px; cursor: pointer;
    font-size: 13px; color: #1D4ED8; font-weight: 500;
    transition: all 0.2s;
}
.quick-prompt:hover {
    background: #EFF6FF; box-shadow: 0 2px 8px rgba(37,99,235,0.1);
}
.divider { height:1px; background:linear-gradient(90deg,transparent,#E2E8F0,transparent); margin:20px 0; }
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
    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ─── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_context():
    try:
        p = pd.read_csv("data/products.csv").to_string(index=False)
    except:
        p = "No product data available."
    try:
        s = pd.read_csv("data/suppliers.csv").to_string(index=False)
    except:
        s = "No supplier data available."
    try:
        r = pd.read_csv("data/ratings.csv").to_string(index=False)
    except:
        r = "No ratings data available."
    return p, s, r

products_ctx, suppliers_ctx, ratings_ctx = load_context()

SYSTEM_PROMPT = f"""You are VendorVault AI, an intelligent procurement advisor for small retailers and kirana shops.
You have deep expertise in supply chain management, vendor selection, and inventory optimization.

You have access to the following live data:

=== PRODUCTS / INVENTORY ===
{products_ctx}

=== SUPPLIERS ===
{suppliers_ctx}

=== SUPPLIER RATINGS & REVIEWS ===
{ratings_ctx}

=== RELIABILITY SCORE FORMULA ===
Reliability Score = (Fulfillment × 0.4) + (OnTime × 0.3) + (Rating × 20 × 0.2) + (PriceScore × 20 × 0.1)

Your job:
- Answer questions about suppliers, inventory, and procurement strategy
- Recommend the best suppliers based on data
- Explain why certain suppliers are rated higher or lower
- Identify low-stock risks and suggest restocking plans
- Be concise, clear, and actionable
- Use bullet points and structured answers when helpful
- Always cite specific numbers from the data when making recommendations
- Respond in a friendly, professional tone suited for small business owners
"""

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <div style="font-size:13px;opacity:.7;text-transform:uppercase;letter-spacing:.1em;margin-bottom:6px">
        AI PROCUREMENT ADVISOR
    </div>
    <div style="font-size:32px;font-weight:800;">🤖 AI Assistant</div>
    <div style="opacity:.85;margin-top:4px;">
        Ask anything about your suppliers, inventory, and procurement strategy
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Quick prompts ────────────────────────────────────────────────────────────
st.markdown("**💡 Quick Prompts — Click to ask:**")
quick_col1, quick_col2, quick_col3 = st.columns(3)

quick_prompts = [
    "Which supplier should I use for snacks?",
    "Which products are critically low on stock?",
    "Why is RetailFlow rated lower than others?",
    "Recommend the top 3 suppliers overall.",
    "Which supplier has the best on-time delivery?",
    "Give me a restocking plan for all low-stock items.",
]

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None

for i, prompt in enumerate(quick_prompts):
    col = [quick_col1, quick_col2, quick_col3][i % 3]
    with col:
        if st.button(f"💬 {prompt}", key=f"qp_{i}", use_container_width=True):
            st.session_state.pending_prompt = prompt

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Chat History ─────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat container
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;color:#94A3B8;">
            <div style="font-size:48px;margin-bottom:12px">🤖</div>
            <div style="font-size:18px;font-weight:600;color:#475569;margin-bottom:8px">
                Hello! I'm VendorVault AI
            </div>
            <div style="font-size:14px">
                Ask me about suppliers, inventory, or procurement recommendations.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="chat-bubble-user">
                    <div style="font-size:11px;opacity:.75;margin-bottom:4px;font-weight:600">YOU</div>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-bubble-ai">
                    <div style="font-size:11px;color:#059669;font-weight:700;margin-bottom:6px">
                        🤖 VENDORVAULT AI
                    </div>
                    {msg["content"].replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ─── Input ────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask about suppliers, inventory, recommendations...")

# Use quick prompt or typed input
prompt_to_send = st.session_state.pending_prompt or user_input
st.session_state.pending_prompt = None

if prompt_to_send:
    st.session_state.chat_history.append({"role": "user", "content": prompt_to_send})

    # Build messages for API
    messages = []
    for m in st.session_state.chat_history:
        messages.append({"role": m["role"], "content": m["content"]})

    # Call OpenAI
    try:
       from groq import Groq

       api_key = st.secrets.get("GROQ_API_KEY","")

       if not api_key:
            raise ValueError("No Groq API key found")

       client = Groq(api_key=api_key)

       with st.spinner("🤖 VendorVault AI is thinking..."):

            response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT}
        ] + messages,
        temperature=0.7,
        max_tokens=800,
    )

       reply = response.choices[0].message.content
    except ValueError:
        # Fallback: rule-based responses when no API key
        q = prompt_to_send.lower()
        if "snack" in q:
            reply = ("**Best Supplier for Snacks: QuickSupply**\n\n"
                     "• Fulfillment Rate: 88%\n• On-time Delivery: 85%\n• Rating: ⭐ 4.4\n"
                     "• Available Inventory: 300 units\n\n"
                     "QuickSupply is your top choice for snacks. SnackKing is a solid backup "
                     "with 85% fulfillment and 280 units available.")
        elif "low stock" in q or "critical" in q or "restock" in q:
            try:
                p = pd.read_csv("data/products.csv")
                low = p[p["CurrentStock"] < p["MinimumStock"]]
                items = "\n".join([f"• **{r['Product']}**: {r['CurrentStock']}/{r['MinimumStock']} units ({r['Category']})"
                                   for _, r in low.iterrows()])
                reply = f"**Low-Stock Alert — {len(low)} products need restocking:**\n\n{items}\n\nI recommend ordering immediately to avoid stockouts."
            except:
                reply = "I couldn't load product data. Please check your data files."
        elif "retailflow" in q:
            reply = ("**Why RetailFlow is Rated Lower:**\n\n"
                     "RetailFlow has a lower performance profile compared to peers:\n"
                     "• Fulfillment Rate: **75%** (network avg: ~88%)\n"
                     "• On-time Delivery: **70%** (network avg: ~85%)\n"
                     "• Rating: **⭐ 3.9** (lowest in network)\n\n"
                     "Their reliability score of ~79.5 is the lowest. Consider switching to "
                     "DairyBest (score ~88.6) for Dairy category instead.")
        elif "top" in q or "best" in q or "recommend" in q:
            reply = ("**Top 3 Suppliers Overall:**\n\n"
                     "🥇 **SmartStock** — Score: 95.6 | Fulfillment: 98% | ⭐ 4.9 | 700 units\n"
                     "🥈 **FreshFoods Ltd** — Score: 91.6 | Fulfillment: 95% | ⭐ 4.8 | 500 units\n"
                     "🥉 **BeveragePro** — Score: 91.1 | Fulfillment: 93% | ⭐ 4.7 | 450 units\n\n"
                     "SmartStock is your most reliable partner with a near-perfect fulfillment rate.")
        elif "on-time" in q or "delivery" in q:
            reply = ("**Best On-Time Delivery Performers:**\n\n"
                     "1. SmartStock — **95%** on-time delivery\n"
                     "2. FreshFoods Ltd — **92%**\n"
                     "3. BeveragePro — **90%**\n\n"
                     "For time-critical orders, SmartStock and FreshFoods are your safest bets.")
        else:
            reply = (f"I understand you're asking about: *{prompt_to_send}*\n\n"
                     "**Note:** I'm running in demo mode (no OpenAI API key configured). "
                     "To unlock full AI capabilities, add your OpenAI API key to `.streamlit/secrets.toml`.\n\n"
                     "Meanwhile, I can answer questions about:\n"
                     "• Snack / Dairy / Grocery supplier recommendations\n"
                     "• Low stock alerts and restock plans\n"
                     "• Supplier comparisons and ratings explanation\n"
                     "• Top-ranked vendors in your network")
    except Exception as e:
        reply = f"⚠️ AI Error: {str(e)}\n\nPlease check your OpenAI API key in `.streamlit/secrets.toml`."

    st.session_state.chat_history.append({"role": "assistant", "content": reply})
    st.rerun()

# Stats
if st.session_state.chat_history:
    num_turns = len([m for m in st.session_state.chat_history if m["role"] == "user"])
    st.caption(f"💬 {num_turns} question(s) in this session · Context includes {len(suppliers_ctx.splitlines())} supplier records")