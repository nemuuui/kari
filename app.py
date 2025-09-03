import streamlit as st
import os
from openai import OpenAI

# APIキー
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PASSWORD = os.getenv("APP_PASSWORD", "demo123")

st.set_page_config(page_title="AI要約デモ", page_icon="📝", layout="centered")

# CSSで背景・カード・余白を調整
st.markdown("""
<style>
body {
    background-color: #f5f5f5;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 5%;
    padding-right: 5%;
}
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
div.stButton > button:first-child {
    background-color: #2F4F4F;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    padding: 0.5em 1em;
}
</style>
""", unsafe_allow_html=True)

# タイトル
st.markdown(
    """
    <h1 style="text-align:center; color:#2F4F4F; font-family:Arial, sans-serif;">
        📝 AI要約ツール
    </h1>
    <p style="text-align:center; color:#555; font-size:16px;">
        文章を入力すると <b>AIが日本語で要約</b> してくれます。
    </p>
    """,
    unsafe_allow_html=True
)

# 認証
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    pwd = st.text_input("パスワードを入力してください", type="password", max_chars=20)
    if st.button("ログイン"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.success("ログイン成功！")
        else:
            st.error("パスワードが違います")
else:
    # 入力カード
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### ✍️ 入力テキスト")
    text = st.text_area("", placeholder="ここに文章をペーストしてください...", height=200)
    st.markdown('</div>', unsafe_allow_html=True)

    # 要約ボタン
    if st.button("🚀 要約する"):
        if text.strip():
            with st.spinner("AIが要約中..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "あなたは優秀な要約アシスタントです。"},
                        {"role": "user", "content": f"次の文章を必ず日本語で短く要約してください:\n\n{text}"}
                    ]
                )
                summary = response.choices[0].message.content

                # 結果カード
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("### ✨ 要約結果")
                st.info(summary)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("文章を入力してください。")