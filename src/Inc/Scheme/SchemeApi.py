# Created: 2022.06.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from bs4 import BeautifulSoup, Comment
#
from Inc.Http.HttpUrl import UrlToDict, UrlToStr
from Inc.Util.ModHelp import GetClass
from Inc.Var.Dict import DictUpdate
from Inc.Var.Obj import Iif
from Inc.Var.Str import ToJson
from .Utils import GetPrice, SoupGetParentsObj
from .SchemeApiBase import TSchemeApiBase
from .ProductItemProp import TProductItemProp
from .ProductLdJson import TProductLdJson
from .ProductSocial import TProductOg
from .Product import TProduct


class TSchemeExt():
    def __init__(self, aParent):
        self.Parent = aParent

    def __ProductParse(self, aMethod):
        Res = {}

        PossibleCategoryCnt = 1+2 # 1 category + 2 products
        Items = aMethod.Parse(PossibleCategoryCnt)
        if (len(Items) == PossibleCategoryCnt):
            # possible: name, image, price, stock
            Products = [True for xItem in Items if len(xItem.keys()) >= 3]
            if (len(Products) > 2):
                return Res

        for xItem in Items:
            DictUpdate(Res, xItem)

        for Key, Val in Res.items():
            if (Val):
                match Key:
                    case 'images':
                        for Idx, xVal in enumerate(Val):
                            Val[Idx] = self.url_pad(xVal)
                    case 'image':
                        Val = self.url_pad(Val)
                        Res[Key] = Val
                    case 'category':
                        Name = Res.get('name')
                        if (Name) and ('/' + Name in Val):
                            Res[Key] = Val.replace(Name, '').rstrip('/')

            self.Parent.Var[f'${Key}'] = Val
        return Res

    def product_itemprop(self, aVal: BeautifulSoup) -> dict:
        Product = TProductItemProp(aVal)
        if (Product.Soup):
            self.Parent.Var['$product_itemprop_root'] = Product.Soup
            return self.__ProductParse(Product)

    def product_ldjson(self, aVal: BeautifulSoup) -> dict:
        Product = TProductLdJson(aVal)
        if (Product.Soup):
            self.Parent.Var['$product_ldjson_root'] = Product.Soup
            return self.__ProductParse(Product)

    def product_og(self, aVal: BeautifulSoup) -> dict:
        Product = TProductOg(aVal)
        if (Product.Soup):
            self.Parent.Var['$product_og_root'] = Product.Soup
            return self.__ProductParse(Product)

    def product(self, aVal: BeautifulSoup) -> dict:
        Product = TProduct(aVal)
        return self.__ProductParse(Product)

    def list_map(self, aVal: list, *aItems: list) -> list:
        '''
        call pipe mapper over a list
        ["list_map", [
            ["get", ["offers"]],
            ["list", [0]],
            ["get", ["url"]]
        ]]
        '''

        Res = []
        for xVal in aVal:
            Data = self.Parent.ParsePipes(xVal, aItems, 'list_map')
            if (Data is not None):
                Res.append(Data)
        return Res

    def check_or(self, aVal: object, *aPipes: list) -> list:
        '''
         check pipes until result is not None
         ["check_or", [
            [
                ["get", ["offers.price"]]
            ],
            [
                ["find", ["div", {"class": "product__price"}]], ["text"], ["price"]
            ]
        ]]

        '''

        for xPipe in aPipes:
            Res = self.Parent.ParsePipes(aVal, xPipe, 'check_or')
            if (Res is not None):
                return Res

    def check_and(self, aVal: object, *aPipes: list) -> list:
        '''
         check all pipes for not None
         ["check_and", [
            [
                ["get", ["offers.price"]]
            ],
            [
              ["find", ["div", {"class": "product__price"}]], ["text"], ["price"]
            ]
        ]]
        '''

        for xPipe in aPipes:
            Res = self.Parent.ParsePipes(aVal, xPipe, 'check_and')
            if (Res is None):
                break
        return Res

    def url_pad(self, aVal: str) -> str:
        '''
        pad url with host prefix
        ["url_pad"]
        '''

        if (not aVal.startswith('http')):
            UrlDict = UrlToDict(self.Parent.Var.get('$url'))
            if (aVal.startswith('?')):
                Host = UrlToStr(UrlDict, ['scheme', 'host', 'path'])
            else:
                Host = UrlToStr(UrlDict, ['scheme', 'host'])
            aVal = Host + '/' + aVal.lstrip('/')
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

    def find_all_get_url(self, aVal: BeautifulSoup, *aPath: list, a_get: dict) -> list[str]:
        '''
        find tags + get attr + strip text + pad url + unique list
        ["find_all_get", ["a"], {"a_get": "href"}],
        '''

        Items = aVal.find_all(*aPath)
        if (Items):
            Res = []
            for xItem in Items:
                Val = xItem.get(a_get)
                if (Val):
                    Res.append(self.url_pad(Val.strip()))
            return list(set(Res))

