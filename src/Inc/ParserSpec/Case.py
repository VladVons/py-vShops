# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ._Common import TSpecBase

class TSpecCase(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'tower': [
                r'\b('
                r'mini\s*tower|'
                r'midi\s*tower|'
                r'big\s*tower|'
                r'full\s*tower|'
                r'tower|'
                r'bmt|'
                r'bt|'
                r'mt|'
                r'башня|'
                r'корпус'
                r')\b'
            ],
            'sff': [
                r'\b('
                r'sff|'
                r'small'
                r')\b'
            ],
            'usff': [
                r'\b('
                r'usff|'
                r'ultra small'
                r')\b'
            ],
            'desktop':[
                r'\b('
                r'desktop|'
                r'slimline|'
                r'десктоп'
                r')\b'
            ],
            'mini': [
                r'\b('
                r'mini|'
                r'mff|'
                r'micro|'
                r'tiny|'
                r'міні|'
                r'мини'
                r')\b'
            ],
            'aio': [
                r'\b('
                r'all.?in.?one|'
                r'aio|'
                r'моноблок'
                r')\b'
            ],
            'thinclient': [
                r'\b('
                r'thinclient|'
                r'тонкий клієнт|'
                r'тонкий клиент'
                r')\b'
            ],
            'pos': [
                r'\b('
                r'pos-terminal|'
                r'pos|'
                r'платіжний термінал|'
                r'payment terminal'
                r')\b'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, _aMatch):
        aRes['case'] = aKey
