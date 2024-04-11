
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
    def strip(aVal: str) -> str:
        '''
        remove invisible chars
        ["strip"]
        '''

        #return aVal.strip()
        return aVal.strip(StrWhiteSpaces)
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
    def is_equal(aVal: str, aStr: list) -> bool:
        '''
        compare values
        ["is_equal", ["InStock", "available"]]
        '''

        if (isinstance(aStr, list)):
            return (aVal in aStr)

    @staticmethod
    def val2bool(aVal: object) -> bool:
        '''
        convert value to boolean
        ["val2bool"]
        '''

        return (aVal is not None)

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
    def search(aVal: object, aStr: list) -> bool:
        '''
        search any string value from a list
        ["search", ["InStock", "available"]]
        '''

        if (isinstance(aStr, list)):
            for x in aStr:
                if (aVal.find(x) >= 0):
                    return True
            return False

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

        return float(aVal.replace(',', ''))

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
        '''
        regEx replace string
        ["replace_re", ["\s*,\s*", "/"]]
        '''

        Res = re.sub(aFind, aRepl, aVal)
        return Res

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
    def comment(aVal: object, aText: str = '') -> object:
        '''
        comment
        ["comment", ["just comment"]]
        '''

        if (aText):
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
    def keyval(aVal: dict, aKeyName: str, aValName: str) -> tuple:
        '''
        get key and value pair from dict into tuple
        ["keyval", ["name", "descr"]]
        '''
        return (aVal[aKeyName], aVal[aValName])

    @staticmethod
    def keyval2dict(aVal: list) -> dict:
        '''
        get dict from keyval list
        ["list_map", [ ["keyval", ["name", "value"]]]]
        ["keyval2dict"]
        '''
        return {xVal[0].replace("'", ''): xVal[1] for xVal in aVal}
