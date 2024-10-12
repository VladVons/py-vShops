# Created: 2024.08.03
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
from datetime import datetime
#
from .DbList import TDbList


class TJsonEncoder(json.JSONEncoder):
    def default(self, o):
        # match_
        if (isinstance(o, TDbList)):
            Res = o.Export()
        elif (isinstance(o, set)):
            Res = list(o)
        elif (isinstance(o, datetime)):
            Res = o.strftime('%Y-%m-%d %H:%M:%S')
        else:
            Res = str(o)
        return Res

    @staticmethod
    def Dumps(aObj):
        return json.dumps(aObj, cls = TJsonEncoder)
