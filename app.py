import streamlit as st
import google.generativeai as genai

st.title("AI接続テスト（成功するか？）")

# サイドバーでAPIキー入力
key = st.sidebar.text_input("API Keyを貼り付け", type="password")

if key:
    try:
        genai.configure(api_key=key)
        # 最も古い、しかし最も安定しているモデル名を指定
        model = genai.GenerativeModel('gemini-pro')
        
        if st.button("テスト実行"):
            response = model.generate_content("「こんにちは」と返事して")
            st.success("成功しました！")
            st.write("AIからの返事:", response.text)
            
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
else:
    st.info("サイドバーにキーを入れてください")
