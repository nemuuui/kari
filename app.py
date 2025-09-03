import streamlit as st
import os
from openai import OpenAI

# OpenAI APIクライアント
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# パスワード（環境変数から取得。未設定なら "kari123"）
PASSWORD = os.getenv("APP_PASSWORD", "kari123")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 AI要約ツール")
    pwd = st.text_input("パスワードを入力してください", type="password")
    if st.button("ログイン"):
        if pwd == PASSWORD:
            st.session_state.authenticated = True
            st.success("ログイン成功！")
        else:
            st.error("パスワードが違います")
else:
    st.title("📝 AI要約ツール（デモ版）")

    text = st.text_area("要約したい文章を入力してください:")

    if st.button("要約する"):
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
                st.subheader("要約結果（日本語）")
                st.write(summary)
        else:
            st.warning("文章を入力してください。")
