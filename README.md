# Line Bot 生活小幫手
![Static Badge](https://img.shields.io/badge/Python-3.8.10-blue)


## 大綱
- [使用限制](#使用限制)
- [功能](#功能)
- [參考資料](#參考資料)
- [執行環境要求](#執行環境要求)


## 使用限制
1. 本專案是部署在免費版的Render上，每當超過15分鐘無任何人使用時，會進入休眠狀態，可藉由切換選單來喚醒，喚醒時需等待2~3分鐘，接著即可正常使用。

2. 金融資訊的部分，資料來源分別為：台灣銀行(黃金、匯率)、富聯網(交叉匯率)、鉅亨網(匯率、加權指數、櫃買指數、個股股價)。不保證任何資料的正確性。


## 功能
* ⛅ 查詢天氣資訊：提供目前位置的天氣概況、各地天氣預報、天氣圖。

* 📈 查詢金融資訊：提供黃金、匯率、股市的即時報價和歷史走勢圖 （股市僅提供台股的即時報價）。而查詢股票報價的部分，可接受股票名稱/代號的模糊搜尋，例如輸入「$$ q 台灣50」，會收到「您可能想搜尋以下股票名稱：元大台灣50、富邦台50、國泰台灣領袖50」。

* ☎ 查詢來電資訊：查詢不明簡訊與電話號碼。

* 🤑 樂透彩：產生樂透的投注號碼，以及查詢台灣彩券的開獎結果。

* ⛽️ 查詢油價：查詢中油油價。


## 執行環境需求
* 本專案使用 Python 3.8.10 開發
* .env 可參考
* 模組要求請見 [requirements.txt](https://github.com/cheng1103/line-bot-demo/blob/main/requirements.txt)


## 參考資料
* [LINE 官方文件](https://developers.line.biz/en/docs/)
* [LINE BOT 教學](https://steam.oxxostudio.tw/category/python/example/line-bot.html)
* [[Python+LINE Bot教學]提升使用者體驗的按鈕樣板訊息(Buttons template message)實用技巧](https://www.learncodewithmike.com/2020/07/line-bot-buttons-template-message.html)
* [黑客松 LINE Bot 賽前補帖](https://kanido386.github.io/2021/07/hackathon-line-hint/)
* [將 python flask Web app 部屬到 Render](https://hackmd.io/@KszW-VhuTFiRIBfviwcT7Q/r1ZCbfSLj)


