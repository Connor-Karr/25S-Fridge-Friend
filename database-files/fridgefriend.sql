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

-- Sample inserts for base tables
-- Insert ingredients
INSERT INTO Ingredient (ingredient_id, expiration_date, name) VALUES 
(1, '2025-05-01', 'Milk - Dairy'),
(2, '2025-05-15', 'Eggs'),
(3, '2025-06-01', 'Chicken Breast'),
(4, '2025-05-20', 'Spinach'),
(5, '2025-07-10', 'Rice'),
(6, '2025-06-15', 'Tomatoes'),
(7, '2025-05-30', 'Flour'),
(8, '2025-06-30', 'Quinoa'),
(9, '2025-06-01', 'Unknown Cereal'),
(10, '2025-07-15', 'Protein Powder');

-- Insert recipes
INSERT INTO Recipe (recipe_id, name, instructions) VALUES
(1, 'Pasta Bowl', 'Boil water then cook the pasta then we finally serve.'),
(2, 'Chicken Stir Fry', 'Cut chicken into small pieces. Heat oil in pan. Add chicken and cook until browned. Add vegetables and stir fry until tender.'),
(3, 'Spinach Omelette', 'Beat eggs in a bowl. Heat oil in pan. Pour eggs and add spinach. Cook until set.'),
(4, 'Protein Shake', 'Blend protein powder with milk and a banana.'),
(5, 'Power Bowl', 'Mix quinoa, chicken, and vegetables in a bowl.'),
(6, 'Chicken Rice Soup', 'Simmer chicken broth with rice, chicken pieces, and vegetables until cooked through.');

-- Insert users
INSERT INTO User (user_id, f_name, l_name, username, password, email) VALUES
(1, 'Test', 'User', 'testuser', 'pass', 'test@example.com'),
(2, 'Jane', 'Doe', 'janedoe', 'password123', 'jane@example.com');

-- Insert personal constraints
INSERT INTO Personal_Constraints (pc_id, budget, dietary_restrictions, personal_diet, age_group) VALUES
(1, 100.00, 'peanuts,dairy', 'balanced', 'teen'),
(2, 150.00, 'gluten', 'keto', 'adult');

-- Insert fridges
INSERT INTO Fridge_Inventory (fridge_id) VALUES (1), (2);

-- Insert shopping lists
INSERT INTO Shopping_List (list_id) VALUES (1), (2);

-- Insert bridge tables
-- Recipe ingredients
INSERT INTO Recipe_Ingredient (recipe_id, ingredient_id, quantity, unit) VALUES
(1, 5, 1.0, 'cup'), -- Pasta Bowl - Rice
(1, 6, 2.0, 'whole'), -- Pasta Bowl - Tomatoes
(2, 3, 8.0, 'oz'), -- Chicken Stir Fry - Chicken Breast
(2, 4, 2.0, 'cup'), -- Chicken Stir Fry - Spinach
(2, 5, 1.0, 'cup'), -- Chicken Stir Fry - Rice
(3, 2, 3.0, 'whole'), -- Spinach Omelette - Eggs
(3, 4, 1.0, 'cup'), -- Spinach Omelette - Spinach
(4, 1, 1.0, 'cup'), -- Protein Shake - Milk
(4, 10, 2.0, 'scoop'), -- Protein Shake - Protein Powder
(5, 3, 6.0, 'oz'), -- Power Bowl - Chicken Breast
(5, 4, 2.0, 'cup'), -- Power Bowl - Spinach
(5, 8, 1.0, 'cup'), -- Power Bowl - Quinoa
(6, 3, 4.0, 'oz'), -- Chicken Rice Soup - Chicken Breast
(6, 5, 0.5, 'cup'), -- Chicken Rice Soup - Rice
(6, 6, 2.0, 'whole'), -- Chicken Rice Soup - Tomatoes
(6, 4, 1.0, 'cup'); -- Chicken Rice Soup - Spinach

-- Fridge ingredients
INSERT INTO Fridge_Ingredient (fridge_id, ingredient_id, quantity, unit, is_expired) VALUES
(1, 1, 1.0, 'gallon', FALSE), -- Fridge 1 - Milk
(1, 2, 12.0, 'whole', FALSE), -- Fridge 1 - Eggs
(1, 4, 1.0, 'bag', FALSE), -- Fridge 1 - Spinach
(2, 3, 16.0, 'oz', FALSE), -- Fridge 2 - Chicken Breast
(2, 5, 5.0, 'pound', FALSE), -- Fridge 2 - Rice
(2, 6, 4.0, 'whole', FALSE); -- Fridge 2 - Tomatoes

