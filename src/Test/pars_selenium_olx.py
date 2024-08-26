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
        for product in products:
            Name = product.find_element(By.CSS_SELECTOR, "p.css-ki4ei7 a").text
            Price = product.find_element(By.CSS_SELECTOR, "span[data-testid='ad-price']").text
            Price = Price.replace('грн.', '').replace(' ', '')
            Url = product.find_element(By.CSS_SELECTOR, "p.css-ki4ei7 a").get_attribute('href')
            Res.append([Name, Price, Url])
        return Res

    def Parse(self, aUrl: str, aMax: int = 100) -> TDbList:
        Dbl = TDbList(['name', 'price', 'url'])
        for i in range(0, aMax):
            Url = f'{aUrl}?page={i+1}'
            Data = self.GetProducts(Url)
            if (not Data):
                break

            Dbl.RecAdds(Data)
        return Dbl

class TReDrogobich():
    def Init(self) -> list:
        reModel1 = re.compile(r'(?P<model>(Dell|HP|Lenovo|Gateway) \w+ \w+ )', re.IGNORECASE)
        #reModel2 = re.compile(r'(?P<model>(DELL|HP|Lenovo) [A-Za-z\s\d\-]+) ', re.IGNORECASE)

        reCpu1 = re.compile(r'(?P<cpu>(i\d)-\w+)', re.IGNORECASE)

        reScreen1 = re.compile(r'(?P<screen>\d{1,2}[\.,]?\d?\")')
        reScreen2 = re.compile(r"(?P<screen>\d{1,2}[\.,]?\d?\'')")
        reScreen3 = re.compile(r"(?P<screen>\d{1,2}\.\d)")

        reMatrix1 = re.compile(r'(?P<matrix>(HD|FHD|UHD)[ /])')

        reRam1 = re.compile(r'(?P<ram>RAM?\d{1,2}G?b?)')
        reRam2 = re.compile(r'(?P<ram>/\d{1,2}GB)', re.IGNORECASE)

        reDisk1 = re.compile(r'(?P<disk>(SSD|HDD)\d{1,3}[GT]?B?)', re.IGNORECASE)
        return [reModel1, reCpu1, reScreen1, reScreen2, reScreen3, reMatrix1, reRam1, reRam2, reDisk1]

    def Adjust(self, aDbl: TDbList) -> TDbList:
        DblNew = TDbList(['model',	'cpu', 'ram', 'disk', 'screen', 'matrix', 'price_in', 'name', 'url'])

        Patterns = self.Init()
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
                    RVal = re.search(r'(\d+)([Gg]?[Bb]?)', Val).groups()
                    RVal = list(RVal)
                    if (not RVal[1]):
                        RVal[1] = 'Gb'
                    Val = f'{RVal[0]}{RVal[1].upper()}'
                elif (Key == 'disk'):
                    RVal = re.search(r'(SSD|HDD)(\d+)([GgTtBb]?)', Val).groups()
                    RVal = list(RVal)
                    if (not RVal[2]):
                        RVal[2] = 'Gb'
                    elif (not RVal[2].lower().endswith('b')):
                        RVal[2] += 'b'
                    Val = f'{RVal[1]}{RVal[2].upper()} {RVal[0]}'
                if (Key == 'screen'):
                    RVal = re.search(r'(\d+),?\d*', Val).groups()
                    Val = f'{RVal[0]}"'

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
        Dbl.Save(File, True)
        DblToXlsxSave([Dbl], aFile + '.xlsx')

    #ReDrogobich = TReDrogobich()
    #DblAdj = ReDrogobich.Adjust(Dbl)
    #DblToXlsxSave([DblAdj], aFile + '_price.xlsx')

#Main('olx_drogobich', 'https://www.olx.ua/uk/list/user/1WdU1/', 14)
Main('olx_krig', 'https://laptopshop.olx.ua/uk/home/', 1)
