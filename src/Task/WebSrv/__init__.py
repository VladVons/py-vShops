from Inc.WebSrv.WebSrv import TWebSrvConf, TSrvConf
from Task import ConfTask
from .Api import Api
from .Main import TWebSrv


def Main(aConf) -> tuple:
    Api.WebClient.Auth = aConf.SrvAuth
    aConf.Def = ConfTask

    Conf = aConf.get('srv_conf', {})
    WebSrvConf = TWebSrvConf(**Conf)
    Obj = TWebSrv(WebSrvConf, aConf)
    return (Obj, Obj.RunApp())
