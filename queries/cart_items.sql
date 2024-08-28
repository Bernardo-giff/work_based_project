WITH 
    cart_items AS (
        SELECT * FROM prd.gold.fct_cart_item
        WHERE 
            vl_quantity_sell > 0
            AND vl_unit_price_sell > 0
    )

    , orders AS (
        SELECT * FROM prd.gold.fct_order
        WHERE 
            lower(ds_type_of_load) IN ('mixed', 'liquidation')
            AND lower(ds_status_label) = 'completed'
    )

    , materials AS (
        SELECT * FROM prd.silver.stg_salesforce__material
    )

    , aliases AS (
        SELECT * FROM prd.silver.stg_salesforce__material_alias
        INNER JOIN materials
        ON fk_material = materials.pk_material
    )

    , final AS (
        SELECT
            cart_items.ds_sale_price_formula
            , cart_items.ds_purchase_price_formula
            , cart_items.ds_material_alias
            , cart_items.vl_quantity_sell
            , cart_items.vl_unit_price_sell
            , cart_items.fk_material
            , lower(aliases.cd_alias_language) AS cd_alias_language
            , cast(aliases.cd_product_id as int) AS cd_product_id
            , lower(aliases.ds_category_en) AS ds_category_en
            , lower(ds_record_type_name) AS ds_order_type
        FROM cart_items
        INNER JOIN orders
        ON cart_items.fk_order = orders.pk_order
        INNER JOIN aliases
        ON cart_items.fk_material_alias = aliases.pk_material_alias

    )

SELECT * FROM final
