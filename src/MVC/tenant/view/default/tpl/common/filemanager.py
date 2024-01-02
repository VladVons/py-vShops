# Created: 2023.12.15
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import DeepGetByList
from IncP.FormBase import TFormBase


class TForm(TFormBase):
    async def _DoRender(self):
        if (DeepGetByList(self.out, ['data', 'btn_upload'])):
            for FileField, Key in self.out.files:
                Data = FileField.file.read()
                FileField.file.close()

                if (Key not in self.out.data):
                    self.out.data[Key] = {}
                self.out.data[Key][FileField.filename] = Data

        Data = await self.ExecCtrlDef()
        self.out.update(Data)
