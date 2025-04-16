# -*- coding: utf-8 -*-
"""期中.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1mP0IrC42vnF1uYDxOhhKUhmeTMcG9pKs
"""

# -*- coding: utf-8 -*-
# 安裝必要套件（Colab 可能已預先安裝，但此行不會有影響）
!pip install requests beautifulsoup4

import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

def scrape_professors_expertise(base_url, max_pages=5):
    """
    爬取指定 URL 的教授資訊，最多掃描 max_pages 頁，
    依據網頁結構，從 class "teacher-list" 區塊中提取姓名及研究領域。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }
    all_professors = []

    for page in range(1, max_pages + 1):
        if page == 1:
            current_url = base_url
        else:
            current_url = f"{base_url}?page_no={page}"

        try:
            req = Request(current_url, headers=headers)
            with urlopen(req) as html:
                soup = BeautifulSoup(html, 'html.parser')

                # 移除可能干擾解析的分頁與頁尾區塊
                for tag in soup.find_all('div', class_='pagination'):
                    tag.decompose()
                for tag in soup.find_all('div', class_='footer'):
                    tag.decompose()

                # 以結構化方式提取各個教授區塊
                professor_blocks = soup.find_all('div', class_='teacher-list')
                if not professor_blocks and page > 1:
                    break  # 若後續頁面找不到資料則離開迴圈

                for block in professor_blocks:
                    # 取得姓名（必須有 teacher-list-name 區塊）
                    name_element = block.find('div', class_='teacher-list-name')
                    if not name_element:
                        continue
                    name = name_element.get_text(strip=True)

                    # 從 teacher-list-info 區塊內找出包含「研究領域：」的段落
                    expertise = ""
                    info_elements = block.find_all('div', class_='teacher-list-info')
                    for info in info_elements:
                        info_text = info.get_text(strip=True)
                        if "研究領域" in info_text:
                            # 嘗試以「研究領域：」為分隔字串進行拆解
                            parts = info_text.split("研究領域：")
                            if len(parts) > 1:
                                expertise = parts[1].strip()
                            else:
                                expertise = info_text.replace("研究領域", "").strip()
                            break

                    # 整理專長文字（移除多餘空白與標點符號替換）
                    expertise = re.sub(r'\s+', ' ', expertise)
                    expertise = expertise.replace(', ', '、').replace('，', '、')

                    if name and expertise:
                        all_professors.append({
                            '姓名': name,
                            '專長': expertise
                        })
                        print(f"教授: {name}, 專長: {expertise[:50]}...")
        except Exception as e:
            print(f"爬取 {current_url} 時發生錯誤：{e}")
            break
    return all_professors

def save_professors_to_file(professors_data, filename="professors_expertise.txt"):
    """
    將教授資料列表寫入文字檔案
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for prof in professors_data:
            f.write(f"教授: {prof['姓名']}, 專長: {prof['專長']}\n")
    print(f"資料已保存至 {filename}")
    return filename

def main():
    # 分別爬取各類型的教授資料
    associate_professors = scrape_professors_expertise("https://csie.asia.edu.tw/zh_tw/associate_professors_2", max_pages=5)
    assistant_professors = scrape_professors_expertise("https://csie.asia.edu.tw/zh_tw/assistant_professors_2", max_pages=5)
    lecturers = scrape_professors_expertise("https://csie.asia.edu.tw/zh_tw/senior_lecturer", max_pages=5)
    # 可依需求增加更多類別，如 "all_professors_1"
    all_professors = associate_professors + assistant_professors + lecturers

    # 添加特殊案例（僅添加一次）
    special_cases = [
        {"姓名": "Tadao Murata", "專長": "分散式通訊軟體、網路協議、邏輯與規則基礎AI系統、製造系統、平行計算系統和具有模糊延遲的系統的Petri網應用"},
        {"姓名": "曾憲章(Zeng Xianzhang)", "專長": "計算機科學"},
        {"姓名": "李錦輝(Chin-Hui Lee)", "專長": "語音訊號處理、機器學習"},
        {"姓名": "黃光彩", "專長": "電機工程"},
        {"姓名": "林一平(Jason Yi-Bing Lin)", "專長": "個人通信網路、行動計算、系統模擬"},
        {"姓名": "張嘉淵(Zhang Jiayuan)", "專長": "雲端運算、大數據分析、演算法、社群媒體、人工智慧物聯網、人本創新應用"},
        {"姓名": "許健(Gene Sheu)", "專長": "電子電路、微電子、產品研發、積體電路"},
        {"姓名": "梁文隆(Wen-Lung Liang)", "專長": "物聯網技術、嵌入式系統、智慧家庭"},
        {"姓名": "林詠章(Lin Yongzhang)", "專長": "資訊安全、區塊鏈應用、精準健康、智慧醫療、工控安全"}
    ]
    for case in special_cases:
        all_professors.append(case)
        print(f"特殊案例 - 教授: {case['姓名']}, 專長: {case['專長'][:50]}...")

    # 過濾重複的教授
    seen = set()
    unique_professors = []
    for prof in all_professors:
        name = prof['姓名'].strip()
        if name not in seen and prof['專長'].strip():
            unique_professors.append(prof)
            seen.add(name)

    # 寫入檔案
    filename = save_professors_to_file(unique_professors)

    # Colab下載檔案
    try:
        from google.colab import files
        files.download(filename)
        print(f"\n檔案 {filename} 已準備好下載，請檢查瀏覽器下載提示。")
    except ImportError:
        print(f"\n程式執行完成，檔案儲存在目錄：{filename}")

if __name__ == "__main__":
    main()