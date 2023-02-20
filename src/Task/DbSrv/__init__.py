# Created: 2023.02.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.WebSrv.WebSrv import TSrvConf
from Inc.Sql.ADb import TDbAuth
from .Main import TDbSrv


def Main(aConf) -> tuple:
    SrvConf = aConf.get('srv_conf')
    DbConf = aConf['db_conf']['auth']
    Obj = TDbSrv(TSrvConf(**SrvConf), TDbAuth(**DbConf))
    return (Obj, Obj.RunApp())
