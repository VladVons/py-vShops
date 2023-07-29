-- in: aLang, aTenantId, aRoute
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
    join ref_lang rlng
        on rlng.alias = '{aLang}'
    join ref_module_lang rml
        on rlm.module_id = rml.module_id and rml.lang_id = rlng.id
    where
        ((rl.tenant_id = 0) or (rl.tenant_id = {aTenantId})) and
        (rm.enabled) and
        (rlm.enabled) and
        ((rl.route = '{aRoute}') or (rl.id = 0))
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
