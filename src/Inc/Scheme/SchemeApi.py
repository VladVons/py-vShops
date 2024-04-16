# Created: 2022.06.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import re
from bs4 import BeautifulSoup
#
from Inc.Util.ModHelp import GetClass
from Inc.Misc.Misc import FilterMatch
from .Utils import DigSplit, TInStock, SoupGetParentsObj
from .SchemeApiBase import TSchemeApiBase


InStock = TInStock()


class TSchemeExt():
    def __init__(self, aParent):
        self.Parent = aParent

    def list_map(self, aVal: list, aItem: list) -> list:
        '''
        call pipe mapper over a list
          ["list_map", [[
            ["get", ["offers"]],
            ["list", [0]],
            ["get", ["url"]]
          ]]]
        '''

        Res = []
        for x in aVal:
            Data = self.Parent.ParsePipes(x, aItem, 'list_map')
            if (Data is not None):
                Res.append(Data)
        return Res

    def url_pad(self, aVal: str) -> str:
        '''
        pad url with host prefix
        ["url_pad"]
        '''

        if (not aVal.startswith('http')):
            aVal = self.Parent.Var.get('$host') + '/' + aVal.strip('/')
        return aVal

    def var_get(self, _aNotUsed: object, aName: str) -> object:
        '''
        get variable
        ["var_get", ["$root"]]
        '''

        Res = self.Parent.Var.get(aName)
        if (not Res):
            self.Parent.Err.append('%s (unknown)' % (aName))
        return Res

    def var_set(self, aVal: object, aName: str) -> object:
        '''
        set current chain value to variable
        ["var_set", ["$Price"]]
        '''

        self.Parent.Var[aName] = aVal
        return aVal


