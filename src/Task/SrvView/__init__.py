from Task import ConfTask
from .Main import TSrvView, TSrvViewConf


def Main(aConf) -> tuple:
    Conf = aConf.get('srv_conf', {})
    SrvViewFormConf = TSrvViewConf(**Conf)
    Obj = TSrvView(SrvViewFormConf)
    return (Obj, Obj.RunApp())
