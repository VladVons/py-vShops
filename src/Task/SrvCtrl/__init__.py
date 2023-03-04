# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.SrvWeb.SrvBase import TSrvConf
from Inc.Sql.ADb import TDbAuth
from .Api import ApiCtrl, TApiConf
from .Main import TSrvCtrl


def Main(aConf) -> tuple:
    ApiCtrl.LoadConf()

    SrvConf = aConf.get('srv_conf')
    Obj = TSrvCtrl(TSrvConf(**SrvConf))
    return (Obj, Obj.RunApp())
