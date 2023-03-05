import inspect
import sys
import os
from Inc.Util.Str import Format


def Main():
    #Items = inspect.stack()
    #q2 = sys._getframe().f_back.f_code.co_name
    # q1 = sys._getframe()
    # q1a = q1.f_back

    # q2 = sys._getframe(1)
    # q2a = q2.f_back

    # q3 = sys.exc_info()
    # q4 = q3.tb_frame.f_back

    # print(os.getcwd())

    Sql = Format('fmtGetCategoriesByParent.sql',
        {'aTenantId': 1, 'aParentIdt': 0, 'aDepth': 2},
        __file__
    )
    return Sql
