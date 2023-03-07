select
    rp.id,
    rp.enabled,
    rp.model,
    rp.is_service,
    rp.idt,
    rp.product0_id
from
    ref_product rp
where
    (rp.idt in ({ProductIdts}))
