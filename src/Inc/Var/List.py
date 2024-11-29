# Created: 2020.03.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://blog.finxter.com/list-to-dict-convert-a-list-into-a-dictionary-in-python


# Sort list of dictionaries by value
# SortL([{'key': '/b1', 'val': 21}, {'key': '/a1', 'val': 11}], 'key')
def SortLD(aObj: list, aName: str) -> list:
    return sorted(aObj, key = lambda k: k[aName])

def Parts(aData: list, aStep: int):
    '''
    Parts([1,2,3,4,5,6,7,8], 3) -> [1,2,3][4,5,6][7,8]
    '''
    for i in range(0, len(aData), aStep):
        yield aData[i : i + aStep]

def PartsB(aData: list, aStep: int) -> list:
    '''
    PartsB([1,2,3,4,5,6,7,8], 3) -> [1,4,7][2,5,8][3,6]
    '''
    for i in range(aStep):
        yield aData[i::aStep]

def PartsC(aData: list, aStep: int) -> list:
    '''
    PartsC([1,2,3,4,5,6,7,8], 2) -> [1,3][2,4][5,7][6,8]
    '''
    for xParts in Parts(aData, aStep*aStep):
        for i in range(aStep):
            yield xParts[i::aStep]
