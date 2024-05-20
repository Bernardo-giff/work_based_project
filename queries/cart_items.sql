select 
  cart_item.pk_cart_item
  , cart_item.fk_order
  , cart_item.ds_material_alias
  , cart_item.ds_material
  , cart_item.fk_material_alias
  , cart_item.fk_material
  , cart_item.ds_purchase_price_formula
  , material.cd_alias_language
  , cart_item.ds_sale_price_formula
  , cart_item.vl_quantity_purchase
  , cart_item.vl_quantity_sell
  , cart_item.vl_unit_price_purchase
  , cart_item.vl_unit_price_sell
  , order.ds_status_label
from prd.gold.fct_cart_item cart_item
left join prd.gold.fct_order order
on cart_item.fk_order = order.pk_order
left join prd.gold.dim_material material
on cart_item.fk_material_alias = material.pk_material_alias

where
  vl_unit_price_purchase > 0 
  or vl_unit_price_sell > 0
  and ds_status_label = 'Completed'