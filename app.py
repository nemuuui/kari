import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# --- ページ設定 ---
st.set_page_config(
    page_title="ロト6 AI傾向デモ",
    page_icon="🎲",
    layout="centered"
)

st.title("🎲 ロト6 AI傾向スコアデモ")
st.write("""
過去のロト6当選番号をもとに、入力した数字の傾向スコアを計算し、  
傾向上位の候補数字を提案します。  
⚠️ 実際の当選確率ではありません。遊び・デモ用です。
""")

# --- CSV読み込み ---
@st.cache_data
def load_data():
    df = pd.read_csv("loto6_past.csv")
    return df

df = load_data()

# --- 特徴量作成関数 ---
def numbers_to_features(nums):
    feat = np.zeros(43)
    for n in nums:
        if 1 <= n <= 43:
            feat[n-1] = 1
    return feat

# --- デモ用モデル学習 ---
@st.cache_resource
def train_model(df):
    X = np.array([numbers_to_features(row) for row in df[['番号1','番号2','番号3','番号4','番号5','番号6']].values])
    y = np.ones(len(X))  # デモ用、全て1
    model = RandomForestRegressor()
    model.fit(X, y)
    return model

model = train_model(df)

# --- 入力 ---
numbers_input = st.text_input("6つの数字をカンマ区切りで入力 (例: 1,5,12,23,34,42)")

# --- ボタン押下で計算 ---
if st.button("スコア計算"):
    try:
        nums = [int(x.strip()) for x in numbers_input.split(",")]
        if len(nums) != 6:
            st.error("6つの数字を入力してください")
        else:
            # AIモデルで傾向スコア計算
            score = model.predict([numbers_to_features(nums)])[0]

            # 過去出現回数ベースの候補数字生成
            number_counts = pd.Series(np.zeros(43), index=range(1,44))
            for i in range(1,7):
                counts = df[f'番号{i}'].value_counts()
                for num, c in counts.items():
                    number_counts[num] += c
            # 出現回数を正規化して確率に
            probs = number_counts / number_counts.sum()
            candidate_numbers = np.random.choice(probs.index, size=6, replace=False, p=probs.values)

            # 結果表示
            st.success(f"入力した数字の傾向スコア: {score:.2%}")
            st.info(f"傾向上位候補番号（過去出現傾向ベース）: {sorted(candidate_numbers)}")
    except:
        st.error("数字の形式が正しくありません")