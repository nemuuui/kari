# AI要約ツール（Streamlit + OpenAI）

## 概要
文章を入力するとAIが短く要約してくれるWebアプリです。  
パスワードを知っている人だけが利用できます。

## 使い方
1. このリポジトリを [Streamlit Community Cloud](https://streamlit.io/cloud) にデプロイ
2. Secretsに以下を設定  
   - `OPENAI_API_KEY=sk-xxxx`  
   - `APP_PASSWORD=任意のパスワード`  
3. 発行されたURLを仲間に共有してください