import streamlit as st
import google.generativeai as genai
import pandas as pd

st.set_page_config(page_title="爆速銘柄スキャナー", layout="wide")
st.title("⚡️ 10分完了：プロフェッショナル・スクリーニング")

# サイドバー：設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Key", type="password")
    sheet_url = st.text_input("GoogleシートのCSV変換URLを入力")
    if api_key:
        genai.configure(api_key=api_key)

if st.button("シートから最新決算を分析"):
    if not api_key or not sheet_url:
        st.warning("APIキーとシートURLの両方を入力してください。")
    else:
        try:
            # 1. スプレッドシート読み込み
            df = pd.read_csv(sheet_url)
            st.write("取得データ（プレビュー）:", df.head(3))
            raw_text = df.to_string()

            # 2. モデル自動取得
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            model = genai.GenerativeModel(available_models[0])

            # 3. プロフェッショナル・プロンプト（いびつな銘柄を排除）
            prompt = f"""
あなたは保守的かつ鋭い目を持つプロの証券アナリストです。
コピペされた未整理データから、単なる「数字の跳ね」ではない、真に投資価値のある銘柄を厳選してください。

【排除すべき「いびつな」銘柄（これらは除外）】
1. 前期が極端な赤字だったための「見せかけの高増益率」銘柄。
2. 本業以外の利益（特別利益）で数字が良くなっているだけの銘柄。
3. 出来高が極端に少なく、株価形成が不自然な銘柄。

【厳選の評価軸】
1. 本業の稼ぐ力（営業利益）が伴っているか。
2. 通期計画に対する進捗率が健全かつ高いか。
3. 一過性の要因ではない持続的な成長性があるか。

【出力フォーマット】
■ 銘柄(コード)
■ アナリスト評価：【S：最優先】or【A：有力】
■ 厳選理由：(なぜ「いびつ」ではなく「本物」と判断したか)
■ 数値の質：(本業の利益率や進捗の健全性について)
■ 注意リスク：(あえて懸念点を1つ挙げる)

【対象データ】
{raw_text}
"""

            with st.spinner("プロの視点で精査中..."):
                response = model.generate_content(prompt)
                st.success("分析完了！")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
