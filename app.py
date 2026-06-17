import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime

st.set_page_config(page_title="Mantle X Dashboard", layout="wide")
st.title("📊 Mantle Network X Social Dashboard")
st.caption("Auto via Apify • Mantle Squad Live Dashboard")

with st.sidebar:
    st.header("🔑 Apify Config")
    apify_token = st.text_input("Apify API Token", type="password", help="Lấy tại console.apify.com → Integrations")
    max_items = st.slider("Số posts gần nhất", 10, 50, 20)
    
    if st.button("🔄 Fetch Fresh Data", type="primary", use_container_width=True):
        if apify_token:
            with st.spinner("Đang scrape @Mantle_Official từ Apify..."):
                result = fetch_data(apify_token, max_items)
                if result:
                    st.session_state.user = result['profile']
                    st.session_state.df = pd.DataFrame(result['tweets'])
                    st.success("✅ Cập nhật thành công!")
        else:
            st.error("Nhập Apify Token trước")

def fetch_data(token, max_items):
    url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "twitterHandles": ["Mantle_Official"],
        "maxItems": max_items,
        "sort": "Latest"
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
        run_id = resp.json()["data"]["id"]
        
        dataset_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs/{run_id}/dataset/items"
        items = requests.get(dataset_url, headers=headers).json()
        
        profile = items[0].get("user", {}) if items else {}
        
        tweets = []
        for t in items:
            if "text" not in t: continue
            m = t.get("publicMetrics", {})
            tweets.append({
                "created_at": t.get("createdAt"),
                "text": t.get("text", "")[:180] + ("..." if len(t.get("text","")) > 180 else ""),
                "impressions": m.get("impressionCount", 0),
                "likes": m.get("likeCount", 0),
                "retweets": m.get("retweetCount", 0),
                "replies": m.get("replyCount", 0),
                "quotes": m.get("quoteCount", 0),
                "post_url": f"https://x.com/Mantle_Official/status/{t.get('id')}"
            })
        return {"profile": profile, "tweets": tweets}
    except Exception as e:
        st.error(f"Lỗi: {str(e)}")
        return None

# Hiển thị dữ liệu
if "df" in st.session_state:
    df = st.session_state.df
    user = st.session_state.user
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Followers", f"{user.get('followers', 'N/A'):,}")
    col2.metric("Posts in view", len(df))
    col3.metric("Avg ER", f"{(df['likes']+df['retweets']+df['replies']+df['quotes']).sum() / df['impressions'].sum() * 100 if df['impressions'].sum() > 0 else 0 :.2f}%")
    
    tab1, tab2 = st.tabs(["📋 Posts Table", "📈 Charts"])
    
    with tab1:
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        fig = px.bar(df, x="created_at", y="impressions", title="Impressions per Post")
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Nhập Apify Token bên trái và bấm Fetch Fresh Data")

st.caption("Live Dashboard cho Mantle Squad • Dùng chung thoải mái")
