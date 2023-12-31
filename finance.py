import io  # 資料暫存檔
import os
import base64
import difflib
import arrow  # 時間處理
import json
import time
import random
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from fake_useragent import UserAgent
from lxml import etree
import bs4
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager  # 字體管理
# import mplfinance as mpf
from linebot.models import *  # linebot模組
from fugle_marketdata import RestClient  # fugle模組


class FinanceMenu:
    '''
    金融選單

    輸入：
    由app.py作為主控，透過richmenu呼叫menu，再由menu呼叫各個次選單
    輸出：
    讓指定的選單回傳到聊天室

    '''

    # 金融主選單
    def menu(self):
        menu = TemplateSendMessage(
            alt_text='金融選單',    # 訊息預覽
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn.pixabay.com/photo/2017/08/30/07/56/money-2696228_1280.jpg',
                title='金融資訊',
                text='目前不提供股市走勢圖！',
                actions=[
                    PostbackAction(
                        label='黃金',
                        text=None,
                        data='Gold'
                    ),
                    PostbackAction(
                        label='外匯',
                        text=None,
                        data='FX_rate'
                    ),
                    PostbackAction(
                        label='股市',
                        text=None,
                        data='Stock'
                    ),
                    MessageAction(
                        label='📖使用說明📖',
                        text='$finance_explain'
                    ),
                ]
            )
        )

        return menu

    # 黃金次選單
    def menu_gold(self):
        menu = TemplateSendMessage(
            alt_text='黃金牌價',    # 訊息預覽
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.pixabay.com/photo/2014/11/01/22/33/gold-513062_1280.jpg',
                        title='🇹🇼 臺幣 黃金存摺價格 🇹🇼',
                        text='臺幣黃金即時牌價與歷史走勢',
                        actions=[
                            MessageAction(
                                label='即時黃金牌價(臺幣)',
                                text='$gold twd_realtime'
                            ),
                            PostbackAction(
                                label='📈臺幣黃金走勢📈',  # 跳出quickreply
                                text=None,
                                data='$gold_twd_trend'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.pixabay.com/photo/2014/11/01/22/33/gold-513062_1280.jpg',
                        title='🇺🇸 美元 黃金存摺價格 🇺🇸',
                        text='美元黃金即時牌價與歷史走勢',
                        actions=[
                            MessageAction(
                                label='即時黃金牌價(美元)',
                                text='$gold usd_realtime'
                            ),
                            PostbackAction(
                                label='📈美元黃金走勢📈',  # 跳出quickreply
                                text=None,
                                data='$gold_usd_trend'
                            ),
                        ]
                    )
                ]
            )
        )

        return menu

    # 臺幣黃金走勢 快速回覆紐
    def quickreply_gold_trend_twd(self):
        menu = TextSendMessage(
            text='點擊按鈕\n 🇹🇼 查看臺幣計價黃金走勢圖📈',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="📈 3個月黃金走勢圖(臺幣)", text="$gold twd_3m")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="📈 6個月黃金走勢圖(臺幣)", text="$gold twd_6m")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="📈 1年黃金走勢圖(臺幣)", text="$gold twd_12m")
                    ),
                ]
            )
        )

        return menu

    # 美元黃金走勢 快速回覆紐
    def quickreply_gold_trend_usd(self):
        menu = TextSendMessage(
            text='點擊按鈕\n 🇺🇸 查看美元計價黃金走勢圖📈',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="📈 3個月黃金走勢圖(美元)", text="$gold usd_3m")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="📈 6個月黃金走勢圖(美元)", text="$gold usd_6m")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="📈 1年黃金走勢圖(美元)", text="$gold usd_12m")
                    ),
                ]
            )
        )

        return menu

    # 匯率次選單
    def menu_fxrate(self):
        menu = TemplateSendMessage(
            alt_text='匯率資訊',    # 訊息預覽
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn.pixabay.com/photo/2014/10/23/10/10/dollars-499481_1280.jpg',
                title='匯率資訊',
                text='即時匯率與歷史走勢',
                actions=[
                    MessageAction(
                        label='臺灣銀行即時匯率',
                        text='$fxrate realtime'
                    ),
                    MessageAction(
                        label='交叉匯率',
                        text='$fxrate cross'
                    ),
                    PostbackAction(
                        label='📈匯率走勢📈',
                        text=None,
                        data='$fxrate_trend_first'
                    ),

                ]
            )
        )

        return menu

    # 匯率走勢 快速回覆紐 第一頁
    def quickreply_fxrate_trend_first(self):
        menu = TextSendMessage(
            text='第一頁\n◀左右滑動▶\n點擊外幣\n查看外幣兌台幣走勢圖📈',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇺🇸 美金", text="$fxrate trend_USD")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇪🇺 歐元", text="$fxrate trend_EUR")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇬🇧 英鎊", text="$fxrate trend_GBP")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇯🇵 日圓", text="$fxrate trend_JPY")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇨🇳 人民幣", text="$fxrate trend_CNY")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇨🇦 加拿大幣", text="$fxrate trend_CAD")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇦🇺 澳幣", text="$fxrate trend_AUD")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇭🇰 港幣", text="$fxrate trend_HKD")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇸🇬 新加坡幣", text="$fxrate trend_SGD")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇨🇭 瑞士法郎/瑞郎", text="$fxrate trend_CHF")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=PostbackAction(
                            label='下一頁▶',
                            text=None,
                            data='$fxrate_trend_second'
                        ),
                    ),
                ]
            )
        )

        return menu

    # 匯率走勢 快速回覆紐 第二頁
    def quickreply_fxrate_trend_second(self):
        menu = TextSendMessage(
            text='第二頁\n◀左右滑動▶\n點擊外幣\n查看外幣兌台幣走勢圖📈',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇸🇪 瑞典克朗/瑞典幣", text="$fxrate trend_SEK")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇹🇭 泰銖/泰幣", text="$fxrate trend_THB")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇲🇾 馬來西亞令吉/馬來幣", text="$fxrate trend_MYR")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇳🇿 紐元/紐幣", text="$fxrate trend_NZD")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇵🇭 菲律賓幣/菲國比索", text="$fxrate trend_PHP")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇿🇦 南非幣", text="$fxrate trend_ZAR")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇰🇷 韓元", text="$fxrate trend_KRW")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇮🇩 印尼幣/印尼盾", text="$fxrate trend_IDR")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=MessageAction(
                            label="🇻🇳 越南盾", text="$fxrate trend_VND")
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=PostbackAction(
                            label='◀上一頁',
                            text=None,
                            data='$fxrate_trend_first'
                        ),
                    ),
                ]
            )
        )

        return menu

    def menu_stock(self):
        menu = TemplateSendMessage(
            alt_text='股市資訊',    # 訊息預覽
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg',
                        title='個股即時報價',
                        text='目前只提供個股的文字即時報價',
                        actions=[
                            MessageAction(
                                label='個股即時報價範例',
                                text='$$ q 006208'
                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg',
                        title='加權指數即時報價',
                        text='目前只提供加權指數的文字即時報價',
                        actions=[
                            MessageAction(
                                label='加權指數即時報價',
                                text='$$ q twse'
                            ),

                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.pixabay.com/photo/2016/11/27/21/42/stock-1863880_1280.jpg',
                        title='櫃買指數即時報價',
                        text='目前只提供櫃買指數的文字即時報價',
                        actions=[
                            MessageAction(
                                label='櫃買指數即時報價',
                                text='$$ q tpex'
                            ),

                        ]
                    )
                ]
            )
        )

        return menu


