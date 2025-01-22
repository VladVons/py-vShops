# Created: 2024.12.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def ToGbUnit(aVal: int, aName: str = 'gb') -> tuple:
    Table = {
        'tb': 1000,
        'gb': 1,
        'mb': 0.001
    }

    Val = Table.get(aName)
    if (Val):
        aVal *= Val
        aName = 'gb'
    return (aVal, aName)

class TLang():
    def __init__(self):
        self.Data = {
            'гб': 'gb',
            'тб': 'tb',
        }

    def Translate(self, aVal: str) -> str:
        Val = aVal.lower()
        return self.Data.get(Val, Val)

Lang = TLang()
