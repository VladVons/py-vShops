# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ._Common import TSpecBase

class TSpecCase(TSpecBase):
    def _GetPatterns(self) -> dict:
        return self._LoadPatternsFile()

    def _OnParse(self, aRes: dict, aKey: str, _aMatch) -> bool:
        aRes['case'] = aKey
        return True
