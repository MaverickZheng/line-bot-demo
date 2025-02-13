# Line Bot 生活小幫手 
![Static Badge](https://img.shields.io/badge/Python-3.8.10-blue)
![Static Badge](https://img.shields.io/badge/Flask-3.0.0-white)
![Static Badge](https://img.shields.io/badge/Line_bot_sdk-3.5.0-green)

<p align=center>
    <img src="assets/head_shot.jpg" width="60%">
</p>

「生活小幫手」是一款可以整合生活資訊的Line Bot，因為現在的生活離不開網路，但資訊是分散在各個網站中，搜尋時需要頻繁切換網頁，使用上並不方便。因此藉由「生活小幫手」，整合生活相關的資訊，提供一站式的生活資訊服務。本專案目前提供天氣、金融、樂透、油價以及不明來電的查詢功能，詳細的功能說明，請點擊[連結](#功能)。


## 大綱
- [使用限制和警語](#使用限制和警語)
- [開始使用](#開始使用)
- [功能](#功能)
- [操作示範](#操作示範)
- [專案目錄](#專案目錄)
- [執行環境要求](#執行環境要求)
- [安裝與執行](#安裝與執行)
- [參考資料](#參考資料)


## 使用限制和警語
* __《！！重要！！》本專案是部署在免費版的Render上，每當超過15分鐘無任何人使用時，會進入休眠狀態，可藉由切換選單來喚醒，喚醒時需等待2~3分鐘，接著即可正常使用。__



* 金融資訊的部分，資料來源分別為：[台灣銀行](https://rate.bot.com.tw/)(黃金、即時匯率報價)、[富聯網](https://ww2.money-link.com.tw/Exchange/CrossRate.aspx)(交叉匯率)、[鉅亨網](https://www.cnyes.com/)(匯率走勢、加權指數、櫃買指數、個股股價)。__開發者不保證資料的正確性。__

[⏫回大綱](#大綱)


## 開始使用
掃描以下QRcode，或是點擊 [連結](https://lin.ee/uQJhNXf) 加入好友

![Line QRcode](assets/line_qrcode.png)

[⏫回大綱](#大綱)


## 功能
* ⛅ 查詢天氣資訊：提供目前位置的天氣概況、各地天氣預報、以及天氣圖。 資料來源：[交通部中央氣象署](https://www.cwa.gov.tw/V8/C/)

* 📈 查詢金融資訊：提供黃金、匯率、股市的即時報價和歷史走勢圖 （股市僅提供台股的即時報價）。而查詢即時個股報價的部分，__可接受股票名稱/代號的模糊搜尋，例如輸入「$$ q 台灣50」，會收到「您可能想搜尋以下股票名稱：元大台灣50、富邦台50、國泰台灣領袖50」的訊息。__

* ☎ 查詢來電資訊：查詢不明簡訊與電話號碼， __查詢方式：@0911510914、@0223491234。__ 資料來源：[查電話](https://whocall.cc/)

* 🤑 樂透彩：產生樂透的投注號碼，以及查詢台灣彩券的開獎結果。 派彩結果：[台灣彩券](https://www.taiwanlottery.com/)

* ⛽️ 查詢油價：查詢中油油價。 資料來源：[中油](https://www.cpc.com.tw/)

[⏫回大綱](#大綱)


## 操作示範
* 天氣

![Weather demo](assets/demo_weather.gif)

* 金融資訊

![Finance demo](assets/demo_finance.gif)

* 來電反查

![Whoscall demo](assets/demo_whoscall.gif)

* 樂透彩

![Lotto demo](assets/demo_lotto.gif)

* 油價

![Oil price demo](assets/demo_oil_price.gif)

[⏫回大綱](#大綱)


## 專案目錄
```
.
+-- assets      # 包含 gif、png 等素材圖檔
+-- src
|   +-- TaipeiSansTCBeta-Regular.ttf  # 繁體中文字體檔
|   +-- code_area.json   # 氣象署行政區代碼轉換列表
|   +-- code_city.json   # 氣象署縣市代碼轉換列表
|   +-- stock_list.json  # 股票代碼轉換列表
|
+-- app.py  # 主程式
+-- weather.py  # 處理天氣資訊、爬取資料、回傳樣板訊息
+-- finance.py  # 處理金融資訊、爬取資料、回傳樣板訊息
+-- lottery.py  # 處理樂透開獎、產生樂透號碼、回傳樣板訊息
+-- otherfunction.py  # 處理油價查詢和來電查詢、回傳樣板訊息
+-- requirements.txt  # 相依套件
+-- .env.example  # 環境變數範例
+-- build.sh   # 部署在Render上的腳本
+-- README.md  # 說明文件
```
[⏫回大綱](#大綱)


## 執行環境要求
* 本專案建議在 [Python 3.8.10](https://www.python.org/downloads/release/python-3810/) 、 [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) 所建立的虛擬環境之下執行，確保不會發生相依套件上的衝突。
* `.env` 填寫內容可參考 [.env.example](.env.example)
* 套件要求詳見 [requirements.txt](requirements.txt)

[⏫回大綱](#大綱)


## 安裝與執行
### Line 設定
* 請參考 [建立 LINE Channel](https://steam.oxxostudio.tw/category/python/example/line-developer.html) 和 [建立並串接 Webhook](https://steam.oxxostudio.tw/category/python/example/line-webhook.html) 兩篇教學，完成必要設定。而Webhook URL的設定，需要在網址結尾加上`/callback`
### 本地端執行
1. 安裝 [Python 3.8.10](https://www.python.org/downloads/release/python-3810/) (Linux 免安裝)，Windwos 需安裝 [virtualenvwrapper-win](https://pypi.org/project/virtualenvwrapper-win/)、Linux 則是安裝[Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)，並且按照官方文件說明進行設定 (需確認 Virtualenvwrapper 已經安裝並正確設定，以方便接下來建立虛擬環境)
2. 按以下步驟操作，接著在 `.env.example` 中設定環境變數，再將檔名修改為 `.env`。接著開啟 __Ngrok__ ，將 Ngrok 的網址填入 Webhook URL ，最後下指令 `python app.py`
```shell
mkdir linebot
cd linebot
git clone https://github.com/cheng1103/line-bot-demo.git
mkvirtualenv linebot
pip install -r requirements.txt
```
### Render部署
* 部署方法可參考 [Render 官方文件](https://docs.render.com/deploy-flask)
* 中文教學可移至[參考資料](#參考資料)中 __第5點和第6點__ 的內容

[⏫回大綱](#大綱)


## 參考資料
1. [LINE 官方文件](https://developers.line.biz/en/docs/messaging-api/)
2. [LINE BOT 教學](https://steam.oxxostudio.tw/category/python/example/line-bot.html)
3. [[Python+LINE Bot教學]提升使用者體驗的按鈕樣板訊息(Buttons template message)實用技巧](https://www.learncodewithmike.com/2020/07/line-bot-buttons-template-message.html)
4. [黑客松 LINE Bot 賽前補帖](https://kanido386.github.io/2021/07/hackathon-line-hint/)
5. [關於從 Heroku 跳到 Render 這件事情](https://israynotarray.com/other/20221213/3036227586/)
6. [將 python flask Web app 部屬到 Render](https://hackmd.io/@KszW-VhuTFiRIBfviwcT7Q/r1ZCbfSLj)
7. [你知道對專案來說，README.md 有多麼重要嗎？ ── 工程師血淚史](https://medium.com/dean-lin/%E4%BD%A0%E7%9F%A5%E9%81%93%E5%B0%8D%E5%B0%88%E6%A1%88%E4%BE%86%E8%AA%AA-readme-md-%E6%9C%89%E5%A4%9A%E9%BA%BC%E9%87%8D%E8%A6%81%E5%97%8E-%E5%B7%A5%E7%A8%8B%E5%B8%AB%E8%A1%80%E6%B7%9A%E5%8F%B2-c0fb0908343e)
8. [你的git项目需要一个高质量的README](https://juejin.cn/post/6844903845785501710)
9. [Uptime Robot 老牌免費網頁監控服務，可加入 50 頁面、5 分鐘間距](https://free.com.tw/uptime-robot/)

[⏫回大綱](#大綱)