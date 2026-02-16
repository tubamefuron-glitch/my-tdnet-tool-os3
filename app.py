import streamlit as st
import urllib.parse

st.set_page_config(page_title="TDnet 検索ポータル", layout="centered")
st.title("🎯 TDnet 爆速検索ショートカット")

keywords = ["増産", "上方修正", "最高益", "増配", "初配", "復配", "中期経営計画"]

st.write("気になるワードを押すと、24時間以内のTDnet PDFをGoogleが直撃します。")

for kw in keywords:
    query = f'"{kw}" TDnet filetype:pdf'
    url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbs=qdr:d"
    
    st.markdown(f"""
        <a href="{url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #f0f2f6; color: #31333F; padding: 10px; margin: 5px; border-radius: 5px; border: 1px solid #d1d1d1; text-align: center; font-weight: bold; display: inline-block; width: 140px;">
                {kw}
            </div>
        </a>
    """, unsafe_allow_html=True)

st.markdown("---")
custom_kw = st.text_input("自由なキーワードで検索", value="")
if custom_kw:
    q = f'"{custom_kw}" TDnet filetype:pdf'
    u = f"https://www.google.com/search?q={urllib.parse.quote(q)}&tbs=qdr:d"
    st.link_button(f"「{custom_kw}」でPDF検索", u)
