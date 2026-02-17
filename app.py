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

           # --- ここから貼り替え ---
            prompt = f"""
            あなたはプロの証券アナリストです。
            以下は決算サイトから丸ごとコピー＆ペーストされた未整理のデータです。
            不要な文字が多く含まれていますが、その中から「銘柄名」「コード」「決算数値」を正確に抽出し、
            株価に強いポジティブな影響を与える銘柄を最大3つ厳選してください。

            【選別基準】
            ・「大幅増益」「過去最高益」「黒字浮上」「上方修正」「増配」「自社株買い」
            ・進捗率が極めて高いもの（1Qで35%超など）

            【出力フォーマット】
            ■ 銘柄(コード)
            ■ 判定：【特選】
            ■ ポジティブ材料：(なぜ良いのか、数字を交えて解説)
            ■ AIのアドバイス：(今後の注目点)

            【対象データ】
            {raw_text}
            """
            
            with st.spinner("AIが全銘柄を瞬時に精査中..."):
                response = model.generate_content(prompt)
                st.success("スキャン完了！")
                st.markdown(response.text)
            # --- ここまで貼り替え ---
                
        except Exception as e:
            st.error(f"エラー: {e}")
