# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def GetProductsCountInCategories(aTenantId: int, aLangId: int) -> str:
    return f'''
    with wpic as (
        select
            rptc.id,
            rptc.idt,
            count(*) as protucts
        from
            ref_product_to_category rptc
        join
            ref_product_category rpc on
            (rptc.id = rpc.id)
        where
            (rpc.tenant_id = {aTenantId})
        group by
            rptc.id
    )

    select
        rpc.parent_idt,
        wpic.category_id as id,
        wpic.protucts,
        rpcl.title
    from
        wpic
    join
        ref_product_category rpc on
        (wpic.category_id = rpc.id)
    join
        ref_product_category_lang rpcl on
        (wpic.category_id = rpcl.category_id)
    where
        (rpcl.lang_id = {aLangId})
        '''

# https://habr.com/ru/post/269497
def GetCategoriesByParent(aTenatId: int, aParentId: int) -> str:
    return f'''
    with recursive wrpc as (
        select
            id,
            idt,
            parent_idt,
            1 as level
        from
            ref_product_category
        where
            (tenant_id = {aTenatId}) and
            (parent_idt = {aParentId})

        union all

        select
            rpc.id,
            rpc.idt,
            rpc.parent_idt,
            wrpc.level + 1 as level
        from
            ref_product_category rpc
        join
            wrpc on
            (rpc.parent_idt = wrpc.id)
    )
    select
        *
    from
        wrpc
    '''
