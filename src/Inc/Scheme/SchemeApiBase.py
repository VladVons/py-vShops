# Created: 2022.06.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json
#import operator
#
from Inc.Http.HttpUrl import UrlToDict, UrlToStr, QueryToDict, QueryToStr
from Inc.Var.Dict import DeepGet, DeepSet, Filter
from Inc.Var.Obj import Iif
from Inc.Util.Sys import IsDebug


StrWhiteSpaces = ' \t\n\r\v\f\xA0✓→'

class TSchemeApiBase():
    def __new__(cls):
        raise TypeError('Cant instantiate static class')

    @staticmethod
    def strip(aVal: str, aChars: str = None) -> str:
        '''
        Remove invisible chars.
        ["strip"]
        '''

        aChars = aChars or StrWhiteSpaces
        return aVal.strip(aChars)
        #return ReCmp_Strip.sub('', aVal)

    # @staticmethod
    # def _strip_all(aVal: str) -> str:
    #     '''
    #     remove all invisible chars
    #     ["strip_all"]
    #     '''

    #     def Search(aData: str, aIter: list) -> int:
    #         for i in aIter:
    #             if (aData[i].isdigit() or aData[i].isalpha()):
    #                 return i
    #         return -1

    #     L = Search(aVal, range(len(aVal)))
    #     R = Search(aVal, range(len(aVal) - 1, L, -1))
    #     return aVal[L:R+1]

    # @staticmethod
    # def _length(aVal: object) -> int:
    #     '''
    #     get object length
    #     ["length"]
    #     '''

    #     return len(aVal)

    @staticmethod
    def list(aVal: list, aIdx: int, aEnd: int = 0) -> object:
        '''
        Get object from list by index.
        ["list", [1]]
        '''

        if (aIdx < len(aVal)):
            if (aEnd):
                Res = aVal[aIdx:aEnd]
            else:
                Res = aVal[aIdx]
            return Res

    @staticmethod
    def list_uniq(aVal: list) -> list:
        '''
        return unique sorted items from a list'
        ["list_uniq"]
        '''

        return sorted(set(aVal))

    @staticmethod
    def list_in(aVal: list, *aFind: str) -> bool:
        '''
        search value in list'
        ["list_in"]
        '''
        return any(xVal in aFind for xVal in aVal)

    @staticmethod
    def list_group(aVal: list, aStep: int, aIdxs: list) -> list:
        '''
        Group list [1,2,3,4,5,6,7,8,9,0] into [[1,3], [4,6], [7,9]].
        ["list_group", [3, [0, 1]]]
        '''

        Res = []
        for Idx in range(0, len(aVal), aStep):
            Data = aVal[Idx : Idx + aStep]
            Val = [Data[i] for i in aIdxs]
            Res.append(Val)
        return Res

    @staticmethod
    def list_join(aVal: list, aDelim: str = '\n') -> str:
        '''
        Join list ['one', 'two', 'three'] into string 'one. two. three'.
        ["list_join", [". "]]
        '''

        return aDelim.join(aVal)

    # @staticmethod
    # def _list_sort(aVal: list, aReverse: bool = False) -> list:
    #     '''
    #     sort list alphabetically
    #     ["list_sort", [False]]
    #     '''

    #     if (isinstance(aVal, list)):
    #         return sorted(aVal, reverse=aReverse)

    # @staticmethod
    # def _list_sort_len(aVal: list, aReverse: bool = False) -> list:
    #     '''
    #     sort string list by length
    #     ["list_sort_len", [False]]
    #     '''

    #     if (isinstance(aVal, list)):
    #         return sorted(aVal, key=len, reverse=aReverse)

    @staticmethod
    def list_filter_len(aVal: list, aLen: int) -> list:
        '''
        Filter list by size
        ["list_filter_len", [2]]
        '''

        return [xVal for xVal in aVal if len(xVal) == aLen]

    @staticmethod
    def split(aVal: str, aDelim: str, aIdx: int = None) -> str:
        '''
        Split string by delimiter and get object from list by index.
        ["split", [" ", -1]]
        '''

        Res = aVal.split(aDelim)
        if (aIdx is not None):
            Res = Res[aIdx].strip()
        return Res

    # @staticmethod
    # def _split_keys(aVal: str, aDelim: list) -> dict:
    #     '''
    #     split string by list of delimiters and get dict Delim: Value
    #     ["split_keys", [["color:", "weight:", "size:"]]]

    #     aVal = "color: red, green white. size: big, smal, mini. weight: 1.2, 30"
    #     Res = {'color': 'red, green white.', 'size': 'big, smal, mini.', 'weight': '1.2, 30'}
    #     '''

    #     RDelim = "|".join(map(re.escape, aDelim))
    #     Pattern = fr'\s*({RDelim})\s*'
    #     Matches = re.split(Pattern, aVal, re.IGNORECASE | re.UNICODE)[1:]
    #     Res = {Matches[i]: Matches[i + 1] for i in range(0, len(Matches), 2)}
    #     return Res

    @staticmethod
    def split_cr(aVal: str, aDelim: str = '\t\n') -> dict:
        '''
        Split string into list.
        aVal = '\\n\\t\\t\\t Weight\\t\\t\\n\\n1.23\\n\\n'
        return ['Weight', '1.23']
        '''

        Parts = re.split(rf'[{aDelim}]+', aVal.strip(aDelim))
        if (len(Parts) > 1):
            return Parts

    @staticmethod
    def val2bool(aVal: object) -> bool:
        '''
        Convert value to boolean.
        ["val2bool"]
        '''

        return Iif(aVal, True, False)

    # @staticmethod
    # def val_return(_aVal: object, aValRet: object) -> object:
    #     '''
    #     Return given value.
    #     ["val_return", true]
    #     '''

    #     return aValRet

    # @staticmethod
    # def _not_none(aVal: list) -> object:
    #     '''
    #     get first not None item
    #     ["not_none"]
    #     '''

    #     for xVal in aVal:
    #         if (xVal is not None):
    #             return xVal

    @staticmethod
    def search_eq(aVal: str, *aStr: list) -> bool:
        '''
        Search any string from a list in aVal.
        ["search_eq", ["InStock", "available"]]
        '''

        return aVal in aStr

    @staticmethod
    def search_in(aVal: str, *aStr: list) -> bool:
        '''
        Search any substring from a list in aVal.
        ["search_in", ["InStock", "available"]]
        '''

        for xStr in aStr:
            if (xStr in aVal):
                return True
        return False

    @staticmethod
    def search_start(aVal: str, *aStr: list) -> bool:
        '''
        Search string that starts with.
        ["search_start", ["InStock", "available"]]
        '''

        for xStr in aStr:
            if (aVal.startswith(xStr)):
                return True
        return False

    # @staticmethod
    # def _search_xlat(aVal: str, aSearch: list, aXlat: list) -> str:
    #     '''
    #     search string and return associated string
    #     ["search_xlat", ["NewCondition", "UsedCondition"], ["нове", "вживане"]]
    #     '''

    #     for xSearch, xXlat in zip(aSearch, aXlat):
    #         if (xSearch in aVal):
    #             return xXlat
    #     return aVal

    # @staticmethod
    # def _compare(aVal: object, aOp: str, aValue = None) -> bool:
    #     Func = getattr(operator, aOp, None)
    #     if (Func):
    #         if (aValue is None):
    #             Res = Func(aVal)
    #         else:
    #             Res = Func(aVal, aValue)
    #         return Res

    # @staticmethod
    # def _dig(aVal: str) -> str:
    #     '''
    #     get filtered chars from [0..9]
    #     ["dig"]
    #     '''

    #     Arr = []
    #     for xVal in aVal:
    #         if ('0' <= xVal <= '9'):
    #             Arr.append(xVal)
    #     return ''.join(Arr)

    # @staticmethod
    # def _dig_lat(aVal: str) -> str:
    #     '''
    #     get filtered chars from [0..9], [a..Z], [.-/]
    #     ["dig_lat"]
    #     '''

    #     Res = ''
    #     for xVal in aVal:
    #         if ('0' <= xVal <= '9') or ('a' <= xVal <= 'z') or ('A' <= xVal <= 'Z') or (xVal in '.-/'):
    #             Res += xVal
    #     return Res

    @staticmethod
    def text_to_json(aVal: str) -> dict:
        '''
        Convert text to json
        ["text_to_json"]
        '''

        return json.loads(aVal)

    @staticmethod
    def text_to_float(aVal: str) -> float:
        '''
        Convert text to float.
        ["text_to_float"]
        '''

        if (isinstance(aVal, str)):
            aVal = float(aVal.replace(',', ''))
        elif (isinstance(aVal, (int, float))):
            aVal = float(aVal)
        return aVal

    @staticmethod
    def text_eqi(aVal: str, *aStr: list) -> str:
        '''
        Filter string by string list.
        ["text_eq", ["dell", "hp", "lenovo"]]
        '''

        Val = aVal.lower()
        for xStr in aStr:
            if (Val == xStr.lower()):
                return aVal

    # @staticmethod
    # def text_to_int(aVal: str) -> int:
    #     '''
    #     convert text to int
    #     ["text_to_int"]
    #     '''

    #     return int(TSchemeApiBase.text_to_float(aVal))

    # @staticmethod
    # def _json2txt(aVal: dict) -> str:
    #     '''
    #     convert json to text
    #     ["json2txt"]
    #     '''

    #     return json.dumps(aVal, indent=2, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def gets(aVal: dict, aKeys: str) -> object:
        '''
        Get nested key from dict.
        Equal to get('key1').get('key2').
        ["gets", ["offers.availability"]]
        '''

        return DeepGet(aVal, aKeys)

    @staticmethod
    def lower(aVal: str) -> str:
        '''
        String to lower case.
        ["lower"]
        '''

        return aVal.lower()

    @staticmethod
    def replace(aVal: str, aFind: str, aRepl: str) -> str:
        '''
        Replace string.
        ["replace", ["1", "one"]]
        hint. use \u00a0 to represen \xa0
        '''

        if (isinstance(aFind, list)) and (isinstance(aRepl, list)):
            for xFind, xRepl in zip(aFind, aRepl, strict=True):
                aVal = aVal.replace(xFind, xRepl)
        elif (isinstance(aFind, list)) and (isinstance(aRepl, str)):
            for xFind in aFind:
                aVal = aVal.replace(xFind, aRepl)
        else:
            aVal = aVal.replace(aFind, aRepl)
        return aVal

    # @staticmethod
    # def _replace_re(aVal: str, aFind: str, aRepl: str) -> str:
    #     r'''
    #     regEx replace string
    #     ["replace_re", ["\s*,\s*", "/"]]
    #     '''
    #     Res = re.sub(aFind, aRepl, aVal)
    #     return Res

    # @staticmethod
    # def _replace_list(aVal: str, aFind: list, aRepl: list) -> str:
    #     '''
    #     multiple replace string
    #     ["replace", [["1", "2"], ["one", "two"]]]
    #     '''
    #     for xFind, xRepl in zip(aFind, aRepl, strict=True):
    #         aVal = aVal.replace(xFind, xRepl)
    #     return aVal

    # @staticmethod
    # def _translate(aVal: str, aFind: str, aRepl: str, aDel: str = None) -> str:
    #     '''
    #     multiple replace string
    #     ["translate", ["abcd", "1234"]]
    #     '''
    #     return aVal.translate(aFind, aRepl, aDel)

    # @staticmethod
    # def _left(aVal: str, aIdx: int) -> str:
    #     '''
    #     get left string part
    #     ["left", [3]]
    #     '''

    #     return aVal[:aIdx]

    @staticmethod
    def comment(aVal: object, aText: str, aShow: bool = False) -> object:
        '''
        Comment.
        ["comment", ["just comment"]]
        '''

        if (aShow):
            print(aText)
        return aVal

    # @staticmethod
    # def _none(_aVal: object) -> None:
    #     '''
    #     return None and stop parsing
    #     ["none"]
    #     '''

    #     return None

    @staticmethod
    def invert(aVal: bool) -> bool:
        '''
        Invert logical value.
        ["invert"]
        '''

        return not aVal

    # @staticmethod
    # def _sub(aVal: str, aIdx: int, aEnd: int) -> str:
    #     '''
    #     get sub string
    #     ["sub", [2, 7]]
    #     '''

    #     return aVal[aIdx:aEnd]

    # @staticmethod
    # def _unbracket(aVal: str, aPair: str = '()', aIdx: int = None) -> str:
    #     '''
    #     ["unbracket", ["()", -1]]
    #     '''

    #     Pattern = r'\%s(.*?)\%s' % (aPair[0], aPair[1])
    #     Res = re.findall(Pattern, aVal)
    #     if (Res):
    #         if (aIdx is not None):
    #             Res = Res[aIdx].strip()
    #         return Res

    # @staticmethod
    # def _concat(aVal: str, aStr: str, aRight: bool =  True) -> str:
    #     '''
    #     concatinate string to left or right side
    #     ["concat", ["hello", true]]
    #     '''

    #     if (aRight):
    #         Res = aVal + aStr
    #     else:
    #         Res = aStr + aVal
    #     return Res

    @staticmethod
    def debug(aVal: object) -> object:
        '''
        Stops program executing under IDE.
        For internal debugging purposes.
        '''

        if (IsDebug()):
            #pylint: disable-next=forgotten-debug-statement
            breakpoint()
        return aVal

    @staticmethod
    def show(aVal: object) -> object:
        '''
        Show current chain value.
        ["show"]
        '''

        print(aVal)
        return aVal

    # @staticmethod
    # def _dict_update(aVal: list) -> dict:
    #     '''
    #     join dict from list of dict
    #     ["dict_update"]
    #     '''

    #     Res = {}
    #     for xVal in aVal:
    #         if (xVal):
    #             Res.update(xVal)
    #     return Res

    @staticmethod
    def dict_keydel(aVal: dict, *aKeys: list) -> dict:
        '''
        Delete key from dictionary.
        ["dict_keydel", ["name", "descr"]]
        '''

        for Key in aKeys:
            if Key in aVal:
                del aVal[Key]
        return aVal

    # @staticmethod
    # def dict_keyget(aVal: dict, *aKeys: list) -> dict:
    #     '''
    #     get keys from dict
    #     ["dict_filter", ["name", "descr"]]
    #     '''

    #     Res = {}
    #     for xKey in aKeys:
    #         Data = DeepGet(aVal, xKey)
    #         if (Data is not None):
    #             DeepSet(Res, xKey, Data)
    #     return Res

    # @staticmethod
    # def _dict_keyren(aVal: dict, *aPairs: list) -> dict:
    #     '''
    #     delete key from dict
    #     ["dict_keyren", [["old1", "new1"], ["old2", "new2]]
    #     '''

    #     for Old, New in aPairs:
    #         aVal[New] = aVal.pop(Old)
    #     return aVal

    # @staticmethod
    # def _dict_keyval2list(aVal: dict, aKeyName: str, aValName: str) -> tuple:
    #     '''
    #     get key and value pair from dict into tuple
    #     ["keyval", ["name", "descr"]]
    #     '''
    #     return (aVal[aKeyName], aVal[aValName])

    @staticmethod
    def keyval2dict(aVal: list, aIdxKey: int = 0, aIdxVal: int = 1, aSaparRest = None) -> dict:
        '''
        Get dictionary from key-val list.

        ex. 1
        ["list_map", [
          ["keyval", ["name", "value"]]]
        ],
        ["keyval2dict"]

        ex. 2
        ["table"]]
        ["keyval2dict", [1, 3, ", "]]
        '''

        Res = {}
        for xVal in aVal:
            Len = len(xVal)
            if (aIdxKey < Len):
                Key = xVal[aIdxKey].replace("'", '').strip().rstrip(':')
                if (Key) and (aIdxVal < Len):
                    if (aSaparRest):
                        Arr = [x.strip() for x in xVal[aIdxVal:]]
                        Val = aSaparRest.join(Arr)
                    else:
                        Val = xVal[aIdxVal].strip()
                    Res[Key] = Val
        if (Res):
            return Res

    @staticmethod
    def urlquery_filter(aVal: str, *aFilter: list) -> str:
        '''
        Filter query parameters in URL.
        ["urlquery_filter", ["page"]]
        '''

        UrlDict = UrlToDict(aVal)
        Query = UrlDict.get('query')
        if (Query):
            QueryDict = QueryToDict(Query)
            QueryDict = Filter(QueryDict, aFilter)
            UrlDict['query'] = QueryToStr(QueryDict)
            aVal = UrlToStr(UrlDict)
        return aVal
