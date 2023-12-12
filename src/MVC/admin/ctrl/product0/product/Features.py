from Inc.Util.Obj import DeepGetByList


class TFeatures():
    Lang = {
        'ua': {
            'main': 'Головне',
            'size': 'Розмір',
            'name': 'Назва',
            'misc': 'Різне',
            'nutrition': 'Складники',
            'ingredients': 'Вміст',
            'retention': 'Зберігання',
            'sustainability': 'Стабільність'
        }
    }

    def __init__(self, aLang: str):
        self.Lang = aLang

    def Translate(self, aKey: str) -> str:
        return DeepGetByList(self.Lang, [self.Lang, aKey.lower()], aKey)

    def Adjust(self, aObj: object) -> list:
        def Recurs(aObj: object, aDepth: int) -> list:
            Res = []
            if (isinstance(aObj, dict)):
                for xKey, xVal in aObj.items():
                    if (isinstance(xVal, (str, int, float))):
                        Res.append(['i', f'{xKey}: {xVal}'])
                    else:
                        Res.append(['g', self.Translate(xKey)])
                        Res += Recurs(xVal, aDepth + 1)
            elif (isinstance(aObj, list)):
                for xVal in aObj:
                    if (len(xVal) == 2):
                        xVal = ': '.join(xVal)
                    Res.append(['i', xVal])
            return Res
        return Recurs(aObj, 0)
