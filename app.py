import streamlit as st
import google.generativeai as genai
import requests
import xml.etree.ElementTree as ET

# 画面設定
st.set_page_config(page_title="自動決算スキャナー", layout="wide")
st.title("📡 最新決算・爆速自動検知")
st.caption("TDnetの最新開示を自動取得し、AIが『お宝銘柄』を判定します")

# サイドバー設定
with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# TDnet RSSから最新情報を取得する関数
def fetch_tdnet_latest():
    # TDnetの最新開示RSS（公式）
    RSS_URL = "https://www.release.tdnet.info/inbs/if_p001.rss"
    try:
        response = requests.get(RSS_URL)
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            items.append({"title": title, "link": link})
        return items
    except Exception as e:
        st.error(f"RSS取得エラー: {e}")
        return []

# AIによる銘柄選別
def scan_with_ai(disclosures):
    if not api_key:
        st.error("APIキーを入力してください。")
        return

    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])

        # 開示タイトルを一つのテキストにまとめる
        titles_text = "\n".join([f"- {d['title']}" for d in disclosures])

        prompt = f"""
        あなたは機関投資家専属のデータサイエンティストです。
        以下の最新開示タイトル一覧から、「株価にポジティブな影響を与える可能性が高いもの」を厳選してください。

        【選別基準：強いキーワード】
        ・増益（20%以上）、過去最高、黒字浮上、上方修正、増配、自社株買い、株主優待新設。
        ・中計策定、業務提携、DX関連など。

        【回答形式】
        1. 【期待度：特大】（銘柄名・コード・理由）
        2. 【期待度：大】（銘柄名・コード・理由）

        【開示タイトル一覧】
        {titles_text}
        """

        with st.spinner("AIが最新開示をスクリーニング中..."):
            response = model.generate_content(prompt)
            st.success("スキャン完了！")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"AI解析エラー: {e}")

# メイン処理
if st.button("最新のTDnetをスキャンする"):
    disclosures = fetch_tdnet_latest()
    if disclosures:
        st.info(f"現在、最新の開示を {len(disclosures)} 件取得しました。")
        scan_with_ai(disclosures)
    else:
        st.warning("開示情報が見つかりませんでした。")
