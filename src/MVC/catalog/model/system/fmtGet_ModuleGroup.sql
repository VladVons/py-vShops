-- in: aLangId, aModuleId
select
    rlm.place,
    rm.id,
    rm.code,
    rm.conf,
    rm.image,
    rm.route,
    rml.title,
    rml.intro,
    rml.descr
from
    ref_module_group rmg
join ref_module_to_group rmtg
    on rmg.id = rmtg.group_id
join ref_module_lang rml
    on (rmtg.module_id = rml.module_id) and (rml.lang_id = {{aLangId}})
join ref_module rm
    on rmtg.module_id = rm.id
join ref_layout_module rlm
    on rmg.module_id = rlm.module_id
join ref_layout rl
    on rlm.layout_id = rl.id
where
    (rm.enabled) and
    (rlm.enabled) and
    (rmg.module_id = {{aModuleId}}) and
    (rl.theme = 't2')
order by
    rm.sort_order
