
USE recipe;

CREATE TABLE IF NOT EXISTS recipes (
    name VARCHAR(255),
    id INT PRIMARY KEY,
    minutes INT,
    contributor_id INT,
    submitted VARCHAR(50),  -- We use VARCHAR first, then convert it to DATE
    tags TEXT,
    nutrition TEXT,
    n_steps INT,
    steps TEXT,
    description TEXT,
    ingredients TEXT,
    n_ingredients INT
);



LOAD DATA LOCAL INFILE 'C:/Users/jonat/Desktop/Projects/Dataset/archive(1)/RAW_recipes.csv'
INTO TABLE recipes
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- test 
SELECT *
FROM recipes 
LIMIT 5;

-- return top 5 contributor 
SELECT contributor_id, COUNT(*) AS recipe_count, recipe_count / Count(*)
FROM recipes
WHERE contributor_id IS NOT NULL
GROUP BY contributor_id
ORDER BY recipe_count DESC
LIMIT 5;



-- average time, # of nutrition, steps 
SELECT 
    AVG(minutes) AS average_cook_time,
    AVG(n_steps) AS average_number_of_steps,
    AVG(n_ingredients) AS average_ingredients_count
FROM recipes;



-- 5 recipes with most types of nutrition
SELECT name, n_ingredients, ingredients
FROM recipes
ORDER BY n_ingredients DESC
LIMIT 5;

-- 5 Ingredients that is used in most recipes
  