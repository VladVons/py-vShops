# Created: 2024.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.Misc.Mail import TMail, TMailSend, TMailSmtp
from IncP.LibCtrl import Log


async def Main(self, aData: dict = None) -> dict:
    Post = aData.get('post')
    if (Post):
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
    else:
        LangKey = ''

    LangTr = aData['lang']
    AddressJ = LangTr['addressJ_']
    Schema = {
        '@context': 'https://schema.org',
        '@type': 'Organization',
        'url': LangTr.get('url_'),
        'logo': LangTr.get('url_') + '/' + LangTr.get('logo_'),
        'name': AddressJ['company'],
        'description': LangTr.get('about_descr'),
        'email': LangTr.get('email_'),
        'telephone': LangTr.get('phone_'),
        'address': {
            '@type': 'PostalAddress',
            'streetAddress': AddressJ['street'],
            'addressLocality': AddressJ['city'],
            'addressCountry': AddressJ['country'],
            'postalCode': AddressJ['post_code']
        }
    }

    return {
        'schema': json.dumps(Schema),
        'mail_status': LangKey
    }
