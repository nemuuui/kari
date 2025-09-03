import streamlit as st
import pandas as pd

# --- ページ設定 ---
st.set_page_config(
    page_title="ロト6 当選傾向デモ",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 ロト6 当選傾向スコア デモ")
st.write("""
このアプリは過去のロト6当選番号をもとに、入力した数字の出現傾向スコアを計算します。  
⚠️ 実際の当選確率ではありません。遊び・デモ用です。
""")

# --- 過去データ読み込み ---
@st.cache_data
def load_data():
    # CSV例: 回,番号1,番号2,番号3,番号4,番号5,番号6,ボーナス
    # githubやローカルに置いたCSVのパスに置き換えてください
    return pd.read_csv("lotto6_past.csv")

df = load_data()

# --- 入力 ---
numbers = st.text_input("6つの数字をカンマ区切りで入力 (例: 1,5,12,23,34,42)")

# --- スコア計算 ---
if st.button("スコア計算"):
    try:
        nums = [int(x.strip()) for x in numbers.split(",")]
        if len(nums) != 6:
            st.error("6つの数字を入力してください")
        else:
            # 過去の出現回数
            count = sum(df[[f'番号{i}' for i in range(1,7)]].isin(nums).sum())
            total_draws = df.shape[0] * 6  # 6個の番号×回数
            score = count / total_draws  # 過去の出現傾向スコア

            # 偶数・奇数比率
            even_count = sum(1 for n in nums if n % 2 == 0)
            odd_count = 6 - even_count

            # 連番の有無
            sorted_nums = sorted(nums)
            consecutive = any(sorted_nums[i+1] - sorted_nums[i] == 1 for i in range(5))

            # 結果表示
            st.success(f"🔹 過去出現傾向スコア: {score:.2%}")
            st.info(f"🔹 偶数: {even_count}, 奇数: {odd_count}, 連番あり: {'はい' if consecutive else 'いいえ'}")
    except:
        st.error("数字の形式が正しくありません")