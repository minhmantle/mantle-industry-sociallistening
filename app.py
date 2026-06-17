import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import time

st.set_page_config(
    page_title="Mantle X Dashboard",
    page_icon="📊",
    layout="wide"
)

# ─── Load token từ Streamlit Secrets ───────────────────────────────────────────
def get_token():
    try:
        return st.secrets["APIFY_TOKEN"]
    except Exception:
        return None

APIFY_TOKEN = get_token()

# ─── Fetch data từ Apify ────────────────────────────────────────────────────────
def fetch_data(token: str, max_items: int):
    run_url = "https://api.apify.com/v2/acts/apidojo~tweet-scraper/runs"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "twitterHandles": ["Mantle_Official"],
        "maxItems": max_items,
        "sort": "Latest"
    }

    try:
        # Khởi chạy scraper
        resp = requests.post(run_url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        run_data = resp.json().get("data", {})
        run_id = run_data.get("id")
        if not run_id:
            st.error("Không lấy được run ID từ Apify.")
            return None

        # Poll trạng thái run
        status_url = f"https://api.apify.com/v2/actor-runs/{run_id}"
        progress = st.progress(0, text="⏳ Đang chạy scraper...")

        for attempt in range(45):
            time.sleep(2)
            s_resp = requests.get(status_url, headers=headers, timeout=15)
            if s_resp.status_code != 200:
                continue
            status = s_resp.json().get("data", {}).get("status", "")
            pct = min(int((attempt / 45) * 90), 90)
            progress.progress(pct, text=f"⏳ Trạng thái: {status} ({attempt * 2}s)")

            if status == "SUCCEEDED":
                progress.progress(95, text="✅ Scrape xong, đang lấy data...")
                break
            elif status in ("FAILED", "ABORTED", "TIMED-OUT"):
                progress.empty()
                st.error(f"❌ Run thất bại: {status}")
                return None
        else:
            progress.empty()
            st.error("⏰ Timeout — thử lại hoặc giảm số posts.")
            return None

        # Lấy dataset
        dataset_url = f"https://api.apify.com/v2/actor-runs/{run_id}/dataset/items"
        d_resp = requests.get(dataset_url, headers=headers, timeout=30)
        d_resp.raise_for_status()
        items = d_resp.json()
        progress.progress(100, text="🎉 Hoàn tất!")
        time.sleep(0.5)
        progress.empty()

        if not items:
            st.warning("Không có data. Thử tăng số posts.")
            return None

        # Parse profile từ item đầu tiên
        profile = {}
        first_user = items[0].get("author") or items[0].get("user") or {}
        profile = {
            "name": first_user.get("name", "Mantle_Official"),
            "username": first_user.get("userName") or first_user.get("screen_name", "Mantle_Official"),
            "followers": first_user.get("followers") or first_user.get("followersCount", 0),
            "following": first_user.get("following") or first_user.get("friendsCount", 0),
            "bio": first_user.get("description", ""),
            "verified": first_user.get("isBlueVerified") or first_user.get("verified", False),
        }

        # Parse tweets
        tweets = []
        for t in items:
            if not t.get("text") and not t.get("full_text"):
                continue

            # Support cả 2 schema phổ biến của Apify tweet-scraper
            m = t.get("publicMetrics") or {}
            text_raw = t.get("text") or t.get("full_text") or ""
            created = t.get("createdAt") or t.get("created_at") or ""
            tweet_id = t.get("id") or t.get("id_str") or ""

            likes     = m.get("likeCount")     or t.get("likeCount")      or t.get("favorite_count", 0)
            retweets  = m.get("retweetCount")   or t.get("retweetCount")   or t.get("retweet_count", 0)
            replies   = m.get("replyCount")     or t.get("replyCount")     or 0
            quotes    = m.get("quoteCount")     or t.get("quoteCount")     or 0
            impressions = m.get("impressionCount") or t.get("viewCount")   or 0

            tweets.append({
                "created_at": created[:16] if created else "",
                "text": (text_raw[:160] + "…") if len(text_raw) > 160 else text_raw,
                "impressions": int(impressions),
                "likes": int(likes),
                "retweets": int(retweets),
                "replies": int(replies),
                "quotes": int(quotes),
                "engagement": int(likes) + int(retweets) + int(replies) + int(quotes),
                "url": f"https://x.com/Mantle_Official/status/{tweet_id}" if tweet_id else "",
            })

        return {"profile": profile, "tweets": tweets}

    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e.response.status_code} — {e.response.text[:200]}")
    except requests.exceptions.Timeout:
        st.error("Request timeout. Thử lại sau.")
    except Exception as e:
        st.error(f"Lỗi không xác định: {e}")
    return None


# ─── UI ─────────────────────────────────────────────────────────────────────────
st.title("📊 Mantle Network — X Social Dashboard")
st.caption("Powered by Apify • Data realtime từ @Mantle_Official")

