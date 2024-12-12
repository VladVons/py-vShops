# Created: 2024.11.01
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
import base64
from datetime import datetime


def Encode(aData):
    if isinstance(aData, (str, int, float, bool, type(None))):
        Res = aData
    elif isinstance(aData, dict):
        Res = {xKey: Encode(xVal) for xKey, xVal in aData.items()}
    elif isinstance(aData, (list, tuple)):
        Res = [Encode(xData) for xData in aData]
    elif isinstance(aData, bytes):
        Res = {'__type__': 'bytes', 'data': base64.b64encode(aData).decode('utf-8')}
    elif isinstance(aData, datetime):
        Res = {'__type__': 'datetime', 'data': aData.isoformat()}
    elif isinstance(aData, set):
        Res = {'__type__': 'set', 'data': list(aData)}
    else:
        raise TypeError(f'Unsupported data type: {type(aData).__name__}')
    return Res

def Decode(aData):
    if isinstance(aData, (str, int, float, bool, type(None))):
        Res = aData
    elif isinstance(aData, dict):
        if ('__type__' in aData):
            match aData['__type__']:
                case 'bytes':
                    Res = base64.b64decode(aData['data'])
                case 'datetime':
                    Res = datetime.fromisoformat(aData['data'])
                case 'set':
                    Res = set(aData['data'])
                case _:
                    raise ValueError(f'Unsupported type: {aData['__type__']}')
        else:
            Res = {xKey: Decode(xVal) for xKey, xVal in aData.items()}
    elif isinstance(aData, list):
        Res = [Decode(xData) for xData in aData]
    else:
        raise TypeError(f'Unsupported type: {type(aData).__name__}')
    return Res

def WriteFile(aFile: str, aData):
    Data = Encode(aData)
    with open(aFile, 'w', encoding='utf-8') as F:
        json.dump({'data': Data}, F, ensure_ascii=False)

def ReadFile(aFile: str):
    with open(aFile, 'r', encoding='utf-8') as F:
        Data = json.load(F)
    Res = Decode(Data)
    return Res['data']
