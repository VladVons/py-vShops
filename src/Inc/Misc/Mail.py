# Created: 2022.10.29
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import asyncio
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
#
from Inc.DataClass import DDataClass


@DDataClass
class TMailSmtp():
    username: str
    password: str
    hostname: str = 'smtp.gmail.com'
    port: int = 465
    use_tls: bool = True


@DDataClass
class TMailSend():
    mail_to: list[str]
    mail_subject: str
    mail_from: str
    mail_body: str = ''
    file: list[str] = []
    Data: dict = {}
    Lock: asyncio.Lock = None


class TMail():
    def __init__(self, aMailSmtp: TMailSmtp):
        self._MailSmtp = aMailSmtp

    async def Send(self, aData: TMailSend) :
        EMsg = MIMEMultipart()
        EMsg['From'] = aData.mail_from
        EMsg['To'] = ', '.join(aData.mail_to)
        EMsg['Subject'] = aData.mail_subject
        if (aData.mail_body):
            EMsg.attach(MIMEText(aData.mail_body))

        for File in aData.file:
            with open(File, 'rb') as F:
                Part = MIMEApplication(F.read(), Name=os.path.basename(File))
                Part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(File)
                EMsg.attach(Part)

        for Key, Stream in aData.Data.items():
            Stream.seek(0)
            Part = MIMEApplication(Stream.read(), Name=Key)
            Part['Content-Disposition'] = f'attachment; filename="{Key}"'
            EMsg.attach(Part)
            Stream.close()

        Smtp = self._MailSmtp.__dict__
        return await aiosmtplib.send(EMsg, **Smtp)
