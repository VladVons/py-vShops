# Created: 2020.03.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# https://blog.finxter.com/list-to-dict-convert-a-list-into-a-dictionary-in-python



# python Sort dictionary of dictionaries by value
# SortD({'a1': {'key': 1, 'val': 111}, 'a2':{'key': 2, 'val': 222}})
def SortDD(aObj: dict, aName: str) -> list:
    return sorted(aObj.items(), key = lambda k: k[1][aName])

# python Sort list of dictionaries by value
# SortL([{'key': '/b1', 'val': 21}, {'key': '/a1', 'val': 11}], 'key')
def SortLD(aObj: list, aName: str) -> list:
    return sorted(aObj, key = lambda k: k[aName])

#{'one1': 1, 'two1': {'two2': 22}, 'three1': {'three2': {'three3': 333}}}
#def GetDeepD(aObj: dict, aKeys: list, aDef = None):
#    for Key in aKeys:
#        aObj = aObj.get(Key)
#        if (aObj is None):
#            return aDef
#    return aObj

def Parts(aData: list, aStep: int):
    '''
    Parts([1,2,3,4,5,6,7], 3) -> [1,2,3][4,5,6][7]
    '''
    for i in range(0, len(aData), aStep):
        yield aData[i : i + aStep]
