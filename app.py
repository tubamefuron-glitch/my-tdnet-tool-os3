import streamlit as st
import google.generativeai as genai
import pdfplumber
import io

# 画面の設定
st.set_page_config(page_title="AI株探風要約ツール", layout="centered")
st.title("📈 AI決算サマリー (株探風)")

# サイドバーにAPIキー入力欄を作成
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Keyを入力", type="password")
    if api_key:
        # APIキーの設定
        genai.configure(api_key=api_key)

def generate_summary(text):
    if not api_key:
        st.error("左側のサイドバーでAPIキーを入力してください。")
        return
    
    # モデルの指定（最新の安定版）
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    # 株探風のプロンプト
    prompt = f"""
    以下の決算短信の内容を読み取り、日本の投資ニュースサイト「株探（Kabutan）」の見出し風に1行で要約してください。
    
    【ルール】
    ・「社名、結論（増益・黒字浮上など）、具体的な数字」の構成にすること。
    ・ポジティブな要素を強調しつつ、進捗率や配当修正があれば盛り込むこと。
    ・簡潔で読みやすい日本語にすること。

    【対象テキスト】
    {text}
    """
    
    with st.spinner("AIが解析中..."):
        try:
            # AIに生成を依頼
            response = model.generate_content(prompt)
            st.subheader("📋 AI生成見出し")
            st.success(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# メイン画面の操作部分
tab1, tab2 = st.tabs(["PDFアップロード", "テキスト貼り付け"])

with tab1:
    uploaded_file = st.file_uploader("決算短信のPDFを選択", type="pdf")
    if uploaded_file and st.button("AI要約を実行 (PDF)"):
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            # 1ページ目からテキストを抽出
            text = pdf.pages[0].extract_text()
            generate_summary(text)

with tab2:
    input_text = st.text_area("決算短信のテキストをここにペースト", height=300)
    if st.button("AI要約を実行 (テキスト)"):
        generate_summary(input_text)

st.markdown("---")
st.caption("※このツールはGoogle Gemini APIを使用しています。")
