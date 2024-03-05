--fmtGet_Langs.sql

select
    id, 
    alias,
    title
from 
    ref_lang
where 
    enabled
