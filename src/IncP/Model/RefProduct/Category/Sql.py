# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def GetProductsCountInCategories(aTenantId: int, aLangId: int) -> str:
    return f'''
    with wpic as (
        select
            rptc.category_id,
            count(*) as protucts
        from
            ref_product_to_category rptc
        join
            ref_product_category rpc on
            (rptc.category_id = rpc.id)
        where
            (rpc.tenant_id = {aTenantId})
        group by
            rptc.category_id
    )

    select
        rpc.parent_id,
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
            parent_id,
            1 as level
        from
            ref_product_category
        where
            (tenant_id = {aTenatId}) and
            (parent_id = {aParentId})

        union all

        select
            rpc.id,
            rpc.parent_id,
            wrpc.level + 1 as level
        from
            ref_product_category rpc
        join
            wrpc on
            (rpc.parent_id = wrpc.id)
    )
    select
        *
    from
        wrpc
    '''
