# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbAuth
from .Main import TSrvCtrl, TSrvCtrlConf


def Main(aConf) -> tuple:
    SrvConf = aConf.get('srv_conf')
    Obj = TSrvCtrl(TSrvCtrlConf(**SrvConf))
    return (Obj, Obj.RunApp())
