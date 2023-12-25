import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import time
import random
import difflib
import js2py
from linebot.models import *


class WeatherMenu:

    '''
    天氣選單

    輸入：
    由app.py作為主控，透過richmenu呼叫menu
    輸出：
    讓指定的選單回傳到聊天室

    '''

    # 天氣選單
    def menu(self):
        menu = TemplateSendMessage(
            alt_text='查天氣',    # 訊息預覽
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://cdn.pixabay.com/photo/2017/01/17/16/46/cloud-1987416_1280.png',
                        title=None,
                        text='🔍天氣查詢',
                        actions=[
                            URIAction(
                                label='目前位置天氣',
                                uri='https://line.me/R/nv/location/'
                            ),
                            PostbackAction(
                                label='天氣預報',
                                text=None,
                                data='wx_quickreply_first'
                            ),
                            URIAction(
                                label='更多天氣資訊',
                                uri='https://www.cwa.gov.tw/V8/C/'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.cwa.gov.tw/Data/fcst_img/SFCcombo.jpg',
                        title=None,
                        text='天氣圖 1',
                        actions=[
                            PostbackAction(
                                label='衛星雲圖(真實色)',
                                text=None,
                                data='wx img_satellite'
                            ),
                            PostbackAction(
                                label='雷達回波圖',
                                text=None,
                                data='wx img_radar'
                            ),
                            PostbackAction(
                                label='雨量圖(日累積)',
                                text=None,
                                data='wx img_rainfall'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.cwa.gov.tw/Data/fcst_img/SFCcombo.jpg',
                        title=None,
                        text='天氣圖 2',
                        actions=[
                            PostbackAction(
                                label='溫度分布圖',
                                text=None,
                                data='wx img_temperature'
                            ),
                            PostbackAction(
                                label='即時閃電圖',
                                text=None,
                                data='wx img_lightning'
                            ),
                            PostbackAction(
                                label='紫外線觀測圖',
                                text=None,
                                data='wx img_uvi'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.cwa.gov.tw/V8/assets/img/radar/radar_coverage.jpg',
                        title=None,
                        text='📡雷達回波圖(降雨)',
                        actions=[
                            PostbackAction(
                                label='北台灣雷達回波圖',
                                text=None,
                                data='wx img_radar_north'
                            ),
                            PostbackAction(
                                label='中台灣雷達回波圖',
                                text=None,
                                data='wx img_radar_central'
                            ),
                            PostbackAction(
                                label='南台灣雷達回波圖',
                                text=None,
                                data='wx img_radar_south'
                            ),
                        ]
                    )
                ]
            )
        )

        return menu

    # 天氣預報 快速回覆紐 第一頁
    def quickreply_first(self):
        menu = TextSendMessage(
            text='第一頁\n◀左右滑動▶\n點擊縣市查看天氣預報⛅',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍基隆市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10017'
                        )
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍台北市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=63'
                        )
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍新北市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=65'
                        )
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍桃園市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=68'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍新竹市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10018'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍新竹縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10004'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍苗栗縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10005'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍台中市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=66'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍彰化縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10007'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍南投縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10008'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍雲林縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10009'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=PostbackAction(
                            label='下一頁▶',
                            text=None,
                            data='wx_quickreply_second'
                        ),
                    ),
                ]
            )
        )

        return menu

    # 天氣預報 快速回覆紐 第二頁
    def quickreply_second(self):
        menu = TextSendMessage(
            text='第二頁\n◀左右滑動▶\n點擊縣市查看天氣預報⛅',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍嘉義市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10020'
                        )
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍嘉義縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10010'
                        )
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍台南市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=67'
                        )
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍高雄市',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=64'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍屏東縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10013'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍宜蘭縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10002'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍花蓮縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10015'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍台東縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10014'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍澎湖縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=10016'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍金門縣',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=09020'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=URIAction(
                            label='📍連江縣(馬祖)',
                            uri='https://www.cwa.gov.tw/V8/C/W/County/County.html?CID=09007'
                        ),
                    ),
                    QuickReplyButton(
                        image_url=None,
                        action=PostbackAction(
                            label='◀上一頁',
                            text=None,
                            data='wx_quickreply_first'
                        ),
                    ),
                ]
            )
        )

        return menu


