select 
    rlm.place,
    rm.code,
    rm.conf,
    rml.title,
    rml.descr
from 
    ref_layout rl
join ref_layout_module rlm
    on rl.id = rlm.layout_id
join ref_module rm
    on rlm.module_id = rm.id
join ref_module_lang rml
    on rlm.module_id = rml.module_id 
where 
    rl.route = '{aRoute}' and
    rml.lang_id = {aLangId}
order by
    rlm.sort_order
