# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def GetProductsCountInCategories(aTenantId: int, aLangId: int) -> str:
    return f'''
    with wpic as (
        select
            rptc.category_id,
            count(*) as products
        from
            ref_product_to_category rptc
        left join
            ref_product_category rpc on
            (rptc.product_id = rpc.id)
        where
            (rpc.tenant_id = {aTenantId})
        group by
            rptc.category_id
    )

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        COALESCE(wpic.products, 0),
        rpcl.title
    from
        ref_product_category rpc
    left join
        wpic on
        (rpc.id = wpic.category_id)
    left join
        ref_product_category_lang rpcl on
        (rpc.id = rpcl.category_id)
    where
        (rpcl.lang_id = {aLangId})
        '''

# https://habr.com/ru/post/269497
def GetCategoriesByParent(aTenantId: int, aParentIdt: int, aDepth: int = 99) -> str:
    return f'''
    with recursive wrpc as (
        select
            rpc.id,
            rpc.idt,
            rpc.parent_idt,
            1 as level
        from
            ref_product_category rpc
        where
            (tenant_id = {aTenantId}) and
            (parent_idt = {aParentIdt})

        union all

        select
            rpc.id,
            rpc.idt,
            rpc.parent_idt,
            wrpc.level + 1
        from
            ref_product_category rpc
        join
            wrpc on
            (rpc.parent_idt = wrpc.idt)
		where
			wrpc.level < {aDepth}
    )
    select
        *
    from
        wrpc
    '''