class FinanceProcess:
    '''
    金融訊息處理

    輸入：
    由app.py作為主控，藉由FinanceMenu發送訊息
    輸出：
    將訊息分類後，使用FinanceInfo和StockMarket的功能，將資訊回傳給用戶

    '''

    def __init__(self):
        self.finance_info = FinanceInfo()
        self.stock_market = StockMarket()
        self.gold_switch = {
            'twd_realtime': self.finance_info.gold_twd_realtime(),
            'usd_realtime': self.finance_info.gold_usd_realtime(),
        }

        # 使用說明
        self.explain_text = """資訊提供項目：
1.黃金：提供臺銀黃金即時牌價與趨勢圖
2.匯率：提供臺銀即時匯率、交叉匯率表、以及近半年匯率走勢圖
3.股市：僅提供加權指數、櫃買指數與個股的即時文字報價

股市的操作說明：
精確搜尋的格式為「$$ q 006208」、「$$ q 富邦台50」。並且支援模糊搜尋，格式如：「$$ q 台灣50」。

產製趨勢圖需要時間，請耐心等待！

資料來源：
臺銀：黃金即時牌價、趨勢圖、即時匯率
富聯網：交叉匯率表
鉅亨網：匯率趨勢、加權指數、櫃買指數、個股報價
"""

    def process(self, receive):

        # 金融服務使用說明
        if 'finance_explain' in receive:
            content = TextSendMessage(self.explain_text)

        # 黃金
        elif 'gold' in receive:
            receive_code = receive.split(' ')[1]

            # 處理黃金即時報價
            if receive_code in self.gold_switch.keys():
                content = self.gold_switch[receive_code]

            # 處理黃金趨勢圖
            else:
                currency = receive_code.split('_')[0]  # 擷取計價幣別
                period = receive_code.split('_')[1]  # 擷取查詢區間

                content = self.finance_info.gold_trend_graph(currency, period)

        # 匯率
        elif 'fxrate' in receive:
            receive_code = receive.split(' ')[1]

            # 處理匯率即時報價
            if 'realtime' in receive_code:
                content = self.finance_info.fxrate_realtime()

            # 處理交叉匯率
            elif 'cross' in receive_code:
                content = self.finance_info.fxrate_cross()

            # 處理匯率趨勢
            elif 'trend' in receive_code:
                currency = receive_code.split('_')[1]  # 擷取貨幣別
                content = self.finance_info.fxrate_trend(currency)

            else:
                content = TextSendMessage('您輸入有誤喔！請檢查內容！')

        # 股市
        elif '$$' in receive:
            search = receive.replace('$$ ', '')

            # if 'explain' in search:
            #     message = '目前可提供精確、模糊搜尋\n\n精確搜尋方法：\n$$ q 台積電 或 $$ q 2330\n\n模糊搜尋方法：\n$$ q 台灣50\n模糊搜尋結果：\n「您可能想搜尋以下股票名稱：元大台灣50、富邦台50、國泰台灣領袖50」'
            #     content = TextSendMessage(message)

            # 檢查輸入格式，若錯誤則提醒用戶
            if len(search.split(' ')) != 2:
                content = TextSendMessage('您輸入的格式有誤喔！請檢查內容！')

            # 檢查輸入格式，若正確則執行
            else:
                data_type = search.split(' ')[0]
                stock_symbol = search.split(' ')[1]

                # 指數資訊
                if stock_symbol in ['twse', 'tpex']:
                    content = self.stock_market.index_info(
                        data_type, stock_symbol)

                # 個股資訊
                else:
                    content = self.stock_market.stock_info(
                        data_type, stock_symbol)

        else:
            content = TextSendMessage('您輸入有誤喔！請檢查內容！')

        return content


