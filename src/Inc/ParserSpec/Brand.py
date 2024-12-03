# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Common import TSpecBase


class TSpecBrand(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'brand': [
                r'dell|latitude|poweredge|precision|inspiron|vostro|'
                r'hp|hewlett[- ]packard|elitebook|probook|pavilion|'
                r'lenovo|thinkpad|thinkcentre|thinkstation|'
                r'apple|iphone|macbook|'
                r'kyocera|nec|'
                r'fujitsu|lifebook|esprimo|'
                r'toshiba|satellite|'
                r'asus|zenbook|vivobook|'
                r'acer|aspire|predator'
            ]
        }
        return Res

    def _OnParse(self, _aKey: str, aMatch) -> list:
        return aMatch.group(0).lower()