class TSchemeApi(TSchemeApiBase):
    @staticmethod
    def text_strip(aVal: BeautifulSoup, aDelim = None) -> str:
        '''
        get text object and strip string
        ["text_strip", ["|"]]
        hello world|john
        '''

        if (aDelim):
            Res = aVal.get_text(strip=True, separator=aDelim)
        else:
            Res = aVal.text.strip()
        return Res

    @staticmethod
    def text_tag(aVal: BeautifulSoup, aTag: str = 'p') -> str:
        '''
        get all <p>, strip text, delimit with '\n'
        ["text_tag"]
        '''

        Arr = [xTag.text.strip() for xTag in aVal.find_all(aTag)]
        return '\n'.join(Arr)

    @staticmethod
    def price(aVal: str) -> list:
        '''
        get price
        ["price"]
        '''

        return GetPrice(aVal)

    @staticmethod
    def meta_price(aVal: BeautifulSoup) -> list:
        '''
        get price from meta
        ["meta_price"]
        '''
        Price = aVal.find('meta', {'itemprop': 'price'}).get('content')
        Currency = aVal.find('meta', {'itemprop': 'priceCurrency'}).get('content')
        return [float(Price), Currency]

    @staticmethod
    def meta_nears(aVal: BeautifulSoup) -> list:
        '''
        get next and prev urls from head
        ["meta_pages"]
        '''

        Soup = aVal.find('head')
        if (Soup):
            Items = aVal.find_all('link', rel=re.compile(r'(next|prev)'))
            if (Items):
                Res = [xItem.get('href') for xItem in Items]
                return Res

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

    # @staticmethod
    # def serial_check(aVal: str, aLen: int = 5) -> str:
    #     '''
    #     check ranges [A..Z], [0..9], [-/ ] and length >= aLen
    #     ["serial_check"]
    #     '''

    #     if (len(aVal) >= aLen):
    #         Res = [x for x in aVal if ('A' <= x <= 'Z') or (x in '0123456789-/. ')]
    #         if (len(aVal) == len(Res)):
    #             return aVal

    # @staticmethod
    # def serial_find(aVal: str, aMatch: str = r'[A-Z0-9\-\./]{5,}') -> str:
    #     '''
    #     get serial number with regex matches
    #     ["serial_find"]
    #     '''

    #     #Res = ReCmp_Serial.findall(aVal)
    #     Res = re.findall(aMatch, aVal)
    #     if (Res):
    #         return Res

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
                    Arr = [x.replace('/', '-') for x in Arr if (len(x) > 1)]
                    Res = '/'.join(Arr)
                else:
                    Res = Items[aIdx].text.strip()
                return Res

    @staticmethod
    def find_or(aVal: BeautifulSoup, *aPath: list) -> object:
        '''
        find first pattern from list
        ["find_or", [
            ["p", {"class": "price"}],
            ["span", {"class": "price_new"}]
        ]],
        '''

        for xPath in aPath:
            Res = aVal.find(*xPath)
            if (Res is not None):
                return Res

    @staticmethod
    def find_not(aVal: BeautifulSoup, aTag: str, aParam: dict = None) -> bool:
        '''
        if true if not found
        ["find_not", ["a", {"class": "__grayscale"}]]
        '''

        Data = aVal.find(aTag, **aParam)
        return not bool(Data)

    @staticmethod
    def find_re(aVal: BeautifulSoup, aTag: str, aParam: dict = None) -> object:
        '''
        find more than one word in class
        ["find_re", ["catalog_block.*items"]]
        '''
        for Key, Val in aParam.items():
            aParam[Key] = re.compile(Val)

        return aVal.find(aTag, aParam)

    @staticmethod
    def find_path(aVal: BeautifulSoup, *aPath: list) -> object:
        for xPath in aPath:
            aVal = aVal.find(*xPath)
            if (aVal is None):
                break
        return aVal

    @staticmethod
    def find_check(aVal: BeautifulSoup, *aPath: list) -> object:
        '''
        if find element do nothing else returnd none
        ["find_stop", ["div", {"class": "product"}]]
        '''

        Val = aVal.find(*aPath)
        if (Val):
            return aVal

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
    def find_comment(aVal: BeautifulSoup, aStr: str) -> object:
        '''
        find first element after comment
        ["find_comment", ["catalog - start"]]
        '''

        Items = aVal.find_all(string=lambda xText: isinstance(xText, Comment) and aStr in xText)
        if (Items):
            return Items[0].find_next()

    @staticmethod
    def find_all_get(aVal: BeautifulSoup, *aPath: list, a_get: dict) -> list[str]:
        '''
        find tags + get attr + strip text
        ["find_all_get", ["a"], {"a_get": "href"}]
        '''

        Items = aVal.find_all(*aPath)
        if (Items):
            Res = []
            for xItem in Items:
                Val = xItem.get(a_get)
                if (Val):
                    Res.append(Val.strip())
            return Res

    @staticmethod
    def script_var(aVal: BeautifulSoup, aVar: str) -> dict:
        '''
        get dict var in script
        ["find_script_var", ["var product"]]
        '''

        reVar = re.compile(aVar + r'\s*=\s*(\{.*?\})\s*;', re.DOTALL)

        Scripts = aVal.find_all('script')
        for xScript in Scripts:
            Script = xScript.text
            Match = reVar.search(Script)
            if (Match):
                Val = Match.group(1)
                Res = ToJson(Val)
                return Res

    @staticmethod
    def list_get_keyval(aVal: list, aIdxKey: int = 0, aIdxVal: int = 1) -> tuple:
        Res = []
        for xVal in aVal:
            Arr = xVal.find_all()
            Res.append((Arr[aIdxKey].text.strip(), Arr[aIdxVal].text.strip()))
        return Res

    @staticmethod
    def find_string(aVal: BeautifulSoup, aTag: str, aStr: str) -> object:
        return aVal.find(aTag, string=aStr)

    @staticmethod
    def table(aVal: BeautifulSoup, aHeader: bool = True) -> list:
        '''
        parse table by tr, th+td
        ["table"]
        '''

        Res = []
        for xTr in aVal.find_all('tr'):
            ResTag = []
            Td = Iif(aHeader, xTr.find_all('th'), []) + xTr.find_all('td')
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
    def help(_aVal: object) -> list:
        '''
        show brief help
        ["help"]
        '''

        Data = GetClass(TSchemeApi)
        SchemeApi = [[x[2], x[3].strip()] for x in Data]

        Data = GetClass(TSchemeExt)
        SchemeExt = [[x[2], x[3].strip()] for x in Data]

        return SchemeApi + SchemeExt

    @staticmethod
    def replace_br(aVal: object, aNew: str = '\n') -> list:
        '''
        replace <br> with '\n'
        ["replace_br", ["\n"]]
        '''

        for xBr in aVal.find_all('br'):
            xBr.replace_with(aNew)
        return aVal


