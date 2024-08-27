# 2024.08.26

import os
import re
import time
import random

from selenium.webdriver.firefox.service import Service

# install driver
#from webdriver_manager.firefox import GeckoDriverManager as Manager
#Service(Manager().install())

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
#
from Inc.DbList.DbList import TDbList
from Inc.DbList.DbUtil import DblToXlsxSave

class TOlx():
    def __init__(self):
        Opt = Options()
        Opt.add_argument('--headless')
        service = Service('/snap/bin/firefox.geckodriver')
        self.driver = webdriver.Firefox(service=service, options=Opt)

    def __del__(self):
        self.driver.quit()

    def GetProducts(self, aUrl: str) -> list:
        print(aUrl)
        self.driver.get(aUrl)

        PageReady = 2
        time.sleep(PageReady)
        Sleep = random.randint(1, 3)
        time.sleep(Sleep)

        # WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, ".css-bc4qtv"))
        # )
        # WebDriverWait(self.driver, 10).until(
        #     lambda driver: driver.execute_script("return document.readyState") == "complete"
        # )

        Res = []
        products = self.driver.find_elements(By.CSS_SELECTOR, ".css-1grlwc9")
        pass
        for Idx, product in enumerate(products):
            Name = product.find_element(By.CSS_SELECTOR, "p.css-ki4ei7 a").text
            Price = product.find_element(By.CSS_SELECTOR, "span[data-testid='ad-price']").text
            Price = Price.replace('грн.', '').replace(' ', '')
            Url = product.find_element(By.CSS_SELECTOR, "p.css-ki4ei7 a").get_attribute('href')

            Descr = ''
            # Error: The element with the reference is stale
            # print(Idx+1, Url)
            # self.driver.get(Url)
            # time.sleep(PageReady+1)
            # Descr = self.driver.find_element(By.CSS_SELECTOR, ".css-1o924a9").text
            # self.driver.back()

            Res.append([Name, Price, Url, Descr])
        return Res

    def Parse(self, aUrl: str, aMax: int = 100) -> TDbList:
        Dbl = TDbList(['name', 'price', 'url', 'descr'])
        for i in range(0, aMax):
            Url = f'{aUrl}?page={i+1}'
            Data = self.GetProducts(Url)
            if (not Data):
                break
            Dbl.RecAdds(Data)
        return Dbl

class TRePriceList():
    @staticmethod
    def GetPatterns(aKeys: list) -> list:
        Patterns = {
            'model1': re.compile(r'(?P<model>(Dell|HP|Lenovo|Gateway) \w+ \w+ )', re.IGNORECASE),
            'model2': re.compile(r'(?P<model>(DELL|HP|Lenovo) [A-Za-z\s\d\-]+) ', re.IGNORECASE),

            'cpu1': re.compile(r'(?P<cpu>(i\d)-\w+)', re.IGNORECASE),

            'screen1': re.compile(r'(?P<screen>\d{1,2}[\.,]?\d?\")'),
            'screen2': re.compile(r"(?P<screen>\d{1,2}[\.,]?\d?\'')"),
            'screen3': re.compile(r"(?P<screen>\d{1,2}\.\d)"),

            'matrix1': re.compile(r'(?P<matrix>(HD|FHD|UHD)[ /])'),

            'ram1': re.compile(r'(?P<ram>RAM?\d{1,2}G?b?)'),
            'ram2': re.compile(r'(?P<ram>/\d{1,2}GB)', re.IGNORECASE),

            'disk1': re.compile(r'(?P<disk>(SSD|HDD)\d{1,3}[GT]?B?)', re.IGNORECASE)
        }
        return [Patterns[xKey] for xKey in aKeys]

    @staticmethod
    def Ram1(aVal: str) -> str:
        RVal = re.search(r'(\d+)([Gg]?[Bb]?)', aVal).groups()
        RVal = list(RVal)
        if (not RVal[1]):
            RVal[1] = 'gb'
        elif (not RVal[1].lower().endswith('b')):
            RVal[1] += 'b'
        return f'{RVal[0]}{RVal[1].upper()}'

    @staticmethod
    def Disk1(aVal: str) -> str:
        RVal = re.search(r'(SSD|HDD)(\d+)([GgTtBb]?)', aVal).groups()
        RVal = list(RVal)
        if (not RVal[2]):
            RVal[2] = 'gb'
        elif (not RVal[2].lower().endswith('b')):
            RVal[2] += 'b'
        return f'{RVal[1]}{RVal[2].upper()} {RVal[0]}'

    @staticmethod
    def Screen1(aVal: str) -> str:
        RVal = re.search(r'(\d+),?\d*', aVal).groups()
        return f'{RVal[0]}"'

class TReDrogobich(TRePriceList):
    def Adjust(self, aDbl: TDbList) -> TDbList:
        DblNew = TDbList(
            ['model',	'cpu', 'ram', 'disk', 'screen', 'matrix', 'os', 'price_in', 'price', 'name', 'url']
        )

        Patterns = self.GetPatterns(
            ['model1', 'cpu1', 'screen1', 'screen2', 'screen3', 'matrix1', 'ram1', 'ram2', 'disk1']
        )

        for Rec in aDbl:
            Name = Rec.name.strip()
            Parts = {}
            for xPattern in Patterns:
                Match = xPattern.search(Name)
                if (Match):
                    Group = Match.groupdict()
                    Key = tuple(Group.keys())[0]
                    if (Key not in Parts):
                        Parts.update(Group)

            RecNew = DblNew.RecAdd()
            for Key, Val in Parts.items():
                Val = Val.strip('/ ')
                if (Key == 'ram'):
                    Val = self.Ram1(Val)
                elif (Key == 'disk'):
                    Val = self.Disk1(Val)
                if (Key == 'screen'):
                    Val = self.Screen1(Val)
                RecNew.SetField(Key, Val)

            RecNew.SetField('price_in', Rec.price)
            RecNew.SetField('name', Rec.name)
            RecNew.SetField('url', Rec.url)
        return DblNew

def Main(aFile: str, aUrl: str, aMax: int):
    File = aFile + '_dbl.json'
    if (os.path.exists(File)):
        Dbl = TDbList()
        Dbl.Load(File)
    else:
        Olx = TOlx()
        Dbl = Olx.Parse(aUrl, aMax)
        print(f'Found products: {len(Dbl)}')
        Dbl.Save(File, True)
        DblToXlsxSave([Dbl], aFile + '.xlsx')

    ReDrogobich = TReDrogobich()
    DblAdj = ReDrogobich.Adjust(Dbl)
    DblToXlsxSave([DblAdj], aFile + '_price.xlsx')
    print('Done')

Main('olx_drogobich', 'https://www.olx.ua/uk/list/user/1WdU1/', 18)
#Main('olx_krig', 'https://laptopshop.olx.ua/uk/home/', 1)
