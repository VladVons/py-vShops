import json
from datetime import datetime
#
from Inc.Misc.Misc import TJsonEncoder

Obj = {
    'now': datetime.now()
}

Str = json.dumps(Obj, cls=TJsonEncoder)
print(Str)
