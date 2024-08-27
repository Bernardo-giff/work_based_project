WITH 
    aliases AS (
        SELECT * FROM prd.silver.stg_salesforce__material_alias
    )

    , materials AS (
        SELECT * FROM prd.silver.stg_salesforce__material
    )

    , final AS (
        SELECT
            lower(aliases.ds_material_alias) AS ds_material_alias
            , lower(aliases.cd_alias_language) AS cd_alias_language
            , cast(materials.cd_product_id as int) AS cd_product_id
        FROM aliases
        LEFT JOIN materials
        ON aliases.fk_material = materials.pk_material
    )

SELECT * FROM final