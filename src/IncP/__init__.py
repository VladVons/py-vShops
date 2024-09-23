#Created:     2022.04.30
#Author:      Vladimir Vons <VladVons@gmail.com>
#License:     GNU, see LICENSE for more details


__version__ = '1.0.23'
__date__ =  '2024.09.23'


def GetAppVer() -> dict:
    return {
        'app_name': 'vShops',
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  'Vladimir Vons, VladVons@gmail.com',
        'home': 'http://oster.com.ua',
    }
