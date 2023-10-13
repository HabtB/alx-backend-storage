-- Lists all bands with Glam rock AS their main style, ranked by their longevity

SELECT
    band_name,
    YEAR('2022-12-31') - CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(attributes, 'formed:', -1), ',', 1) AS SIGNED) AS lifespan
FROM metal_bands
WHERE LOCATE('Glam rock', attributes) > 0
ORDER BY lifespan DESC;