# Sidebar
with st.sidebar:
    st.header("⚙️ Config")

    if APIFY_TOKEN:
        st.success("🔑 Token đã được load từ Secrets")
    else:
        st.warning("⚠️ Không tìm thấy APIFY_TOKEN trong Secrets")
        st.info("Xem hướng dẫn setup bên dưới")
        with st.expander("📖 Hướng dẫn setup"):
            st.markdown("""
**Local:**
Tạo file `.streamlit/secrets.toml`:
```toml
APIFY_TOKEN = "apify_api_xxxx"
```

**Streamlit Cloud:**
Settings → Secrets → paste:
```
APIFY_TOKEN = "apify_api_xxxx"
```
""")

    max_items = st.slider("Số posts muốn fetch", 10, 50, 20, step=5)
    st.divider()

    fetch_btn = st.button(
        "🔄 Fetch @Mantle_Official",
        type="primary",
        use_container_width=True,
        disabled=(APIFY_TOKEN is None)
    )

    if fetch_btn:
        result = fetch_data(APIFY_TOKEN, max_items)
        if result and result.get("tweets"):
            st.session_state["profile"] = result["profile"]
            st.session_state["df"] = pd.DataFrame(result["tweets"])
            st.success(f"✅ Lấy được {len(result['tweets'])} posts!")
        elif result:
            st.warning("Fetch xong nhưng không có tweet nào.")

    if "df" in st.session_state:
        df_export = st.session_state["df"]
        st.download_button(
            "⬇️ Export CSV",
            data=df_export.to_csv(index=False).encode("utf-8"),
            file_name="mantle_tweets.csv",
            mime="text/csv",
            use_container_width=True
        )

# ─── Main content ────────────────────────────────────────────────────────────────
if "df" not in st.session_state:
    st.info("👈 Bấm **Fetch** ở sidebar để load data")
    st.stop()

df = st.session_state["df"]
profile = st.session_state.get("profile", {})

# Profile card
col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
total_eng = df["engagement"].sum()
total_imp = df["impressions"].sum() or 1
avg_er = (total_eng / total_imp * 100)

col_p1.metric("👤 Account", f"@{profile.get('username', 'Mantle_Official')}")
col_p2.metric("👥 Followers", f"{profile.get('followers', 0):,}")
col_p3.metric("📝 Posts fetched", len(df))
col_p4.metric("❤️ Total engagement", f"{total_eng:,}")
col_p5.metric("📈 Avg ER", f"{avg_er:.2f}%")

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["📋 Posts", "📈 Charts", "🏆 Top Posts"])

# ── Tab 1: Bảng dữ liệu
with tab1:
    st.dataframe(
        df[["created_at", "text", "impressions", "likes", "retweets", "replies", "quotes", "engagement", "url"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "url": st.column_config.LinkColumn("🔗 Link"),
            "impressions": st.column_config.NumberColumn(format="%d"),
            "engagement": st.column_config.ProgressColumn(
                "Engagement",
                min_value=0,
                max_value=int(df["engagement"].max()) or 1,
                format="%d"
            ),
        }
    )

# ── Tab 2: Charts
with tab2:
    c1, c2 = st.columns(2)

    with c1:
        fig_imp = px.bar(
            df.sort_values("created_at"),
            x="created_at", y="impressions",
            title="Impressions theo post",
            color="impressions",
            color_continuous_scale="Blues"
        )
        fig_imp.update_layout(showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig_imp, use_container_width=True)

    with c2:
        eng_totals = {
            "Likes": df["likes"].sum(),
            "Retweets": df["retweets"].sum(),
            "Replies": df["replies"].sum(),
            "Quotes": df["quotes"].sum(),
        }
        fig_pie = px.pie(
            values=list(eng_totals.values()),
            names=list(eng_totals.keys()),
            title="Phân bổ Engagement",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    fig_eng = px.bar(
        df.sort_values("created_at"),
        x="created_at",
        y=["likes", "retweets", "replies", "quotes"],
        title="Breakdown Engagement theo post",
        barmode="stack"
    )
    st.plotly_chart(fig_eng, use_container_width=True)

# ── Tab 3: Top posts
with tab3:
    st.subheader("🏆 Top 5 posts — Engagement cao nhất")
    top5 = df.nlargest(5, "engagement")[["created_at", "text", "likes", "retweets", "replies", "engagement", "url"]]
    for _, row in top5.iterrows():
        with st.container(border=True):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.caption(row["created_at"])
                st.write(row["text"])
                if row["url"]:
                    st.markdown(f"[🔗 Xem tweet]({row['url']})")
            with col_b:
                st.metric("❤️ Likes", f"{row['likes']:,}")
                st.metric("🔁 RTs", f"{row['retweets']:,}")
                st.metric("💬 Replies", f"{row['replies']:,}")

st.caption("Mantle Squad Dashboard • Data via Apify")
