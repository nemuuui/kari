import streamlit as st
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI要約デモ", page_icon="📝", layout="centered")

# CSSでカード風
st.markdown("""
<style>
.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin-top: 20px;
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

st.title("📝 AI要約ツール")
st.write("文章を入力すると **AIが日本語で要約** してくれます。")

# 入力欄
text = st.text_area("✍️ 入力テキスト", placeholder="ここに文章を入力してください...", height=200)

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

            # カード風表示：st.containerで中身を確実に描画
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.write(summary)  # st.writeを使うことで内容が必ず表示される
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("文章を入力してください。")