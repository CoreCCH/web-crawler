from bs4 import BeautifulSoup
import requests
import time
import random
import pandas as pd
from parserMethod import House591Parser

 
class rent(House591Parser):
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
        self.data={'物件':[], '月租金':[], '位置':[]}
        self.session=self.getSession()
        self.getCSRF()

    def getCSRF(self):
        __url = 'https://rent.591.com.tw/'
        __get = self.session.get(__url, headers=self.headers)
        __soup = BeautifulSoup(__get.text, 'html.parser')
        __token_item = __soup.select_one('meta[name="csrf-token"]')
        self.headers['X-CSRF-TOKEN'] = __token_item.get('content')

    def gethouselist(self, __region, __page, __error):
        # 搜尋房屋
        __url = 'https://rent.591.com.tw/home/search/rsList'
        __params = 'is_format_data=1&is_new_list=1&type=1&region='+__region+f'&firstRow={__page*30}'

        # 在 cookie 設定地區縣市，避免某些條件無法取得資料
        self.session.cookies.set('urlJumpIp', __region, domain='.591.com.tw')
        __result = self.session.get(__url, params=__params, headers=self.headers)

        # 伺服器deny
        if __result.status_code != requests.codes.ok:
            if __error >= 3:
                return 0;
            else:
                self.gethouselist(__region, __page, __error+1)
             
        __data = __result.json()

        # 頁面超出可搜尋範圍
        if(__data['status'] == 0):
            return 0;

        # 使用 map() 函數將資料取出來並轉換成新的資料結構
        self.data['物件'].extend(list(map(lambda x: x['title'], __data['data']['topData'])))
        self.data['月租金'].extend(list(map(lambda x: x['price'], __data['data']['topData'])))
        self.data['位置'].extend(list(map(lambda x: x['section_name']+x['street_name'], __data['data']['topData'])))
        
        # 隨機等待1~3秒
        time.sleep(random.uniform(1, 3))

        # Recursion
        self.gethouselist(__region, __page+1, __error)


class sale(House591Parser):
    def __init__(self):
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
        self.data={'物件':[], '價位/坪':[], '總價':[],'房間':[], '位置':[]}
        self.session=self.getSession()
        self.getCSRF()
    
    def getCSRF(self):
        __url = 'https://sale.591.com.tw/'
        __get = self.session.get(__url, headers=self.headers)
        __soup = BeautifulSoup(__get.text, 'html.parser')
        __token_item = __soup.select_one('meta[name="csrf-token"]')
        self.headers['X-CSRF-TOKEN'] = __token_item.get('content')
    
    def gethouselist(self, __region, __page, __error):
        # 搜尋房屋
        __url = 'https://sale.591.com.tw/home/search/list'
        __params = 'type=2&shType=list&regionid='+__region+f'&firstRow={__page*30}&timestamp='+str(int(time.time()))

        self.headers['device']='PC'
        self.headers['deviceid']='09d5239d-88e6-46a9-aff3-977c857aea48'
        # 在 cookie 設定地區縣市，避免某些條件無法取得資料
        self.session.cookies.set('urlJumpIp', __region, domain='.591.com.tw')
        __result = self.session.get(__url, params=__params, headers=self.headers)

        # 伺服器deny
        if __result.status_code != requests.codes.ok:
            if __error >= 3:
                return 0;
            else:
                self.gethouselist(__region, __page, __error+1)
                return 0;
             
        __data = __result.json()

        # 頁面超出可搜尋範圍
        if(int(__data['data']['total']) < __page*30):
            return 0;

        # 使用 map() 函數將資料取出來並轉換成新的資料結構
        self.data['物件'].extend(list(map(lambda x: x['title'], __data['data']['house_list'])))
        self.data['價位/坪'].extend(list(map(lambda x: x['unitprice'], __data['data']['house_list'])))
        self.data['房間'].extend(list(map(lambda x: x['room'], __data['data']['house_list'])))
        self.data['總價'].extend(list(map(lambda x: x['showprice'] if 'showprice' in __data['data']['house_list'] else '', __data['data']['house_list'])))
        self.data['位置'].extend(list(map(lambda x: x['section_name']+x['address'] if 'address' in __data['data']['house_list'] else x['section_name'], __data['data']['house_list'])))

        # 隨機等待1~3秒
        time.sleep(random.uniform(1, 3))

        # Recursion
        self.gethouselist(__region, __page+1, __error)

    

if __name__ == "__main__":
    # house591_crawler = House591Crawler()
    # house591_crawler.gethouselist('23',0,0)
    # df = pd.DataFrame(house591_crawler.data)
    # print(df)
    # df.to_excel('output.xlsx', index=False)

    # house591_crawler = rent()
    # house591_crawler.gethouselist('23',0,0)
    # df = pd.DataFrame(house591_crawler.data)
    # print(df)
    # df.to_excel('output.xlsx', index=False)

    house591_crawler = sale()
    house591_crawler.gethouselist('23',0,0)
    df = pd.DataFrame(house591_crawler.data)
    print(df)
    df.to_excel('output.xlsx', index=False)