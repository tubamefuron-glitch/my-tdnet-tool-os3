import streamlit as st
import google.generativeai as genai

st.title("Gemini API 接続テスト")

# サイドバーで設定
api_key = st.sidebar.text_input("API Keyを入力", type="password")

if api_key:
    genai.configure(api_key=api_key)
    
    # 3つの主要なモデル名を試せるようにします
    model_choice = st.selectbox("モデル名を選択してテスト", [
        "gemini-1.5-flash", 
        "gemini-1.5-flash-latest",
        "gemini-1.5-pro"
    ])

    test_text = st.text_input("テストメッセージ", value="こんにちは！")

    if st.button("AIに送信"):
        try:
            model = genai.GenerativeModel(model_choice)
            response = model.generate_content(test_text)
            st.success(f"成功しました！ モデル: {model_choice}")
            st.write("AIの返答:", response.text)
        except Exception as e:
            st.error(f"エラー（{model_choice}）: {e}")
else:
    st.warning("左側のサイドバーにAPIキーを入力してください。")
