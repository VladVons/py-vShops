# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.Sql.ADb import TDbAuth
from Inc.SrvWeb.SrvBase import TSrvConf
from .Api import ApiModel
from .Main import TSrvModel


def Main(aConf) -> tuple:
    SrvConf = aConf.get('srv_conf')
    Obj = TSrvModel(TSrvConf(**SrvConf))
    if (aConf.get('fs_api')):
        Res = (Obj, Obj.RunApi())
    else:
        Res = (Obj, Obj.RunApp())
    return Res

ApiModel.LoadConf()
