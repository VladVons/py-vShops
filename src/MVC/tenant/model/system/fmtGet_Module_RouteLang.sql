-- in: aLangId, aTenantId, aRoute, aPath
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
    left join ref_layout_module rlm
        on (rlm.layout_id = rl.id)
    left join ref_module rm
        on (rm.id = rlm.module_id)
    left join ref_module_to_lang rmtl
        on (rmtl.module_id = rm.id)
    join ref_module_lang rml
        on (rml.id = rmtl.module_lang_id) and (rml.lang_id = {{aLangId}})
    where
        (rl.enabled) and
        (rl.theme = '{{aTheme}}') and
        (rl.path = '{{aPath}}') and
        ((rl.tenant_id = 0) or (rl.tenant_id = {{aLangId}})) and
        (rm.enabled) and
        (rlm.enabled) and
        ((rl.route = '{{aRoute}}') or (rl.common))
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
