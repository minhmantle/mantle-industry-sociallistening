import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import time

st.set_page_config(page_title="Mantle X Dashboard", layout="wide")
st.title("📊 Mantle Network X Social Dashboard")
st.caption("Auto via Apify • Live cho Mantle Squad")

def fetch_data(token, max_items):
    url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "twitterHandles": ["Mantle_Official"],
        "maxItems": max_items,
        "sort": "Latest"
    }
    
    try:
        # Start the run
        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        run_id = resp.json()["data"]["id"]
        st.info(f"✅ Run started: {run_id}. Đang chờ Apify scrape...")

        # Poll until run is finished
        status_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs/{run_id}"
        for i in range(30):  # max 60 giây
            time.sleep(2)
            status_resp = requests.get(status_url, headers=headers)
            status_data = status_resp.json()["data"]
            status = status_data.get("status")
            
            if status == "SUCCEEDED":
                st.success("✅ Scrape hoàn tất!")
                break
            elif status in ["FAILED", "ABORTED", "TIMED_OUT"]:
                st.error(f"❌ Run failed với status: {status}")
                return None
        else:
            st.warning("⏳ Timeout, thử lại sau.")
            return None

        # Get dataset
        dataset_url = f"https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs/{run_id}/dataset/items"
        data_resp = requests.get(dataset_url, headers=headers, timeout=60)
        data_resp.raise_for_status()
        items = data_resp.json()
        
        if not items:
            st.warning("Không có dữ liệu tweets nào. Thử tăng maxItems hoặc kiểm tra lại.")
            return None

        profile = items[0].get("user", {}) if items else {}
        
        tweets = []
        for t in items:
            if "text" not in t: continue
            m = t.get("publicMetrics", {})
            tweets.append({
                "created_at": t.get("createdAt")[:16] if t.get("createdAt") else "",
                "text": (t.get("text", "")[:160] + "...") if len(t.get("text", "")) > 160 else t.get("text", ""),
                "impressions": m.get("impressionCount", 0),
                "likes": m.get("likeCount", 0),
                "retweets": m.get("retweetCount", 0),
                "replies": m.get("replyCount", 0),
                "quotes": m.get("quoteCount", 0),
                "post_url": f"https://x.com/Mantle_Official/status/{t.get('id')}"
            })
        
        return {"profile": profile, "tweets": tweets}
        
    except Exception as e:
        st.error(f"❌ Lỗi: {str(e)}")
        return None

# Sidebar
with st.sidebar:
    st.header("🔑 Apify Config")
    apify_token = st.text_input("Apify API Token", type="password")
    max_items = st.slider("Số posts gần nhất", 10, 50, 20)
    
    if st.button("🔄 Fetch Fresh Data (@Mantle_Official)", type="primary", use_container_width=True):
        if apify_token:
            with st.spinner("Đang scrape... (có thể mất 20-60 giây)"):
                result = fetch_data(apify_token, max_items)
                if result and result.get('tweets'):
                    st.session_state.user = result['profile']
                    st.session_state.df = pd.DataFrame(result['tweets'])
                    st.success(f"✅ Lấy thành công {len(result['tweets'])} posts!")
        else:
            st.error("Nhập Apify Token trước")

# Main UI
if "df" in st.session_state:
    df = st.session_state.df
    user = st.session_state.get("user", {})
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Followers", f"{user.get('followers', 'N/A'):,}")
    c2.metric("Posts", len(df))
    
    total_eng = (df['likes'] + df['retweets'] + df['replies'] + df['quotes']).sum()
    total_imp = df['impressions'].sum() or 1
    c3.metric("Avg ER", f"{(total_eng / total_imp * 100):.2f}%")
    
    tab1, tab2 = st.tabs(["📋 Bảng Posts", "📈 Biểu đồ"])
    with tab1:
        st.dataframe(df, use_container_width=True, hide_index=True)
    with tab2:
        fig = px.bar(df, x="created_at", y="impressions", title="Impressions theo Post")
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Nhập Token và bấm Fetch")

st.caption("Mantle Squad Live Dashboard")
