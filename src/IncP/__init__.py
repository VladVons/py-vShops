#Created:     2022.04.30
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


import os
import sys
import platform
#
from Inc.Misc.Info import GetSysInfo, DictToText


__version__ = '1.0.5'
__date__ =  '2023.03.23'



def GetAppVer() -> dict:
    return {
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  'Vladimir Vons, VladVons@gmail.com',
        'home': 'http://oster.com.ua',
    }

def GetInfo() -> dict:
    Res = GetAppVer()
    Res.update(GetSysInfo())
    return Res

def GetInfoText():
    Data = GetInfo()
    return DictToText(Data)
