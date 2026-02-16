import streamlit as st
import google.generativeai as genai

st.title("Gemini 最終診断ツール")

key = st.sidebar.text_input("API Keyを貼り付け", type="password")

if key:
    try:
        genai.configure(api_key=key)
        
        # 1. あなたのキーが認識しているモデルを全部リストアップ
        models = [m.name for m in genai.list_models()]
        
        if not models:
            st.error("⚠️ 致命的なエラー: このキーで利用可能なモデルが1つもありません。Google AI Studioで新しいキーを作成し直してください。")
        else:
            st.success(f"利用可能なモデルが見つかりました: {models}")
            # リストの最初にあるモデルを自動選択
            target_model = models[0] 
            model = genai.GenerativeModel(target_model)
            
            if st.button("このモデルでテスト実行"):
                response = model.generate_content("Hello")
                st.write("AIの返答:", response.text)

    except Exception as e:
        st.error(f"診断エラー: {e}")
        st.info("これが表示される場合、APIキー自体がGoogle側でまだアクティブになっていないか、アカウント制限がかかっています。")
else:
    st.info("サイドバーにキーを入力してください")
