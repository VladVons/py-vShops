# Created: 2024.06.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import random
#
from Inc.ParserX.Common import TPluginBase
from Inc.ParserX.CommonSql import TSqlBase, TSqlTenantConf
from Inc.Sql import TDbPg, TDbAuth, TDbExecPool, ListToComma
from IncP.Log import Log
from .AI import TOpenAI



Textes = {
    'Ноутбук': '''Напиши унікальний опис товару для покращення SEO інтернет сторінки до {TextSize} символів.
Опиши сильні сторони товару, дай приклади що ним можна робити і як використовувати.
Якщо розмір оперативної пам'яті менше або рівна 4Gb, то запропонуй для кращої роботи докупити пам'ять, щоб стало 8Gb.
Підкресли про заощадження грошей вибираючи вживаний компютер.
Використовуй теги <h3> для характеристик товару і <b> для підкреслення цікавих моментів. Не використовуй тег <ul>.
Замість ціни пиши {{{{product.price_sale}}}}.
''',
    "Комп'ютер": '''Напиши унікальний обєктивний опис товару для покращення SEO інтернет сторінки до {TextSize} символів.
Опиши сильні сторони товару, дай приклади що ним можна робити і як використовувати.
Зазнач про переваги розміру корпусу.
Якщо розмір оперативної пам'яті менше або рівна 4Gb, то запропонуй для кращої роботи докупити пам'ять, щоб стало 8Gb.
Якщо тип сховища HDD, то запропонуй докупити більш швидший тип SSD.
Якщо обєм жорсткого диску менше 250Gb, то порекомендуй його збільшити для домашнього відео архіву.
Підкресли про заощадження грошей вибираючи вживаний компютер.
Використовуй теги <h3> для характеристик товару і <b> для підкреслення цікавих моментів. Не використовуй тег <ul>.
Замість ціни пиши {{{{product.price_sale}}}}.
''',
    'Монітор': '''Напиши унікальний обєктивний опис товару для покращення SEO інтернет сторінки до {TextSize} символів.
Опиши сильні сторони товару, дай приклади що ним можна робити і як використовувати.
Підкресли про заощадження грошей вибираючи вживаний компютер.
Використовуй теги <h3> для характеристик товару і <b> для підкреслення цікавих моментів. Не використовуй тег <ul>.
Замість ціни пиши {{{{product.price_sale}}}}.
'''
}


async def UpdateDb(aSql: TSqlBase, aSqlConf: TSqlTenantConf) -> list[int]:
    assert(aSqlConf.categories), 'no categories defined'
    Categories = [x.translate(aSql.Escape) for x in aSqlConf.categories]
    Dbl = await aSql.ExecQuery(__package__, 'fmtGet_NoDescr.sql',
        {
            'aLangId': aSql.lang_id,
            'aTenantId': aSql.tenant_id,
            'aLimit': aSqlConf.parts,
            'aCategories': ListToComma(Categories)
        }
    )
    if (not Dbl):
        Log.Print(1, 'i', f'No products without descr in {aSqlConf.categories}')
        return

    Queries = []
    for Rec in Dbl:
        Attr = [f'{xKey}: {xVal}' for xKey, xVal in Rec.attr]
        Cond = 'вживаний' if Rec.cond_en == 'used' else 'новий'
        Attr.append(f'Стан: {Cond}')
        Attr.append('Ціна: 1000 грн.')

        Text = Textes.get(Rec.category_title)
        assert(Text), f'no AI text found for category {Rec.category_title}'
        Text = Text.format(TextSize=random.randint(2500, 5000))

        Query = f'''
            {Text}
            {Rec.category_title} {Rec.title}
            {'\n'.join(Attr)}
        '''
        Queries.append(Query)

    AI = TOpenAI()
    ResAI = await AI.Exec(Queries, 5)

    Values = [
        f"({xRec.id}, '{xResAI['data'].replace("'", '')}')"
        for xRec, xResAI in zip(Dbl, ResAI)
        if 'err' not in xResAI
    ]

    Res = []
    if (Values):
        Query = f'''
            with src (id, descr) as (
                values {', '.join(Values)}
            )
            update
                ref_product_lang rpl
            set
                descr = src.descr
            from
                src
            where
                (product_id = src.id)
            returning
                product_id
        '''
        Dbl = await TDbExecPool(aSql.Db.Pool).Exec(Query)

        Res = Dbl.ExportList('product_id')
        Log.Print(1, 'i', f'Descr updated for product_id {Res}')
    else:
        Log.Print(1, 'i', 'No AI text returned')
    return Res


class TOut_vShopNoDescr_db(TPluginBase):
    async def Run(self):
        Conf = self.Conf.GetKey('auth')
        DbAuth = TDbAuth(**Conf)
        Db = TDbPg(DbAuth)
        await Db.Connect()

        SqlDef = self.Conf.GetKey('sql', {})
        SqlConf = TSqlTenantConf(**SqlDef)

        Sql = TSqlBase(Db)
        await Sql.LoadTenantConf(SqlConf.tenant, SqlConf.lang)
        await UpdateDb(Sql, SqlConf)

        await Db.Close()
