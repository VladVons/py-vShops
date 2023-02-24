# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


def GetProductsCountInCategories(aTenantId: int) -> str:
    return f'''
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
    '''

def GetProductsCountAndNameInCategories(aTenantId: int, aLangId: int) -> str:
    return f'''
    with wrptc as (
    {GetProductsCountInCategories(aTenantId)}
    )

    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        COALESCE(wrptc.products, 0) as products,
        rpcl.title
    from
        ref_product_category rpc
    left join
        wrptc on
        (rpc.id = wrptc.category_id)
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
            1 as level,
            '' || rpc.idt as path
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
            wrpc.level + 1,
            wrpc.path  || '/' || rpc.idt
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

def GetCategoriesByParentWithProductCount(aTenantId: int, aParentIdt: int) -> str:
    return f'''
    '''
