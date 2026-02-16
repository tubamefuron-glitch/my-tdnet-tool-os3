import streamlit as st
import google.generativeai as genai
import pdfplumber
import io

# 画面設定
st.set_page_config(page_title="AI株探風要約ツール", layout="centered")
st.title("📈 AI決算サマリー (株探風)")

# サイドバー設定
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Keyを入力", type="password")
    if api_key:
        genai.configure(api_key=api_key)

def generate_summary(text):
    if not api_key:
        st.error("左側のサイドバーでAPIキーを入力してください。")
        return
    
    # 【重要】あなたの環境で確実に動く「Gemini 2.5 Flash」を指定
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    
    prompt = f"""
    以下の決算短信を読み取り、投資家に役立つ情報を整理して出力してください。

    【出力形式】
    1. 【見出し】株探風のインパクトある1行要約
    2. 【好材料のポイント】なぜ好調なのか、数字を交えて3項目で箇条書き
    3. 【懸念・注目点】今後のリスクや配当、進捗率などについて1行

    【ルール】
    ・社名と証券コードを必ず含めること。
    ・専門用語を使いつつ、分かりやすく。

    【対象テキスト】
    {text}
    """
    
    with st.spinner("最新AI（Gemini 2.5）が解析中..."):
        try:
            response = model.generate_content(prompt)
            st.subheader("📋 AI生成見出し")
            st.success(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# メイン機能
tab1, tab2 = st.tabs(["PDFアップロード", "テキスト貼り付け"])

with tab1:
    uploaded_file = st.file_uploader("決算短信のPDFを選択", type="pdf")
    if uploaded_file and st.button("AI要約を実行 (PDF)"):
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            # 1ページ目からテキスト抽出
            text = pdf.pages[0].extract_text()
            generate_summary(text)

with tab2:
    input_text = st.text_area("決算短信のテキストをここにペースト", height=300)
    if st.button("AI要約を実行 (テキスト)"):
        generate_summary(input_text)
