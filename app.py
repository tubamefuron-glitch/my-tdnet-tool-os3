import streamlit as st
import google.generativeai as genai
import requests
import xml.etree.ElementTree as ET

# 画面設定
st.set_page_config(page_title="自動決算スキャナー", layout="wide")
st.title("📡 最新決算・爆速自動検知 (対策版)")

# サイドバー設定
with st.sidebar:
    api_key = st.text_input("Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# TDnet RSS取得（ブラウザのふりをする設定を追加）
def fetch_tdnet_latest():
    RSS_URL = "https://www.release.tdnet.info/inbs/if_p001.rss"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(RSS_URL, headers=headers)
        response.raise_for_status() # 403などのエラーがあればここで例外を出す
        
        # XMLを解析
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall('.//item'):
            title = item.find('title').text
            link = item.find('link').text
            items.append({"title": title, "link": link})
        return items
    except Exception as e:
        st.error(f"取得失敗: {e}")
        st.info("TDnet側で一時的なアクセス制限がかかっている可能性があります。少し時間を置いて試してください。")
        return []

# AI選別ロジック
def scan_with_ai(disclosures):
    if not api_key:
        st.error("APIキーを入力してください。")
        return

    try:
        # あなたの環境で使える最新モデルを自動取得
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model = genai.GenerativeModel(available_models[0])

        titles_text = "\n".join([f"- {d['title']}" for d in disclosures])

        prompt = f"""
        あなたは機関投資家です。以下の開示一覧から「株価が爆上がりしそうなもの」を厳選し、理由を添えて教えてください。
        特に増益、増配、自社株買い、黒字転換を見逃さないでください。

        【一覧】
        {titles_text}
        """

        with st.spinner("AIが精査中..."):
            response = model.generate_content(prompt)
            st.success("スキャン完了！")
            st.markdown(response.text)
            
    except Exception as e:
        st.error(f"AI解析エラー: {e}")

# メインボタン
if st.button("最新のTDnetをスキャン"):
    disclosures = fetch_tdnet_latest()
    if disclosures:
        st.info(f"最新の開示を {len(disclosures)} 件チェックします。")
        scan_with_ai(disclosures)