class TSchemeApi(TSchemeApiBase):
    @staticmethod
    def get_text(aVal: BeautifulSoup, aDelim = '\n') -> str:
        '''
        strip object from any tags
        ["get_text", [": "]]
        '''
        return aVal.get_text(strip=True, separator=aDelim)

    @staticmethod
    def _text(aVal: BeautifulSoup) -> str:
        '''
        equal to text + strip
        ["text"]
        '''

        return TSchemeApi.strip(aVal.get_text())

    @staticmethod
    def price(aVal: str) -> list:
        '''
        get price
        ["price"]
        '''

        Before, Dig, After = DigSplit(aVal)
        if (not Dig):
            Dig = '0'

        if (not After) and (Before):
            After = Before

        return [float(Dig), After.lower()]

    @staticmethod
    def price_find(aVal: str, aCur: str = 'грн') -> list:
        r'''
        get prices from string using regEx r'[\d\.]{2,}\s*' + aCur
        ["price_find"]
        '''

        Pattern = r'[\d\.]{2,}\s*' + aCur
        Res = re.findall(Pattern, aVal)
        if (Res):
            return Res

    @staticmethod
    def stock(aVal: str, aPresent: bool = True) -> bool:
        '''
        Get stock availability
        ["stock"]
        '''

        return InStock.Check(aVal, aPresent) == aPresent

    @staticmethod
    def serial_check(aVal: str, aLen: int = 5) -> str:
        '''
        check ranges [A..Z], [0..9], [-/ ] and length >= aLen
        ["serial_check"]
        '''

        if (len(aVal) >= aLen):
            Res = [x for x in aVal if ('A' <= x <= 'Z') or (x in '0123456789-/. ')]
            if (len(aVal) == len(Res)):
                return aVal

    @staticmethod
    def serial_find(aVal: str, aMatch: str = r'[A-Z0-9\-\./]{5,}') -> str:
        '''
        get serial number with regex matches
        ["serial_find"]
        '''

        #Res = ReCmp_Serial.findall(aVal)
        Res = re.findall(aMatch, aVal)
        if (Res):
            return Res

    @staticmethod
    def breadcrumb(aVal: BeautifulSoup, aFind: list, aIdx: int, aChain: bool = True) -> str:
        '''
        equal to find_all() + list()
        ["breadcrumb", [["a"], -1]]
        '''

        if (hasattr(aVal, 'find_all')):
            Items = aVal.find_all(*aFind)
            if (Items):
                if (aChain):
                    Items = Items if (aIdx == -1) else Items[:aIdx + 1]
                    Arr = [TSchemeApi.strip(x.text) for x in Items]
                    Arr = [x for x in Arr if (len(x) > 1)]
                    Res = '/'.join(Arr)
                else:
                    Res = Items[aIdx].text.strip()
                return Res

    @staticmethod
    def app_json(aVal: BeautifulSoup, aFind: dict = None) -> dict:
        '''
        searches value in sections <script>application/ld+json</script>
        ["app_json", [{"@type": "product"}]]
        '''
        if (aFind is None):
            aFind = {'@type': 'product'}

        Res = {}
        Items = aVal.find_all('script', type='application/ld+json')
        for x in Items:
            Data: str = x.text
            #Pos1 = Data.find('{')
            #Pos2 = Data.rfind('}')
            #if (Pos1 == -1) or (Pos2 == -1):
            #    continue
            #Data = Data[Pos1 : Pos2 + 1]

            try:
                Data = json.loads(Data, strict=False)
            except ValueError:
                return None

            if (isinstance(Data, list)):
                Data = Data[0]

            if (isinstance(Data, dict)):
                if (aFind):
                    Match = FilterMatch(Data, aFind)
                    if (Match == aFind):
                        return Data
                else:
                    Name = Data.get('@type')
                    Res[Name] = Data
        if (len(Res) > 0):
            return Res

    @staticmethod
    def find_parent(aVal: BeautifulSoup, aStr: str, aDepth: int = 1) -> object:
        '''
        find parent object by text
        ["find_parent", ["hello", [3]]]
        '''

        Items = aVal.findAll(string=re.compile(aStr))
        if (Items):
            Res = SoupGetParentsObj(aVal, Items, aDepth)
            return Res[0][-1]

    @staticmethod
    def find_next_text(aVal: BeautifulSoup, aIsText: bool = True) -> object:
        return aVal.find_next_sibling(text = aIsText)

    @staticmethod
    def keyval_fromlist(aVal: list, aIdxKey: int = 0, aIdxVal: int = 1) -> tuple:
        Res = []
        for xVal in aVal:
            Arr = xVal.find_all()
            Res.append((Arr[aIdxKey].text.strip(), Arr[aIdxVal].text.strip()))
        return Res

    # @staticmethod
    # def find_next_string(aVal: BeautifulSoup, aStr: str) -> object:
    #     return soup.find('b', string='Назва:')

    @staticmethod
    def table(aVal: BeautifulSoup) -> list:
        '''
        parse table by tr, th+td
        ["table"]
        '''

        Res = []
        for Row in aVal.find_all('tr'):
            ResTag = []
            Td = Row.find_all('th') + Row.find_all('td')
            for xTd in Td:
                Text = xTd.text.strip()
                ResTag.append(Text)
            Res.append(ResTag)
        return Res

    @staticmethod
    def table_tag(aVal: BeautifulSoup, aTag: list) -> list:
        '''
        parse table
        ["table_tag", [["dt", "dd"]]]
        '''

        Res = []
        Tags = [aVal.find_all(Tag) for Tag in aTag]
        for Tag in zip(*Tags):
            ResTag = []
            for xTag in Tag:
                Text = xTag.text.strip()
                ResTag.append(Text)
            Res.append(ResTag)
        return Res

    @staticmethod
    def _help(_aVal: object) -> list:
        '''
        show brief help
        ["help"]
        '''

        Data = GetClass(TSchemeApi)
        return [x[2] for x in Data]


class TSchemeApiExt():
    @staticmethod
    def ext_image(aIdx: int = 0) -> list:
        Res = [
            ['find_all', ['img']],
            ['list', [aIdx]],
            ['get', ['src']],
            ['url_pad']
        ]
        return Res

    @staticmethod
    def ext_image_og() -> list:
        Res = [
            ['find', ['head']],
            ['find', ['meta', {'property': 'og:image'}]],
            ['get', ['content']],
            ['url_pad']
        ]
        return Res

    @staticmethod
    def ext_category_prom(aIdx: int = -2) -> list:
        Res = [
            ['find', ['div', {'class': 'b-breadcrumb'}]],
            ['get', ['data-crumbs-path']],
            ['txt2json'],
            ['list', [aIdx]],
            ['get', ['name']]
        ]
        return Res

    @staticmethod
    def ext_price_app(aTxt2Float: bool = False) -> list:
        txt2float = ['txt2float'] if (aTxt2Float) else ['comment']
        Res = [
            ['get', ['offers']],
            ['as_list', [
                [
                    ['get', ['price']],
                    txt2float
                ],
                [
                    ['get', ['priceCurrency']]
                ]
            ]]
        ]
        return Res

    @staticmethod
    def ext_title() -> list:
        Res = [
            ["var_get", ["$root"]],
            ["find", ["title"]],
            ["text"]
        ]
        return Res
