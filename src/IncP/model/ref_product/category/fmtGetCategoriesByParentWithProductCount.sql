with recursive wrpc as (
    select
        rpc.id,
        rpc.idt,
        rpc.parent_idt,
        1 as level,
        ARRAY[rpc.idt] as path
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
        wrpc.path  || array[rpc.idt]
    from
        ref_product_category rpc
    join
        wrpc on
        (rpc.parent_idt = wrpc.idt)
),

category_cardinatilies as (
    select
        rpc.cat_id,
        count(*) as products
    from
        ref_product_to_category rptc
    left join
        (
            select 
                id,
                unnest(path) as cat_id
            from wrpc
        ) rpc on
    (rptc.category_id = rpc.id)
    group by
        rpc.cat_id
)

select
    rpc.id,
    rpc.idt,
    rpc.parent_idt,
    rpc.level,
    rpc.path,
    products
from
     wrpc rpc
left join 
    category_cardinatilies cc
    on (rpc.idt = cc.cat_id)
