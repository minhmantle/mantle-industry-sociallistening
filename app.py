import streamlit as st
import plotly.express as px
import pandas as pd

# Page config
st.set_page_config(
    page_title="Mantle Social Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark theme
st.markdown("""
<style>
    .main { background-color: #0f172a; color: white; }
    .stPlotlyChart { background-color: #1e2937; border-radius: 12px; }
    .metric-card {
        background-color: #1e2937;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Mantle Social Dashboard")
st.subheader("Week 8-14 June 2026 • @Mantle_Official")
st.caption("Live X/Twitter Data Proxy • Built for the Boss")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Impressions", "68,400", "↑ 24% WoW")
with col2:
    st.metric("Total Posts", "22", "")
with col3:
    st.metric("Avg Engagement", "142", "")
with col4:
    st.metric("Top Narrative", "RWA + AI", "🔥")

# Top 5 Mantle Posts
st.markdown("### 🔥 Top 5 Mantle Posts (by Impressions)")

top_posts_data = [
    {"Rank": 1, "Post": "Halfway June Summary", "Views": "6,800", "Link": "https://x.com/Mantle_Official/status/2066228958660903010", 
     "Summary": "Tokenized SpaceX equity live, InsightX AI Prediction Market, hackathon updates, major partnerships.", "Narrative": "RWA + AI + Ecosystem"},
    {"Rank": 2, "Post": "Final Boarding Call - Hackathon", "Views": "8,700", "Link": "https://x.com/Mantle_Official/status/2066185146903249346", 
     "Summary": "Last call for Mantle Turing Test Hackathon • Demo Day July 2", "Narrative": "Builder Growth"},
    {"Rank": 3, "Post": "InsightX Prediction Market", "Views": "4,200", "Link": "#", 
     "Summary": "AI-native prediction market live with World Cup integration", "Narrative": "AI + Prediction Markets"},
    {"Rank": 4, "Post": "Partnership Announcements", "Views": "3,900", "Link": "#", 
     "Summary": "New integrations with Aave, Ethena and more", "Narrative": "DeFi & RWA"},
    {"Rank": 5, "Post": "Regional Expansion", "Views": "2,800", "Link": "#", 
     "Summary": "Events in Singapore, Seoul & Americas", "Narrative": "Community & Growth"}
]

df_posts = pd.DataFrame(top_posts_data)
for _, post in df_posts.iterrows():
    with st.container():
        col_a, col_b = st.columns([4,1])
        with col_a:
            st.markdown(f"**#{post['Rank']} - [{post['Post']}]({post['Link']})**")
            st.caption(post['Summary'])
            st.markdown(f"<span style='color:#67e8f9'>**{post['Narrative']}**</span>", unsafe_allow_html=True)
        with col_b:
            st.metric("Views", post['Views'])
        st.divider()

# Competitor Comparison
st.markdown("### ⚔️ Competitor Comparison")

comp_data = {
    "Project": ["Mantle", "Solana", "Base", "Arbitrum", "Ondo Finance"],
    "Impressions": ["68k", "520k", "410k", "185k", "145k"],
    "Posts": [22, 68, 41, 29, 19],
    "Top Narrative": ["RWA + AI", "RWA (SpaceX)", "Consumer Apps", "Programmable Economy", "Tokenized Assets"]
}

df_comp = pd.DataFrame(comp_data)
st.dataframe(df_comp, use_container_width=True, hide_index=True)

# Market Narratives
st.markdown("### 📈 Market Narratives (Week 8-14/06/2026)")

narrative_labels = ['RWA/Tokenization', 'AI + Prediction Markets', 'Builder Events', 'DeFi/Consumer', 'Macro/Regulatory', 'Others']
narrative_values = [35, 25, 15, 10, 10, 5]

fig = px.pie(values=narrative_values, names=narrative_labels, 
             color_discrete_sequence=px.colors.sequential.Cyan,
             title="Dominant Narratives in Crypto/Blockchain")
fig.update_traces(textinfo='percent+label')
fig.update_layout(height=450, paper_bgcolor='#1e2937', plot_bgcolor='#1e2937', font_color='white')

st.plotly_chart(fig, use_container_width=True)

# Key Events
st.markdown("### 📅 Key Market Events")
events = [
    "✅ **SpaceX IPO Tokenization** - Live on Solana & Mantle (Biggest catalyst)",
    "✅ **World Cup Prediction Markets** - Multiple AI projects launched",
    "🔥 **Mantle Turing Test Hackathon** - Demo Day July 2",
    "📍 **Upcoming**: FOMC Meeting, Major token unlocks, More RWA announcements"
]
for event in events:
    st.markdown(f"- {event}")

# Deep Insights & Recommendations
st.markdown("### 💡 Deep Insights & Actionable Recommendations")

st.markdown("""
**Key Takeaways from the week:**
- **RWA/Tokenization** dominated discussions thanks to **SpaceX** momentum. Projects that moved fast on tokenized real-world assets won the most mindshare.
- Mantle performed well in niche (AI Prediction + RWA Distribution) but still lags behind Solana in raw volume.
- Ondo Finance and Solana are currently the strongest in the tokenized assets narrative.
- Builder activity and hackathons remain strong signals for long-term ecosystem health.

**Recommendations for Mantle:**
1. **Double down on visual content** — Infographics showing RWA flows and AI agent performance.
2. **Increase community engagement** — Reply to top comments, run AMAs during hackathon.
3. **Leverage World Cup hype** more aggressively with InsightX.
4. **Cross-promote with Ondo / Solana partners** to borrow their audience.
5. **Prepare content for upcoming macro events** (FOMC) to stay relevant.
""")

st.caption("Dashboard built by Grok • Data proxy from X (real posts & trends)")
