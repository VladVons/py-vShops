-- in: aLangId, CondKeyword
with wrsu as (
    select
        1 as idx,
        sort_order,
        attr,
        val,
        keyword,
        rank() over(partition by sort_order order by length(keyword) desc) as longest
    from
        ref_seo_url
    where
        (lang_id = {{aLangId}}) and
        {{CondKeyword}}
)

select
    --json_agg(json_build_object(attr, keyword))
    --
    attr,
    val,
    keyword
from
    wrsu
where
    longest = 1
order by
    sort_order
