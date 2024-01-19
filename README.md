# Line Bot 生活小幫手 
![Static Badge](https://img.shields.io/badge/Python-3.8.10-blue)
![Static Badge](https://img.shields.io/badge/Flask-3.0.0-white)

現在的生活離不開網路，而查找生活資訊又需要頻繁切換網頁，使用上並不方便。因此藉由Line Bot，整合生活的相關資訊。本專案目前提供天氣、金融、樂透、油價以及不明來電的查詢功能，**在圖表方面，使用Pandas和Matplotlib整理資料並繪製圖表，接著藉由Imgur的API，上傳圖資並取得圖片連結，再回傳給用戶。**


## 大綱
- [使用限制](#使用限制)
- [展示](#展示)
- [功能](#功能)
- [專案目錄](#專案目錄)
- [執行環境要求](#執行環境要求)
- [安裝與執行](#安裝與執行)
- [參考資料](#參考資料)


## 使用限制
1. <u>本專案是部署在免費版的Render上，每當超過15分鐘無任何人使用時，會進入休眠狀態，可藉由切換選單來喚醒，喚醒時需等待2~3分鐘，接著即可正常使用。</u>

2. 金融資訊的部分，資料來源分別為：[台灣銀行](https://rate.bot.com.tw/)(黃金、即時匯率報價)、[富聯網](https://ww2.money-link.com.tw/Exchange/CrossRate.aspx)(交叉匯率)、[鉅亨網](https://www.cnyes.com/)(匯率走勢、加權指數、櫃買指數、個股股價)。**開發者不保證資料的正確性。**

[⏫回大綱](#大綱)


## 展示
掃描以下QRcode，或是直接 [點擊](https://lin.ee/uQJhNXf) 加入好友

![Alt text](image-1.png)

[⏫回大綱](#大綱)


## 功能
* ⛅ 查詢天氣資訊：提供目前位置的天氣概況、各地天氣預報、天氣圖。 資料來源：[交通部中央氣象署](https://www.cwa.gov.tw/V8/C/)

* 📈 查詢金融資訊：提供黃金、匯率、股市的即時報價和歷史走勢圖 （股市僅提供台股的即時報價）。而查詢即時個股報價的部分，可接受股票名稱/代號的模糊搜尋，例如輸入「$$ q 台灣50」，會收到「您可能想搜尋以下股票名稱：元大台灣50、富邦台50、國泰台灣領袖50」的訊息。

* ☎ 查詢來電資訊：查詢不明簡訊與電話號碼。 資料來源：[查電話](https://whocall.cc/)

* 🤑 樂透彩：產生樂透的投注號碼，以及查詢台灣彩券的開獎結果。 派彩結果：[台灣彩券](https://www.taiwanlottery.com/)

* ⛽️ 查詢油價：查詢中油油價。 資料來源：[中油](https://www.cpc.com.tw/)

[⏫回大綱](#大綱)


## 專案目錄
```
.
+-- src
|   +-- TaipeiSansTCBeta-Regular.ttf  # 繁體中文字體包
|   +-- code_area.json   # 氣象署行政區代碼轉換列表
|   +-- code_city.json   # 氣象署縣市代碼轉換列表
|   +-- code_city.json   # 氣象署縣市代碼轉換列表
|   +-- stock_list.json  # 股票代碼轉換列表
|
+-- app.py  # 主程式
+-- weather.py  # 處理天氣資訊、爬取資料、回傳樣板訊息
+-- finance.py  # 處理金融資訊、爬取資料、回傳樣板訊息
+-- lottery.py  # 處理樂透開獎、產生樂透號碼、回傳樣板訊息
+-- otherfunction.py  # 處理油價查詢和來電查詢、回傳樣板訊息
+-- requirements.txt  # 相依模組
+-- .env.example  # 環境變數範例
+-- build.sh   # 部署在Render上的腳本
+-- README.md  # 說明文件
```
[⏫回大綱](#大綱)


## 執行環境要求
* 本專案建議在 Python 3.8.10 、 [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) 環境之下執行
* `.env` 填寫內容可參考 [.env.example](https://github.com/cheng1103/line-bot-demo/blob/main/.env.example)
* 模組要求詳見 [requirements.txt](https://github.com/cheng1103/line-bot-demo/blob/main/requirements.txt)

[⏫回大綱](#大綱)


## 安裝與執行
### Line 設定
* 請參考 [建立 LINE Channel](https://steam.oxxostudio.tw/category/python/example/line-developer.html) 和 [建立並串接 Webhook](https://steam.oxxostudio.tw/category/python/example/line-webhook.html) 兩篇教學，完成必要設定。而Webhook URL的設定部分，需要在網址結尾加上`/callback`
### 本地端 
1. 安裝 [Python 3.8.10](https://www.python.org/downloads/release/python-3810/) (Linux 免安裝)，Windwos 需安裝 [virtualenvwrapper-win](https://pypi.org/project/virtualenvwrapper-win/)、Linux 則是安裝[Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)，並且按照官方文件說明進行設定
2. 按以下步驟操作，接著在 `.env.example` 中設定環境變數，最後將檔名修改為 `.env`。啟動指令為 `python app.py`
```shell
mkdir linebot
cd linebot
git clone https://github.com/cheng1103/line-bot-demo.git
mkvirtualenv linebot
pip install -r requirements.txt
```
### Render
* 部署方法可參考 [Render 官方文件](https://docs.render.com/deploy-flask)
* 中文教學可移至[參考資料](#參考資料)中 **第5點** 的內容

[⏫回大綱](#大綱)


## 參考資料
1. [LINE 官方文件](https://developers.line.biz/en/docs/messaging-api/)
2. [LINE BOT 教學](https://steam.oxxostudio.tw/category/python/example/line-bot.html)
3. [[Python+LINE Bot教學]提升使用者體驗的按鈕樣板訊息(Buttons template message)實用技巧](https://www.learncodewithmike.com/2020/07/line-bot-buttons-template-message.html)
4. [黑客松 LINE Bot 賽前補帖](https://kanido386.github.io/2021/07/hackathon-line-hint/)
5. [將 python flask Web app 部屬到 Render](https://hackmd.io/@KszW-VhuTFiRIBfviwcT7Q/r1ZCbfSLj)
6. [你知道對專案來說，README.md 有多麼重要嗎？ ── 工程師血淚史](https://medium.com/dean-lin/%E4%BD%A0%E7%9F%A5%E9%81%93%E5%B0%8D%E5%B0%88%E6%A1%88%E4%BE%86%E8%AA%AA-readme-md-%E6%9C%89%E5%A4%9A%E9%BA%BC%E9%87%8D%E8%A6%81%E5%97%8E-%E5%B7%A5%E7%A8%8B%E5%B8%AB%E8%A1%80%E6%B7%9A%E5%8F%B2-c0fb0908343e)

[⏫回大綱](#大綱)