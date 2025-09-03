import streamlit as st
import os
from openai import OpenAI

# APIキー
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PASSWORD = os.getenv("APP_PASSWORD", "demo123")

st.set_page_config(page_title="AI要約デモ", page_icon="🔄", layout="centered")

# タイトル
st.markdown(
    """
    <h1 style="text-align:center; color:#2F4F4F; font-family:Arial, sans-serif;">
        🔄 AI要約ツール
    </h1>
    <p style="text-align:center; color:#555; font-size:16px;">
        文章を入力すると <b>AIが『不思議の国のアリス』に置き換えて要約</b> してくれます。
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
    st.markdown("### 入力テキスト")
    text = st.text_area("", placeholder="ここに文章を入力してください...", height=200)

    # 要約ボタン
    if st.button("要約する"):
        if text.strip():
            with st.spinner("AIが要約中..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "あなたは『不思議の国のアリス』の世界観を使った優秀な要約アシスタントです。登場人物や世界観のイメージで文章を表現してください。"},
                        {"role": "user", "content": f"次の文章を『不思議の国のアリス』の世界観で、必ず日本語で要約してください:\n\n{text}"}
                    ]
                )
                summary = response.choices[0].message.content
                st.markdown("### 要約結果")
                st.info(summary)
        else:
            st.warning("文章を入力してください。")