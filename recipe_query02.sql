CREATE DATABASE IF NOT EXISTS culinary_db;
USE culinary_db;

DROP TABLE IF EXISTS recipe_r1;

CREATE TABLE recipe_r1 (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    minutes INT DEFAULT 0,
    contributor_id INT,
    submitted DATE,
    tags TEXT,
    nutrition TEXT,
    steps TEXT NOT NULL,
    description TEXT,
    ingredients TEXT NOT NULL,
    step_count INT,
    ingredient_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'C:/Users/jonat/Desktop/Projects/python/Recipe_App/dataset/df1/cleaned_recipes.csv' 
INTO TABLE recipe_r1 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;



SELECT * FROM recipe_r1;

-- return top 5 contributor 
SELECT 
    contributor_id, 
    COUNT(*) AS recipe_count
FROM recipe_r1
WHERE contributor_id IS NOT NULL
GROUP BY contributor_id
ORDER BY recipe_count DESC
LIMIT 5;


-- average time, # of nutrition, steps 
SELECT 
    AVG(minutes) AS average_cook_time,
    AVG(step_count) AS average_number_of_steps,
    AVG(ingredient_count) AS average_ingredients_count
FROM recipe_r1;


-- 5 recipes with most types of nutrition
SELECT 
    name, 
    ingredient_count, 
    ingredients
FROM recipe_r1
ORDER BY ingredient_count DESC
LIMIT 5;


-- 5 Ingredients that is used in most recipes
WITH RECURSIVE ingredient_split AS (
    SELECT 
        id,
        SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(ingredients, '[', ''), ']', ''), "'", ""), ',', 1), ',', -1) AS ingredient,
        1 AS n
    FROM recipe_r1
    
    UNION ALL
    
    SELECT 
        r.id,
        SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(r.ingredients, '[', ''), ']', ''), "'", ""), ',', n + 1), ',', -1) AS ingredient,
        n + 1
    FROM recipe_r1 r
    INNER JOIN ingredient_split ig ON r.id = ig.id
    WHERE n < r.ingredient_count
)
SELECT 
    TRIM(ingredient) AS ingredient_name, 
    COUNT(*) AS frequency
FROM ingredient_split
WHERE ingredient != ''
GROUP BY ingredient_name
ORDER BY frequency DESC
LIMIT 5;

-- top 10 most frequent recipe tags 
WITH RECURSIVE tag_split AS (
    SELECT 
        id,
        SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(tags, '[', ''), ']', ''), "'", ""), ',', 1), ',', -1) AS tag,
        1 AS n
    FROM recipe_r1
    
    UNION ALL
    
    SELECT 
        r.id,
        SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(r.tags, '[', ''), ']', ''), "'", ""), ',', n + 1), ',', -1) AS tag,
        n + 1
    FROM recipe_r1 r
    INNER JOIN tag_split ts ON r.id = ts.id
    WHERE n < 20 AND SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(r.tags, '[', ''), ']', ''), "'", ""), ',', n + 1), ',', -1) 
          != SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(REPLACE(REPLACE(r.tags, '[', ''), ']', ''), "'", ""), ',', n), ',', -1)
)
SELECT 
    TRIM(tag) AS tag_name, 
    COUNT(*) AS recipe_count
FROM tag_split
WHERE tag != '' 
  AND tag NOT REGEXP '^[0-9]+$' -- Filter out numeric-only tags if they exist
GROUP BY tag_name
ORDER BY recipe_count DESC
LIMIT 10;