class WeatherProcess:
    '''
    處理天氣圖
    '''

    # 初始化
    def __init__(self):
        wx_info = WeatherInfo()

        # 天氣圖
        self.wx_graph_switch = {
            'img_satellite': wx_info.graph_satellite(),
            'img_radar': wx_info.graph_radar(),
            'img_rainfall': wx_info.graph_rainfall(),
            'img_temperature': wx_info.graph_temperature(),
            'img_lightning': wx_info.graph_lightning(),
            'img_uvi': wx_info.graph_uvi(),
            'img_radar_north': wx_info.graph_radar_north(),
            'img_radar_central': wx_info.graph_radar_central(),
            'img_radar_south': wx_info.graph_radar_south()
        }

    def process(self, receive):
        receive = receive.split(' ')[1]
        content = self.wx_graph_switch[receive]
        return content


class WeatherInfo:
    '''
    查詢氣象資料

    輸入：
    由app.py作為主控，透過WeatherMenu查詢氣象資料
    輸出：
    將氣象資料回傳到聊天室

    '''

    # 初始化
    def __init__(self):

        # 讀取城市代碼
        file_path = 'src/code_city.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.citycode = json.load(file)

        # 讀取區域代碼
        file_path = 'src/code_area.json'
        with open(file_path, 'r', encoding='utf-8') as file:
            self.areacode = json.load(file)

    # 發送請求

    def __web_requests(self, url, headers):

        response = requests.get(url, headers=headers, timeout=5)

        while response.status_code != requests.codes.ok:
            t = random.uniform(0.5, 2.5)
            time.sleep(t)
            response = requests.get(url, headers=headers, timeout=5)

        return response

    # 查詢目前天氣
    def __current_weather(self, city, area):

        # 建立爬蟲所需資料
        url = f'https://www.cwa.gov.tw/Data/js/GT/TableData_GT_T_{city}.js'
        headers = {
            'User-Agent': UserAgent().random
        }

        response = self.__web_requests(url, headers)  # 發送請求

        # 解析內容
        soup = BeautifulSoup(response.text, "html.parser")
        js_code = str(soup)

        # 觀測時間，將js內容轉為dict
        obs_time = js_code.split('var')[1]
        obs_time = ''.join(['var', obs_time])
        obs_time = js2py.eval_js(obs_time)
        obs_time = obs_time.to_dict()['C']
        obs_time = obs_time.replace('<br/>', ' ')

        # 觀測資料，將js內容轉為dict
        obs_data = js_code.split('var')[2]
        obs_data = ''.join(['var', obs_data])
        obs_data = js2py.eval_js(obs_data)
        obs_data = obs_data.to_dict()

        obs_info = obs_data[area]
        obs_abs = "觀測時間：{obs_time}\n溫度： {C_T}°C\n體感溫度： {C_AT}°C\n相對濕度： {RH}%\n時雨量： {Rain}mm" \
            .format(obs_time=obs_time, **obs_info)

        obs_abs = '\n'.join(['--------天氣觀測--------', obs_abs])

        return obs_abs

    # 天氣描述
    def __describe_weather(self, city):

        # 建立爬蟲所需資料
        url = 'https://www.cwa.gov.tw/Data/js/fcst/W50_Data.js?'
        headers = {
            'User-Agent': UserAgent().random
        }

        response = self.__web_requests(url, headers)  # 發送請求

        # 解析內容
        soup = BeautifulSoup(response.text, "html.parser")
        js_code = str(soup)

        # 將JavaScript轉換為dict
        all_dsc = js2py.eval_js(js_code)
        all_dsc = all_dsc.to_dict()

        # 資料整理
        sec_1 = f"小提醒：\n{all_dsc[city]['Title']}"
        sec_2 = f"更新時間：{all_dsc[city]['DataTime']}"
        sec_3 = '\n'.join(all_dsc[city]['Content'])
        weather_desc = '\n\n'.join([sec_1, sec_2, sec_3])
        weather_desc = '\n'.join(['--------天氣概要--------', weather_desc])

        return weather_desc

    # 空氣品質
    def __aq_info(self, city):

        # 建立爬蟲所需資料
        url = 'https://www.cwa.gov.tw/Data/js/AirQuality.js?'
        headers = {
            'User-Agent': UserAgent().random
        }

        response = self.__web_requests(url, headers)  # 發送請求

        # 解析內容
        soup = BeautifulSoup(response.text, "html.parser")
        js_code = str(soup)

        # 將JavaScript轉換為dict
        all_aq = js2py.eval_js(js_code)
        all_aq = all_aq.to_dict()

        # 整理氣象局資料
        aq_loc = all_aq[city]['SiteName']['C']  # 擷取空氣品質觀測站名稱
        aq_site = f"觀測站：{aq_loc}"
        aq_index = f"AQI：{all_aq[city]['AQI']}"

        # 取得完整AQ資料，資料說明請見：https://data.gov.tw/dataset/40448
        # 建立爬蟲所需資料
        url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
        headers = {
            'User-Agent': UserAgent().random
        }

        response = self.__web_requests(url, headers)  # 發送請求
        aq_data = response.json()

        for aq_info in aq_data['records']:
            if aq_info['sitename'] == aq_loc:
                break

        aq_desc = f"空氣品質{aq_info['status']}"
        aq_pm25 = f"PM2.5： {aq_info['pm2.5']} μg/m3"
        aq_pm10 = f"PM10： {aq_info['pm10']} μg/m3"

        aq_summary = '\n'.join(
            ['--------空氣品質--------', aq_site, aq_desc, aq_index, aq_pm25, aq_pm10])

        return aq_summary

    # 查詢目前位置天氣
    def query_weather(self, address):

        address = address.replace('台', '臺')

        # 舊 擷取和轉換地址編碼
        # for cityname in self.citycode.keys():
        #     if cityname in address:
        #         city = self.citycode[cityname]

        #         for areaname in self.areacode.keys():
        #             if areaname in address:
        #                 area = self.areacode[areaname]
        #                 break

        # 新 擷取和轉換地址編碼
        areaname = difflib.get_close_matches(
            address, self.areacode.keys(), n=1, cutoff=0.2)  # 模糊比對
        area = self.areacode[areaname[0]]

        for areaname in self.citycode.keys():
            if areaname[0:3] in address:
                city = self.citycode[areaname[0:3]]
                break

        # 目前天氣
        current_weather = self.__current_weather(city, area)

        # 空氣品質
        aq_info = self.__aq_info(city)

        # 天氣描述
        describe_weather = self.__describe_weather(city)

        # 整理內容
        summary_weather = '\n\n'.join(
            [address, current_weather, aq_info, describe_weather])

        message = TextSendMessage(summary_weather)

        return message

    # 真實色衛星雲圖
    def graph_satellite(self):
        link = 'https://www.cwa.gov.tw/Data/satellite/LCC_VIS_TRGB_2750/LCC_VIS_TRGB_2750.jpg'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 雷達回波圖
    def graph_radar(self):
        link = 'https://www.cwa.gov.tw/Data/radar/CV1_TW_3600.png'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 雨量圖
    def graph_rainfall(self):
        link = 'https://www.cwa.gov.tw/Data/rainfall/QZJ.jpg'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 溫度分布圖
    def graph_temperature(self):
        link = 'https://www.cwa.gov.tw/Data/temperature/temp.jpg'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 即時閃電圖
    def graph_lightning(self):
        link = 'https://www.cwa.gov.tw/Data/lightning/lightning_s.jpg'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 紫外線圖
    def graph_uvi(self):
        link = 'https://www.cwa.gov.tw/Data/UVI/UVI_CWB.png'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 北台灣雷達回波圖
    def graph_radar_north(self):
        link = 'https://www.cwa.gov.tw/Data/radar_rain/CV1_RCSL_3600/CV1_RCSL_3600.png'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 中台灣雷達回波圖
    def graph_radar_central(self):
        link = 'https://www.cwa.gov.tw/Data/radar_rain/CV1_RCNT_3600/CV1_RCNT_3600.png'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message

    # 南台灣雷達回波圖
    def graph_radar_south(self):
        link = 'https://www.cwa.gov.tw/Data/radar_rain/CV1_RCLY_3600/CV1_RCLY_3600.png'
        message = ImageSendMessage(
            original_content_url=link, preview_image_url=link)

        return message
