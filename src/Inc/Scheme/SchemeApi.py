# Created: 2022.06.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from bs4 import BeautifulSoup, Comment
#
from Inc.Http.HttpUrl import UrlToDict, UrlToStr, QueryUpdate
from Inc.Util.ModHelp import GetClass
from Inc.Var.List import Parts
from Inc.Var.Dict import DictUpdate
from Inc.Var.Obj import Iif
from Inc.Var.Str import ToJson
from .Utils import SoupTextTag
from .SchemeApiBase import TSchemeApiBase
from .ProductItemProp import TProductItemProp
from .ProductLdJson import TProductLdJson
# from .ProductSocial import TProductOg
# from .Product import TProduct


class TSchemeExt():
    def __init__(self, aParent):
        self.Parent = aParent

    def __ProductParse(self, aVal: BeautifulSoup, aClass, aMaxCnt: int):
        Res = {}

        Items = aClass.Parse(aMaxCnt)
        if (len(Items) == aMaxCnt):
            # possible: name, image, price, stock
            Products = [True for xItem in Items if len(xItem.keys()) >= 3]
            if (len(Products) > 2):
                return Res

        for xItem in Items:
            DictUpdate(Res, xItem)

        if ('image' not in Res):
            Macros = TSchemeApiExt.ext_image_og()
            Val = self.Parent.ParsePipes(aVal, Macros, 'ProductParse')
            if (Val):
                Res['image'] = Val

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

    def product_itemprop(self, aVal: BeautifulSoup, aMaxCnt: int = None) -> dict:
        '''
        Get product items as schema.org standard using meta key itemprop.
        Mostly brand, name, price, stock, images.
        '''

        Product = TProductItemProp(aVal)
        if (Product.Soup):
            if (not aMaxCnt):
                aMaxCnt = 1+2 # 1 category + 2 products

            self.Parent.Var['$product_itemprop_root'] = Product.Soup
            return self.__ProductParse(aVal, Product, aMaxCnt)

    def product_ldjson(self, aVal: BeautifulSoup, aMaxCnt: int = None) -> dict:
        '''
        Get product items as schema.org standard using json.
        Mostly brand, name, price, stock, images.
        '''

        Product = TProductLdJson(aVal)
        if (Product.Soup):
            if (not aMaxCnt):
                aMaxCnt = 1+2 # 1 category + 2 products

            self.Parent.Var['$product_ldjson_root'] = Product.Soup
            return self.__ProductParse(aVal, Product, aMaxCnt)

    # def product_og(self, aVal: BeautifulSoup) -> dict:
    #     Product = TProductOg(aVal)
    #     if (Product.Soup):
    #         self.Parent.Var['$product_og_root'] = Product.Soup
    #         return self.__ProductParse(aVal, Product)

    # def product(self, aVal: BeautifulSoup) -> dict:
    #     Product = TProduct(aVal)
    #     return self.__ProductParse(aVal, Product)

    def list_map(self, aVal: list, *aItems: list) -> list:
        '''
        Call pipe mapper over a list.
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
                ["find", ["div", {"class": "product__price"}]],
                ["text"],
                ["price"]
            ]
        ]]
        '''

        for xPipe in aPipes:
            Res = self.Parent.ParsePipes(aVal, xPipe, 'check_or')
            if (Res is not None):
                return Res

    # def check_and(self, aVal: object, *aPipes: list) -> list:
    #     '''
    #      check all pipes for not None
    #      ["check_and", [
    #         [
    #             ["get", ["offers.price"]]
    #         ],
    #         [
    #           ["find", ["div", {"class": "product__price"}]], ["text"], ["price"]
    #         ]
    #     ]]
    #     '''

    #     for xPipe in aPipes:
    #         Res = self.Parent.ParsePipes(aVal, xPipe, 'check_and')
    #         if (Res is None):
    #             break
    #     return Res

    def url_pad(self, aVal: str) -> str:
        '''
        Pad url with host prefix.
        ["url_pad"]
        '''

        if (aVal) and (not aVal.startswith('http')):
            UrlDict = UrlToDict(self.Parent.Var.get('$url'))
            if (aVal.startswith('?')):
                Url = UrlToStr(UrlDict, ['scheme', 'host', 'path'])
            elif (aVal.startswith('//')):
                Url = UrlDict['scheme'] + ':/'
            else:
                Url = UrlToStr(UrlDict, ['scheme', 'host'])
            aVal = Url + '/' + aVal.lstrip('/')
        return aVal

    def url_format(self, aVal: str|list, aFormat: str) -> str:
        '''
        Format url using string or list params.
        ["url_format", ["&page={0}"]]
        '''

        Url = self.Parent.Var.get('$url')

        if (isinstance(aVal, str|int)):
            aVal = [aVal]

        Suffix = aFormat.format(*aVal)
        if (Suffix[0] in ['&', '?']):
            UrlDict = UrlToDict(Url)
            UrlDict['query'] = QueryUpdate([UrlDict['query'], Suffix[1:]])
            Res = UrlToStr(UrlDict)
        elif (Suffix[0] == '/'):
            Res = Url.rstrip('/') + Suffix
        else:
            Res = Url + Suffix
        return Res

    def var_get(self, _aNotUsed: object, aName: str) -> object:
        '''
        Get chain variable.
        ["var_get", ["$root"]]
        '''

        Res = self.Parent.Var.get(aName)
        if (not Res):
            self.Parent.Err.append('%s (unknown)' % (aName))
        return Res

    def var_set(self, aVal: object, aName: str) -> object:
        '''
        Set current chain value to variable.
        ["var_set", ["$Price"]]
        '''

        self.Parent.Var[aName] = aVal
        return aVal

    def find_all_get_url(self, aVal: BeautifulSoup, *aPath: list, a_get: dict) -> list[str]:
        '''
        Find tags + get attr + strip text + pad url + unique list.
        ["find_all_get", ["a"], {"a_get": "href"}],
        '''

        Items = aVal.find_all(*aPath)
        if (Items):
            Res = []
            for xItem in Items:
                Val = xItem.get(a_get)
                if (Val) and (Val != '#'):
                    # get pure image path without query
                    if any(xExt in Val for xExt in ('.jpg?', '.webp?', '.png?', '.html?')):
                        Val = Val.split('?', maxsplit=1)[0]
                    Url = self.url_pad(Val.strip())
                    Res.append(Url)
            return list(set(Res))

