with wt1 as (
    select 
        distinct on (rlm.module_id, rlm.place) rlm.module_id as id,
        rlm.place,
        rlm.sort_order,
        rm.code,
        rm.conf,
        rm.image,
        rml.title,
        rml.intro,
        rml.descr
    from
        ref_layout rl
    join ref_tenant rt
        on rl.tenant_id = rt.id
    join ref_layout_module rlm
        on rl.id = rlm.layout_id
    join ref_module rm
        on rlm.module_id = rm.id
    join ref_module_lang rml
        on rlm.module_id = rml.module_id
    where
        (rm.enabled) and
        (rlm.enabled) and
        (rt.id = {aTenantId}) and
        ((rl.route = '{aRoute}') or (rl.id = 0)) and
        (rml.lang_id = {aLangId})
)
select
    id,
    place,
    code,
    conf,
    image,
    title,
    intro,
    descr
from 
    wt1
order by 
    place, 
    sort_order
