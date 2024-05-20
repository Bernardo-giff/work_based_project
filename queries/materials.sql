with default_aliases as (
  select 
    fk_material
    , ds_material_alias
  from prd.silver.stg_salesforce__material_alias
  where cd_alias_language = 'EN' and flg_is_enable = true
)

, products as (
select 
materials.cd_product_id as product_id
, materials.ds_material as material_name
, materials.ds_category_en as material_category
, default_aliases.ds_material_alias as default_english_alias
from prd.silver.stg_salesforce__material materials
left join default_aliases
on materials.pk_material = default_aliases.fk_material)

select * from products
where product_id is not null