-- fmtGet_ModuleLang.sql
-- aLangId, aModuleId

select
    rml.title,
    rml.descr,
    rml.image
from
    ref_module rm
left join ref_module_to_lang rmtl
    on (rmtl.module_id = rm.id)
left join ref_module_lang rml
    on (rml.id = rmtl.module_lang_id) and (rml.lang_id = {{aLangId}})
where
    (rm.id = {{aModuleId}}) and (rm.enabled)
order by
    rml.sort_order
