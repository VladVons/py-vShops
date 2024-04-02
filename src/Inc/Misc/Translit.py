# Created: 2024.04.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


Xlat_CyrToLat = {
    'А': 'A',  'а': 'a',
    'Б': 'B',  'б': 'b',
    'В': 'V',  'в': 'v',
    'Г': 'G',  'г': 'g',
    'Д': 'D',  'д': 'd',
    'Е': 'E',  'е': 'e',
    'Ё': 'Yo', 'ё': 'yo',
    'Ж': 'Zh', 'ж': 'zh',
    'З': 'Z',  'з': 'z',
    'И': 'I',  'и': 'i',
    'Й': 'J',  'й': 'j',
    'К': 'K',  'к': 'k',
    'Л': 'L',  'л': 'l',
    'М': 'M',  'м': 'm',
    'Н': 'N',  'н': 'n',
    'О': 'O',  'о': 'o',
    'П': 'P',  'п': 'p',
    'Р': 'R',  'р': 'r',
    'С': 'S',  'с': 's',
    'Т': 'T',  'т': 't',
    'У': '',   'у': '',
    'Ф': 'F',  'ф': 'f',
    'Х': 'X',  'х': 'x',
    'Ц': 'Cz', 'ц': 'cz',
    'Ч': 'Ch', 'ч': 'ch',
    'Ш': 'Sh', 'ш': 'sh',
    'Щ': 'Sh', 'щ': 'sh',
    'Ъ': '',   'ъ': '',
    'Ы': 'Y',  'ы': 'y',
    'Ь': '',   'ь': '',
    'Э': 'E',  'э': 'e',
    'Ю': 'Y',  'ю': 'y',
    'Я': 'Ya', 'я': 'ya',
}

class TTranslit():
    def __init__(self, aTable: dict = None):
        self.Table = aTable or Xlat_CyrToLat

    def Xlat(self, aText: str) -> str:
        Res = []
        for x in aText:
            x = self.Table.get(x, x)
            Res.append(x)
        return ''.join(Res)
