# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import TDbAuth
from .Api import Api, TApiConf
from .Main import TSrvDb, TSrvDbConf


def Main(aConf) -> tuple:
    ApiConf = aConf['api_conf']
    Api.Init(TApiConf(**ApiConf))

    SrvConf = aConf['srv_conf']
    DbConf = aConf['db_auth']
    Obj = TSrvDb(
        TSrvDbConf(**SrvConf),
        TDbAuth(**DbConf)
    )
    return (Obj, Obj.RunApp())
