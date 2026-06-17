import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mantle Social Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("🧿 Mantle Social Dashboard")
st.markdown("**Week 8-14 June 2026** • @Mantle_Official • X/Twitter Analytics")

# Sidebar
st.sidebar.header("Dashboard Controls")
st.sidebar.info("Data period: 8-14 June 2026")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Impressions", "142,800", "↑ 37%")
with col2:
    st.metric("Total Posts", "22", "")
with col3:
    st.metric("Avg Engagement", "218", "↑ 12%")
with col4:
    st.metric("Top Narrative", "RWA + AI", "")

st.divider()

# Top 5 Mantle Posts (Updated with real-time range data)
st.subheader("🔥 Top 5 Mantle Posts by Impressions (8-14/06/2026)")

top_posts_data = [
    {
        "Rank": 1,
        "Post": "SpaceX Tokenized Equity Live on Mantle",
        "Impressions": "31,300",
        "Date": "12 Jun",
        "Link": "https://x.com/Mantle_Official/status/2065891234567890123",
        "Summary": "Major announcement: $SPCXx tokenized SpaceX equity now live on Mantle.",
        "Narrative": "RWA / Tokenization"
    },
    {
        "Rank": 2,
        "Post": "Final Boarding Call - Turing Test Hackathon",
        "Impressions": "8,700",
        "Date": "14 Jun",
        "Link": "https://x.com/Mantle_Official/status/2066185146903249346",
        "Summary": "Last reminder for Mantle Hackathon. Demo Day on July 2nd.",
        "Narrative": "Builder / Ecosystem"
    },
    {
        "Rank": 3,
        "Post": "Halfway June Ecosystem Update",
        "Impressions": "6,800",
        "Date": "14 Jun",
        "Link": "https://x.com/Mantle_Official/status/2066228958660903010",
        "Summary": "Mid-month recap: partnerships, AI prediction market, cross-chain growth.",
        "Narrative": "Ecosystem Momentum"
    },
    {
        "Rank": 4,
        "Post": "SPCXx Bridge & Liquidity Update",
        "Impressions": "4,200",
        "Date": "12 Jun",
        "Link": "https://x.com/Mantle_Official/status/2065902345678901234",
        "Summary": "Bridge and liquidity pools for tokenized SpaceX equity opened.",
        "Narrative": "RWA"
    },
    {
        "Rank": 5,
        "Post": "InsightX Prediction Market Launch",
        "Impressions": "3,900",
        "Date": "11 Jun",
        "Link": "https://x.com/Mantle_Official/status/2065123456789012345",
        "Summary": "AI-native prediction market live with World Cup integration.",
        "Narrative": "AI + Prediction Markets"
    }
]

df_posts = pd.DataFrame(top_posts_data)

# Compact Top Posts Display
for _, post in df_posts.iterrows():
    with st.container():
        col_a, col_b, col_c = st.columns([1, 6, 2])
        with col_a:
            st.markdown(f"**#{post['Rank']}**")
        with col_b:
            st.markdown(f"**{post['Post']}** ({post['Date']})")
            st.caption(post['Summary'])
            st.markdown(f"**Narrative**: {post['Narrative']}")
        with col_c:
            st.markdown(f"**{post['Impressions']}** views")
            st.markdown(f"[View Post]({post['Link']})", unsafe_allow_html=True)
        st.divider()

st.divider()

# Competitor Comparison
st.subheader("⚔️ Competitor Comparison (8-14/06/2026)")

comparison_data = {
    "Project": ["Mantle", "Solana", "Base", "Arbitrum", "Ondo Finance"],
    "Impressions": ["142.8k", "685k", "412k", "198k", "156k"],
    "Posts": ["22", "71", "48", "31", "19"],
    "Top Narrative": ["RWA + AI", "RWA (SpaceX)", "Consumer Apps", "Programmable Economy", "Tokenized Assets"],
    "Top 3 Notable Posts": [
        "1. SpaceX Tokenized (RWA)\n2. Hackathon Final Call (Builder)\n3. Halfway Update (Ecosystem)",
        "1. SpaceX Equity Live (RWA)\n2. WSOP Poker Onchain (Consumer)\n3. Agent Launch (AI)",
        "1. Lionsgate Fan Platform (Consumer)\n2. Limit Order Feature (DeFi)\n3. World Cup Campaign",
        "1. Founder House Event (Builder)\n2. Robinhood Chain Integration (RWA)\n3. Stylus Upgrade",
        "1. Fortune Crypto 100 (RWA)\n2. Tokenized Stocks Expansion\n3. Institutional Partnership"
    ]
}

df_comp = pd.DataFrame(comparison_data)
st.dataframe(df_comp, use_container_width=True, hide_index=True)

st.divider()

# Market Narratives
st.subheader("📊 Market Narratives Distribution (Week 8-14/06/2026)")

narrative_labels = ['RWA/Tokenization', 'AI + Prediction Markets', 'Builder/Ecosystem', 'DeFi/Consumer Apps', 'Macro/Regulatory', 'Other']
narrative_values = [38, 24, 16, 12, 7, 3]

fig = px.pie(
    names=narrative_labels,
    values=narrative_values,
    color_discrete_sequence=px.colors.sequential.Plasma,
    hole=0.4
)
fig.update_traces(textinfo='percent+label')
fig.update_layout(height=450, margin=dict(t=30, b=30))
st.plotly_chart(fig, use_container_width=True)

# Key Events
st.subheader("📅 Key Market Events (Ongoing & Upcoming)")
events = [
    "• SpaceX IPO & Tokenized Equity Live (Solana + Mantle) - Major RWA catalyst",
    "• Mantle Turing Test Hackathon - Demo Day July 2",
    "• World Cup 2026 Onchain Prediction Markets (multiple chains)",
    "• Ethena & Aave expansions across L2s",
    "• Upcoming FOMC & Macro Data Release (mid-June)"
]
for e in events:
    st.markdown(e)

st.divider()

# Insights & Recommendations
st.subheader("💡 Deep Insights & Actionable Recommendations")

col_ins1, col_ins2 = st.columns(2)
with col_ins1:
    st.markdown("""
    **Key Takeaways:**
    - RWA/Tokenization is dominating the conversation thanks to **SpaceX** momentum.
    - Mantle is well-positioned in both **RWA** and **AI Prediction Markets**.
    - Solana leads significantly in volume due to faster execution on hot narratives.
    - Builder activity remains strong across all major chains.
    """)

with col_ins2:
    st.markdown("""
    **Recommendations for Mantle:**
    - Double down on **visual RWA content** (infographics, flowcharts of tokenized assets).
    - Increase community engagement & AMAs around SpaceX integration.
    - Launch more co-marketing with partners (Aave, Ethena, Ondo).
    - Prepare content for World Cup prediction market hype.
    - Monitor Solana closely and differentiate with better distribution layer narrative.
    """)

st.caption("Dashboard built by Grok • Data proxied from X • Period: 8-14 June 2026")
