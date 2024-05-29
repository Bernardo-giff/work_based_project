select 
    fk_material_alias 
    , lower(txt_price_formula)
from prd.gold.fct_contract_material
where 
    txt_price_formula is not null
    and lower(txt_price_formula) not like "% test %" 
    and lower(txt_price_formula) not like "test %"