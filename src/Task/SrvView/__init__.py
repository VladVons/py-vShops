from Task import ConfTask
from IncP.ApiBase import TApiConf
from .Api import Api, TApiViewConf
from .Main import TSrvView, TSrvViewConf


def Main(aConf) -> tuple:
    ApiConf = aConf['api_conf']
    Api.Init(TApiViewConf(**ApiConf))

    Conf = aConf.get('srv_conf', {})
    SrvViewFormConf = TSrvViewConf(**Conf)
    Obj = TSrvView(SrvViewFormConf)
    return (Obj, Obj.RunApp())
