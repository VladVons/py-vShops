# Created: 2022.06.21
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
import json
import operator
#
from Inc.Util.Obj import DeepGet


StrWhiteSpaces = ' \t\n\r\v\f\xA0✓→'

class TSchemeApiBase():
    def __new__(cls):
        raise TypeError('Cant instantiate static class')

    @staticmethod
    def strip(aVal: str, aChars: str = None) -> str:
        '''
        remove invisible chars
        ["strip"]
        '''

        aChars = aChars or StrWhiteSpaces
        return aVal.strip(aChars)
        #return ReCmp_Strip.sub('', aVal)

    @staticmethod
    def _strip_all(aVal: str) -> str:
        '''
        remove all invisible chars
        ["strip_all"]
        '''

        def Search(aData: str, aIter: list) -> int:
            for i in aIter:
                if (aData[i].isdigit() or aData[i].isalpha()):
                    return i
            return -1

        L = Search(aVal, range(len(aVal)))
        R = Search(aVal, range(len(aVal) - 1, L, -1))
        return aVal[L:R+1]

    @staticmethod
    def _length(aVal: object) -> int:
        '''
        get object length
        ["length"]
        '''

        return len(aVal)

    @staticmethod
    def list(aVal: list, aIdx: int, aEnd: int = 0) -> object:
        '''
        get object from list by index
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
    def list_group(aVal: list, aStep: int, aIdxs: list) -> list:
        '''
        group list [1,2,3,4,5,6,7,8,9,0] into [[1,3], [4,6], [7,9]]
        ["list_group", [3, [0, 1]]]
        '''

        Res = []
        for Idx in range(0, len(aVal), aStep):
            Data = aVal[Idx : Idx + aStep]
            Val = [Data[i] for i in aIdxs]
            Res.append(Val)
        return Res

    @staticmethod
    def list_listgroup(aVal: list, aStep: int, aIdxs: list) -> list:
        '''
        group list [1,2,3,4,5,6,7,8,9,0] into [[1,3], [4,6], [7,9]]
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
        join list ['one', 'two', 'three'] into string 'one. two. three'
        ["list_join", [". "]]
        '''

        return aDelim.join(aVal)

    @staticmethod
    def list_sort(aVal: list, aReverse: bool = False) -> list:
        '''
        sort list alphabetically
        ["list_sort", [False]]
        '''

        if (isinstance(aVal, list)):
            return sorted(aVal, reverse=aReverse)

    @staticmethod
    def list_sort_len(aVal: list, aReverse: bool = False) -> list:
        '''
        sort string list by length
        ["list_sort_len", [False]]
        '''

        if (isinstance(aVal, list)):
            return sorted(aVal, key=len, reverse=aReverse)

    @staticmethod
    def list_filter_len(aVal: list, aLen: int) -> list:
        '''
        filter list by size
        ["list_filter_len", [2]]
        '''

        return [xVal for xVal in aVal if len(xVal) == aLen]

    @staticmethod
    def split(aVal: str, aDelim: str, aIdx: int = None) -> str:
        '''
        split string by delimiter and get object from list by index
        ["split", [" ", -1]]
        '''

        Res = aVal.split(aDelim)
        if (aIdx is not None):
            Res = Res[aIdx].strip()
        return Res

    @staticmethod
    def split_keys(aVal: str, aDelim: list) -> dict:
        '''
        split string by list of delimiters and get dict Delim: Value
        ["split_keys", [["color:", "weight:", "size:"]]]

        aVal = "color: red, green white. size: big, smal, mini. weight: 1.2, 30"
        Res = {'color': 'red, green white.', 'size': 'big, smal, mini.', 'weight': '1.2, 30'}
        '''

        RDelim = "|".join(map(re.escape, aDelim))
        Pattern = fr'\s*({RDelim})\s*'
        Matches = re.split(Pattern, aVal, re.IGNORECASE | re.UNICODE)[1:]
        Res = {Matches[i]: Matches[i + 1] for i in range(0, len(Matches), 2)}
        return Res

    @staticmethod
    def split_cr(aVal: str, aDelim: str = '\t\n') -> dict:
        '''
        split string into list
        aVal = '\n\t\t\t\tWeight\t\t\n\n1.23\n\n'
        return ['Weight', '1.23']
        '''

        Parts = re.split(rf'[{aDelim}]+', aVal.strip(aDelim))
        if (len(Parts) > 1):
            return Parts

    @staticmethod
    def val2bool(aVal: object) -> bool:
        '''
        convert value to boolean
        ["val2bool"]
        '''

        return (aVal is not None)

    @staticmethod
    def val_return(_aVal: object, aValRet: object) -> object:
        '''
        return value
        ["val_return", true]
        '''

        return aValRet

    @staticmethod
    def not_none(aVal: list) -> object:
        '''
        get first not None item
        ["not_none"]
        '''

        for x in aVal:
            if (x is not None):
                return x

    @staticmethod
    def search(aVal: str, *aStr: list) -> bool:
        '''
        search any substring from a list in aVal
        ["search", ["InStock", "available"]]
        '''

        for xStr in aStr:
            if (aVal.find(xStr) >= 0):
                return True
        return False

    @staticmethod
    def search_prefix(aVal: str, *aStr: list) -> bool:
        '''
        search string that starts with a given prefix
        ["search_prefix", ["InStock", "available"]]
        '''

        for xStr in aStr:
            if (aVal.startswith(xStr)):
                return True
        return False

    @staticmethod
    def search_eq(aVal: str, *aStr: list) -> bool:
        '''
        search any string from a list in aVal
        ["search_eq", ["InStock", "available"]]
        '''

        return aVal in aStr

    @staticmethod
    def search_xlat(aVal: str, aSearch: list, aXlat: list) -> str:
        '''
        search string and return associated string
        ["search_xlat", ["NewCondition", "UsedCondition"], ["нове", "вживане"]]
        '''

        for xSearch, xXlat in zip(aSearch, aXlat):
            if (xSearch in aVal):
                return xXlat
        return aVal

    @staticmethod
    def _compare(aVal: object, aOp: str, aValue = None) -> bool:
        Func = getattr(operator, aOp, None)
        if (Func):
            if (aValue is None):
                Res = Func(aVal)
            else:
                Res = Func(aVal, aValue)
            return Res

    @staticmethod
    def dig(aVal: str) -> str:
        '''
        get filtered chars from [0..9]
        ["dig"]
        '''

        Arr = []
        for x in aVal:
            if ('0' <= x <= '9'):
                Arr.append(x)
        return ''.join(Arr)

    @staticmethod
    def _dig_lat(aVal: str) -> str:
        '''
        get filtered chars from [0..9], [a..Z], [.-/]
        ["dig_lat"]
        '''

        Res = ''
        for x in aVal:
            if ('0' <= x <= '9') or ('a' <= x <= 'z') or ('A' <= x <= 'Z') or (x in '.-/'):
                Res += x
        return Res

    @staticmethod
    def txt2json(aVal: str) -> dict:
        '''
        convert text to json
        ["txt2json"]
        '''

        return json.loads(aVal)

    @staticmethod
    def txt2float(aVal: str) -> float:
        '''
        convert text to float
        ["txt2float"]
        '''

        if (isinstance(aVal, str)):
            Res = float(aVal.replace(',', ''))
        elif (isinstance(aVal, (int, float))):
            Res = float(aVal)
        return Res

    @staticmethod
    def txt2int(aVal: str) -> int:
        '''
        convert text to int
        ["txt2int"]
        '''

        return int(TSchemeApiBase.txt2float(aVal))

    @staticmethod
    def json2txt(aVal: dict) -> str:
        '''
        convert json to text
        ["json2txt"]
        '''

        return json.dumps(aVal, indent=2, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def gets(aVal: dict, aKeys: str) -> object:
        '''
        multiple get. equal to get('key1').get('key2')
        ["gets", ["offers.availability"]]
        '''

        return DeepGet(aVal, aKeys)

    @staticmethod
    def lower(aVal: str) -> str:
        '''
        string to lower case
        ["lower"]
        '''

        return aVal.lower()

    @staticmethod
    def replace(aVal: str, aFind: str, aRepl: str) -> str:
        '''
        replace string
        ["replace", ["1", "one"]]
        hint. use \u00a0 to represen \xa0
        '''
        return aVal.replace(aFind, aRepl)

    @staticmethod
    def replace_re(aVal: str, aFind: str, aRepl: str) -> str:
        r'''
        regEx replace string
        ["replace_re", ["\s*,\s*", "/"]]
        '''
        Res = re.sub(aFind, aRepl, aVal)
        return Res

    @staticmethod
    def replace_list(aVal: str, aFind: list, aRepl: list) -> str:
        '''
        multiple replace string
        ["replace", [["1", "2"], ["one", "two"]]]
        '''
        for xFind, xRepl in zip(aFind, aRepl, strict=True):
            aVal = aVal.replace(xFind, xRepl)
        return aVal

    @staticmethod
    def _translate(aVal: str, aFind: str, aRepl: str, aDel: str = None) -> str:
        '''
        multiple replace string
        ["translate", ["abcd", "1234"]]
        '''
        return aVal.translate(aFind, aRepl, aDel)

    @staticmethod
    def _left(aVal: str, aIdx: int) -> str:
        '''
        get left string part
        ["left", [3]]
        '''

        return aVal[:aIdx]

    @staticmethod
    def comment(aVal: object, aText: str, aShow: bool = False) -> object:
        '''
        comment
        ["comment", ["just comment"]]
        '''

        if (aShow):
            print(aText)
        return aVal

    @staticmethod
    def none(_aVal: object) -> None:
        '''
        return None and stop parsing
        ["none"]
        '''

        return None

    @staticmethod
    def invert(aVal: bool) -> bool:
        '''
        return logical not
        ["invert"]
        '''

        return not aVal

    @staticmethod
    def _sub(aVal: str, aIdx: int, aEnd: int) -> str:
        '''
        get sub string
        ["sub", [2, 7]]
        '''

        return aVal[aIdx:aEnd]

    @staticmethod
    def unbracket(aVal: str, aPair: str = '()', aIdx: int = None) -> str:
        '''
        ["unbracket", ["()", -1]]
        '''

        Pattern = r'\%s(.*?)\%s' % (aPair[0], aPair[1])
        Res = re.findall(Pattern, aVal)
        if (Res):
            if (aIdx is not None):
                Res = Res[aIdx].strip()
            return Res

    @staticmethod
    def concat(aVal: str, aStr: str, aRight: bool =  True) -> str:
        '''
        concatinate string to left or right side
        ["concat", ["hello", true]]
        '''

        if (aRight):
            Res = aVal + aStr
        else:
            Res = aStr + aVal
        return Res

    @staticmethod
    def show(aVal: object) -> object:
        '''
        show value
        ["show"]
        '''

        print(aVal)
        return aVal

    @staticmethod
    def dict_update(aVal: list) -> dict:
        '''
        join dict from list of dict
        ["dict_update"]
        '''

        Res = {}
        for xVal in aVal:
            if (xVal):
                Res.update(xVal)
        return Res

    @staticmethod
    def dict_key_del(aVal: dict, aKeys: list) -> dict:
        '''
        delete key from dict
        ["keydel", [["name", "descr"]]]
        '''

        for Key in aKeys:
            if Key in aVal:
                del aVal[Key]
        return aVal

    @staticmethod
    def dict_keyval2list(aVal: dict, aKeyName: str, aValName: str) -> tuple:
        '''
        get key and value pair from dict into tuple
        ["keyval", ["name", "descr"]]
        '''
        return (aVal[aKeyName], aVal[aValName])

    @staticmethod
    def keyval2dict(aVal: list, aIdxKey: int = 0, aIdxVal: int = 1) -> dict:
        '''
        get dict from keyval list

        ex. 1
        ["list_map", [ ["keyval", ["name", "value"]]]]
        ["keyval2dict"]

        ex. 2
        ["table"]]
        ["keyval2dict", [1, 3]]
        '''

        Res = {}
        for xVal in aVal:
            Len = len(xVal)
            if (aIdxKey < Len) and (aIdxVal < Len):
                Key = xVal[aIdxKey].replace("'", '').strip().rstrip(':')
                Val = xVal[aIdxVal].strip()
                Res[Key] = Val
        return Res