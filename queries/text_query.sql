WITH alias_desc AS (
    SELECT 
        "productId" AS product_id,
        "alias" AS text
    FROM public."ProductAlias" pa
)

, name_desc AS (
    SELECT 
        id AS product_id,
        "internalName" AS text
    FROM public."Product" p
)

, short_desc_desc AS (
    SELECT
        id AS product_id,
        "shortDescription" AS text
    FROM public."Product" p 
    WHERE "shortDescription" IS NOT NULL AND LENGTH("shortDescription") > 4
)

, long_desc_desc AS (
    SELECT
        id AS product_id,
        "longDescription" AS text
    FROM public."Product" p 
    WHERE "longDescription" IS NOT NULL AND LENGTH("longDescription") > 4
)

, join_text as (
SELECT * FROM alias_desc
UNION ALL
SELECT * FROM name_desc
UNION ALL
SELECT * FROM short_desc_desc
UNION ALL 
SELECT * FROM long_desc_desc)
SELECT DISTINCT * FROM join_text
