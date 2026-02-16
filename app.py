import streamlit as st
import google.generativeai as genai
import pdfplumber
import io

st.set_page_config(page_title="AI株探風要約ツール", layout="centered")
st.title("📈 AI決算サマリー (株探風)")

# --- 設定：APIキーの入力 ---
# 本来はSecretsに隠すべきですが、まずは動かすためにサイドバーに入力欄を作ります
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Keyを入力してください", type="password")
    if api_key:
        genai.configure(api_key=api_key)

st.info("PDFをアップロードするか、決算短信のテキストを貼り付けてください。")

# --- 入力方法の選択 ---
tab1, tab2 = st.tabs(["PDFアップロード", "テキスト貼り付け"])

def generate_summary(text):
    if not api_key:
        st.error("サイドバーでAPIキーを入力してください。")
        return
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    # 株探風に見せるための「最強の命令文（プロンプト）」
    prompt = f"""
    以下の決算短信の内容を読み取り、日本の投資ニュースサイト「株探（Kabutan）」の見出し風に1行で要約してください。
    
    【ルール】
    ・「社名、結論（増益・黒字浮上など）、具体的な数字」の構成にすること。
    ・ポジティブな要素を強調しつつ、進捗率や配当修正があれば必ず盛り込むこと。
    ・新聞の見出しのように簡潔で読みやすい日本語にすること。

    【解析対象テキスト】
    {text}
    """
    
    with st.spinner("AIが解析中..."):
        response = model.generate_content(prompt)
        st.subheader("📋 AI生成見出し")
        st.success(response.text)

with tab1:
    uploaded_file = st.file_uploader("決算短信のPDFを選択", type="pdf")
    if uploaded_file:
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            # 1ページ目が最も重要なので、1ページ目からテキストを抽出
            text = pdf.pages[0].extract_text()
        
        if st.button("AI要約を実行 (PDF)"):
            generate_summary(text)

with tab2:
    input_text = st.text_area("決算短信のテキストをここにペースト", height=300)
    if st.button("AI要約を実行 (テキスト)"):
        generate_summary(input_text)

st.markdown("---")
st.caption("※このツールはGoogle Gemini APIを使用しています。")
