import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mantle Social Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("🧿 Mantle Social Dashboard")
st.markdown(f"**Week 8-14 June 2026** • @Mantle_Official • X/Twitter Analytics • Updated: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Sidebar
with st.sidebar:
    st.header("Dashboard Controls")
    week = st.text_input("Tuần báo cáo", value="8-14 June 2026")
    st.info("Dữ liệu được tổng hợp từ X + internal tracking")

# Key Metrics
st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Impressions", "142,800", "↑ 37%")
with col2:
    st.metric("Total Posts", "22", "↑ 5")
with col3:
    st.metric("Avg Engagement/Post", "218", "↑ 12%")
with col4:
    st.metric("Top Narrative", "RWA + AI", "")

st.divider()

# Top 5 Posts
st.subheader("🔥 Top 5 Posts by Impressions")
top_posts_data = [ ... ]  # giữ nguyên data mày có, hoặc tao sẽ giúp update sau

df_posts = pd.DataFrame(top_posts_data)

for _, post in df_posts.iterrows():
    with st.expander(f"#{post['Rank']} - {post['Post']} ({post['Date']}) • {post['Impressions']} views"):
        st.markdown(f"**Summary**: {post['Summary']}")
        st.markdown(f"**Narrative**: {post['Narrative']}")
        st.markdown(f"[🔗 View Post]({post['Link']})")

st.divider()

# Competitor Comparison
st.subheader("⚔️ Competitor Comparison")
comparison_data = { ... }  # giữ nguyên
df_comp = pd.DataFrame(comparison_data)
st.dataframe(df_comp, use_container_width=True, hide_index=True)

st.divider()

# Narrative Pie
st.subheader("📊 Market Narratives Distribution")
narrative_labels = ['RWA/Tokenization', 'AI + Prediction Markets', 'Builder/Ecosystem', 'DeFi/Consumer Apps', 'Macro/Regulatory', 'Other']
narrative_values = [38, 24, 16, 12, 7, 3]

fig = px.pie(names=narrative_labels, values=narrative_values, hole=0.4, 
             color_discrete_sequence=px.colors.sequential.Plasma)
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)

# Key Events + Insights
st.subheader("📅 Key Events & Insights")
# ... (giữ nguyên phần events và recommendations của mày)

st.caption("Dashboard built for Mantle Squad • Grok + Minh Anh")
