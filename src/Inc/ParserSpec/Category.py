# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from ._Common import TSpecBase


class TSpecCategoryLang(TSpecBase):
    def _GetPatterns(self) -> dict:
        return self._LoadPatternsFile()

    def _OnParse(self, aRes: dict, aKey: str, _aMatch) -> bool:
        aRes['category'] = aKey
        return True

class TSpecCategoryModel(TSpecBase):
    def _GetPatterns(self) -> dict:
        return self._LoadPatternsFile()

    def _OnParse(self, aRes: dict, aKey: str, _aMatch) -> bool:
        aRes['category'] = aKey
        return True

class TSpecCategory():
    def __init__(self):
        self.Lang = TSpecCategoryLang()
        self.Model = TSpecCategoryModel()

    def Parse(self, aText: str) -> list:
        Res = self.Lang.Parse(aText)
        if (not Res):
            Res = self.Model.Parse(aText)
        return Res