# 黃金和外匯資訊
class FinanceInfo:

    def __init__(self):
        # 讀取環境變量(金鑰)
        self.imgur_client_id = os.environ.get("IMGUR_CLIENT_ID")  # Imgur 金鑰
        self.fugle_api_key = os.environ.get("FUGLE_API_KEY")  # Fugle 金鑰

        # matplotlib 字體設定
        fontManager.addfont('src/TaipeiSansTCBeta-Regular.ttf')
        plt.rcParams['font.family'] = 'Taipei Sans TC Beta'

        # 初始化連線物件
        self.session = requests.Session()
        retry = Retry(total=2, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.keep_alive = False

        # 臺灣銀行標頭
        self.bot_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Dnt': '1',
            'Host': 'rate.bot.com.tw',
            'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1'
        }

    # 發送請求
    def __web_requests_get(self, url, headers):

        response = self.session.get(url, headers=headers, timeout=5)

        while response.status_code != requests.codes.ok:
            t = random.uniform(0.5, 2.5)
            time.sleep(t)
            response = self.session.get(url, headers=headers, timeout=5)
            self.session.close()

        return response

    # 上傳圖片，並取得地址
    def __upload_image(self, fig):

        temp_image = io.BytesIO()  # 建立暫存用容器
        fig.savefig(temp_image, format='png')  # 將圖片匯出至容器
        temp_image.seek(0)
        base64_png_data = base64.b64encode(temp_image.read()).decode()

        # 設定API需要傳送的資料
        url = "https://api.imgur.com/3/image"
        headers = {"Authorization": f'Client-ID {self.imgur_client_id}'}
        payload = {"image": base64_png_data}

        # 上傳圖片並取得回應資料
        response = requests.post(url, headers=headers, data=payload)

        # 擷取圖片網址
        image_url = response.json()["data"]['link']

        return image_url

    # 台幣黃金存摺即時牌價
    def gold_twd_realtime(self):

        # 建立爬蟲所需資料
        url = 'https://rate.bot.com.tw/gold?Lang=zh-TW'
        headers = self.bot_headers
        headers['User-Agent'] = UserAgent().random

        response = self.__web_requests_get(url, headers)  # 發送請求
        response.encoding = 'utf-8'

        # 解析並擷取網頁資料
        dom = etree.HTML(response.text, etree.HTMLParser())
        title = dom.xpath(
            '//*[@id="h1_small_id"]/text() | //*[@id="h1_id"]/span/text()')
        time = dom.xpath(
            '//*[@id="ie11andabove"]/div/div[1]/div/text()')[1].strip()
        ask = dom.xpath(
            '//*[@id="ie11andabove"]/div/div[2]/table/tbody/tr[1]/td[3]/text()')[0].strip()  # 銀行賣出價
        bid = dom.xpath(
            '//*[@id="ie11andabove"]/div/div[2]/table/tbody/tr[2]/td[3]/text()')[0].strip()  # 銀行買進價

        # 整理資料
        title = ' '.join(title)
        ask = f'本行賣出(客戶買進)： {ask} 元'
        bid = f'本行買進(客戶賣出)： {bid} 元'

        # 將內容以條列呈現
        content = ''.join(
            [title, '\n', time, '\n---------------------\n', ask, '\n', bid, '\n\n單位： 1公克/新臺幣元'])
        content = f'臺灣銀行 黃金存摺即時價格(臺幣) \n\n{content}'

        #
        message = TextSendMessage(content)

        return message

    # 美元黃金存摺即時牌價
    def gold_usd_realtime(self):

        # 建立爬蟲所需資料
        url = 'https://rate.bot.com.tw/gold/obu'
        headers = self.bot_headers
        headers['User-Agent'] = UserAgent().random

        response = self.__web_requests_get(url, headers)  # 發送請求
        response.encoding = 'utf-8'

        # 解析並擷取網頁資料
        dom = etree.HTML(response.text, etree.HTMLParser())
        title = dom.xpath(
            '//*[@id="h1_small_id"]/text() | //*[@id="h1_id"]/span/text()')
        time = dom.xpath(
            '//*[@id="ie11andabove"]/div/table/tbody/tr[1]/td[1]/text()')[0]
        ask = dom.xpath(
            '//*[@id="ie11andabove"]/div/table/tbody/tr[1]/td[5]/text()')[0].strip()  # 銀行賣出價
        bid = dom.xpath(
            '//*[@id="ie11andabove"]/div/table/tbody/tr[1]/td[4]/text()')[0].strip()  # 銀行買進價

        # 整理資料
        title = ' '.join(title)
        time = f'掛牌時間： {time} '
        ask = f'本行賣出(客戶買進)： {ask} 元'
        bid = f'本行買進(客戶賣出)： {bid} 元'

        # 將內容以條列呈現
        content = ''.join(
            [title, '\n', time, '\n---------------------\n', ask, '\n', bid, '\n\n單位： 1英兩/美元'])
        content = f'臺灣銀行 黃金存摺即時價格(美元) \n\n{content}'

        message = TextSendMessage(content)

        return message

    # 黃金存摺價格趨勢圖
    def gold_trend_graph(self, currency, period):

        # 建立繪圖所需資料
        # 3個月趨勢圖 臺幣
        if currency == 'twd' and period == '3m':
            url = 'https://rate.bot.com.tw/gold/csv/ltm/TWD/0'
            currency_name = '(台幣)'
            gap = 14
            marker = '.'

        # 3個月趨勢圖 美元
        elif currency == 'usd' and period == '3m':
            url = 'https://rate.bot.com.tw/gold/csv/ltm/USD/0'
            currency_name = '(美元)'
            gap = 14
            marker = '.'

        # 6個月趨勢圖 臺幣
        elif currency == 'twd' and period == '6m':
            url = 'https://rate.bot.com.tw/gold/csv/half/TWD/0'
            currency_name = '(台幣)'
            gap = 28
            marker = None

        # 6個月趨勢圖 美元
        elif currency == 'usd' and period == '6m':
            url = 'https://rate.bot.com.tw/gold/csv/half/USD/0'
            currency_name = '(美元)'
            gap = 28
            marker = None

        # 12個月趨勢圖 臺幣
        elif currency == 'twd' and period == '12m':
            url = 'https://rate.bot.com.tw/gold/csv/year/TWD/0'
            currency_name = '(台幣)'
            gap = 28
            marker = None

        # 12個月趨勢圖 美元
        elif currency == 'usd' and period == '12m':
            url = 'https://rate.bot.com.tw/gold/csv/year/USD/0'
            currency_name = '(美元)'
            gap = 28
            marker = None

        # 建立爬蟲所需資料
        headers = self.bot_headers
        headers['User-Agent'] = UserAgent().random

        response = self.__web_requests_get(url, headers)  # 發送請求
        response.encoding = 'utf-8'

        # 整理資料
        df = pd.read_csv(io.StringIO(response.text))  # 檔案讀取並轉換
        df = df.sort_values(by='日期', ascending=True)  # 按日期排序遞增
        df = df.reset_index(drop=True)  # 重設索引
        df['日期'] = pd.to_datetime(df['日期'], format='%Y%m%d')  # 轉換資料格式

        # 設定圖表和尺寸
        fig, ax = plt.subplots(figsize=(6, 4), dpi=200)

        # 繪製折線圖
        ax.plot(df['日期'], df["本行賣出價格"], label="銀行賣出",
                color="red", marker=marker)
        ax.plot(df['日期'], df["本行買入價格"], label="銀行買入",
                color="blue", marker=marker)

        # 設定X軸為日期格式
        ax.xaxis_date()

        # 設定坐標軸標籤
        # ax.set_xlabel("日期")
        # ax.set_ylabel("台幣")

        # 設定刻度
        ax.xaxis.set_major_locator(plt.MultipleLocator(gap))
        # ax.xaxis.set_tick_params(rotation=45, labelsize=10)

        # 設定圖例
        ax.legend(loc="best")

        # 自動調整X軸
        plt.gcf().autofmt_xdate()

        # 顯示橫軸格線
        plt.grid()

        # 設定標題
        title = f'臺灣銀行 黃金存摺牌價 {currency_name}'
        ax.set_title(title)

        plt.tight_layout()

        # 上傳圖片，並取得網址
        link = self.__upload_image(fig)

        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 臺銀即時牌告匯率表
    def fxrate_realtime(self):
        # 建立爬蟲所需資料
        url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
        headers = self.bot_headers
        headers['User-Agent'] = UserAgent().random

        response = self.__web_requests_get(url, headers)  # 發送請求
        response.encoding = 'utf-8'

        # 解析並擷取網頁資料
        dom = etree.HTML(response.text, etree.HTMLParser())
        title = dom.xpath(
            '//*[@id="h1_small_id"]/text() | //*[@id="h1_id"]/span/text()')
        title = ' '.join(title)
        time = dom.xpath(
            '//*[@id="ie11andabove"]/div/p[2]/text()[2] | //*[@id="ie11andabove"]/div/p[2]/span[2]/text()')
        time = ' '.join(time)
        time = time.strip()

        # 解析網頁並擷取表格資料
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        fx_table = soup.select('table')[0]
        df = pd.read_html(fx_table.prettify())[0]

        # 整理匯率資料
        fx_column_label = ['幣別', '本行現金賣出', '本行現金買入', '本行即期賣出', '本行即期買入']
        fx_table = []
        # fx_data = []

        for idx in range(df.shape[0]):
            currency = df.iloc[idx, 0].split('  ')[0]
            fx_table.append(
                (currency, df.iloc[idx, 2], df.iloc[idx, 1], df.iloc[idx, 4], df.iloc[idx, 3]))

            # 文字版報價
            # cash_buy = ' '.join(['本行現金買入：', df.iloc[idx, 1], '\n'])
            # cash_sell = ' '.join(['本行現金賣出：', df.iloc[idx, 2], '\n'])
            # spot_buy = ' '.join(['本行即期買入：', df.iloc[idx, 3], '\n'])
            # spot_sell = ' '.join(['本行即期賣出：', df.iloc[idx, 4], '\n'])
            # fx = ''.join(['\n', currency, '\n\n', cash_sell,
            #              cash_buy, '\n', spot_sell, spot_buy])
            # fx_data.append(fx)

        # 文字版報價
        # fx_data = '\n==================\n'.join(fx_data)
        # content = ''.join(
        #     [title, '\n', time, '\n==================\n', fx_data])
        # content = '\n\n'.join(['臺灣銀行 即時牌告匯率', content])

        # 設定圖表和尺寸
        fig, ax = plt.subplots(figsize=(4, 5), dpi=200)

        # 關閉座標軸線
        ax.axis('off')
        ax.table(cellText=fx_table,
                 colLabels=fx_column_label, cellLoc="center", loc="center")

        # 設定標題
        ax.set_title("臺灣銀行牌告匯率")

        # 說明文字
        ax.text(0, 0, time, wrap=True)

        # 文字版報價
        # reply_content = TextSendMessage(content)

        plt.tight_layout()

        # 上傳圖片，並取得網址
        link = self.__upload_image(fig)

        # 圖片版報價
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 即時交叉匯率表
    def fxrate_cross(self):

        # 建立爬蟲所需資料
        url = 'https://ww2.money-link.com.tw/Exchange/CrossRate.aspx'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Dnt': '1',
            'Host': 'ww2.money-link.com.tw',
            'Referer': 'https://www.google.com/',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UserAgent().random
        }

        response = self.__web_requests_get(url, headers)  # 發送請求
        response.encoding = 'utf-8'

        # 解析並擷取網頁資料
        dom = etree.HTML(response.text, etree.HTMLParser())
        time = dom.xpath(
            '/html/body/div[10]/table[1]/tr[1]/td[2]/div/text()')[0]

        # 解析並擷取網頁資料
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        fx_cross = soup.select('table')[5]
        df = pd.read_html(fx_cross.prettify())[0]
        df.iloc[0, 0] = '貨幣對'
        fx_table = []

        for idx in range(0, df.shape[0]):
            fx_table.append(tuple(df.iloc[idx, :]))

        # 設定圖表和尺寸
        fig, ax = plt.subplots(figsize=(6, 3.5), dpi=200)

        # 關閉座標軸線
        ax.axis('off')
        ax.table(cellText=fx_table, cellLoc="center", loc="upper center")

        # 設定標題
        ax.set_title("交叉匯率表")

        # 說明文字
        note = f'{time}\n資料來源：富聯網'
        ax.text(0, 0.1, note, wrap=True)

        plt.tight_layout()

        # 上傳圖片，並取得網址
        link = self.__upload_image(fig)

        # 圖片版報價
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 匯率趨勢圖
    def fxrate_trend(self, currency):

        # 貨幣對清單
        fx_pair = {
            'USD': {'pair_name': '美元/台幣', 'pair_code': 'FX:USDTWD:FOREX'},
            'EUR': {'pair_name': '歐元/台幣', 'pair_code': 'FX:EURTWD:FOREX'},
            'GBP': {'pair_name': '英鎊/台幣', 'pair_code': 'FX:GBPTWD:FOREX'},
            'JPY': {'pair_name': '日元/台幣', 'pair_code': 'FX:JPYTWD:FOREX'},
            'CNY': {'pair_name': '人民幣/台幣', 'pair_code': 'FX:CNYTWD:FOREX'},
            'CAD': {'pair_name': '加拿大幣/台幣', 'pair_code': 'FX:CADTWD:FOREX'},
            'AUD': {'pair_name': '澳幣/台幣', 'pair_code': 'FX:AUDTWD:FOREX'},
            'HKD': {'pair_name': '港幣/台幣', 'pair_code': 'FX:HKDTWD:FOREX'},
            'SGD': {'pair_name': '新加坡幣/台幣', 'pair_code': 'FX:SGDTWD:FOREX'},
            'CHF': {'pair_name': '瑞士法郎/台幣', 'pair_code': 'FX:CHFTWD:FOREX'},
            'SEK': {'pair_name': '瑞典克朗/台幣', 'pair_code': 'FX:SEKTWD:FOREX'},
            'THB': {'pair_name': '泰銖/台幣', 'pair_code': 'FX:THBTWD:FOREX'},
            'MYR': {'pair_name': '馬來西亞令吉/台幣', 'pair_code': 'FX:MYRTWD:FOREX'},
            'NZD': {'pair_name': '紐元/台幣', 'pair_code': 'FX:NZDTWD:FOREX'},
            'PHP': {'pair_name': '菲律賓幣/台幣', 'pair_code': 'FX:PHPTWD:FOREX'},
            'ZAR': {'pair_name': '南非幣/台幣', 'pair_code': 'FX:ZARTWD:FOREX'},
            'KRW': {'pair_name': '韓元/台幣', 'pair_code': 'FX:KRWTWD:FOREX'},
            'IDR': {'pair_name': '印尼盾/台幣', 'pair_code': 'FX:IDRTWD:FOREX'},
            'VND': {'pair_name': '越南盾/台幣', 'pair_code': 'FX:VNDTWD:FOREX'}
        }

        item = fx_pair[currency]  # 接收查詢項目
        pair_title = item['pair_name']  # 取得標題
        pair_code = item['pair_code']  # 取得貨幣對代碼

        # 時間處理
        et = arrow.now()  # 取得當前時間
        st = et.shift(days=-183)  # 取得半年前時間
        et_stamp = int(et.timestamp())  # 轉為unix timestamp格式
        st_stamp = int(st.timestamp())  # 轉為unix timestamp格式

        # 建立爬蟲所需資料
        url = f'https://ws.api.cnyes.com/ws/api/v1/charting/history?resolution=D&symbol={pair_code}&from={et_stamp}&to={st_stamp}'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Dnt': '1',
            'Origin': 'https://invest.cnyes.com',
            'Referer': 'https://invest.cnyes.com/',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': UserAgent().random,
            'X-Cnyes-App': 'unknown',
            'X-Platform': 'WEB',
            'X-System-Kind': 'FUND_OLD_DRIVER'
        }

        response = self.__web_requests_get(url, headers)  # 發送請求

        data = response.json()['data']  # 擷取資料

        # 整理資料
        fx_trend = {'date': data['t'], 'price': data['c']}
        df = pd.DataFrame(fx_trend)  # 建立資料表
        df['date'] = pd.to_datetime(df['date'], unit='s')  # 時間格式轉換
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')  # 轉換格式
        df = df.sort_values(by='date', ascending=True)  # 按日期排序遞增
        df = df.reset_index(drop=True)  # 重設索引

        # 設定圖表和尺寸
        fig, ax = plt.subplots(figsize=(6, 4), dpi=200)

        # 繪製折線圖
        ax.plot(df['date'], df["price"], color="blue")

        # 設定X軸為日期格式
        ax.xaxis_date()

        # 設定刻度
        ax.xaxis.set_major_locator(plt.MultipleLocator(14))

        # 自動調整X軸
        plt.gcf().autofmt_xdate()

        # 顯示橫軸格線
        plt.grid()

        # 設定標題
        title = f'{pair_title} 近半年走勢圖'
        ax.set_title(title)

        # 說明文字 <------------------------------
        note = '資料來源：鉅亨網'
        ax.text(0, 0.1, note, wrap=True)

        # plt.tight_layout()

        # 上傳圖片，並取得網址
        link = self.__upload_image(fig)

        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message


