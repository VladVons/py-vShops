-- fmtGet_LayoutLang.sql
-- aLangId, aTenantId, aRoute, aTheme, aPath

select
    rll.title,
    rll.descr,
    rll.meta_descr,
    rll.meta_key
from
    ref_layout rl
join ref_layout_lang rll
    on (rll.layout_id = rl.id) and (rll.lang_id = {{aLangId}})
where
    (rl.enabled) and
    (rl.theme = '{{aTheme}}') and
    (rl.path = '{{aPath}}') and
    (rl.tenant_id = 0 or rl.tenant_id = {{aTenantId}}) and
    (rl.route = '{{aRoute}}')
