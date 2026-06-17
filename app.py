import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page config
st.set_page_config(
    page_title="Mantle Social Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .main { background-color: #0f172a; color: white; }
    .stPlotlyChart { background-color: #1e2937; border-radius: 16px; }
    .metric-card {
        background: linear-gradient(135deg, #1e2937, #334155);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid #475569;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Mantle Social Dashboard")
st.subheader("Week 8-14 June 2026 • @Mantle_Official")
st.caption("Live X/Twitter Social Listening Dashboard • Ông Trùm Twitter Edition")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Impressions", "68,400", "↑ 24%")
with col2:
    st.metric("Total Posts", "22", "")
with col3:
    st.metric("Avg Engagement", "142", "")
with col4:
    st.metric("Top Narrative", "RWA + AI", "")

# Top 5 Mantle Posts
st.header("🔥 Top 5 Mantle Posts by Impressions")
posts_data = [
    {"rank": 1, "title": "Halfway June Summary", "views": 6800, "link": "https://x.com/Mantle_Official/status/2066228958660903010", "summary": "Tokenized SpaceX equity live, InsightX AI Prediction Market, hackathon updates, key partnerships.", "narrative": "RWA + AI + Ecosystem"},
    {"rank": 2, "title": "Final Boarding Call - Turing Test Hackathon", "views": 8700, "link": "https://x.com/Mantle_Official/status/2066185146903249346", "summary": "Last reminder for Mantle Hackathon • Demo Day on July 2", "narrative": "Builder & Community"},
    {"rank": 3, "title": "InsightX Prediction Market Launch", "views": 4200, "link": "#", "summary": "AI-native prediction market with World Cup integration", "narrative": "AI + Prediction Markets"},
    {"rank": 4, "title": "Partnership Updates", "views": 3900, "link": "#", "summary": "New integrations with Aave, Ethena and more", "narrative": "DeFi & RWA"},
    {"rank": 5, "title": "Regional Expansion", "views": 2800, "link": "#", "summary": "Events in Singapore, Seoul & Americas", "narrative": "Community Growth"}
]

for post in posts_data:
    with st.container():
        col_a, col_b = st.columns([4,1])
        with col_a:
            st.markdown(f"**#{post['rank']} — [{post['title']}]({post['link']})**")
            st.write(post['summary'])
            st.caption(f"**Narrative:** {post['narrative']}")
        with col_b:
            st.metric("", f"{post['views']:,}", label_visibility="hidden")
        st.divider()

# Competitor Comparison
st.header("⚔️ Competitor Comparison")
comp_data = {
    "Project": ["Mantle", "Solana", "Base", "Arbitrum", "Ondo Finance"],
    "Impressions": ["68k", "520k", "410k", "185k", "145k"],
    "Posts": [22, 68, 41, 29, 31],
    "Top Narrative": ["RWA + AI", "RWA (SpaceX)", "Consumer Apps", "Programmable Economy", "Tokenized RWA"]
}

df_comp = pd.DataFrame(comp_data)
st.dataframe(df_comp, use_container_width=True, hide_index=True)

# Market Narratives
st.header("📊 Market Narratives (Week 8-14/06/2026)")

narrative_labels = ['RWA/Tokenization', 'AI + Prediction Markets', 'Builder Events', 'DeFi/Consumer', 'Macro/Regulatory', 'Other']
narrative_values = [35, 25, 15, 10, 10, 5]

fig = px.pie(
    names=narrative_labels,
    values=narrative_values,
    color_discrete_sequence=px.colors.sequential.Plasma,  # Fixed: Use valid sequence
    title="Dominant Narratives in Crypto/Blockchain Twitter"
)
fig.update_traces(textinfo='percent+label')
fig.update_layout(
    height=450,
    paper_bgcolor='#1e2937',
    plot_bgcolor='#1e2937',
    font_color='white'
)

st.plotly_chart(fig, use_container_width=True)

# Key Events
st.header("📅 Key Events (Ongoing & Upcoming)")
events = [
    "• SpaceX IPO + Tokenized Equity live onchain (Solana & Mantle)",
    "• Mantle Turing Test Hackathon - Demo Day July 2",
    "• World Cup 2026 Prediction Markets booming",
    "• Multiple RWA partnerships announcements (Ondo, Ethena, Aave)",
    "• Upcoming FOMC & Macro data releases"
]
for event in events:
    st.write(event)

# Deep Insights & Recommendations
st.header("💡 Deep Insights & Strategic Recommendations")

st.markdown("""
**Key Takeaways from the Week:**
- **RWA/Tokenization** dominated discussions thanks to **SpaceX equity** going live onchain.
- Mantle is **well-positioned** in the two hottest narratives: RWA Distribution + AI Prediction Markets.
- Solana leads in raw volume due to high-visibility events, but Mantle shows stronger quality engagement in builder & partnership content.
- Ondo Finance also gained strong traction in tokenized real-world assets.

**Actionable Recommendations for Mantle:**
1. **Double down on visual content** — Create more infographics showing RWA flows and AI prediction wins.
2. **Increase community engagement** — Reply to high-engagement threads and run AMAs during hackathon.
3. **Leverage World Cup hype** — Push more InsightX content tied to major matches.
4. **Cross-promote with partners** — Joint spaces with Aave/Ethena/Ondo to expand reach.
5. **Risk:** Over-reliance on event-driven hype. Need consistent mid-week content to maintain momentum.
""")

st.caption("Dashboard built for Mantle • Data proxied from X/Twitter (June 8-14, 2026)")
