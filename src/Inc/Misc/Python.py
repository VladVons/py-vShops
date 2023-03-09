# Created: 2022.05.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
import traceback


class TPython():
    def __init__(self, aScript: str):
        self.Script = aScript
        self.ByteCode = None

    def ErrMsg(self, aE: Exception, aInfo: tuple = None) -> dict:
        EName = '%s, %s' % (type(aE).__name__, str(aE))
        if (aInfo):
            tb = traceback.extract_tb(aInfo[2])[-1]
            if (tb.filename):
                Res = {'type': 'err', 'data': EName, 'line_no': tb.lineno, 'line': tb.line, 'file': tb.filename}
            else:
                Res = {'type': 'err', 'data': EName, 'line_no': tb.lineno, 'line': self.GetLine(tb.lineno - 1)}
        else:
            Res = {'type': 'err', 'data': EName, 'line_no': aE.lineno, 'line': self.GetLine(aE.lineno - 1)}
        return Res

    def GetLine(self, aIdx: int) -> str:
        Lines = self.Script.splitlines()
        return Lines[aIdx].strip()

    def Compile(self) -> bool:
        try:
            self.ByteCode = None
            self.ByteCode = compile(self.Script, '', 'exec')
        except (IndentationError, SyntaxError) as E:
            return self.ErrMsg(E)
        except Exception as E:
            return self.ErrMsg(E, sys.exc_info())

    def Exec(self, aParam: dict = None) -> object:
        if (aParam is None):
            aParam = {}

        try:
            Out = {}
            Script = self.ByteCode if (self.ByteCode) else self.Script
            # pylint: disable-next=exec-used
            exec(Script, aParam, Out)
            Res = {'data': Out.get('res')}
        except (IndentationError, SyntaxError) as E:
            Res = self.ErrMsg(E)
        except Exception as E:
            Res = self.ErrMsg(E, sys.exc_info())
        return Res
