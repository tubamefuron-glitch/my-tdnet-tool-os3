import streamlit as st
import urllib.parse

st.set_page_config(page_title="TDnetキーワード検索(安定版)", layout="wide")
st.title("🔍 TDnet PDFキーワード横断検索ツール")

st.markdown("""
### ⚠️ TDnet直接アクセス制限への対応
現在、クラウドサーバーからのTDnet直接取得が制限されています。
代わりに、**Googleが解析済みのTDnet内PDFデータを一括検索**する方式で「お宝」を探します。
""")

with st.sidebar:
    st.header("検索設定")
    keyword = st.text_input("検索キーワード", value="増産")
    duration = st.selectbox("期間", ["24時間以内", "1週間以内", "指定なし"], index=0)
    st.info("月曜日の新着を探すなら『24時間以内』が最適です。")

# Google検索用URLを構築
# site:release.tdnet.info でドメイン固定
# filetype:pdf でPDFのみに固定
# tbs=qdr:d で24時間以内に固定
query = f'site:release.tdnet.info "{keyword}" filetype:pdf'
tbs = ""
if duration == "24時間以内": tbs = "&tbs=qdr:d"
elif duration == "1週間以内": tbs = "&tbs=qdr:w"

search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query) + tbs

st.subheader(f"「{keyword}」の検索準備が整いました")

st.markdown(f"""
<div style="background-color: #e1f5fe; padding: 20px; border-radius: 10px; border-left: 5px solid #0288d1;">
    <h4>🚀 月曜夜の「増産」チェック実行</h4>
    <p>Googleのエンジンを使って、TDnetに保存されたPDFの<b>「中身」</b>からキーワードを抜き出します。</p>
    <a href="{search_url}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #0288d1; color: white; padding: 15px; text-align: center; border-radius: 5px; font-size: 20px; font-weight: bold;">
            GoogleでTDnet内の「{keyword}」を今すぐ検索
        </div>
    </a>
</div>
""", unsafe_allow_html=True)

st.write("")
st.warning("※ボタンを押すとGoogleの検索結果が開きます。そこで表示されるPDFが「お宝」です。")
