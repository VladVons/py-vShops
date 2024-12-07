# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from ._Common import TSpecBase


class TSpecCategory(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'laptop': [
                r'\b('
                r'aspire|lifebook|thinkpad|thinkbook|ideapad|latitude|zbook|elitebook|probook|macbook|inspiron|vostro|'
                r'toughbook|chromebook|travelmate|zenbook|vivobook|yoga|nitro|envy|swift|expertbook|surface|erazer|edge|'

                r'laptop|notebook|'
                r'laptopy|'
                r'ноутбук|ультрабук'
                r')\b'
            ],
            'server': [
                r'\b('
                r'primergy|poweredge|proliant|vxrail|'
                r'server|datacenter|blade|'
                r'serwer|'
                r'сервер'
                r')\b'
            ],
            'desktop': [
                r'\b('
                r'optiplex|elitedesk|prodesk|esprimo|thinkcentre|chromebox|'
                r'desktop|tower|sff|workstation|komputer|computer|'
                r'десктоп|робоча станція|пк|компьютер|комп\'ютер|системний|системник'
                r')\b'
            ],
            'monitor': [
                r'\b('
                r'proline|ultrasharp|'
                r'monitor|lcd|led|display|'
                r'bildschirm|'
                r'wyświetlacz|'
                r'монітор|дисплей|монитор|екран'
                r')\b'
            ],
            'printer': [
                r'\b('
                r'printer|ecosys|laserjet|'
                r'drucker|'
                r'принтер|мфу|'
                r'drukarka|urządzenie wielofunkcyjne'
                r')\b'
            ],
            'storage': [
                r'\b('
                r'storage|nas|'
                r'сховище|хранилище'
                r')\b'
            ],
            'mobile': [
                r'\b('
                r'galaxy|poco|iphone|ipad|pixel|'
                r'планшет'
                r')\b'
            ],
            'aio': [
                r'\b('
                r'eliteone|veriton|'
                r'all.?in.?one|'
                r'aio|'
                r'2w1|'
                r'моноблок'
                r')\b'
            ],
            'thin client': [
                r'\b('
                r'wyse|'
                r'thin\*client|'
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
            ],
            'switch': [
                r'\b('
                r'switch'
                r')\b'
            ],
            'keyboard': [
                r'\b('
                r'keyboard'
                r')\b'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, _aMatch):
        aRes['category'] = aKey
