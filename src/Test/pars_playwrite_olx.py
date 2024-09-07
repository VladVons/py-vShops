# pip install playwright
# playwright install
# playwright install-deps


import time
import random
from playwright.sync_api import sync_playwright


class TOlx:
    def __init__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=not True)
        self.page = self.browser.new_page()

    def GetProducts(self, aUrl: str) -> list:
        print(aUrl)
        self.page.goto(aUrl)

        PageReady = 2
        time.sleep(PageReady)
        #Sleep = random.randint(1, 3)
        #time.sleep(Sleep)

        self.page.wait_for_selector(".css-bc4qtv", timeout=10000)

        Res = []
        products = self.page.query_selector_all(".css-1grlwc9")

        for product in products:
            Name = product.query_selector("p.css-ki4ei7 a").inner_text()
            Price = product.query_selector("span[data-testid='ad-price']").inner_text()
            Price = Price.replace('грн.', '').replace(' ', '')
            Url = product.query_selector("p.css-ki4ei7 a").get_attribute('href')
            Res.append([Name, Price, Url])

        return Res

    def __del__(self):
        self.browser.close()
        self.playwright.stop()

Olx = TOlx()
Olx.GetProducts('https://www.olx.ua/uk/list/user/1WdU1/?page=1')
