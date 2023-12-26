from flask import Flask, request, abort
import os

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi

from linebot.v3 import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

from weather import *
from lottery import *
from finance import *
from otherfunction import *

# 讀取 LINE 聊天機器人的基本資料設定檔
channel_access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.environ.get("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(channel_access_token)   # 確認 token 是否正確
handler = WebhookHandler(channel_secret)          # 確認 secret 是否正確

# 讀取自定義程式
wx_menu = WeatherMenu()
wx_info = WeatherInfo()
wx_process = WeatherProcess()
finance_menu = FinanceMenu()
finance_process = FinanceProcess()

lotterymenu = LotteryMenu()
lottery_generate = LotteryGenerateNums()

whoscall = Whoscall()
other_function = OtherFunction()

app = Flask(__name__)


# 接收訊息
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("-------------------------------------------------\n" + "Request body:\n" + body,
          "\n Signature:\n" + signature + "\n-------------------------------------------------")

    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 處理和回傳訊息
@handler.add(MessageEvent)
def handle_message(event: MessageEvent):

    # show MessageEvent detail
    print('==============>>> MessageEvent <<<==============')
    print(event)

    # 處理文字訊息
    if event.message.type == 'text':

        menu_switch_case = {
            '天氣': wx_menu.menu(),
            '金融': finance_menu.menu(),
            '新聞': TextSendMessage('規劃中，敬請期待！'),
            '來電反查': whoscall.menu(),
            '備忘錄': TextSendMessage('規劃中，敬請期待！'),
            '使用說明': TextSendMessage('努力中，再等等！'),
            '發票中獎號碼': TextSendMessage('努力中，再等等！'),
            '樂透彩': lotterymenu.lottery_menu(),
            '油價': other_function.query_oil_price(),
            '還沒想到': TextSendMessage('工程師正在思考人生中！')
        }

        receive = event.message.text

        # 來電反查
        if '@' in receive:
            reply_content = whoscall.check_pn(receive.split('@')[1])
            line_bot_api.reply_message(event.reply_token, reply_content)

        # 金融
        elif '$' in receive:
            reply_content = finance_process.process(receive)
            line_bot_api.reply_message(event.reply_token, reply_content)

        # 跳出選單或直接回傳內容
        elif receive in menu_switch_case.keys():
            reply_content = menu_switch_case[receive]
            line_bot_api.reply_message(event.reply_token, reply_content)

        else:
            reply_content = TextSendMessage('輸入錯誤！請檢查內容！')
            line_bot_api.reply_message(event.reply_token, reply_content)

    # 目前位置天氣
    if event.message.type == 'location':
        receive_location = event.message.address
        reply_content = wx_info.query_weather(receive_location)
        line_bot_api.reply_message(event.reply_token, reply_content)


# 處理和回傳訊息
@handler.add(PostbackEvent)
def handle_postback(event: PostbackEvent):

    # show PostbackEvent detail
    print('==============>>> PostbackEvent <<<==============')
    print(event)

    receive = event.postback.data

    switch_case = {
        # weather menu
        'wx_quickreply_first': wx_menu.quickreply_first(),
        'wx_quickreply_second': wx_menu.quickreply_second(),

        # whocall
        'whoscall_explain': whoscall.explain(),

        # finance menu
        'Gold': finance_menu.menu_gold(),
        'FX_rate': finance_menu.menu_fxrate(),
        'Stock': finance_menu.menu_stock(),

        '$gold_twd_trend': finance_menu.quickreply_gold_trend_twd(),
        '$gold_usd_trend': finance_menu.quickreply_gold_trend_usd(),

        '$fxrate_trend_first': finance_menu.quickreply_fxrate_trend_first(),
        '$fxrate_trend_second': finance_menu.quickreply_fxrate_trend_second(),

    }

    if 'richmenu' in event.postback.data:
        pass

    # 處理選單
    elif receive in switch_case.keys():
        reply_content = switch_case[receive]
        line_bot_api.reply_message(event.reply_token, reply_content)

    # 處理天氣圖
    elif 'wx' in receive:
        reply_content = wx_process.process(receive)
        line_bot_api.reply_message(event.reply_token, reply_content)

    # 處理樂透產生號碼
    elif 'LGN' in receive:
        reply_content = lottery_generate.lgn_process(receive)
        line_bot_api.reply_message(event.reply_token, reply_content)

    else:
        reply_content = TextSendMessage('功能建置中！敬請期待！')
        line_bot_api.reply_message(event.reply_token, reply_content)


# 主程式
if __name__ == "__main__":
    app.run(host="13.228.225.19", port=10000)
