# Created: 2023.02.16
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Sql.ADb import ListIntToComma


def GetProductsImages(aProductId: list[int]) -> str:
    return f'''
    select
        rpi.id,
        rpi.product_id,
        rpi.image
    from
        ref_product_image rpi
    where
        (rpi.product_id in ({ListIntToComma(aProductId)}))
    order by
        rpi.sort_order
        '''

def GetProductImages(aProductId: int) -> str:
    return GetProductImages([aProductId])


def GetProductsWithoutImages(aTenantId: int) -> str:
    return f'''
    select
        rp.id
    from
        ref_product rp
    left join
        ref_product_image rpi on
        (rp.id = rpi.product_id)
    where
        (rp.tenant_id = {aTenantId}) and
        (rpi.product_id is null)
    order by
        rp.id
    '''

def GetProductsCountImages(aTenantId: int) -> str:
    return f'''
    select
        rp.id,
        count(*) as images
    from
        ref_product rp
    right join
        ref_product_image rpi on
        (rp.id = rpi.product_id)
    where
        (rp.tenant_id = {aTenantId})
    group by
        rp.id
    order by
        images
    '''
