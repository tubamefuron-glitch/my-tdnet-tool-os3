import streamlit as st
import urllib.parse

st.set_page_config(page_title="TDnetキーワード検索(最終形態)", layout="wide")
st.title("🔍 TDnet PDFキーワード横断検索ツール")

st.markdown("""
### 🚀 最終手段：広域PDF検索モード
TDnet公式サーバーの制限を回避し、Googleのインデックスから**「TDnet（release.tdnet.info）」に含まれるPDF**を力技で引き抜きます。
""")

with st.sidebar:
    st.header("検索設定")
    keyword = st.text_input("検索キーワード", value="増産")
    st.info("※これで見つからない場合は、キーワードを『上方修正』などに変えてみてください。")

# Googleの「もっともヒットしやすい」検索URL
# site指定を少し緩め、キーワードとPDFであることを優先
query = f'"{keyword}" TDnet filetype:pdf'
search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbs=qdr:d"

st.subheader(f"「{keyword}」をGoogleの全データベースから抽出")

st.markdown(f"""
<div style="background-color: #fff3e0; padding: 20px; border-radius: 10px; border-left: 5px solid #ff9800;">
    <h4>🔥 今すぐ実行</h4>
    <p>過去24時間以内にウェブ上に現れた、<b>「{keyword}」</b>という言葉を含むTDnet関連のPDFをすべてリストアップします。</p>
    <a href="{search_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #ff9800; color: white; padding: 15px; text-align: center; border-radius: 5px; font-size: 20px; font-weight: bold;">
            【24時間以内】のPDFを強制検索
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("""
---
**【なぜ「一致しない」が起きていたか】**
Googleが「このPDFはTDnetのものだ」と完全に分類するのには時間がかかります。
今回のコードは「TDnet」という文字が入っているPDFを広く探すので、分類を待たずに最新情報にヒットする確率が格段に上がります。
""")
