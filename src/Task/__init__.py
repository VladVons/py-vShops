from Inc.Conf import TConf
from Inc.UtilP.Misc import GetEnvWithWarn
from IncP.Log import Log


ConfTask = TConf('Conf/Task.py')
ConfTask.Load()
ConfTask.Def = {'Env_EmailPassw': GetEnvWithWarn('Env_EmailPassw', Log)}
