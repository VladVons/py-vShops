# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.Sql.ADb import TDbAuth
from Inc.SrvWeb.SrvBase import TSrvConf
from .Api import Api, TApiConf
from .Main import TSrvDb


def Main(aConf) -> tuple:
    ApiConf = aConf['api_conf']
    Api.Init(TApiConf(**ApiConf))

    SrvConf = aConf['srv_conf']
    DbConf = aConf['db_auth']
    Obj = TSrvDb(
        TSrvConf(**SrvConf),
        TDbAuth(**DbConf)
    )
    return (Obj, Obj.RunApp())
