import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="爆速銘柄スキャナー", layout="wide")
st.title("⚡️ 10分完了：決算自動スクリーニング")

# サイドバー：設定
with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    # スプレッドシートのURL（CSV書き出し用URL）を入力
    sheet_url = st.text_input("GoogleシートのCSV変換URLを入力")
    if api_key:
        genai.configure(api_key=api_key)

if st.button("シートから最新決算を分析"):
    if not api_key or not sheet_url:
        st.warning("APIキーとシートURLを入力してください。")
    else:
        try:
            # 1. スプレッドシートを1秒で読み込み
            df = pd.read_csv(sheet_url)
            st.write("取得したデータ（プレビュー）:", df.head(3))
            
            raw_text = df.to_string() # データをテキスト化

            # 2. AI選別
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0])

            prompt = f"以下の銘柄リストから、株価に好影響を与える『強い材料』がある銘柄を3つ厳選して:\n\n{raw_text}"
            
            with st.spinner("AIが全銘柄を瞬時に精査中..."):
                response = model.generate_content(prompt)
                st.success("スキャン完了！")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"エラー: {e}")
