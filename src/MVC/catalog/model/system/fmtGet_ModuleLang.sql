-- aLangId, aModuleId
select
    rml.title,
    rml.descr,
    rml.image
from
    ref_module rm
left join ref_module_lang rml
    on (rml.module_id = rm.id and rml.lang_id = {{aLangId}})
where
    (rm.id = {{aModuleId}}) and rm.enabled
order by
    rml.sort_order
