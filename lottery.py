import random
from linebot.models import *


class LotteryMenu:
    '''
    樂透選單

    輸入：
    由app.py作為主控，透過richmenu呼叫lottery_menu
    輸出：
    讓選單顯示在聊天室中

    '''

    # 樂透選單
    def lottery_menu(self):
        menu = TemplateSendMessage(
            alt_text='樂透選單',    # 訊息預覽
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.taiwanlottery.com.tw/images/intx_logo01.jpg',
                        title=None,
                        text='威力彩',
                        actions=[
                            URIAction(
                                label='威力彩開獎結果',
                                uri='https://www.taiwanlottery.com.tw/lotto/superlotto638/history.aspx'
                            ),
                            # PostbackAction(
                            #     label='威力彩開獎結果',
                            #     text = '威力彩開獎結果',
                            #     data='彩券 威力彩開獎結果'
                            # ),
                            PostbackAction(
                                label='產生威力彩投注號碼',
                                text=None,
                                data='LGN_superlotto'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.taiwanlottery.com.tw/images/intx_logo02.jpg',
                        title=None,
                        text='大樂透',
                        actions=[
                            URIAction(
                                label='大樂透開獎結果',
                                uri='https://www.taiwanlottery.com.tw/lotto/Lotto649/history.aspx'
                            ),
                            # PostbackAction(
                            #     label='大樂透開獎結果',
                            #     text = '大樂透開獎結果',
                            #     data='彩券 大樂透開獎結果'
                            # ),
                            PostbackAction(
                                label='產生大樂透投注號碼',
                                text=None,
                                data='LGN_biglotto'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.taiwanlottery.com.tw/images/intx_logo03.jpg',
                        title=None,
                        text='今彩539',
                        actions=[
                            URIAction(
                                label='今彩539開獎結果',
                                uri='https://www.taiwanlottery.com.tw/Lotto/Dailycash/history.aspx'
                            ),
                            # PostbackAction(
                            #     label='今彩539開獎結果',
                            #     text = '今彩539開獎結果',
                            #     data='彩券 今彩539開獎結果'
                            # ),
                            PostbackAction(
                                label='產生今彩539投注號碼',
                                text=None,
                                data='LGN_dailycash'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.taiwanlottery.com.tw/images/intx_logo13.jpg',
                        title=None,
                        text='雙贏彩',
                        actions=[
                            URIAction(
                                label='雙贏彩開獎結果',
                                uri='https://www.taiwanlottery.com.tw/Lotto/Lotto1224/history.aspx'
                            ),
                            # PostbackAction(
                            #     label='雙贏彩開獎結果',
                            #     text = '雙贏彩開獎結果',
                            #     data='彩券 雙贏彩開獎結果'
                            # ),
                            PostbackAction(
                                label='產生雙贏彩投注號碼',
                                text=None,
                                data='LGN_twowin'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.taiwanlottery.com.tw/images/intx_logo05.jpg',
                        title=None,
                        text='3星彩',
                        actions=[
                            URIAction(
                                label='3星彩開獎結果',
                                uri='https://www.taiwanlottery.com.tw/Lotto/3D/history.aspx'
                            ),
                            # PostbackAction(
                            #     label='3星彩開獎結果',
                            #     text = '3星彩開獎結果',
                            #     data='彩券 3星彩開獎結果'
                            # ),
                            PostbackAction(
                                label='產生3星彩投注號碼',
                                text=None,
                                data='LGN_3stars'
                            ),
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://www.taiwanlottery.com.tw/images/intx_logo06.jpg',
                        title=None,
                        text='4星彩',
                        actions=[
                            URIAction(
                                label='4星彩開獎結果',
                                uri='https://www.taiwanlottery.com.tw/Lotto/4D/history.aspx'
                            ),
                            # PostbackAction(
                            #     label='4星彩開獎結果',
                            #     text = '4星彩開獎結果',
                            #     data='彩券 4星彩開獎結果'
                            # ),
                            PostbackAction(
                                label='產生4星彩投注號碼',
                                text=None,
                                data='LGN_4stars'
                            ),
                        ]
                    )
                ]
            )
        )

        return menu


class LotteryGenerateNums:
    '''
    彩券號碼產生器

    輸入：
    透過app.py呼叫此物件
    輸出：
    回傳樂透幸運號碼

    '''

    def __init__(self):

        # 切換樂透產生號碼
        self.lgn_switch = {
            'LGN_superlotto': self.generate_superlotto(),
            'LGN_biglotto': self.generate_biglotto(),
            'LGN_dailycash': self.generate_dailycash(),
            'LGN_twowin': self.generate_twowin(),
            'LGN_3stars': self.generate_3stars(),
            'LGN_4stars': self.generate_4stars(),
        }

    # 處理樂透產生號碼
    def lgn_process(self, receive):
        content = self.lgn_switch[receive]
        return content

    # 號碼產生器
    def __generate_num(self, limit, count):
        numbers = random.sample(range(1, limit + 1), count)
        numbers.sort()

        numbers_str = [f"{number:02d}" for number in numbers]
        numbers_str = ', '.join(numbers_str)

        return numbers_str

    # 產生組數設定
    def __lottery_sets(self, limit, count, num_of_sets):
        all_numbers = []
        for _ in range(num_of_sets):
            numbers_str = self.__generate_num(limit, count)
            all_numbers.append(numbers_str)

        return all_numbers

    # 產生五組威力採號碼
    def generate_superlotto(self, num_of_sets=5):
        all_numbers = []
        for _ in range(num_of_sets):
            area_a = self.__generate_num(38, 6)
            area_b = str(random.randint(1, 8))
            all_numbers.append((area_a, area_b))

        all_numbers = '\n-----------------------\n'.join(
            [f'第{idx+1}組\n第一區：{numbers[0]} \n第二區：{numbers[1]}' for idx, numbers in enumerate(all_numbers)])
        all_numbers = '\n\n'.join(['威力彩幸運號碼組合：', all_numbers, '祝您早日中大獎！'])

        message = TextSendMessage(all_numbers)

        return message

    # 產生五組大樂透號碼
    def generate_biglotto(self, num_of_sets=5):
        all_numbers = self.__lottery_sets(49, 6, num_of_sets)

        all_numbers = '\n-----------------------\n'.join(
            [f'第{idx+1}組： {numbers}' for idx, numbers in enumerate(all_numbers)])
        all_numbers = '\n\n'.join(['大樂透幸運號碼組合：', all_numbers, '祝您早日中大獎！'])

        message = TextSendMessage(all_numbers)

        return message

    # 產生五組今彩539號碼
    def generate_dailycash(self, num_of_sets=5):
        all_numbers = self.__lottery_sets(39, 5, num_of_sets)

        all_numbers = '\n-----------------------\n'.join(
            [f'第{idx+1}組： {numbers}' for idx, numbers in enumerate(all_numbers)])
        all_numbers = '\n\n'.join(['今彩539幸運號碼組合：', all_numbers, '祝您早日中大獎！'])

        message = TextSendMessage(all_numbers)

        return message

    # 產生五組雙贏彩號碼
    def generate_twowin(self, num_of_sets=5):
        all_numbers = self.__lottery_sets(24, 12, num_of_sets)

        all_numbers = '\n-----------------------\n'.join(
            [f'第{idx+1}組： {numbers}' for idx, numbers in enumerate(all_numbers)])
        all_numbers = '\n\n'.join(['雙贏彩幸運號碼組合：', all_numbers, '祝您早日中大獎！'])

        message = TextSendMessage(all_numbers)

        return message

    # 產生五個三星彩號碼
    def generate_3stars(self, num_of_sets=5):
        all_numbers = random.sample(range(1, 999 + 1), num_of_sets)
        for idx, number in enumerate(all_numbers):
            all_numbers[idx] = f"{number:03d}"

        all_numbers = '\n-------------\n'.join(
            [f'第{idx+1}個： {numbers}' for idx, numbers in enumerate(all_numbers)])
        all_numbers = '\n\n'.join(['3星彩幸運號碼：', all_numbers, '祝您早日中大獎！'])

        message = TextSendMessage(all_numbers)

        return message

    # 產生五個四星彩號碼
    def generate_4stars(self, num_of_sets=5):
        all_numbers = random.sample(range(1, 9999 + 1), num_of_sets)
        for idx, number in enumerate(all_numbers):
            all_numbers[idx] = f"{number:04d}"

        all_numbers = '\n-----------------\n'.join(
            [f'第{idx+1}個： {numbers}' for idx, numbers in enumerate(all_numbers)])
        all_numbers = '\n\n'.join(['4星彩幸運號碼：', all_numbers, '祝您早日中大獎！'])

        message = TextSendMessage(all_numbers)

        return message
