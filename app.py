import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- ページ設定 ---
st.set_page_config(
    page_title="ロト6 AI予測",
    page_icon="🎲",
    layout="centered"
)

st.markdown("""
<style>
/* ページ全体の背景 */
body {
    background-color: #f7f9fc;
}
/* カード共通スタイル */
.card {
    background-color: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.15);
    margin-bottom: 20px;
    text-align: center;
}
input[type="text"] {
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #ccc;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("🎲 ロト6 AI傾向スコアデモ（完全UI版）")
st.write("過去のロト6当選番号をもとに、入力した数字の傾向スコアを計算し、候補数字を提案します。")

# --- CSV読み込み ---
@st.cache_data
def load_data():
    return pd.read_csv("lotto6_past.csv")
df = load_data()

# --- 過去出現回数 ---
number_counts = pd.Series(np.zeros(43), index=range(1,44))
for i in range(1,7):
    counts = df[f'番号{i}'].value_counts()
    for num, c in counts.items():
        number_counts[num] += c

# --- 特徴量関数 ---
def numbers_to_features(nums):
    feat = np.zeros(43)
    for n in nums:
        if 1 <= n <= 43:
            feat[n-1] = 1
    return feat

# --- ラベル作成 ---
X = np.array([numbers_to_features(row) for row in df[['番号1','番号2','番号3','番号4','番号5','番号6']].values])
y = np.array([sum(number_counts[n] for n in row) for row in df[['番号1','番号2','番号3','番号4','番号5','番号6']].values])

# --- モデル学習 ---
@st.cache_resource
def train_model(X, y):
    model = RandomForestRegressor()
    model.fit(X, y)
    return model
model = train_model(X, y)

# --- 入力カード ---
st.markdown('<div class="card">', unsafe_allow_html=True)
numbers_input = st.text_input("6つの数字をカンマ区切りで入力 (例: 1,5,12,23,34,42)")
calculate_btn = st.button("スコア計算")
st.markdown('</div>', unsafe_allow_html=True)

# --- 計算 ---
if calculate_btn:
    try:
        nums = [int(x.strip()) for x in numbers_input.split(",")]
        if len(nums) != 6:
            st.error("6つの数字を入力してください")
        else:
            # スコア予測
            raw_score = model.predict([numbers_to_features(nums)])[0]
            max_score = max(y)
            percent_score = (raw_score / max_score) * 100

            # スコアカード
            st.markdown(
                f"""
                <div class="card" style="background-color:#f0f8ff;">
                    <h3>入力数字の傾向スコア</h3>
                    <p style="font-size:28px; font-weight:bold; color:#ff4500;">{percent_score:.2f}%</p>
                </div>
                """, unsafe_allow_html=True
            )

            # 候補数字カード
            probs = number_counts / number_counts.sum()
            candidate_numbers = np.random.choice(probs.index, size=6, replace=False, p=probs.values)
            st.markdown(
                f"""
                <div class="card" style="background-color:#e6ffe6;">
                    <h3>傾向上位候補番号</h3>
                    <p style="font-size:22px; font-weight:bold;">{sorted(candidate_numbers)}</p>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.error("数字の形式が正しくありません")
