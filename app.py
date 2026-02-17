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

          # --- プロフェッショナル版に差し替え ---
            prompt = f"""
            あなたは保守的かつ鋭い目を持つプロの証券アナリストです。
            コピペされた未整理データから、単なる「数字の跳ね」ではない、真に投資価値のある銘柄を厳選してください。

            【排除すべき「いびつな」銘柄（これらは除外して）】
            1. 前期が極端な赤字だったための「見せかけの高増益率」銘柄。
            2. 本業以外の利益（特別利益）で数字が良くなっているだけの銘柄。
            3. 出来高が極端に少なく、株価形成が不自然な銘柄。

            【厳選の評価軸（これらを重視）】
            1. **本業の稼ぐ力**: 営業利益がしっかりと伴っているか。
            2. **進捗の信憑性**: 季節性を考慮しても通期計画に対して妥当、かつ高い進捗か。
            3. **増配の背景**: 利益成長に伴う還元姿勢が見られるか。
            4. **テーマ性**: 時流（DX, 省力化, 独自の強み）に合致しているか。

            【出力フォーマット】
            ■ 銘柄(コード)
            ■ アナリスト評価：【S：最優先】or【A：有力】
            ■ 厳選理由：(なぜ「いびつ」ではなく「本物」と判断したか)
            ■ 数値の質：(本業の利益率や進捗の健全性について)
            ■ 注意リスク：(あえて懸念点を1つ挙げる)

            【対象データ】
            {raw_text}
            """
            
            with st.spinner("データの『質』を精査中..."):
                response = model.generate_content(prompt)
                st.success("プロフェッショナル分析完了！")
                st.markdown(response.text)
            # --- ここまで差し替え ---
            """
            
            with st.spinner("AIが全銘柄を瞬時に精査中..."):
                response = model.generate_content(prompt)
                st.success("スキャン完了！")
                st.markdown(response.text)
            # --- ここまで貼り替え ---
                
        except Exception as e:
            st.error(f"エラー: {e}")
