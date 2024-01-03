import re
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from lxml import etree
import time
import random
from linebot.models import *


class Whoscall:

    def __init__(self):
        # 初始化連線物件
        self.session = requests.Session()
        retry = Retry(total=2, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        self.session.keep_alive = False

    # 來電反查選單
    def menu(self):
        menu = TemplateSendMessage(
            alt_text='來電反查',    # 訊息預覽
            template=ButtonsTemplate(
                thumbnail_image_url='https://cdn.pixabay.com/photo/2017/07/28/05/12/i-phone-2547677_1280.jpg',
                title='來電反查',
                text='查詢不明來電、簡訊',
                actions=[
                    PostbackAction(
                        label='📖使用說明📖',
                        text=None,
                        data='whoscall_explain'
                    ),
                    MessageAction(
                        label='手機號碼輸入範例',
                        text='@0911510914'
                    ),
                    MessageAction(
                        label='市話號碼輸入範例',
                        text='@0223491234'
                    ),

                ]
            )
        )

        return menu

    # 來電反查使用說明
    def explain(self):
        # content = '\n'.join(['☎使用說明', '以下為輸入格式：', '@0911510914', '@0911-510-914', '@+886 911-510-914', '@0223491234'])
        content = TextSendMessage(
            '☎使用說明 \n以下為輸入格式： \n@0911510914 \n@0911-510-914 \n@+886 911-510-914 \n@0223491234 \n@02-23491234 \n\n查詢需要時間，請稍等！\n同時請勿嘗試撥打以上電話號碼\n\n資料來源：\nhttps://whocall.cc/')
        return content

    # 檢查電話號碼規則
    def check_pn(self, pn):

        pn = re.sub(r"\W+", "", pn)  # 移除空白、符號

        # 符合規則，進行網路爬蟲
        if pn.isdigit():
            content = self.__query_pn(pn)
            return TextSendMessage(content)

        # 不符合規則，並回傳錯誤訊息
        else:
            content = '您輸入的電話號碼不符格式！'
            return TextSendMessage(content)

    # 使用網路執行查詢號碼
    def __query_pn(self, pn) -> str:

        # 建立爬蟲所需資料
        url = f'https://whocall.cc/search/{pn}'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Dnt': '1',
            'Host': 'whocall.cc',
            'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': UserAgent().random
        }

        try:
            response = self.session.get(
                url, headers=headers, timeout=5)  # 發送請求

        except Exception as e:
            print('-------------------------------------------------\n',
                  e, '\n-------------------------------------------------')

        finally:
            # 若有回應，解析內容
            if 'response' in vars():

                # 判斷連線是否正常
                if response.status_code == requests.codes.ok:

                    response.encoding = 'utf-8'

                    dom = etree.HTML(response.text, etree.HTMLParser())

                    teletype = dom.xpath(
                        '//*[@id="comment"]/div[2]/div[1]/div[2]/div/div/dic/div/table/tbody/tr[1]/td[2]/text()')[0]
                    telecom = dom.xpath(
                        '//*[@id="comment"]/div[2]/div[1]/div[2]/div/div/dic/div/table/tbody/tr[2]/td[2]/text()')[0]
                    querycount = dom.xpath(
                        '//*[@id="comment"]/div[2]/div[1]/div[2]/div/div/dic/div/table/tbody/tr[3]/td[2]/text()')[0]
                    all_comment = dom.xpath(
                        "//div[@class='card-body text-start']/p[@class='card-text']/text()")

                    pn_info = ''.join(
                        [f'{pn} 的查詢結果', '\n---------------------'])
                    teletype = f'電話類型： {teletype}'
                    telecom = f'電信公司： {telecom}'
                    querycount = f'查詢次數： {querycount}'

                    all_comment = '\n'.join(
                        [f'第{idx+1}則回報： {comment}' for idx, comment in enumerate(all_comment)])

                    # 若無回報資料
                    if len(all_comment) == 0:
                        all_comment = '無任何回報資料'

                    all_comment = '\n'.join(['-----最近回報-----', all_comment])

                    message = '\n'.join(
                        [pn_info, teletype, telecom, querycount, all_comment])

            # 若無回應
            else:
                message = f'查無「{pn}」此電話號碼！\n請檢查輸入是否錯誤！'

            return message


class OtherFunction:

    # 查詢本周油價
    def query_oil_price(self):

        # 建立爬蟲所需資料
        url = 'https://www.cpc.com.tw/GetOilPriceJson.aspx?type=TodayOilPriceString'
        headers = {
            # 'Accept': '*/*',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'Dnt': '1',
            # 'Sec-Ch-Ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            # 'Sec-Ch-Ua-Mobile': '?0',
            # 'Sec-Ch-Ua-Platform': '"Windows"',
            # 'Sec-Fetch-Dest': 'empty',
            # 'Sec-Fetch-Mode': 'cors',
            # 'Sec-Fetch-Site': 'same-origin',
            'User-Agent': UserAgent().random
        }

        response = requests.get(url, headers=headers, timeout=5)  # 發送請求

        while response.status_code != requests.codes.ok:
            t = random.uniform(0.5, 2.5)
            time.sleep(t)
            response = requests.get(url, headers=headers, timeout=5)

        response.encoding = 'utf-8'

        data = response.json()
        soup = BeautifulSoup(data['UpOrDown_Html'], "html.parser")
        dom = etree.HTML(str(soup))

        update = f"最新資料日期： {data['PriceUpdate']}"
        gasoline92 = f"92無鉛價格： {data['sPrice1']} 元"
        gasoline95 = f"95無鉛價格： {data['sPrice2']} 元"
        gasoline98 = f"98無鉛價格： {data['sPrice3']} 元"
        diesel = f"超級柴油價格： {data['sPrice5']} 元"
        content = '\n'.join(['中油汽柴油價格\n', update, '=====本周油價=====',
                            gasoline92, gasoline95, gasoline98, diesel])

        message = TextSendMessage(content)

        return message
