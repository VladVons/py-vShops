-- fmtGet_SeoRedirect.sql
-- aPath

select
    url_new
from
    ref_seo_redirect
where 
    enabled and 
    (url_old = '{{aPath}}') and
    (url_old != url_new)