class TSchemeApi(TSchemeApiBase):
    @staticmethod
    def text_strip(aVal: BeautifulSoup, aDelim = None) -> str:
        '''
        Get text object and strip string.
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
        Get all <p>, strip text, delimit with CR
        ["text_tag"]
        '''

        return SoupTextTag(aVal, aTag)

    @staticmethod
    def meta_price(aVal: BeautifulSoup) -> list:
        '''
        Get price from meta.
        ["meta_price"]
        '''
        Price = aVal.find('meta', {'itemprop': 'price'}).get('content')
        Currency = aVal.find('meta', {'itemprop': 'priceCurrency'}).get('content')
        return [float(Price), Currency]

    @staticmethod
    def meta_nears(aVal: BeautifulSoup) -> list:
        '''
        Get 'next' and 'prev' navigation urls from html head.
        ["meta_pages"]
        '''

        Soup = aVal.find('head')
        if (Soup):
            Items = aVal.find_all('link', rel=re.compile(r'(next|prev)'))
            if (Items):
                Res = [xItem.get('href') for xItem in Items]
                return Res

    # @staticmethod
    # def price_find(aVal: str, aCur: str = 'грн') -> list:
    #     r'''
    #     get prices from string using regEx r'[\d\.]{2,}\s*' + aCur
    #     ["price_find"]
    #     '''

    #     Pattern = r'[\d\.]{2,}\s*' + aCur
    #     Res = re.findall(Pattern, aVal)
    #     if (Res):
    #         return Res

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
        Get breadcrumb path as string delimited by '/'.
        Equal to find_all() + list().
        ["breadcrumb", [["a"], -1]]
        '''

        if (hasattr(aVal, 'find_all')):
            Items = aVal.find_all(*aFind)
            if (Items):
                if (aChain):
                    Items = Items if (aIdx == -1) else Items[:aIdx + 1]
                    Arr = [x.get_text(strip=True) for x in Items]
                    Arr = [x.replace('/', '-').replace('»', '') for x in Arr if (len(x) > 1)]
                    Res = '/'.join(Arr)
                else:
                    Res = Items[aIdx].get_text(strip=True)

                if (Res):
                    return Res

    @staticmethod
    def get_yes(aVal: BeautifulSoup, aKey: str) -> bool:
        '''
        Return true if key exists.
        ["get_yes", ["__grayscale"]]
        '''

        Res = aVal.get(aKey)
        return bool(Res)

    @staticmethod
    def find_or(aVal: BeautifulSoup, *aPath: list) -> BeautifulSoup:
        '''
        Find first pattern from a list.
        ["find_or", [
            ["p", {"class": "price"}],
            ["span", {"class": "price_new"}]
        ]],
        '''

        for xPath in aPath:
            if (len(xPath) == 3):
                Dict = xPath[2]
                if ('re_text' in Dict):
                    Dict['text'] = re.compile(Dict['re_text'])
                    del Dict['re_text']
                Res = aVal.find(*xPath[:2], **Dict)
            else:
                Res = aVal.find(*xPath)

            if (Res is not None):
                return Res

    @staticmethod
    def find_yes(aVal: BeautifulSoup, aTag: str, aParam: dict = None) -> bool:
        '''
        Return true if found.
        ["find_yes", ["a", {"class": "__grayscale"}]]
        '''

        Res = aVal.find(aTag, **aParam)
        return bool(Res)

    @staticmethod
    def find_re(aVal: BeautifulSoup, aTag: str, aParam: dict = None) -> BeautifulSoup:
        '''
        Find regexp. Use to find more than one word in class etc.
        ["find_re", ["catalog_block.*items"]]
        '''
        for Key, Val in aParam.items():
            aParam[Key] = re.compile(Val)

        return aVal.find(aTag, aParam)

    @staticmethod
    def find_path(aVal: BeautifulSoup, *aPath: list) -> BeautifulSoup:
        '''
        Series of find(). Use to find nested elements.
        ["find_path", [
            ["div", {"class": "product-price"}],
            ["div", {"class": "product-price__old-price"}]
          ]],
        '''

        for xPath in aPath:
            aVal = aVal.find(*xPath)
            if (aVal is None):
                break
        return aVal

    @staticmethod
    def find_check(aVal: BeautifulSoup, *aPath: list) -> BeautifulSoup:
        '''
        If find element do nothing else returns None.
        ["find_stop", ["div", {"class": "product"}]]
        '''

        Val = aVal.find(*aPath)
        if (Val):
            return aVal

    # @staticmethod
    # def find_parent(aVal: BeautifulSoup, aStr: str, aDepth: int = 1) -> object:
    #     '''
    #     find parent object by text
    #     ["find_parent", ["hello", [3]]]
    #     '''

    #     Items = aVal.findAll(string=re.compile(aStr))
    #     if (Items):
    #         Res = SoupGetParentsObj(aVal, Items, aDepth)
    #         return Res[0][-1]

    @staticmethod
    def find_next_text(aVal: BeautifulSoup, aIsText: bool = True) -> BeautifulSoup:
        return aVal.find_next_sibling(text = aIsText)

    @staticmethod
    def find_comment(aVal: BeautifulSoup, aStr: str) -> BeautifulSoup:
        '''
        Find first element after comment.
        ["find_comment", ["catalog - start"]]
        '''

        Items = aVal.find_all(string=lambda xText: isinstance(xText, Comment) and aStr in xText)
        if (Items):
            return Items[0].find_next()

    @staticmethod
    def find_all_text(aVal: BeautifulSoup, *aPath: list, a_text: str, a_pos = 'in') -> list[BeautifulSoup]:
        '''
        Return list of elements containing a_text.
        ["find_text", ["li"], {"a_text": "in stock"}]
        '''

        Res = []
        for xVal in aVal.find_all(*aPath):
            Val = xVal.get_text(strip=True)
            match a_pos:
                case 'in':
                    if (a_text in Val):
                        Res.append(xVal)
                case 'start':
                    if (Val.startswith(a_text)):
                        Res.append(xVal)
                case 'end':
                    if (Val.endswith(a_text)):
                        Res.append(xVal)
        return Res

    @staticmethod
    def find_all_get(aVal: BeautifulSoup, *aPath: list, a_get: dict) -> list[str]:
        '''
        Find tags + get attr + strip text.
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
    def script_var(aVal: list[BeautifulSoup], aVar: str) -> dict:
        '''
        Get dict var in script.
        ["find_all", ["script", {"id": "init-config"}]],
        ["script_var", ["var product"]]
        '''

        # reVar = re.compile(aVar + r'\s*=\s*(\{.*?\})\s*;|', re.DOTALL)
        # reVarAsStr = re.compile(aVar + r'\s*=\s*("\{.*?\}")\s*;', re.DOTALL)
        reVar = re.compile(aVar + r'\s*=\s*(\{.*?\}|"\{.*?\}")\s*;', re.DOTALL)

        for xScript in aVal:
            Script = xScript.text
            Match = reVar.search(Script)
            if (Match):
                Val = Match.group(1)
                if (Val.startswith('"')):
                    Val = Val[1:-1].replace(r'\"', '"').replace(r'\\', '\\')

                try:
                    Res = ToJson(Val)
                except Exception as _E:
                    Val = re.sub(r'(\w+):', r'"\1":', Val)
                    Res = ToJson(Val)
                return Res

    # @staticmethod
    # def list_get_keyval(aVal: list, aIdxKey: int = 0, aIdxVal: int = 1) -> tuple:
    #     Res = []
    #     for xVal in aVal:
    #         Arr = xVal.find_all()
    #         Res.append((Arr[aIdxKey].text.strip(), Arr[aIdxVal].text.strip()))
    #     return Res

    # @staticmethod
    # def find_string(aVal: BeautifulSoup, aTag: str, aStr: str) -> object:
    #     return aVal.find(aTag, string=aStr)

    @staticmethod
    def table(aVal: BeautifulSoup, aHeader: bool = True) -> list:
        '''
        Get <tr>, <th>, <td> tags from <table>.
        ["table"]
        '''

        Res = []
        for xTr in aVal.find_all('tr'):
            ResTag = []
            Td = Iif(aHeader, xTr.find_all('th'), []) + xTr.find_all('td')
            for xTd in Td:
                Text = xTd.get_text(strip=True, separator='\n')
                ResTag.append(Text)
            Res.append(ResTag)
        return Res

    @staticmethod
    def table_tag(aVal: BeautifulSoup, *aPath: list) -> list:
        '''
        Find objects and split each into list of text
        ["table_tag", ["div", {"class": "product-variants-item"}]]
        '''

        Items = aVal.find_all(*aPath)
        if (Items):
            Separ = '\n'
            Res = []
            if (isinstance(aPath[0], str)):
                for xItem in Items:
                    Val = xItem.get_text(strip=True, separator=Separ)
                    Arr = re.split(Separ, Val)
                    if (Arr):
                        Res.append(Arr)
            elif (isinstance(aPath[0], list)):
                Len = len(aPath[0])
                for xPart in Parts(Items, Len):
                    Group = []
                    for x in xPart:
                        Val = x.get_text(strip=True, separator=Separ)
                        Arr = re.split(Separ, Val)
                        if (len(Arr) == 1):
                            Group.append(Arr[0])
                        elif (len(Arr) > 1):
                            Group.append(','.join(Arr))
                    Res.append(Group)
            else:
                raise KeyError('unsupported type')
            return Res

    @staticmethod
    def table_tag_pair(aVal: BeautifulSoup, *aPath: list) -> list:
        '''
        Find paired objects and returns text list.
        First selector becomes a key, rest is value.
        ["table_tag_pair", [["dd", "dt"]]]
        '''

        Items = aVal.find_all(*aPath)
        if (Items):
            Res = []
            Pair = []
            for xItem in Items:
                if (xItem.name == aPath[0][0]):
                    Pair = [xItem.get_text(strip = True), '']
                    Res.append(Pair)
                elif Pair:
                    Pair[1] += Iif(Pair[1], '\n', '') + xItem.get_text(strip = True)
            return Res

    # @staticmethod
    # def table_tag(aVal: BeautifulSoup, aTag: list) -> list:
    #     '''
    #     parse table
    #     ["table_tag", [["dt", "dd"]]]
    #     '''

    #     Res = []
    #     Tags = [aVal.find_all(Tag) for Tag in aTag]
    #     for Tag in zip(*Tags):
    #         ResTag = []
    #         for xTag in Tag:
    #             Text = xTag.text.strip()
    #             ResTag.append(Text)
    #         Res.append(ResTag)
    #     return Res

    @staticmethod
    def help(_aVal: object) -> list:
        '''
        Show brief help.
        ["help"]
        '''

        Data = GetClass(TSchemeApi)
        SchemeApi = [[x[2], x[3].strip()] for x in Data]

        Data = GetClass(TSchemeExt)
        SchemeExt = [[x[2], x[3].strip()] for x in Data]

        Res = sorted(SchemeApi + SchemeExt, key=lambda x: x[0])
        return Res

    @staticmethod
    def replace_br(aVal: BeautifulSoup, aNew: str = '\n') -> BeautifulSoup:
        '''
        Replace <br> with '\\n'.
        ["replace_br", ["\\n"]]
        '''

        for xBr in aVal.find_all('br'):
            xBr.replace_with(aNew)
        return aVal

    @staticmethod
    def remove(aVal: BeautifulSoup, *aPath: list) -> BeautifulSoup:
        '''
        remove object.
        ["remove", ["div", {"class": "price-old"}]]
        '''

        Val = aVal.find(*aPath)
        if (Val):
            Val.decompose()
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
