# Created: 2024.12.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Common import TSpecBase


class TSpecCategory(TSpecBase):
    def _GetPatterns(self) -> dict:
        Res = {
            'laptop': [
                r'laptop|notebook|thinkpad|latitude|zbook|elitebook|probook|macbook|inspiron|vostro|'
                r'laptopy|'
                r'ноутбук'
            ],
            'server': [
                r'server|poweredge|proliant|'
                r'serwer|'
                r'сервер'
            ],
            'desktop': [
                r'desktop|tower|workstation|thinkcentre|komputer|computer|'
                r'десктоп|системный блок|робоча станція|пк|компьютер|комп\'ютер|системний|системник'
            ],
            'monitor': [
                r'monitor|lcd|led|display|'
                r'bildschirm|'
                r'wyświetlacz|'
                r'монітор|дисплей|монитор|екран'
            ],
            'printer': [
                r'printer|ecosys|laserjet|'
                r'drucker|'
                r'принтер|мфу|'
                r'drukarka|urządzenie wielofunkcyjne'
            ],
            'storage': [
                r'storage|nas|'
                r'сховище|хранилище'
            ]
        }
        return Res

    def _OnParse(self, aRes: dict, aKey: str, _aMatch):
        aRes['category'] = aKey
