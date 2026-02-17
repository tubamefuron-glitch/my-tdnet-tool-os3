import streamlit as st
import google.generativeai as genai

# 画面設定
st.set_page_config(page_title="IR Bank選別アナリスト", layout="wide")
st.title("🎯 IR Bank 爆速スクリーニング")
st.caption("IR Bankの『決算速報』や『一覧』をガバッとコピペしてください")

# サイドバー：APIキー設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# AI選別ロジック
def analyze_summary(raw_text):
    if not api_key:
        st.error("APIキーを入力してください。")
        return

    try:
        # 404エラー回避のため、モデルを自動取得
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])

        prompt = f"""
        あなたはプロの証券アナリストです。
        以下のIR Bank等からコピーされた決算データ群を読み、
        「株価に強いポジティブな影響を与えるキーワード」が含まれる銘柄を厳選して報告してください。

        【選別基準】
        ・増益率が高い、黒字浮上、過去最高益、大幅な上方修正、増配。
        ・「進捗率が極めて高い」「自社株買い発表」なども重視。

        【出力形式】
        1. 【期待度：特大】銘柄名(コード) / 理由 / 主要な数字
        2. 【期待度：大】銘柄名(コード) / 理由 / 主要な数字

        【対象データ】
        {raw_text}
        """

        with st.spinner("AIが銘柄を厳選中..."):
            response = model.generate_content(prompt)
            st.success("分析完了！")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"解析エラー: {e}")

# メインUI
st.info("💡 手順：IR Bankの『決算速報』などのページで、複数社分のテキストをマウスでバーっと選択してコピーし、下に貼り付けてください。")
input_data = st.text_area("ここにまとめてペースト（数件〜数十件分OK）", height=400)

if st.button("銘柄を選別する"):
    if input_data:
        analyze_summary(input_data)
    else:
        st.warning("データを貼り付けてください。")
