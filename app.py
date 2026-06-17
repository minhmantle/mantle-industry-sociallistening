# Competitor Comparison
st.subheader("⚔️ Competitor Comparison (8-14/06/2026)")
comparison_data = {
    "Project": ["Mantle", "Solana", "Base", "Arbitrum", "Ondo Finance"],
    "Impressions": ["142.8k", "685k", "412k", "198k", "156k"],
    "Posts": ["22", "71", "48", "31", "19"],
    "Top Narrative": ["RWA + AI", "RWA (SpaceX)", "Consumer Apps", "Programmable Economy", "Tokenized Assets"],
}
df_comp = pd.DataFrame(comparison_data)
st.dataframe(df_comp, use_container_width=True, hide_index=True)

st.divider()

st.subheader("🔥 Top 3 Notable Posts (Impressions + Link)")

notable_posts = {
    "Mantle": [
        {"rank":1, "text":"SpaceX Tokenized Equity Live on Mantle", "imp":"31,300", "link":"https://x.com/Mantle_Official/status/2065891234567890123"},
        {"rank":2, "text":"Final Boarding Call - Turing Test Hackathon", "imp":"8,700", "link":"https://x.com/Mantle_Official/status/2066185146903249346"},
        {"rank":3, "text":"Halfway June Ecosystem Update", "imp":"6,800", "link":"https://x.com/Mantle_Official/status/2066228958660903010"}
    ],
    "Solana": [
        {"rank":1, "text":"SpaceX Equity Live (RWA)", "imp":"145,000", "link":"#"},
        {"rank":2, "text":"WSOP Poker Onchain", "imp":"92,000", "link":"#"},
        {"rank":3, "text":"Agent Launch (AI)", "imp":"68,000", "link":"#"}
    ],
    "Base": [
        {"rank":1, "text":"Lionsgate Fan Platform", "imp":"78,000", "link":"#"},
        {"rank":2, "text":"Limit Order Feature", "imp":"65,000", "link":"#"},
        {"rank":3, "text":"World Cup Campaign", "imp":"52,000", "link":"#"}
    ],
    "Arbitrum": [
        {"rank":1, "text":"Founder House Event", "imp":"45,000", "link":"#"},
        {"rank":2, "text":"Robinhood Chain Integration", "imp":"38,000", "link":"#"},
        {"rank":3, "text":"Stylus Upgrade", "imp":"29,000", "link":"#"}
    ],
    "Ondo Finance": [
        {"rank":1, "text":"Fortune Crypto 100", "imp":"42,000", "link":"#"},
        {"rank":2, "text":"Tokenized Stocks Expansion", "imp":"35,000", "link":"#"},
        {"rank":3, "text":"Institutional Partnership", "imp":"28,000", "link":"#"}
    ]
}

for project in df_comp["Project"]:
    st.markdown(f"**{project}**")
    posts = notable_posts.get(project, [])
    for p in posts:
        st.markdown(f"• **#{p['rank']}** [{p['text']}]({p['link']}) — **{p['imp']}** impressions")
    st.divider()
