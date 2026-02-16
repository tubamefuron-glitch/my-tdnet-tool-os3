import streamlit as st
import requests
from bs4 import BeautifulSoup
import pdfplumber
import io
import pandas as pd
import time

st.set_page_config(page_title="TDnetキーワード検索(月曜夜・最強版)", layout="wide")
st.title("🔍 TDnet PDFキーワード横断検索ツール")

with st.sidebar:
    st.header("検索条件")
    keyword = st.text_input("検索キーワード", value="増産")
    # 月曜夜なので、思い切って200件くらいスキャンしましょう
    search_limit = st.slider("スキャン件数", 10, 300, 100)
    search_button = st.button("検索実行")

@st.cache_data(ttl=300)
def get_tdnet_list():
    url = "https://www.release.tdnet.info/inbs/I_main_00.html"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")
        items = []
        rows = soup.select("#main-list-table tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5: continue
            title_tag = cols[3].find("a")
            if title_tag:
                items.append({
                    "時刻": cols[0].text.strip(),
                    "コード": cols[1].text.strip(),
                    "社名": cols[2].text.strip(),
                    "タイトル": title_tag.text.strip(),
                    "URL": "https://www.release.tdnet.info/inbs/" + title_tag.get("href")
                })
        return items
    except:
        return []

def search_in_pdf(url, kw):
    try:
        # タイムアウトを短くして、ダメなPDFはすぐ飛ばす
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if response.status_code != 200: return None
        
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            # 1ページ目だけでも「キーワード」があれば即ヒットにする（高速化）
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and kw in text:
                    return i + 1
                if i > 5: break # 6ページ目以降は見ない（決算短信のメインは最初の方なので）
    except:
        pass
    return None

if search_button:
    all_items = get_tdnet_list()
    if not all_items:
        st.error("TDnetからリストを取得できませんでした。")
    else:
        target = all_items[:search_limit]
        st.info(f"月曜日の新着 {len(target)} 件をスキャン中... 「{keyword}」を探しています。")
        
        progress = st.progress(0)
        results = []
        status = st.empty()
        
        for idx, item in enumerate(target):
            progress.progress((idx + 1) / len(target))
            status.text(f"【{idx+1}/{len(target)}】 調査中: {item['社名']}")
            
            p = search_in_pdf(item["URL"], keyword)
            if p:
                item["ページ"] = p
                results.append(item)
                # ヒットしたらその場で表示（モチベーション維持！）
                st.toast(f"的中！: {item['社名']}")
            
            # 連続アクセスでブロックされないよう、わずかに待機
            time.sleep(0.05)
        
        status.empty()
        if results:
            st.success(f"お宝発見！ {len(results)} 件ヒットしました。")
            df = pd.DataFrame(results)
            st.dataframe(df, column_config={"URL": st.column_config.LinkColumn()})
        else:
            st.warning(f"「{keyword}」は見つかりませんでした。キーワードを『修正』や『配当』に変えてみてください。")