class TSchemeApiExt():
    @staticmethod
    def ext_image(aIdx: int = 0) -> list:
        return [
            ['find_all', ['img']],
            ['list', [aIdx]],
            ['get', ['src']],
            ['url_pad']
        ]

    @staticmethod
    def ext_image_og() -> list:
        return [
            ['var_get', ['$root']],
            ['find', ['head']],
            ["find_or", [
                ["meta", {"property": "og:image"}],
                ["meta", {"name": "og:image"}]
            ]],
            ['get', ['content']],
            ['url_pad']
        ]

    @staticmethod
    def ext_category_prom(aIdx: int = -2) -> list:
        return [
            ['find', ['div', {'class': 'b-breadcrumb'}]],
            ['get', ['data-crumbs-path']],
            ['txt2json'],
            ['list', [aIdx]],
            ['get', ['name']]
        ]

    @staticmethod
    def ext_price_app(aTxt2Float: bool = True) -> list:
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
        return [
            ["var_get", ["$root"]],
            ["find", ["title"]],
            ["text"],
            ["strip"]
        ]

    @staticmethod
    def ext_stock() -> list:
        return [
          ["var_get", ["$root"]],
          ["find", ["link", {"itemprop": "availability"}]],
          ["get", ["href"]],
          ["stock"]
        ]
