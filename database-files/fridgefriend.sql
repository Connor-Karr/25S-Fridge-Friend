DROP DATABASE IF EXISTS fridgefriend;
CREATE DATABASE fridgefriend;
USE fridgefriend;


CREATE TABLE User (
   user_id INT AUTO_INCREMENT PRIMARY KEY,
   f_name VARCHAR(50) NOT NULL,
   l_name VARCHAR(50) NOT NULL,
   username VARCHAR(50) UNIQUE NOT NULL,
   password VARCHAR(255) NOT NULL,
   email VARCHAR(100) UNIQUE NOT NULL
);


CREATE TABLE Admin (
   admin_id INT AUTO_INCREMENT PRIMARY KEY,
   user_id INT,
   FOREIGN KEY (user_id) REFERENCES User(user_id)
);


CREATE TABLE Personal_Constraints (
   pc_id INT AUTO_INCREMENT PRIMARY KEY,
   budget DECIMAL(10,2),
   dietary_restrictions VARCHAR(50),
   personal_diet VARCHAR(50),
   age_group VARCHAR(20)
);


CREATE TABLE Workout (
   workout_id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   quantity INT,
   weight DECIMAL(5,2),
   calories_burnt INT
);


CREATE TABLE Ingredient (
   ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
   expiration_date DATE,
   name VARCHAR(100)
);


CREATE TABLE Recipe (
   recipe_id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   instructions TEXT
);


