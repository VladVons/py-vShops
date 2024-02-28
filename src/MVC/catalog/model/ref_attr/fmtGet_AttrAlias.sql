-- aLang, aAlias
select 
    --ras.id  as sect_id,
    ras.alias as sect_alias,
    rasi.reqire,
    rasi.val_def,
    rasi.val_min,
    rasi.val_max,
    --ra.id,
    ra.alias,
    ra.val_en,
    ral.title
from 
    ref_attr_set_item rasi  
left join ref_attr_set ras
    on (ras.id = rasi.attr_set_id)
left join ref_attr ra
    on (ra.id = rasi.attr_id)
left join ref_attr_lang ral 
    on (ral.attr_id = ra.id) and (ral.lang_id = {{aLang}})
where 
    (ras.alias = '{{aAlias}}')
order by 
    rasi.sort_order, 
    ral.title
