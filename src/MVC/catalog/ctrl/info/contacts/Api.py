# Created: 2024.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Misc.Mail import TMail, TMailSend, TMailSmtp
from IncP.LibCtrl import Log


async def Main(self, aData: dict = None) -> dict:
    Post = aData.get('post')
    if (not Post):
        return

    Conf = self.Cache.Get('conf_tenant_0', {})

    ConfSmtp = Conf['email_smtp']
    MailSmtp = TMailSmtp(**ConfSmtp)
    MailAdmin = Conf['email_admin'].split(',')

    Body = [Post['comment'], '---', Post['name'], Post['email']]
    Data = TMailSend(
        mail_from = ConfSmtp['username'],
        mail_to = [Post['email']] + MailAdmin,
        mail_subject = f'1x1 post. {Post["name"]}',
        mail_body = '\n'.join(Body)
    )

    try:
        await TMail(MailSmtp).Send(Data)
        LangKey = 'send_ok'
    except Exception as E:
        LangKey = 'send_err'
        Log.Print(1, 'x', 'TMail error', aE=E)
    return {'mail_status': LangKey}
