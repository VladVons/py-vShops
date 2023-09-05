# Created: 2023.09.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Conf import TConf
from Inc.ConfJson import TConfJson
from .Main import TTelegram, TTelegramConf

def Main(aConf: TConf) -> tuple:
    File = aConf.File.replace('.py', '.json')
    Conf = TConfJson().LoadFile(File)
    SrvConf = Conf.get('srv_conf')
    Obj = TTelegram(TTelegramConf(**SrvConf))
    return (Obj, Obj.Run())
