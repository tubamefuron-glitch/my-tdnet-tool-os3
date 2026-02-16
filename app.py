
import streamlit as st
import google.generativeai as genai
import pdfplumber
import io

st.set_page_config(page_title="AI株探風要約ツール", layout="centered")
st.title("📈 AI決算サマリー (株探風)")

# サイドバーにAPIキー入力欄を作成
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Gemini API Keyを入力", type="password")
    if api_key:
        genai.configure(api_key=api_key)

def generate_summary(text):
    if not api_key:
        st.error("左側のサイドバーでAPIキーを入力してください。")
        return
    
   # 修正後
　　model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = f"""
    以下の決算短信の内容を読み取り、株探（Kabutan）の見出し風に1行で要約してください。
    社名、結論、具体的な数字を盛り込み、ポジティブな内容を優先してください。
    
    【対象テキスト】
    {text}
    """
    
    with st.spinner("AIが解析中..."):
        try:
            response = model.generate_content(prompt)
            st.subheader("📋 AI生成見出し")
            st.success(response.text)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")

# メイン画面のタブ
tab1, tab2 = st.tabs(["PDFアップロード", "テキスト貼り付け"])

with tab1:
    uploaded_file = st.file_uploader("決算短信のPDFを選択", type="pdf")
    if uploaded_file and st.button("AI要約を実行 (PDF)"):
        with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
            text = pdf.pages[0].extract_text()
            generate_summary(text)

with tab2:
    input_text = st.text_area("テキストをペースト", height=200)
    if st.button("AI要約を実行 (テキスト)"):
        generate_summary(input_text)
