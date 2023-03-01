from Task import ConfTask
from .Api import Api
from .Main import TSrvViewForm, TSrvViewFormConf


def Main(aConf) -> tuple:
    Api.WebClient.Auth = aConf.SrvAuth
    aConf.Def = ConfTask

    Conf = aConf.get('srv_conf', {})
    SrvViewFormConf = TSrvViewFormConf(**Conf)
    Obj = TSrvViewForm(SrvViewFormConf)
    return (Obj, Obj.RunApp())
