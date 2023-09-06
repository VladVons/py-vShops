-- in: aLang, aModuleId
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
join ref_lang rlng
    on rlng.alias = '{aLang}'
join ref_module_lang rml
    on rmtg.module_id = rml.module_id and rml.lang_id = rlng.id
join ref_module rm
    on rmtg.module_id = rm.id
join ref_layout_module rlm
    on rmg.module_id = rlm.module_id
where
    (rm.enabled) and
    (rlm.enabled) and
    (rmg.module_id = {aModuleId})
order by
    rm.sort_order