# 股市資訊
class StockMarket:

    def __init__(self):
        # 讀取環境變量(金鑰)
        self.imgur_client_id = os.environ.get("IMGUR_CLIENT_ID")  # Imgur 金鑰
        self.fugle_api_key = os.environ.get("FUGLE_API_KEY")  # Fugle 金鑰

        # 建立連線物件
        self.session = requests.Session()
        retry = Retry(total=2, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.keep_alive = False

        # 鉅亨網標頭
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Dnt': '1',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'X-Platform': 'WEB'
        }

    # 發送請求
    def __web_requests_get(self, url, headers):

        response = self.session.get(url, headers=headers, timeout=7)

        while response.status_code != requests.codes.ok:
            t = random.uniform(0.5, 2.5)
            time.sleep(t)
            response = self.session.get(url, headers=headers, timeout=7)
            self.session.close()

        return response

    # 即時文字報價
    def __index_quote(self, url):
        # 建立爬蟲所需資料
        headers = self.headers
        headers['Origin'] = 'https://invest.cnyes.com'
        headers['Referer'] = 'https://invest.cnyes.com/'
        headers['X-Cnyes-App'] = 'unknown'
        headers['X-System-Kind'] = 'FUND_OLD_DRIVER'
        headers['User-Agent'] = UserAgent().random

        response = self.__web_requests_get(url, headers)  # 發送請求

        data = response.json()['data'][0]  # 擷取資料

        change_p = data['11']  # 漲跌點數

        # 漲跌、平盤符號
        if change_p > 0:
            change_symbol = '△'
        elif change_p < 0:
            change_symbol = '▽'
        else:
            change_symbol = '＝'

        # 擷取成交值並轉換
        vol = data["200067"]/100000000

        # 時間擷取和轉換
        ct = arrow.get(data['200007'], tzinfo="Asia/Taipei")
        ct = arrow.get(ct).format("YYYY-MM-DD HH:mm:ss")

        name = data["200009"]  # 商品名稱
        cp = f'\n成交： {data["6"]}'
        change = f'漲跌： {change_symbol} {data["11"]} ({data["56"]}%)\n'
        vol = f'成交值： {vol:.2f} 億元'
        op = f'開盤： {data["19"]}'
        hp = f'最高： {data["12"]}'
        lp = f'最低： {data["13"]}'
        # yp = f'昨收： {data["21"]}'

        row1 = f'{name} {ct}'  # 標的名稱 時間
        # r2 = f'{cp} / {change}'  # 成交價 變動點數
        # r3 = f'{hp} / {lp}'  # 最高 最低

        text_quote = '\n'.join([row1, cp, change, vol, op, hp, lp])

        return text_quote

    # 指數資訊
    def index_info(self, data_type, index_symbol):
        # 加權指數文字報價
        if data_type == 'q' and index_symbol == 'twse':
            url = 'https://ws.api.cnyes.com/ws/api/v1/quote/quotes/TWS:TSE01:INDEX?column=G,QUOTES'
            content = self.__index_quote(url)
            message = TextSendMessage(content)

            return message

        # 櫃買指數文字報價
        elif data_type == 'q' and index_symbol == 'tpex':
            url = 'https://ws.api.cnyes.com/ws/api/v1/quote/quotes/TWS:OTC01:INDEX?column=G,QUOTES'
            content = self.__index_quote(url)
            message = TextSendMessage(content)

            return message

    # 更新股票清單
    def __update_stock_list(self):

        # 取得當前日期
        today = arrow.now()
        today = today.format('YYYY-MM-DD')
        today = str(today)

        # 讀取股票清單
        file_path = 'src/stock_list.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if today != data['date']:

            # 建立爬蟲所需資料  資料來源為Histock
            url = 'https://histock.tw/stock/rank.aspx?p=all'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
                'Cache-Control': 'max-age=0',
                'Dnt': '1',
                'Referer': 'https://histock.tw/stock/rank.aspx?p=all',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': UserAgent().random
            }

            response = self.__web_requests_get(url, headers)  # 發送請求
            response.encoding = 'utf-8'

            # 擷取資料
            dom = etree.HTML(response.text, etree.HTMLParser())
            stock_symbol = dom.xpath('//*[@id="CPHB1_gv"]/tr/td[1]/text()')
            stock_name = dom.xpath('//*[@id="CPHB1_gv"]/tr/td[2]/a/text()')

            data = {}
            data['date'] = today
            data['stock_list'] = {}

            for idx in range(len(stock_symbol)):
                if '臺' in stock_name[idx]:
                    corp = stock_name[idx].replace('臺', '台')
                else:
                    corp = stock_name[idx]

                data['stock_list'][stock_symbol[idx]] = stock_symbol[idx]
                data['stock_list'][corp] = stock_symbol[idx]

            # 將股票清單匯出為檔案
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)

        # 讀取股票清單
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # 整理股票清單
        self.stock_symbol = data['stock_list']

    # 個股即時文字報價報價
    def __stock_quote(self, symbol):
        # 建立爬蟲所需資料
        url = f'https://ws.api.cnyes.com/ws/api/v1/quote/quotes/TWS:{symbol}:STOCK?column=K,E,KEY,M,AI'
        headers = self.headers
        headers['Origin'] = 'https://www.cnyes.com'
        headers['Referer'] = 'https://www.cnyes.com/'
        headers['X-System-Kind'] = 'LOBBY'

        response = self.__web_requests_get(url, headers)  # 發送請求

        data = response.json()['data'][0]  # 擷取資料

        change_p = data['11']  # 漲跌點數

        # 漲跌、平盤符號
        if change_p > 0:
            change_symbol = '△'
        elif change_p < 0:
            change_symbol = '▽'
        else:
            change_symbol = '＝'

        # 擷取成交值並轉換
        vol = data["200067"]/10000
        if vol >= 10000:
            vol = vol/10000
            vol = f'{vol:,.2f} 億'
        else:
            vol = f'{vol:,.2f} 萬'

        # 時間擷取和轉換
        ct = arrow.get(data['200007'], tzinfo="Asia/Taipei")
        ct = arrow.get(ct).format("YYYY-MM-DD HH:mm:ss")

        name = f'{data["200009"]} 【{data["200010"]}】'  # 商品名稱
        cp = f'\n成交： {data["6"]}'
        change = f'漲跌： {change_symbol} {data["11"]} ({data["56"]}%)\n'
        vol = f'成交量： {data["200013"]:,.2f} 張 \n成交值：{vol}元'
        op = f'開盤： {data["19"]}'
        hp = f'最高： {data["12"]}'
        lp = f'最低： {data["13"]}'

        row1 = f'{name}  {ct}'  # 名稱 時間

        text_quote = '\n'.join([row1, cp, change, vol, op, hp, lp])

        return text_quote

    # 個股資訊
    def stock_info(self, data_type, search):

        # 更新股票清單
        self.__update_stock_list()

        # 英文字母統一大寫
        search = search.upper()

        # 統一搜尋字詞
        if '臺' in search:
            search = search.replace('臺', '台')
            search = search.upper()

        # 代號搜尋 完全匹配
        if search in self.stock_symbol.keys():

            # 個股文字報價
            if data_type == 'q':
                stock_code = self.stock_symbol[search]
                content = self.__stock_quote(stock_code)
                message = TextSendMessage(content)

            else:
                message = TextSendMessage('無此功能！')

            return message

        # 代號搜尋 部分匹配
        else:
            # 文字模糊匹配
            search_result = difflib.get_close_matches(
                search, self.stock_symbol.keys(), n=10, cutoff=0.6)

            # 部分相符
            if len(search_result) != 0:
                search_result = '\n'.join(search_result)
                content = '\n\n'.join(['您可能想搜尋以下股票名稱：', search_result])

            # 完全不符
            else:
                content = '查無任何部分相符的股票名稱，請檢查後再輸入！'

            message = TextSendMessage(content)

            return message
