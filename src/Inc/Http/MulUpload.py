# Created: 2021.02.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


try:
    import asyncio
except ModuleNotFoundError:
    import uasyncio as asyncio


class TMulUpload():
    @staticmethod
    def ParseRec(aStr: str) -> dict:
        Res = {}
        for Item in aStr.split(';'):
            Arr = Item.split('=')
            if (len(Arr) == 2):
                Res[Arr[0].strip().lower()] = Arr[1].strip()
            else:
                Res[Item.strip()] = ''
        return Res

    async def Upload(self, aReader: asyncio.StreamReader, aHead: dict, aPath: str):
        Res = {}

        Rec = self.ParseRec(aHead.get('content-type', ''))
        if (not Rec):
            return Res

        Boundary = bytes('--' + Rec.get('boundary'), 'utf-8')
        BoundLen = len(Boundary)

        ContLen = int(aHead.get('content-length', '0'))
        FileN = ''
        FileH = None
        InHead = True
        Len = 0
        while (Len < ContLen):
            Line = await aReader.readline()
            Len += len(Line)

            if (Line[:BoundLen] == Boundary):
                InHead = True

                if (FileH):
                    FileH.seek(0, 2)
                    Res[FileN] = FileH.tell()

                    FileH.close()
                    FileH = None
            else:
                if (InHead):
                    if (Line == b'\r\n'):
                        InHead = False
                    else:
                        Arr = Line.decode('utf-8').split(':')
                        if (Arr[0].lower() == 'content-disposition'):
                            Rec = self.ParseRec(Arr[1])
                            FileN = Rec.get('filename')
                            if (FileN):
                                FileN = aPath + '/' + FileN.replace('"', '')
                                FileH = open(FileN, 'w', encoding='utf-8')
                else:
                    if (FileH):
                        FileH.write(Line)
                        await asyncio.sleep_ms(10)
        return Res
