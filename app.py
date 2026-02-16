import streamlit as st
import google.generativeai as genai

st.title("Gemini API 最終テスト")

# サイドバーでAPIキー入力
key = st.sidebar.text_input("API Keyを貼り付け", type="password")

if key:
    try:
        # 1. APIキーを設定
        genai.configure(api_key=key)
        
        # 2. モデルの指定方法を「最新の正式名称」に変更
        # v1betaエラーを回避するため、あえて models/ を明記します
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        if st.button("テスト実行"):
            # 3. 実行
            response = model.generate_content("「接続成功です」と短く返事して")
            st.success("🎉 ついに成功しました！")
            st.write("AIからの返事:", response.text)
            
    except Exception as e:
        # 具体的なエラー内容を表示
        st.error(f"エラーが発生しました: {e}")
        st.info("もし404が出る場合は、APIキーが『Google AI Studio』の『無料枠』で作成されているか再確認してください。")
else:
    st.info("サイドバーにキーを入れてください")