-- Shopping list ingredients
INSERT INTO ShoppingList_Ingredient (list_id, ingredient_id, quantity, unit, cost) VALUES
(1, 3, 16.0, 'oz', 5.99), -- Shopping List 1 - Chicken Breast
(1, 7, 5.0, 'pound', 2.99), -- Shopping List 1 - Flour
(2, 1, 1.0, 'gallon', 3.49), -- Shopping List 2 - Milk
(2, 4, 1.0, 'bag', 2.99), -- Shopping List 2 - Spinach
(2, 6, 4.0, 'whole', 1.99); -- Shopping List 2 - Tomatoes

-- Insert workout
INSERT INTO Workout (workout_id, name, quantity, weight, calories_burnt) VALUES
(1, 'Running', 30, NULL, 300),
(2, 'Weight Lifting', 45, 150.00, 250);

-- Insert macronutrients
INSERT INTO Macronutrients (macro_id, ingredient_id, protein, fat, fiber, vitamin, sodium, calories, carbs) VALUES
(1, 1, 8.0, 8.0, 0.0, 10.0, 100.0, 150, 12.0), -- Milk
(2, 2, 6.0, 5.0, 0.0, 8.0, 70.0, 70, 1.0), -- Eggs
(3, 3, 25.0, 3.0, 0.0, 5.0, 65.0, 165, 0.0), -- Chicken Breast
(4, 4, 3.0, 0.5, 2.0, 50.0, 65.0, 20, 3.0), -- Spinach
(5, 5, 4.0, 0.5, 1.0, 0.0, 5.0, 200, 45.0), -- Rice
(6, 6, 1.0, 0.2, 1.5, 20.0, 10.0, 25, 5.0), -- Tomatoes
(7, 7, 10.0, 1.0, 3.0, 0.0, 2.0, 400, 80.0), -- Flour
(8, 8, 15.0, 5.0, 2.0, 1.0, 100.0, 250, 30.0), -- Quinoa
(9, 9, 5.0, 1.0, 5.0, 10.0, 50.0, 120, 25.0), -- Unknown Cereal
(10, 10, 25.0, 2.0, 0.0, 5.0, 50.0, 120, 3.0); -- Protein Powder

-- Insert brands
INSERT INTO Brand (brand_id, name, is_trusted) VALUES
(1, 'Organic Valley', TRUE),
(2, 'Tyson', TRUE),
(3, 'Uncle Ben''s', TRUE);

-- Recipe brands
INSERT INTO Recipe_Brand (recipe_id, brand_id) VALUES
(1, 3), -- Pasta Bowl - Uncle Ben's
(2, 2), -- Chicken Stir Fry - Tyson
(3, 1); -- Spinach Omelette - Organic Valley

-- Food scan logs
INSERT INTO Food_Scan_Log (log_id, ingredient_id, status) VALUES
(1, 1, 'FAILED'),
(2, 3, 'SUCCESS'),
(3, 5, 'SUCCESS'),
(4, 9, 'FAILED');

-- Insert clients
INSERT INTO Client (client_id, user_id, pc_id, fridge_id, list_id, log_id, flag) VALUES
(1, 1, 1, 1, 1, 1, 0),
(2, 2, 2, 2, 2, 2, 1);

-- Insert meal plans
INSERT INTO Meal_Plan (meal_id, pc_id, recipe_id, quantity) VALUES
(1, 1, 2, 1), -- Client 1 - Chicken Stir Fry
(2, 1, 3, 2), -- Client 1 - 2 Spinach Omelettes
(3, 2, 1, 1), -- Client 2 - Pasta Bowl
(4, 2, 2, 1); -- Client 2 - Chicken Stir Fry

-- Insert leftovers
INSERT INTO Leftover (leftover_id, recipe_id, quantity, is_expired) VALUES
(1, 1, 1, FALSE), -- Pasta Bowl leftovers
(2, 2, 2, FALSE); -- Chicken Stir Fry leftovers

-- Insert nutrition tracking
INSERT INTO Nutrition_Tracking (tracking_id, client_id, protein, fat, fiber, sodium, vitamins, calories, carbs) VALUES
(1, 1, 80.0, 30.0, 10.0, 1500.0, 100.0, 2000, 200.0),
(2, 2, 100.0, 40.0, 15.0, 1200.0, 120.0, 2200, 150.0);

-- Insert health advisors
INSERT INTO Health_Advisor (advisor_id, experience_years, client_id) VALUES
(1, 5, 1),
(2, 8, 2);

-- Insert client health advisor relationships
INSERT INTO Client_Health_Advisor (client_id, advisor_id) VALUES
(1, 1),
(2, 2);

-- Insert client workout relationships
INSERT INTO Client_Workout (client_id, workout_id) VALUES
(1, 1), -- Client 1 - Running
(2, 2); -- Client 2 - Weight Lifting

-- Insert error logs
INSERT INTO Error_Log (error_id, client_id, log_id, message) VALUES
(1, 1, 1, 'Unrecognized barcode during scan'),
(2, 2, 3, 'Network error during scan');

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