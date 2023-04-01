select
    rlm.place,
    rm.id,
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
    (rl.route = '{aRoute}') and
    (rml.lang_id = {aLangId})
order by
    rlm.sort_order
