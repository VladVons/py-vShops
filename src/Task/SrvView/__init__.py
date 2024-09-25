# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from .Main import TSrvView, TSrvViewConf


def Main(aConf) -> tuple:
    Conf = aConf.get('srv_conf', {})
    SrvViewFormConf = TSrvViewConf(**Conf)
    Obj = TSrvView(SrvViewFormConf)
    return (Obj, Obj.RunApp())
