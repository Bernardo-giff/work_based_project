select 
  pk_cart_item
  , fk_order
  , ds_material_alias
  , ds_material
  , fk_material_alias
  , fk_material
  , ds_purchase_price_formula
  , ds_sale_price_formula
  , vl_quantity_purchase
  , vl_quantity_sell
  , vl_unit_price_purchase
  , vl_unit_price_sell
  , order.status_label
from prd.silver.stg_salesforce__cart_item cart_item
left join prd.gold.fct_order order
on cart_item.fk_order = order.pk_order

where
  vl_unit_price_purchase > 0 
  or vl_unit_price_sell > 0
  and status_label = 'Completed'