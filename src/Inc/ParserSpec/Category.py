# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from ._Common import TSpecBase


class TSpecCategoryLang(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'laptop': [
                r'\b('
                r'laptop|notebook|ultrabook|'
                r'laptopy|'
                r'ноутбук|ультрабук'
                r')\b'
            ],
            'desktop': [
                r'\b('
                r'desktop|tower|sff|workstation|komputer|computer|'
                r'десктоп|робоча станція|пк|компьютер|комп\'ютер|системний|системник'
                r')\b'
            ],
            'monitor': [
                r'\b('
                r'monitor|lcd|led|display|'
                r'bildschirm|'
                r'wyświetlacz|'
                r'монітор|дисплей|монитор|екран'
                r')\b'
            ],
            'server': [
                r'\b('
                r'server|datacenter|blade|2x\d{3,4}w|'
                r'serwer|'
                r'сервер'
                r')\b'
            ],
            'printer': [
                r'\b('
                r'printer|'
                r'drucker|'
                r'принтер|мфу|'
                r'drukarka|urządzenie wielofunkcyjne'
                r')\b'
            ],
            'mobile': [
                r'\b('
                r'phone|tablet|'
                r'телефон|планшет'
                r')\b'
            ],
            'aio': [
                r'\b('
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
            'storage': [
                r'\b('
                r'storage|nas|'
                r'сховище|хранилище'
                r')\b'
            ],
            'pos': [
                r'\b('
                r'terminal|pos|'
                r'термінал|терминал'
                r')\b'
            ],
            'switch': [
                r'\b('
                r'switch'
                r')\b'
            ],
            'keyboard': [
                r'\b('
                r'keyboard|'
                r'клавиатура|'
                r'клавіатура'
                r')\b'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, _aMatch) -> bool:
        aRes['category'] = aKey
        return True

class TSpecCategoryModel(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'laptop': [
                r'\b('
                r'aspire|lifebook|thinkpad|thinkbook|ideapad|latitude|zbook|elitebook|probook|macbook|inspiron|vostro|gram|'
                r'toughbook|chromebook|travelmate|zenbook|vivobook|yoga|nitro|envy|swift|expertbook|surface|erazer|edge|'
                r'portege|katana'
                r')\b'
            ],
            'desktop': [
                r'\b('
                r'optiplex|elitedesk|prodesk|esprimo|thinkcentre|chromebox|thinkstation'
                r')\b'
            ],
            'monitor': [
                r'\b('
                r'proline|ultrasharp|syncmaster|elitedisplay|flexscan'
                r')\b'
            ],
            'server': [
                r'\b('
                r'primergy|poweredge|proliant|vxrail'
                r')\b'
            ],
            'printer': [
                r'\b('
                r'ecosys|laserjet'
                r')\b'
            ],
            'mobile': [
                r'\b('
                r'galaxy|poco|iphone|ipad|pixel'
                r')\b'
            ],
            'aio': [
                r'\b('
                r'eliteone|veriton|imac|proone'
                r')\b'
            ],
            # 'thin client': [
            #     r'\b('
            #     r')\b'
            # ],
            # 'storage': [
            #     r'\b('
            #     r')\b'
            # ],
            'pos': [
                r'\b('
                r'hp engage'
                r')\b'
            ],
            # 'switch': [
            #     r'\b('
            #     r')\b'
            # ],
            # 'keyboard': [
            #     r'\b('
            #     r')\b'
            # ]
        }
        return Res

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