CREATE TABLE Recipe_Ingredient (
   recipe_id INT,
   ingredient_id INT,
   quantity DECIMAL(10,2) NOT NULL,
   unit VARCHAR(20),
   PRIMARY KEY (recipe_id, ingredient_id),
   FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
   FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE Macronutrients (
   macro_id INT AUTO_INCREMENT PRIMARY KEY,
   ingredient_id INT,
   protein DECIMAL(8,2),
   fat DECIMAL(8,2),
   fiber DECIMAL(8,2),
   vitamin DECIMAL(8,2),
   sodium DECIMAL(8,2),
   calories INT,
   carbs DECIMAL(8,2),
   FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE Ingredient_Macronutrient (
   ingredient_id INT,
   macro_id INT,
   PRIMARY KEY (ingredient_id, macro_id),
   FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id),
   FOREIGN KEY (macro_id) REFERENCES Macronutrients(macro_id)
);


CREATE TABLE Brand (
   brand_id INT AUTO_INCREMENT PRIMARY KEY,
   name VARCHAR(100) NOT NULL,
   is_trusted BOOLEAN DEFAULT TRUE
);


CREATE TABLE Recipe_Brand (
   recipe_id INT,
   brand_id INT,
   PRIMARY KEY (recipe_id, brand_id),
   FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
   FOREIGN KEY (brand_id) REFERENCES Brand(brand_id)
);


CREATE TABLE Fridge_Inventory (
   fridge_id INT AUTO_INCREMENT PRIMARY KEY
);


CREATE TABLE Fridge_Ingredient (
   fridge_id INT,
   ingredient_id INT,
   quantity DECIMAL(10,2) NOT NULL,
   unit VARCHAR(20),
   is_expired BOOLEAN DEFAULT FALSE,
   PRIMARY KEY (fridge_id, ingredient_id),
   FOREIGN KEY (fridge_id) REFERENCES Fridge_Inventory(fridge_id),
   FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE Shopping_List (
   list_id INT AUTO_INCREMENT PRIMARY KEY
);


CREATE TABLE ShoppingList_Ingredient (
   list_id INT,
   ingredient_id INT,
   quantity DECIMAL(10,2) NOT NULL,
   unit VARCHAR(20),
   cost DECIMAL(10,2),
   PRIMARY KEY (list_id, ingredient_id),
   FOREIGN KEY (list_id) REFERENCES Shopping_List(list_id),
   FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE Food_Scan_Log (
   log_id INT AUTO_INCREMENT PRIMARY KEY,
   ingredient_id INT,
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   status VARCHAR(50),
   FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE Client (
   client_id INT AUTO_INCREMENT PRIMARY KEY,
   user_id INT,
   pc_id INT,
   fridge_id INT,
   list_id INT,
   log_id INT,
   flag INT,
   FOREIGN KEY (user_id) REFERENCES User(user_id),
   FOREIGN KEY (pc_id) REFERENCES Personal_Constraints(pc_id),
   FOREIGN KEY (fridge_id) REFERENCES Fridge_Inventory(fridge_id),
   FOREIGN KEY (list_id) REFERENCES Shopping_List(list_id),
   FOREIGN KEY (log_id) REFERENCES Food_Scan_Log(log_id)
);


CREATE TABLE Meal_Plan (
   meal_id INT AUTO_INCREMENT PRIMARY KEY,
   pc_id INT,
   recipe_id INT,
   quantity INT,
   FOREIGN KEY (pc_id) REFERENCES Personal_Constraints(pc_id),
   FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id)
);


CREATE TABLE Leftover (
   leftover_id INT AUTO_INCREMENT PRIMARY KEY,
   recipe_id INT,
   quantity INT,
   is_expired BOOLEAN DEFAULT FALSE,
   FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id)
);


CREATE TABLE Nutrition_Tracking (
   tracking_id INT AUTO_INCREMENT PRIMARY KEY,
   client_id INT,
   protein DECIMAL(8,2),
   fat DECIMAL(8,2),
   fiber DECIMAL(8,2),
   sodium DECIMAL(8,2),
   vitamins DECIMAL(8,2),
   calories INT,
   carbs DECIMAL(8,2),
   FOREIGN KEY (client_id) REFERENCES Client(client_id)
);


CREATE TABLE Health_Advisor (
   advisor_id INT AUTO_INCREMENT PRIMARY KEY,
   experience_years INT,
   client_id INT,
   FOREIGN KEY (client_id) REFERENCES Client(client_id)
);


CREATE TABLE Client_Health_Advisor (
   client_id INT,
   advisor_id INT,
   PRIMARY KEY (client_id, advisor_id),
   FOREIGN KEY (client_id) REFERENCES Client(client_id),
   FOREIGN KEY (advisor_id) REFERENCES Health_Advisor(advisor_id)
);


CREATE TABLE Client_Workout (
   client_id INT,
   workout_id INT,
   PRIMARY KEY (client_id, workout_id),
   FOREIGN KEY (client_id) REFERENCES Client(client_id),
   FOREIGN KEY (workout_id) REFERENCES Workout(workout_id)
);


CREATE TABLE Error_Log (
   error_id INT AUTO_INCREMENT PRIMARY KEY,
   client_id INT,
   log_id INT,
   message TEXT,
   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (client_id) REFERENCES Client(client_id),
   FOREIGN KEY (log_id) REFERENCES Food_Scan_Log(log_id)
);

-- MOCK DATA


-- 1.1: Update expired ingredients in fridge
UPDATE Fridge_Ingredient
SET is_expired = TRUE
WHERE ingredient_id IN (
  SELECT ingredient_id FROM Ingredient WHERE expiration_date < '2024-04-01'
);

-- 1.2: Add missing ingredients for planned meals to shopping list
INSERT INTO ShoppingList_Ingredient (list_id, ingredient_id, quantity, unit, cost)
SELECT 1, ri.ingredient_id, ri.quantity, ri.unit, 0.00
FROM Meal_Plan mp
JOIN Recipe_Ingredient ri ON mp.recipe_id = ri.recipe_id
LEFT JOIN Fridge_Ingredient fi ON ri.ingredient_id = fi.ingredient_id AND fi.fridge_id = 1
WHERE fi.ingredient_id IS NULL;

-- 1.3: Add new meal plan if within budget
INSERT INTO Meal_Plan (pc_id, recipe_id, quantity)
SELECT 1, recipe_id, 1
FROM Recipe
WHERE recipe_id = 3;

-- 1.4: Add cooked recipe to leftovers
INSERT INTO Leftover (recipe_id, quantity, is_expired)
VALUES (1, 1, FALSE);

-- 1.5: Delete expired ingredients from fridge
DELETE FROM Fridge_Ingredient
WHERE is_expired = TRUE;

-- 1.6: Delete outdated meal plans
DELETE FROM Meal_Plan
WHERE meal_id = 1;

-- 2.1: Update inaccurate macronutrient values
UPDATE Macronutrients
SET protein = 10.0, fat = 2.0, carbs = 30.0, calories = 200
WHERE macro_id = 1;

-- 2.2: Update ingredient name to reflect new category
UPDATE Ingredient
SET name = 'Milk - Organic Dairy'
WHERE ingredient_id = 1;

-- 2.3: Delete unused ingredients from fridge
DELETE FROM Fridge_Ingredient
WHERE ingredient_id = 7;

-- 2.4: Mark test users as inactive
UPDATE User
SET email = 'inactive@example.com'
WHERE username = 'testuser';

-- 2.5: Add new trusted food item with macros
INSERT INTO Ingredient (ingredient_id, expiration_date, name) 
VALUES (11, '2024-06-01', 'Oatmeal');
INSERT INTO Macronutrients (
  macro_id, ingredient_id, protein, fat, fiber, vitamin, sodium, calories, carbs
) VALUES (11, 11, 15.0, 5.0, 2.0, 1.0, 100.0, 250, 30.0);

-- 2.6: Log a failed food scan for a new ingredient
INSERT INTO Ingredient (ingredient_id, expiration_date, name)
VALUES (12, '2025-06-01', 'Almond Milk');
INSERT INTO Food_Scan_Log (log_id, ingredient_id, status)
VALUES (5, 12, 'FAILED');

-- 3.1: Update dietary restrictions to track allergens
UPDATE Personal_Constraints
SET dietary_restrictions = 'peanuts,dairy,soy'
WHERE pc_id = 1;

-- 3.2: Add meal plan matching dietary preference
INSERT INTO Meal_Plan (pc_id, recipe_id, quantity)
VALUES (1, 3, 1);

-- 3.3: Delete ineffective meal plans
DELETE FROM Meal_Plan
WHERE recipe_id = 1 AND pc_id = 2;

-- 3.4: Update age group for a client's constraints
UPDATE Personal_Constraints
SET age_group = 'adult'
WHERE pc_id = 1;

-- 3.5: Update macro tracking for partial meal consumption
UPDATE Nutrition_Tracking
SET protein = 50.0, fat = 15.0, calories = 1500
WHERE tracking_id = 1;

-- 3.6: Archive old client profiles
UPDATE Client
SET flag = 0
WHERE client_id = 2;

-- 4.1: Delete old meal plans
DELETE FROM Meal_Plan
WHERE meal_id = 3;

-- 4.2: Delete workout connections
DELETE FROM Client_Workout
WHERE client_id = 1 AND workout_id = 1;

-- 4.3: Add carb-heavy meal for race day
INSERT INTO Meal_Plan (pc_id, recipe_id, quantity)
VALUES (1, 1, 2);

-- 4.4: Add high-protein recovery meal
INSERT INTO Meal_Plan (pc_id, recipe_id, quantity)
VALUES (2, 4, 1);

-- 4.5: Update macro goals for bulking
UPDATE Nutrition_Tracking
SET protein = 180.0, fat = 60.0, carbs = 400.0, calories = 2800
WHERE tracking_id = 2;

-- 4.6: Add coach recommended meals to plan
INSERT INTO Meal_Plan (pc_id, recipe_id, quantity)
VALUES (2, 5, 1);