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
   user_id INT,
   FOREIGN KEY (user_id) REFERENCES User(user_id)
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

INSERT INTO User (
    user_id, f_name, l_name, username, password, email
) VALUES
    -- Clients (1-10)
    (1, 'Busy', 'Ben', 'busyben', 'g6ASy6N4(2', 'busy.ben@example.com'),
    (2, 'Nicholas', 'Miller', 'nicholas928', 't4DSCGrg)I', 'nicholas.miller@example.com'),
    (3, 'George', 'Hall', 'george636', '(lHN^3AyN1', 'george.hall@example.com'),
    (4, 'Kelly', 'Thomas', 'kelly742', '_d31KO@p+!', 'kelly.thomas@example.com'),
    (5, 'Olivia', 'Hernandez', 'olivia693', '5a2FykmV*H', 'olivia.hernandez@example.com'),
    (6, 'James', 'Porter', 'james817', '(9zKCkpvfp', 'james.porter@example.com'),
    (7, 'Donald', 'Alvarez', 'donald903', 'XbY&0Jqm_5', 'donald.alvarez@example.com'),
    (8, 'Steve', 'Barnes', 'steve492', '_R8HNVlE34', 'steve.barnes@example.com'),
    (9, 'Timothy', 'Cowan', 'timothy874', 'EP6Mup0_M!', 'timothy.cowan@example.com'),
    (10, 'Emily', 'Grimes', 'emily866', 'I^k18H4vLk', 'emily.grimes@example.com'),

    -- Admins (11-20)
    (11, 'Alvin', 'Admin', 'alvinadmin', 'cD_#2Aem!k', 'alvin.admin@example.com'),
    (12, 'Olivia', 'Johnson', 'olivia366', 'E)3sK&n6@y', 'olivia.johnson@example.com'),
    (13, 'Isaac', 'Hurley', 'isaac147', 'T1VmsQ69@)', 'isaac.hurley@example.com'),
    (14, 'Aaron', 'Adams', 'aaron126', '+LVC35rzn2', 'aaron.adams@example.com'),
    (15, 'Kendra', 'Jefferson', 'kendra510', 'zp#nzeNe%8', 'kendra.jefferson@example.com'),
    (16, 'Michelle', 'Armstrong', 'michelle561', '_9zEUw9BT2', 'michelle.armstrong@example.com'),
    (17, 'Courtney', 'Jones', 'courtney264', '5*^v5UirjQ', 'courtney.jones@example.com'),
    (18, 'Steven', 'Murphy', 'steven560', 'Qi(3eSm3X0', 'steven.murphy@example.com'),
    (19, 'Michael', 'Burns', 'michael737', '5@xY3k!j%*', 'michael.burns@example.com'),
    (20, 'Caleb', 'Blankenship', 'caleb199', '+M*9Cu)P2q', 'caleb.blankenship@example.com'),

    -- Health Advisors (21-40)
    (21, 'Riley', 'Runner', 'rileyrunner', 'm1_i5MtD(7', 'riley.runner@example.com'),
    (22, 'Nancy', 'Nutritionist', 'nancynutri', 'Z17GtsiGM&', 'nancy.nutritionist@example.com'),
    (23, 'Robert', 'Roman', 'robert428', 'B2)53H4n%y', 'robert.roman@example.com'),
    (24, 'Tina', 'Jennings', 'tina825', 'T)2#e3AwY4', 'tina.jennings@example.com'),
    (25, 'Edward', 'Valenzuela', 'edward846', ')+YD3XSoF8', 'edward.valenzuela@example.com'),
    (26, 'Tara', 'Patterson', 'tara479', 'v+)43ODn(X', 'tara.patterson@example.com'),
    (27, 'Cynthia', 'Miller', 'cynthia729', '(7uKl&9kEt', 'cynthia.miller@example.com'),
    (28, 'Kelsey', 'Porter', 'kelsey313', '+v_i)SYS%2', 'kelsey.porter@example.com'),
    (29, 'Daniel', 'Foster', 'daniel761', '#1IFlO6vGj', 'daniel.foster@example.com'),
    (30, 'Aaron', 'Smith', 'aaron690', '@0O_w@zn%9', 'aaron.smith@example.com'),
    (31, 'David', 'Serrano', 'david572', 's#_7Xwj!Z6', 'david.serrano@example.com'),
    (32, 'Patricia', 'Cox', 'patricia336', 'f3NU0C)s)a', 'patricia.cox@example.com'),
    (33, 'Christopher', 'Meadows', 'christopher164', 'zD0Tmn#p%p', 'christopher.meadows@example.com'),
    (34, 'Jason', 'Taylor', 'jason401', ')U26AunhDv', 'jason.taylor@example.com'),
    (35, 'Ryan', 'Lopez', 'ryan737', 'ufFsUnn6&8', 'ryan.lopez@example.com'),
    (36, 'Roger', 'Valencia', 'roger652', '*IsZWMqp3d', 'roger.valencia@example.com'),
    (37, 'Patricia', 'Jimenez', 'patricia197', '9t#A#1Hq_k', 'patricia.jimenez@example.com'),
    (38, 'Todd', 'Howell', 'todd513', 'jpHilSk+%4', 'todd.howell@example.com'),
    (39, 'Heather', 'Rogers', 'heather174', 'h5uQc4Z8#D', 'heather.rogers@example.com'),
    (40, 'Jared', 'Park', 'jared210', 'Q_8UFyiGmS', 'jared.park@example.com');

-- Additional users to reach at least 40 total
INSERT INTO User (
    f_name, l_name, username, password, email
) VALUES
    -- Additional Clients (41-50)
    ('Sarah', 'Johnson', 'sarah123', 'P@ssw0rd123', 'sarah.johnson@example.com'),
    ('Michael', 'Williams', 'mike456', 'Secur3P@ss', 'michael.williams@example.com'),
    ('Jennifer', 'Brown', 'jenbrown', 'Br0wnJ3n!', 'jennifer.brown@example.com'),
    ('David', 'Jones', 'davejones', 'J0n3sD@v3', 'david.jones@example.com'),
    ('Lisa', 'Garcia', 'lisag', 'G@rc1@L1sa', 'lisa.garcia@example.com'),
    ('Robert', 'Martinez', 'robmart', 'M@rt1n3zR', 'robert.martinez@example.com'),
    ('Jessica', 'Robinson', 'jessrob', 'R0b1ns0nJ!', 'jessica.robinson@example.com'),
    ('William', 'Clark', 'willclark', 'Cl@rkW1ll', 'william.clark@example.com'),
    ('Elizabeth', 'Lewis', 'lizlewis', 'L3w1sL1z!', 'elizabeth.lewis@example.com'),
    ('Thomas', 'Walker', 'tomwalker', 'W@lk3rT0m', 'thomas.walker@example.com');

-- Insert admin data (users 11-20)
INSERT INTO Admin (user_id) VALUES
    (11), -- Alvin Admin
    (12),
    (13),
    (14),
    (15),
    (16),
    (17),
    (18),
    (19),
    (20);

INSERT INTO Personal_Constraints (
    budget, dietary_restrictions, personal_diet, age_group
) VALUES
    (140.35, 'none', 'vegetarian', 'senior'),
    (65.43, 'fish,tree nuts,gluten', 'vegetarian', 'child'),
    (132.34, 'peanuts,tree nuts,gluten', 'keto', 'child'),
    (189.49, 'none', 'vegetarian', 'child'),
    (107.4, 'sesame,none,soy', 'vegan', 'senior'),
    (166.27, 'egg,none', 'keto', 'teen'),
    (136.92, 'gluten,shellfish', 'vegetarian', 'teen'),
    (110.57, 'soy,peanuts,fish', 'keto', 'senior'),
    (148.84, 'tree nuts,soy', 'balanced', 'senior'),
    (128.51, 'dairy', 'paleo', 'teen'),
    (152.75, 'shellfish', 'mediterranean', 'adult'),
    (175.20, 'none', 'low-carb', 'adult'),
    (90.65, 'gluten,dairy', 'vegan', 'teen'),
    (120.30, 'peanuts', 'balanced', 'senior'),
    (200.45, 'tree nuts', 'high-protein', 'adult'),
    (95.60, 'soy,fish', 'pescatarian', 'adult'),
    (180.15, 'none', 'keto', 'teen'),
    (135.70, 'dairy,eggs', 'vegetarian', 'child'),
    (160.85, 'fish', 'paleo', 'senior'),
    (110.25, 'gluten', 'low-carb', 'adult'),
    (145.90, 'none', 'balanced', 'teen'),
    (170.50, 'shellfish,fish', 'pescatarian', 'senior'),
    (125.65, 'peanuts,tree nuts', 'high-protein', 'adult'),
    (185.30, 'gluten', 'mediterranean', 'adult'),
    (95.75, 'dairy', 'keto', 'child'),
    (150.20, 'none', 'vegetarian', 'teen'),
    (100.60, 'soy', 'balanced', 'senior'),
    (190.35, 'eggs', 'paleo', 'adult'),
    (140.90, 'fish,shellfish', 'pescatarian', 'teen'),
    (115.55, 'tree nuts', 'low-carb', 'child'),
    (155.80, 'gluten,dairy', 'vegan', 'adult'),
    (105.45, 'none', 'keto', 'senior'),
    (175.70, 'peanuts', 'high-protein', 'teen'),
    (130.25, 'shellfish', 'mediterranean', 'child'),
    (160.50, 'dairy,soy', 'balanced', 'adult'),
    (120.95, 'fish', 'vegetarian', 'senior'),
    (195.40, 'none', 'paleo', 'teen'),
    (145.75, 'gluten', 'pescatarian', 'adult'),
    (165.30, 'tree nuts,peanuts', 'high-protein', 'child'),
    (135.85, 'eggs,dairy', 'low-carb', 'adult');

-- Insert workout data (40 rows for strong entity)
INSERT INTO Workout (
    name, quantity, weight, calories_burnt
) VALUES
    ('Hiking', 33, NULL, 394),
    ('Pilates', 60, NULL, 267),
    ('Hiking', 24, NULL, 574),
    ('Jump Rope', 23, NULL, 459),
    ('Swimming', 57, NULL, 587),
    ('Pilates', 40, NULL, 576),
    ('HIIT', 56, NULL, 151),
    ('HIIT', 50, NULL, 550),
    ('Cycling', 53, NULL, 541),
    ('Boxing', 40, 91.96, 545),
    ('Pilates', 69, NULL, 222),
    ('Yoga', 34, NULL, 568),
    ('Hiking', 61, NULL, 506),
    ('Boxing', 58, 111.42, 235),
    ('Dancing', 58, NULL, 220),
    ('HIIT', 67, NULL, 209),
    ('Hiking', 59, NULL, 171),
    ('Pilates', 32, NULL, 373),
    ('Hiking', 31, NULL, 431),
    ('HIIT', 81, NULL, 240),
    ('Running', 45, NULL, 450),
    ('Weight Training', 60, 135.5, 320),
    ('Rowing', 30, NULL, 280),
    ('Elliptical', 45, NULL, 380),
    ('Stair Climber', 30, NULL, 310),
    ('Kickboxing', 60, NULL, 600),
    ('Zumba', 45, NULL, 350),
    ('CrossFit', 50, NULL, 520),
    ('Basketball', 60, NULL, 450),
    ('Soccer', 90, NULL, 600),
    ('Tennis', 75, NULL, 400),
    ('Spinning', 45, NULL, 500),
    ('Barre', 50, NULL, 250),
    ('Rock Climbing', 60, 160.0, 450),
    ('Circuit Training', 40, NULL, 400),
    ('Mountain Biking', 90, NULL, 650),
    ('Aerobics', 50, NULL, 380),
    ('Tai Chi', 40, NULL, 150),
    ('Power Walking', 60, NULL, 300),
    ('Racquetball', 45, NULL, 390);

INSERT INTO Ingredient (
    name, expiration_date
) VALUES
    ('Chicken Breast', '2025-12-13'),
    ('Ground Beef', '2025-12-23'),
    ('Quinoa', '2026-02-06'),
    ('Brown Rice', '2025-05-18'),
    ('Lentils', '2025-10-30'),
    ('Broccoli', '2025-06-01'),
    ('Sweet Potato', '2026-01-09'),
    ('Eggs', '2025-05-08'),
    ('Milk', '2025-12-27'),
    ('Cheddar Cheese', '2025-10-14'),
    ('Greek Yogurt', '2025-12-23'),
    ('Almonds', '2025-11-01'),
    ('Walnuts', '2025-05-19'),
    ('Orange', '2025-08-20'),
    ('Honey', '2025-12-29'),
    ('Cucumber', '2026-01-04'),
    ('Bell Pepper', '2025-06-27'),
    ('Salmon Fillet', '2025-05-10'),
    ('Avocado', '2025-06-15'),
    ('Spinach', '2025-05-25'),
    ('Tofu', '2025-07-14'),
    ('Black Beans', '2026-01-30'),
    ('Oats', '2026-03-15'),
    ('Blueberries', '2025-06-10'),
    ('Bananas', '2025-05-12'),
    ('Olive Oil', '2026-04-22'),
    ('Almond Milk', '2025-06-18'),
    ('Tomatoes', '2025-05-30'),
    ('Carrots', '2025-06-28'),
    ('Kale', '2025-05-26'),
    ('Shrimp', '2025-05-15'),
    ('Turkey Breast', '2025-07-05'),
    ('Asparagus', '2025-06-05'),
    ('Mushrooms', '2025-05-28'),
    ('Coconut Oil', '2026-01-15'),
    ('Chia Seeds', '2026-05-20'),
    ('Peanut Butter', '2025-11-25'),
    ('Whole Wheat Bread', '2025-06-10'),
    ('Maple Syrup', '2026-02-28'),
    ('Garlic', '2025-08-15'),
    ('Onions', '2025-09-10'),
    ('Potatoes', '2025-08-30'),
    ('Zucchini', '2025-06-12'),
    ('Strawberries', '2025-06-07'),
    ('Apples', '2025-07-15');

INSERT INTO Recipe (
    name, instructions
) VALUES
    ('Event Stew', 'Blood once game local language letter budget stage generation.'),
    ('Rest Bowl', 'Pull far entire east member identify step single.'),
    ('Wide Bowl', 'Clear trouble hope prove indicate culture range occur enter natural throughout international.'),
    ('Glass Wrap', 'Other probably team day couple or end yet success or.'),
    ('That Skillet', 'Particularly Mr vote visit begin surface something theory result national mouth fish the rate.'),
    ('Every Salad', 'Next parent serious him account shoulder born range.'),
    ('Too Wrap', 'Whatever opportunity bag official result manager glass.'),
    ('Never Skillet', 'So box member particular all ahead medical skill talk couple movement not weight forward resource card.'),
    ('Line Bowl', 'Add end case country often establish management car program suffer whom.'),
    ('Already Wrap', 'Good bring opportunity impact upon resource than hand owner fire.'),
    ('Quinoa Power Bowl', 'Combine cooked quinoa with roasted vegetables, avocado, and a lemon tahini dressing.'),
    ('Mediterranean Plate', 'Serve hummus, falafel, tabbouleh, and warm pita with a side of tzatziki sauce.'),
    ('Thai Curry Noodles', 'Simmer vegetables and protein in coconut curry sauce, serve over rice noodles.'),
    ('Classic Burger', 'Grill beef patty to desired doneness, top with cheese, lettuce, tomato on a toasted bun.'),
    ('Vegetable Stir Fry', 'Quick fry mixed vegetables with garlic, ginger, and soy sauce. Serve over rice.'),
    ('Breakfast Smoothie Bowl', 'Blend frozen fruit with yogurt, top with granola, fresh fruit, and honey.'),
    ('Chicken Fajitas', 'Sauté sliced chicken with bell peppers and onions, serve with warm tortillas.'),
    ('Lentil Soup', 'Simmer lentils with vegetables, herbs, and spices until tender. Season to taste.'),
    ('Baked Salmon', 'Season salmon fillet with herbs, lemon, and olive oil. Bake until flaky.'),
    ('Avocado Toast', 'Spread mashed avocado on toasted bread, top with salt, pepper, and red pepper flakes.'),
    ('Mushroom Risotto', 'Slowly add broth to arborio rice, stir continuously. Add sautéed mushrooms and parmesan.'),
    ('Buffalo Cauliflower', 'Coat cauliflower florets in batter, bake until crispy, toss in buffalo sauce.'),
    ('Greek Salad', 'Combine cucumber, tomato, olives, feta, and red onion with olive oil and oregano.'),
    ('Bean Burrito', 'Fill tortilla with refried beans, rice, cheese, and toppings. Roll and serve.'),
    ('Pesto Pasta', 'Toss cooked pasta with homemade basil pesto, cherry tomatoes, and pine nuts.'),
    ('Acai Bowl', 'Blend frozen acai with banana, top with granola, coconut flakes, and fresh berries.'),
    ('Stuffed Bell Peppers', 'Fill halved bell peppers with a mixture of ground meat, rice, and seasonings. Bake until tender.'),
    ('Chickpea Curry', 'Simmer chickpeas in tomato and spice sauce until flavors meld. Serve with rice.'),
    ('Sweet Potato Toast', 'Slice sweet potato, toast until tender, top with nut butter, banana, and cinnamon.'),
    ('Turkey Meatballs', 'Mix ground turkey with breadcrumbs, egg, and seasoning. Form into balls and bake.'),
    ('Shrimp Scampi', 'Sauté shrimp in garlic butter sauce, serve over linguine with lemon and parsley.'),
    ('Veggie Omelet', 'Whisk eggs, pour into hot pan, add vegetables and cheese, fold and serve.'),
    ('Black Bean Soup', 'Simmer black beans with vegetables and spices, blend partially for texture.'),
    ('Chicken Caesar Salad', 'Toss romaine lettuce with grilled chicken, croutons, parmesan, and caesar dressing.'),
    ('Teriyaki Stir Fry', 'Sauté protein and vegetables, add teriyaki sauce, serve over steamed rice.');

INSERT INTO Fridge_Inventory (fridge_id) VALUES
    (1), (2), (3), (4), (5),
    (6), (7), (8), (9), (10),
    (11), (12), (13), (14), (15),
    (16), (17), (18), (19), (20);

INSERT INTO Shopping_List (list_id) VALUES
    (1), (2), (3), (4), (5),
    (6), (7), (8), (9), (10),
    (11), (12), (13), (14), (15),
    (16), (17), (18), (19), (20);

INSERT INTO Food_Scan_Log (ingredient_id, status) VALUES
    (1, 'SUCCESS'),
    (2, 'SUCCESS'),
    (3, 'FAILED'),
    (4, 'FAILED'),
    (5, 'SUCCESS'),
    (6, 'SUCCESS'),
    (7, 'SUCCESS'),
    (8, 'SUCCESS'),
    (9, 'SUCCESS'),
    (10, 'SUCCESS'),
    (11, 'SUCCESS'),
    (12, 'SUCCESS'),
    (13, 'FAILED'),
    (14, 'SUCCESS'),
    (15, 'SUCCESS'),
    (16, 'FAILED'),
    (17, 'SUCCESS'),
    (18, 'SUCCESS'),
    (19, 'FAILED'),
    (20, 'SUCCESS'),
    (21, 'SUCCESS'),
    (22, 'FAILED'),
    (23, 'SUCCESS'),
    (24, 'SUCCESS'),
    (25, 'FAILED'),
    (1, 'SUCCESS'),
    (2, 'FAILED'),
    (3, 'SUCCESS'),
    (4, 'SUCCESS'),
    (5, 'FAILED'),
    (6, 'SUCCESS'),
    (7, 'FAILED'),
    (8, 'SUCCESS'),
    (9, 'SUCCESS'),
    (10, 'FAILED'),
    (11, 'SUCCESS'),
    (12, 'FAILED'),
    (13, 'SUCCESS'),
    (14, 'SUCCESS'),
    (15, 'FAILED'),
    (16, 'SUCCESS'),
    (17, 'SUCCESS'),
    (18, 'FAILED'),
    (19, 'SUCCESS'),
    (20, 'SUCCESS'),
    (21, 'FAILED'),
    (22, 'SUCCESS'),
    (23, 'SUCCESS'),
    (24, 'FAILED'),
    (25, 'SUCCESS'),
    (26, 'SUCCESS'),
    (27, 'FAILED'),
    (28, 'SUCCESS'),
    (29, 'SUCCESS'),
    (30, 'FAILED');

INSERT INTO Client (user_id, pc_id, fridge_id, list_id, log_id, flag) VALUES
    (1, 1, 1, 1, 1, 0),  -- Busy Ben
    (2, 2, 2, 2, 2, 0),
    (3, 3, 3, 3, 3, 0),
    (4, 4, 4, 4, 4, 1),
    (5, 5, 5, 5, 5, 1),
    (6, 6, 6, 6, 6, 1),
    (7, 7, 7, 7, 7, 1),
    (8, 8, 8, 8, 8, 0),
    (9, 9, 9, 9, 9, 0),
    (10, 10, 10, 10, 10, 0),
    (41, 11, 11, 11, 1, 0),
    (42, 12, 12, 12, 2, 1),
    (43, 13, 13, 13, 3, 0),
    (44, 14, 14, 14, 4, 1),
    (45, 15, 15, 15, 5, 0),
    (46, 16, 16, 16, 6, 1),
    (47, 17, 17, 17, 7, 0),
    (48, 18, 18, 18, 8, 1),
    (49, 19, 19, 19, 9, 0),
    (50, 20, 20, 20, 10, 1);

INSERT INTO Health_Advisor (advisor_id, experience_years, user_id) VALUES 
    (1, 7, 21),  -- Riley Runner (user_id 21)
    (2, 11, 22), -- Nancy Nutritionist (user_id 22)
    (3, 10, 23),
    (4, 7, 24),
    (5, 3, 25),
    (6, 9, 26),
    (7, 13, 27),
    (8, 2, 28),
    (9, 4, 29),
    (10, 17, 30),
    (11, 5, 31),
    (12, 8, 32),
    (13, 12, 33),
    (14, 6, 34),
    (15, 9, 35),
    (16, 14, 36),
    (17, 3, 37),
    (18, 10, 38),
    (19, 7, 39),
    (20, 15, 40);

INSERT INTO Recipe_Ingredient (
    recipe_id, ingredient_id, quantity, unit
) VALUES
    -- Recipe 1 ingredients (Event Stew)
    (1, 1, 1.5, 'pound'),   -- Chicken Breast
    (1, 5, 2.0, 'cup'),     -- Lentils
    (1, 6, 3.0, 'whole'),   -- Broccoli
    (1, 7, 2.0, 'whole'),   -- Sweet Potato
    (1, 26, 2.0, 'tbsp'),   -- Olive Oil

    -- Recipe 2 ingredients (Rest Bowl)
    (2, 3, 1.0, 'cup'),     -- Quinoa
    (2, 19, 1.0, 'whole'),  -- Avocado
    (2, 20, 2.0, 'cup'),    -- Spinach
    (2, 16, 0.5, 'whole'),  -- Cucumber
    (2, 28, 2.0, 'whole'),  -- Tomatoes

    -- Recipe 3 ingredients (Wide Bowl)
    (3, 4, 1.5, 'cup'),     -- Brown Rice
    (3, 21, 8.0, 'oz'),     -- Tofu
    (3, 29, 1.0, 'cup'),    -- Carrots
    (3, 17, 1.0, 'whole'),  -- Bell Pepper
    (3, 30, 2.0, 'cup'),    -- Kale

    -- Recipe 4 ingredients (Glass Wrap)
    (4, 38, 2.0, 'slice'),  -- Whole Wheat Bread
    (4, 2, 0.25, 'pound'),  -- Ground Beef
    (4, 10, 2.0, 'slice'),  -- Cheddar Cheese
    (4, 28, 2.0, 'slice'),  -- Tomatoes
    (4, 20, 0.5, 'cup'),    -- Spinach

    -- Recipe 5 ingredients (That Skillet)
    (5, 2, 1.0, 'pound'),   -- Ground Beef
    (5, 41, 1.0, 'whole'),  -- Onions
    (5, 42, 2.0, 'whole'),  -- Potatoes
    (5, 10, 0.5, 'cup'),    -- Cheddar Cheese
    (5, 40, 2.0, 'clove'),  -- Garlic

    -- Recipe 6 ingredients (Every Salad)
    (6, 20, 4.0, 'cup'),    -- Spinach
    (6, 19, 1.0, 'whole'),  -- Avocado
    (6, 28, 1.0, 'cup'),    -- Tomatoes
    (6, 16, 1.0, 'whole'),  -- Cucumber
    (6, 12, 0.25, 'cup'),   -- Almonds

    -- Recipe 7 ingredients (Too Wrap)
    (7, 38, 2.0, 'slice'),  -- Whole Wheat Bread
    (7, 37, 2.0, 'tbsp'),   -- Peanut Butter
    (7, 25, 1.0, 'whole'),  -- Banana
    (7, 15, 1.0, 'tbsp'),   -- Honey
    (7, 36, 1.0, 'tsp'),    -- Chia Seeds

    -- Recipe 8 ingredients (Never Skillet)
    (8, 1, 1.0, 'pound'),   -- Chicken Breast
    (8, 17, 2.0, 'whole'),  -- Bell Pepper
    (8, 41, 1.0, 'whole'),  -- Onions
    (8, 40, 3.0, 'clove'),  -- Garlic
    (8, 26, 2.0, 'tbsp'),   -- Olive Oil

    -- Recipe 9 ingredients (Line Bowl)
    (9, 4, 1.0, 'cup'),     -- Brown Rice
    (9, 22, 1.0, 'cup'),    -- Black Beans
    (9, 19, 1.0, 'whole'),  -- Avocado
    (9, 17, 1.0, 'whole'),  -- Bell Pepper
    (9, 28, 0.5, 'cup'),    -- Tomatoes

    -- Recipe 10 ingredients (Already Wrap)
    (10, 38, 2.0, 'slice'), -- Whole Wheat Bread
    (10, 31, 4.0, 'oz'),    -- Shrimp
    (10, 20, 1.0, 'cup'),   -- Spinach
    (10, 28, 2.0, 'slice'), -- Tomatoes
    (10, 19, 0.5, 'whole'), -- Avocado

    -- Recipe 11 ingredients (Quinoa Power Bowl)
    (11, 3, 1.0, 'cup'),    -- Quinoa
    (11, 6, 1.0, 'cup'),    -- Broccoli
    (11, 7, 1.0, 'whole'),  -- Sweet Potato
    (11, 19, 1.0, 'whole'), -- Avocado
    (11, 12, 2.0, 'tbsp'),  -- Almonds

    -- Recipe 12 ingredients (Mediterranean Plate)
    (12, 21, 8.0, 'oz'),    -- Tofu
    (12, 28, 1.0, 'cup'),   -- Tomatoes
    (12, 16, 1.0, 'whole'), -- Cucumber
    (12, 26, 2.0, 'tbsp'),  -- Olive Oil
    (12, 40, 2.0, 'clove'), -- Garlic

    -- Continue with more recipe-ingredient relationships
    -- Recipe 13-35 ingredients (adding 100+ more rows)
    (13, 9, 1.0, 'cup'),    -- Milk
    (13, 8, 2.0, 'whole'),  -- Eggs
    (13, 15, 2.0, 'tbsp'),  -- Honey
    (13, 23, 1.0, 'cup'),   -- Oats
    (13, 24, 0.5, 'cup'),   -- Blueberries

    (14, 2, 1.0, 'pound'),  -- Ground Beef
    (14, 10, 2.0, 'slice'), -- Cheddar Cheese
    (14, 38, 1.0, 'whole'), -- Whole Wheat Bread
    (14, 28, 2.0, 'slice'), -- Tomatoes
    (14, 41, 2.0, 'slice'), -- Onions

    (15, 17, 2.0, 'whole'), -- Bell Pepper
    (15, 29, 1.0, 'cup'),   -- Carrots
    (15, 6, 2.0, 'cup'),    -- Broccoli
    (15, 43, 1.0, 'whole'), -- Zucchini
    (15, 40, 2.0, 'clove'), -- Garlic

    (16, 9, 1.0, 'cup'),    -- Milk
    (16, 25, 1.0, 'whole'), -- Banana
    (16, 24, 1.0, 'cup'),   -- Blueberries
    (16, 44, 0.5, 'cup'),   -- Strawberries
    (16, 15, 1.0, 'tbsp'),  -- Honey

    (17, 1, 1.0, 'pound'),  -- Chicken Breast
    (17, 17, 2.0, 'whole'), -- Bell Pepper
    (17, 41, 1.0, 'whole'), -- Onions
    (17, 28, 2.0, 'whole'), -- Tomatoes
    (17, 19, 1.0, 'whole'), -- Avocado

    (18, 5, 2.0, 'cup'),    -- Lentils
    (18, 29, 1.0, 'cup'),   -- Carrots
    (18, 41, 1.0, 'whole'), -- Onions
    (18, 40, 2.0, 'clove'), -- Garlic
    (18, 26, 2.0, 'tbsp'),  -- Olive Oil

    (19, 18, 1.0, 'pound'), -- Salmon Fillet
    (19, 33, 1.0, 'bunch'), -- Asparagus
    (19, 26, 2.0, 'tbsp'),  -- Olive Oil
    (19, 40, 2.0, 'clove'), -- Garlic
    (19, 14, 1.0, 'whole'), -- Orange

    (20, 38, 2.0, 'slice'), -- Whole Wheat Bread
    (20, 19, 1.0, 'whole'), -- Avocado
    (20, 20, 0.5, 'cup'),   -- Spinach
    (20, 28, 1.0, 'slice'), -- Tomatoes
    (20, 36, 1.0, 'tsp'),   -- Chia Seeds

    -- Additional relationships to reach 125+ total
    (21, 34, 1.0, 'cup'),   -- Mushrooms
    (21, 4, 1.0, 'cup'),    -- Brown Rice
    (21, 26, 2.0, 'tbsp'),  -- Olive Oil
    (21, 10, 0.25, 'cup'),  -- Cheddar Cheese

    (22, 6, 1.0, 'head'),   -- Broccoli
    (22, 26, 2.0, 'tbsp'),  -- Olive Oil
    (22, 40, 2.0, 'clove'), -- Garlic

    (23, 16, 1.0, 'whole'), -- Cucumber
    (23, 28, 2.0, 'whole'), -- Tomatoes
    (23, 26, 2.0, 'tbsp'),  -- Olive Oil

    (24, 22, 1.0, 'cup'),   -- Black Beans
    (24, 4, 0.5, 'cup'),    -- Brown Rice
    (24, 10, 0.25, 'cup'),  -- Cheddar Cheese

    (25, 3, 1.0, 'cup'),    -- Quinoa
    (25, 12, 0.25, 'cup'),  -- Almonds
    (25, 26, 2.0, 'tbsp'),  -- Olive Oil

    -- Continue adding more until you reach 125+ rows
    (1, 40, 3.0, 'clove'),  -- Garlic for Event Stew
    (1, 41, 1.0, 'whole'),  -- Onions for Event Stew

    (2, 26, 1.0, 'tbsp'),   -- Olive Oil for Rest Bowl
    (2, 12, 2.0, 'tbsp'),   -- Almonds for Rest Bowl

    (3, 26, 2.0, 'tbsp'),   -- Olive Oil for Wide Bowl
    (3, 40, 2.0, 'clove'),  -- Garlic for Wide Bowl

    (4, 37, 1.0, 'tbsp'),   -- Peanut Butter for Glass Wrap
    (4, 40, 1.0, 'clove'),  -- Garlic for Glass Wrap

    (5, 29, 1.0, 'cup'),    -- Carrots for That Skillet
    (5, 17, 1.0, 'whole'),  -- Bell Pepper for That Skillet

    (6, 26, 2.0, 'tbsp'),   -- Olive Oil for Every Salad
    (6, 10, 0.25, 'cup'),   -- Cheddar Cheese for Every Salad

    (7, 13, 2.0, 'tbsp'),   -- Walnuts for Too Wrap
    (7, 24, 0.25, 'cup'),   -- Blueberries for Too Wrap

    (8, 4, 1.0, 'cup'),     -- Brown Rice for Never Skillet
    (8, 10, 0.5, 'cup'),    -- Cheddar Cheese for Never Skillet

    (9, 31, 0.5, 'pound'),  -- Shrimp for Line Bowl
    (9, 40, 2.0, 'clove'),  -- Garlic for Line Bowl

    (10, 9, 2.0, 'tbsp'),   -- Milk for Already Wrap
    (10, 26, 1.0, 'tbsp');  -- Olive Oil for Already Wrap

    INSERT INTO Macronutrients (
    ingredient_id, protein, fat, fiber, vitamin, sodium, calories, carbs
) VALUES
    (1, 24.03, 4.37, 4.95, 0.96, 99.16, 180, 76.35),
    (2, 16.63, 3.47, 2.39, 27.64, 21.12, 327, 8.07),
    (3, 8.41, 1.97, 5.51, 41.84, 199.06, 260, 7.74),
    (4, 13.64, 3.99, 4.06, 62.3, 145.02, 397, 29.46),
    (5, 19.58, 12.15, 4.77, 6.1, 71.31, 303, 54.51),
    (6, 25.43, 3.43, 8.96, 43.56, 130.56, 212, 57.92),
    (7, 12.1, 3.57, 0.92, 66.35, 103.05, 130, 7.43),
    (8, 10.54, 8.02, 5.48, 56.88, 107.85, 100, 7.97),
    (9, 19.12, 2.13, 4.74, 62.39, 198.54, 112, 45.73),
    (10, 21.33, 4.41, 2.65, 39.5, 80.5, 288, 70.83),
    (11, 8.4, 13.95, 6.83, 85.29, 167.01, 50, 77.11),
    (12, 11.28, 6.45, 5.32, 14.96, 141.63, 76, 36.72),
    (13, 19.26, 12.0, 5.56, 28.73, 163.33, 57, 55.79),
    (14, 15.69, 8.51, 3.02, 61.57, 130.69, 106, 76.83),
    (15, 11.31, 12.38, 5.22, 76.9, 78.53, 210, 9.56),
    (16, 5.42, 11.42, 3.42, 47.63, 113.17, 144, 76.4),
    (17, 21.27, 11.79, 1.77, 51.56, 62.34, 345, 65.83),
    (18, 21.86, 12.81, 9.82, 91.24, 91.76, 67, 71.38),
    (19, 14.1, 7.52, 4.46, 40.96, 94.9, 282, 51.26),
    (20, 25.8, 6.15, 9.08, 87.7, 196.57, 293, 54.38),
    (21, 18.1, 2.65, 8.06, 42.12, 119.5, 301, 57.87),
    (22, 24.2, 12.57, 6.3, 6.62, 111.06, 313, 67.85),
    (23, 28.05, 8.39, 0.41, 83.4, 132.59, 156, 18.01),
    (24, 18.6, 9.28, 8.56, 79.02, 11.67, 130, 39.88),
    (25, 11.63, 1.91, 4.43, 84.51, 10.67, 256, 50.01),
    (26, 15.44, 7.51, 5.7, 25.89, 113.96, 328, 54.02),
    (27, 16.26, 7.87, 1.7, 67.72, 25.08, 354, 8.09),
    (28, 17.11, 1.49, 6.69, 95.46, 21.37, 327, 43.92),
    (29, 8.97, 9.91, 3.14, 33.61, 44.11, 238, 26.06),
    (30, 17.47, 10.53, 9.5, 86.27, 114.26, 85, 41.23),
    (31, 28.76, 7.59, 3.78, 73.52, 91.48, 206, 76.1),
    (32, 29.27, 6.34, 1.57, 61.68, 182.83, 181, 61.73),
    (33, 6.16, 10.06, 7.15, 2.39, 63.21, 286, 55.62),
    (34, 15.45, 5.6, 8.81, 2.0, 12.27, 397, 37.53),
    (35, 6.16, 10.06, 7.15, 2.39, 63.21, 286, 55.62),
    (36, 21.17, 8.55, 6.17, 12.67, 199.49, 231, 51.27),
    (37, 5.56, 2.69, 9.66, 1.49, 151.26, 175, 8.75),
    (38, 14.38, 2.68, 5.14, 20.04, 119.13, 347, 59.19),
    (39, 27.96, 6.67, 1.28, 64.98, 94.34, 208, 75.82),
    (40, 10.42, 5.67, 5.1, 75.53, 116.18, 290, 47.29),
    (41, 12.45, 3.21, 4.32, 45.67, 89.45, 185, 35.65),
    (42, 9.87, 1.32, 6.54, 35.78, 105.32, 220, 42.78),
    (43, 8.76, 2.14, 5.43, 28.95, 72.56, 156, 31.45),
    (44, 11.32, 2.87, 7.21, 52.43, 18.34, 142, 33.56),
    (45, 13.45, 4.21, 6.78, 41.23, 34.56, 178, 27.89);

INSERT INTO Ingredient_Macronutrient (
    ingredient_id, macro_id
) VALUES
    -- Creating many-to-many relationships between ingredients and macronutrients
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
    (2, 1), (2, 2), (2, 3), (2, 6), (2, 7),
    (3, 1), (3, 3), (3, 8), (3, 9), (3, 10),
    (4, 2), (4, 4), (4, 11), (4, 12), (4, 13),
    (5, 3), (5, 5), (5, 14), (5, 15), (5, 16),
    (6, 4), (6, 6), (6, 17), (6, 18), (6, 19),
    (7, 5), (7, 7), (7, 20), (7, 21), (7, 22),
    (8, 6), (8, 8), (8, 23), (8, 24), (8, 25),
    (9, 7), (9, 9), (9, 26), (9, 27), (9, 28),
    (10, 8), (10, 10), (10, 29), (10, 30), (10, 31),
    (11, 9), (11, 11), (11, 32), (11, 33), (11, 34),
    (12, 10), (12, 12), (12, 35), (12, 36), (12, 37),
    (13, 11), (13, 13), (13, 38), (13, 39), (13, 40),
    (14, 12), (14, 14), (14, 41), (14, 42), (14, 43),
    (15, 13), (15, 15), (15, 44), (15, 45), (15, 1),
    (16, 14), (16, 16), (16, 2), (16, 3), (16, 4),
    (17, 15), (17, 17), (17, 5), (17, 6), (17, 7),
    (18, 16), (18, 18), (18, 8), (18, 9), (18, 10),
    (19, 17), (19, 19), (19, 11), (19, 12), (19, 13),
    (20, 18), (20, 20), (20, 14), (20, 15), (20, 16),
    (21, 19), (21, 21), (21, 17), (21, 18), (21, 22),
    (22, 20), (22, 22), (22, 23), (22, 21), (22, 24),
    (23, 21), (23, 23), (23, 42), (23, 24), (23, 25),
    (24, 22), (24, 24), (24, 26), (24, 27), (24, 28),
    (25, 23), (25, 25), (25, 29), (25, 30), (25, 31),
    -- Additional relationships to reach 125+ total
    (26, 24), (26, 26), (26, 32), (26, 33),
    (27, 25), (27, 27), (27, 34), (27, 35),
    (28, 26), (28, 28), (28, 36), (28, 37),
    (29, 27), (29, 29), (29, 38), (29, 39),
    (30, 28), (30, 30), (30, 40), (30, 41);

INSERT INTO Brand (
    brand_id, name, is_trusted
) VALUES
    (1, 'Kirkland Signature', TRUE),
    (2, '365 Everyday Value', FALSE),
    (3, 'Trader Joe''s', TRUE),
    (4, 'Great Value', TRUE),
    (5, 'Organic Valley', TRUE),
    (6, 'Annie''s', FALSE),
    (7, 'Amy''s', FALSE),
    (8, 'Green Giant', FALSE),
    (9, 'Horizon Organic', TRUE),
    (10, 'Chobani', FALSE),
    (11, 'Siggi''s', FALSE),
    (12, 'Fage', TRUE),
    (13, 'Tillamook', TRUE),
    (14, 'Stonyfield', FALSE),
    (15, 'Daiya', FALSE),
    (16, 'Gardein', FALSE),
    (17, 'MorningStar Farms', TRUE),
    (18, 'Beyond Meat', TRUE),
    (19, 'Impossible Foods', FALSE),
    (20, 'Field Roast', FALSE),
    (21, 'Applegate', TRUE),
    (22, 'Boca', FALSE),
    (23, 'Earth Balance', FALSE),
    (24, 'Lightlife', TRUE),
    (25, 'Nature''s Path', FALSE),
    (26, 'Kind', TRUE),
    (27, 'Clif Bar', TRUE),
    (28, 'RXBAR', TRUE),
    (29, 'LÄRABAR', TRUE),
    (30, 'Nature Valley', TRUE),
    (31, 'Quaker', FALSE),
    (32, 'Bob''s Red Mill', TRUE),
    (33, 'Barilla', TRUE),
    (34, 'Rao''s Homemade', TRUE),
    (35, 'Prego', FALSE);

INSERT INTO Recipe_Brand (
    recipe_id, brand_id
) VALUES
    -- Creating 125+ many-to-many relationships between recipes and brands
    (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
    (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
    (3, 3), (3, 4), (3, 5), (3, 6), (3, 7),
    (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
    (5, 5), (5, 6), (5, 7), (5, 8), (5, 9),
    (6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
    (7, 7), (7, 8), (7, 9), (7, 10), (7, 11),
    (8, 8), (8, 9), (8, 10), (8, 11), (8, 12),
    (9, 9), (9, 10), (9, 11), (9, 12), (9, 13),
    (10, 10), (10, 11), (10, 12), (10, 13), (10, 14),
    (11, 11), (11, 12), (11, 13), (11, 14), (11, 15),
    (12, 12), (12, 13), (12, 14), (12, 15), (12, 16),
    (13, 13), (13, 14), (13, 15), (13, 16), (13, 17),
    (14, 14), (14, 15), (14, 16), (14, 17), (14, 18),
    (15, 15), (15, 16), (15, 17), (15, 18), (15, 19),
    (16, 16), (16, 17), (16, 18), (16, 19), (16, 20),
    (17, 17), (17, 18), (17, 19), (17, 20), (17, 21),
    (18, 18), (18, 19), (18, 20), (18, 21), (18, 22),
    (19, 19), (19, 20), (19, 21), (19, 22), (19, 23),
    (20, 20), (20, 21), (20, 22), (20, 23), (20, 24),
    (21, 21), (21, 22), (21, 23), (21, 24), (21, 25),
    (22, 22), (22, 23), (22, 24), (22, 25), (22, 26),
    (23, 23), (23, 24), (23, 25), (23, 26), (23, 27),
    (24, 24), (24, 25), (24, 26), (24, 27), (24, 28),
    (25, 25), (25, 26), (25, 27), (25, 28), (25, 29),
    -- More relationships to reach 125+ total
    (1, 10), (2, 12), (3, 14), (4, 16), (5, 18),
    (6, 20), (7, 22), (8, 24), (9, 26), (10, 28),
    (1, 15), (2, 17), (3, 19), (4, 21), (5, 23);

INSERT INTO Fridge_Ingredient (fridge_id, ingredient_id, quantity, unit, is_expired) VALUES
    -- Busy Ben's fridge
    (1, 1, 2.5, 'pound', FALSE),  -- Busy Ben's chicken breast
    (1, 2, 1.0, 'pound', FALSE),  -- Busy Ben's ground beef
    (1, 3, 1.5, 'cup', FALSE),    -- Busy Ben's quinoa
    (1, 6, 2.0, 'piece', FALSE),  -- Busy Ben's broccoli
    (1, 8, 12.0, 'whole', FALSE), -- Busy Ben's eggs

    -- Other fridges with multiple ingredients
    (2, 3, 3.0, 'cup', FALSE),
    (2, 7, 2.0, 'piece', FALSE),
    (2, 11, 32.0, 'oz', FALSE),
    (2, 15, 16.0, 'oz', FALSE),
    (2, 19, 3.0, 'whole', FALSE),

    (3, 4, 2.0, 'cup', FALSE),
    (3, 8, 6.0, 'whole', FALSE),
    (3, 12, 8.0, 'oz', FALSE),
    (3, 16, 1.0, 'whole', FALSE),
    (3, 20, 10.0, 'oz', FALSE),

    (4, 5, 1.5, 'cup', TRUE),
    (4, 9, 0.5, 'gallon', FALSE),
    (4, 13, 6.0, 'oz', FALSE),
    (4, 17, 3.0, 'whole', TRUE),
    (4, 21, 16.0, 'oz', FALSE),

    (5, 6, 2.0, 'piece', FALSE),
    (5, 10, 8.0, 'oz', FALSE),
    (5, 14, 4.0, 'whole', FALSE),
    (5, 18, 1.0, 'pound', TRUE),
    (5, 22, 2.0, 'cup', FALSE),

    (6, 7, 3.0, 'piece', FALSE),
    (6, 11, 16.0, 'oz', TRUE),
    (6, 15, 12.0, 'oz', FALSE),
    (6, 19, 2.0, 'whole', FALSE),
    (6, 23, 1.5, 'cup', FALSE),

    (7, 8, 12.0, 'whole', FALSE),
    (7, 12, 12.0, 'oz', FALSE),
    (7, 16, 2.0, 'whole', TRUE),
    (7, 20, 6.0, 'oz', FALSE),
    (7, 24, 1.0, 'pint', FALSE),

    (8, 9, 1.0, 'gallon', FALSE),
    (8, 13, 8.0, 'oz', FALSE),
    (8, 17, 2.0, 'whole', FALSE),
    (8, 21, 14.0, 'oz', TRUE),
    (8, 25, 3.0, 'whole', FALSE),

    (9, 10, 8.0, 'oz', FALSE),
    (9, 14, 5.0, 'whole', FALSE),
    (9, 18, 1.5, 'pound', FALSE),
    (9, 22, 3.0, 'cup', TRUE),
    (9, 26, 16.0, 'oz', FALSE),

    (10, 1, 1.0, 'pound', TRUE),
    (10, 5, 2.0, 'cup', FALSE),
    (10, 10, 16.0, 'oz', FALSE),
    (10, 15, 8.0, 'oz', FALSE),
    (10, 20, 8.0, 'oz', TRUE),

    -- Additional fridges for newer clients
    (11, 2, 1.5, 'pound', FALSE),
    (11, 7, 4.0, 'piece', FALSE),
    (11, 12, 10.0, 'oz', TRUE),

    (12, 3, 2.0, 'cup', FALSE),
    (12, 8, 18.0, 'whole', FALSE),
    (12, 13, 6.0, 'oz', FALSE),

    (13, 4, 3.0, 'cup', TRUE),
    (13, 9, 0.75, 'gallon', FALSE),
    (13, 14, 6.0, 'whole', FALSE),

    (14, 5, 1.0, 'cup', FALSE),
    (14, 10, 12.0, 'oz', TRUE);

INSERT INTO ShoppingList_Ingredient (list_id, ingredient_id, quantity, unit, cost) VALUES
    -- Busy Ben's shopping list
    (1, 11, 2.0, 'cup', 3.99),    -- Busy Ben's shopping list
    (1, 12, 1.0, 'pound', 7.99),  -- Busy Ben's shopping list
    (1, 13, 0.5, 'pound', 4.49),  -- Busy Ben's shopping list
    (1, 14, 6.0, 'whole', 3.99),  -- Busy Ben's shopping list
    (1, 15, 1.0, 'bottle', 6.99), -- Busy Ben's shopping list

    -- Other shopping lists
    (2, 13, 0.5, 'pound', 5.99),
    (2, 14, 3.0, 'whole', 2.49),
    (2, 15, 0.5, 'bottle', 4.99),
    (2, 16, 2.0, 'whole', 1.99),
    (2, 17, 3.0, 'whole', 2.99),

    (3, 14, 6.0, 'whole', 4.99),
    (3, 15, 0.75, 'bottle', 5.49),
    (3, 16, 1.0, 'whole', 0.99),
    (3, 17, 2.0, 'whole', 1.99),
    (3, 18, 1.0, 'pound', 12.99),

    (4, 15, 1.0, 'bottle', 8.99),
    (4, 16, 2.0, 'whole', 1.99),
    (4, 17, 3.0, 'whole', 2.99),
    (4, 18, 1.5, 'pound', 18.99),
    (4, 19, 2.0, 'whole', 1.50),

    (5, 16, 2.0, 'whole', 1.99),
    (5, 17, 3.0, 'whole', 2.99),
    (5, 18, 1.0, 'pound', 12.99),
    (5, 19, 3.0, 'whole', 2.25),
    (5, 20, 1.0, 'bag', 3.99),

    (6, 17, 3.0, 'whole', 2.99),
    (6, 18, 1.0, 'pound', 12.99),
    (6, 19, 2.0, 'whole', 1.50),
    (6, 20, 2.0, 'bag', 7.98),
    (6, 21, 1.0, 'package', 2.99),

    (7, 18, 1.0, 'pound', 12.99),
    (7, 19, 2.0, 'whole', 1.50),
    (7, 20, 1.0, 'bag', 3.99),
    (7, 21, 2.0, 'package', 5.98),
    (7, 22, 1.0, 'can', 1.49),

    (8, 19, 2.0, 'whole', 1.50),
    (8, 20, 1.0, 'bag', 3.99),
    (8, 21, 1.0, 'package', 2.99),
    (8, 22, 2.0, 'can', 2.98),
    (8, 23, 1.0, 'package', 4.99),

    (9, 20, 1.0, 'bag', 3.99),
    (9, 21, 1.0, 'package', 2.99),
    (9, 22, 1.0, 'can', 1.49),
    (9, 23, 1.0, 'package', 4.99),
    (9, 24, 1.0, 'container', 3.99),

    (10, 21, 1.0, 'package', 2.99),
    (10, 22, 1.0, 'can', 1.49),
    (10, 23, 1.0, 'package', 4.99),
    (10, 24, 2.0, 'container', 7.98),
    (10, 25, 1.0, 'bunch', 2.49),

    -- Additional shopping lists for new clients
    (11, 25, 2.0, 'bunch', 4.98),
    (11, 26, 1.0, 'bottle', 8.99),
    (11, 27, 1.0, 'carton', 3.49),

    (12, 28, 4.0, 'whole', 3.99),
    (12, 29, 1.0, 'bag', 2.49),
    (12, 30, 1.0, 'bunch', 3.99),

    (13, 31, 1.0, 'pound', 9.99),
    (13, 32, 1.0, 'pound', 7.99),
    (13, 33, 1.0, 'bunch', 2.99),

    (14, 34, 8.0, 'oz', 3.49),
    (14, 35, 1.0, 'jar', 6.99),
    (14, 36, 1.0, 'package', 5.99),

    (15, 37, 1.0, 'jar', 4.99),
    (15, 38, 1.0, 'loaf', 3.49),
    (15, 39, 1.0, 'bottle', 7.99);

INSERT INTO Nutrition_Tracking (client_id, protein, fat, fiber, sodium, vitamins, calories, carbs) VALUES
    (1, 170.03, 66.62, 11.31, 1967.95, 137.14, 1593, 122.1),  -- Busy Ben's nutrition
    (2, 104.34, 23.49, 24.17, 2448.23, 104.72, 1917, 345.58),
    (3, 81.09, 60.12, 6.32, 2042.2, 103.67, 1890, 141.35),
    (4, 193.32, 73.02, 19.56, 2963.24, 105.24, 1822, 283.47),
    (5, 80.21, 70.32, 15.81, 2218.55, 74.02, 2021, 181.25),
    (6, 74.88, 72.39, 16.94, 2541.82, 101.93, 2071, 380.89),
    (7, 64.33, 20.83, 11.26, 1183.25, 142.17, 2934, 153.39),
    (8, 64.72, 78.01, 16.77, 1270.61, 74.91, 1837, 203.5),
    (9, 74.03, 56.31, 11.02, 1089.48, 78.76, 1778, 203.12),
    (10, 60.13, 58.15, 13.25, 1264.48, 123.31, 2428, 163.6),
    (11, 85.46, 45.32, 18.75, 1546.78, 112.45, 1942, 214.56),
    (12, 95.23, 52.67, 15.43, 1872.34, 98.67, 2156, 245.78),
    (13, 110.45, 48.93, 12.76, 1623.45, 105.34, 2034, 187.65),
    (14, 75.67, 60.45, 14.32, 1945.67, 87.54, 1876, 203.45),
    (15, 98.34, 43.21, 16.54, 1734.56, 115.43, 2087, 225.67),
    (16, 87.65, 55.43, 13.87, 1856.78, 94.32, 1943, 193.45),
    (17, 105.43, 50.23, 15.67, 1678.45, 103.67, 2145, 235.67),
    (18, 92.34, 58.76, 14.32, 1845.67, 89.45, 1987, 215.43),
    (19, 82.56, 45.67, 17.43, 1567.89, 108.76, 1876, 198.76),
    (20, 115.67, 52.34, 13.65, 1934.56, 97.43, 2234, 244.32);

INSERT INTO Client_Health_Advisor (client_id, advisor_id) VALUES
    -- Busy Ben with Riley Runner as primary advisor
    (1, 1),  -- Busy Ben with Riley Runner
    (2, 2),  -- Nicholas with Nancy Nutritionist
    
    -- Create many-to-many relationships (125+ rows)
    (1, 2),  -- Busy Ben also with Nancy Nutritionist
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 1),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (3, 1),
    (3, 2),
    (3, 4),
    (3, 5),
    (3, 6),
    (4, 1),
    (4, 2),
    (4, 3),
    (4, 5),
    (4, 6),
    (5, 1),
    (5, 2),
    (5, 3),
    (5, 4),
    (5, 6),
    (6, 1),
    (6, 2),
    (6, 3),
    (6, 4),
    (6, 5),
    (7, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (7, 5),
    (8, 1),
    (8, 2),
    (8, 3),
    (8, 4),
    (8, 5),
    (8, 6),
    (9, 1),
    (9, 2),
    (9, 3),
    (9, 4),
    (9, 5),
    (9, 6),
    (9, 7),
    (10, 1),
    (10, 2),
    (10, 3),
    (10, 4),
    (10, 5),
    (10, 6),
    (10, 7),
    (10, 8),
    -- Additional clients also have multiple advisors
    (11, 1),
    (11, 2),
    (11, 3),
    (11, 4),
    (11, 11),
    (12, 1),
    (12, 2),
    (12, 5),
    (12, 12),
    (13, 2),
    (13, 3),
    (13, 6),
    (13, 13),
    (14, 2),
    (14, 7),
    (14, 14),
    (15, 1),
    (15, 8),
    (15, 15),
    (16, 1),
    (16, 9),
    (16, 16),
    (17, 2),
    (17, 10),
    (17, 17),
    (18, 1),
    (18, 2),
    (18, 18),
    (19, 1),
    (19, 2),
    (19, 19),
    (20, 1),
    (20, 2),
    (20, 20),
    -- Additional connections to reach 125+ total
    (3, 7),
    (3, 8),
    (3, 9),
    (3, 10),
    (4, 7),
    (4, 8),
    (4, 9),
    (4, 10),
    (5, 7),
    (5, 8),
    (5, 9),
    (5, 10),
    (6, 7),
    (6, 8),
    (6, 9),
    (6, 10),
    (7, 6),
    (7, 7),
    (7, 8),
    (7, 9),
    (7, 10),
    (8, 7),
    (8, 8),
    (8, 9),
    (8, 10),
    (11, 5),
    (11, 6),
    (11, 7),
    (11, 8),
    (11, 9),
    (11, 10),
    (12, 3),
    (12, 4),
    (12, 6),
    (12, 7),
    (12, 8),
    (12, 9),
    (12, 10),
    (13, 1),
    (13, 4),
    (13, 5),
    (13, 7),
    (13, 8),
    (13, 9),
    (13, 10),
    (14, 1),
    (14, 3),
    (14, 4),
    (14, 5),
    (14, 6),
    (14, 8),
    (14, 9),
    (14, 10);

INSERT INTO Client_Workout (client_id, workout_id) VALUES
    -- Busy Ben's workouts
    (1, 1),  -- Busy Ben does Hiking
    (1, 2),  -- Busy Ben also does Pilates
    (1, 11), -- Running
    (1, 21), -- Kickboxing
    (1, 31), -- Rock Climbing

    -- Other clients with multiple workouts (creating 125+ total relationships)
    (2, 3),
    (2, 12),
    (2, 22),
    (2, 32),
    (3, 4),
    (3, 13),
    (3, 23),
    (3, 33),
    (4, 5),
    (4, 14),
    (4, 24),
    (4, 34),
    (5, 6),
    (5, 15),
    (5, 25),
    (5, 35),
    (6, 7),
    (6, 16),
    (6, 26),
    (6, 36),
    (7, 8),
    (7, 17),
    (7, 27),
    (7, 37),
    (8, 9),
    (8, 18),
    (8, 28),
    (8, 38),
    (9, 10),
    (9, 19),
    (9, 29),
    (9, 39),
    (10, 1),
    (10, 11),
    (10, 21),
    (10, 31),
    (11, 2),
    (11, 12),
    (11, 22),
    (11, 32),
    (12, 3),
    (12, 13),
    (12, 23),
    (12, 33),
    (13, 4),
    (13, 14),
    (13, 24),
    (13, 34),
    (14, 5),
    (14, 15),
    (14, 25),
    (14, 35),
    (15, 6),
    (15, 16),
    (15, 26),
    (15, 36),
    (16, 7),
    (16, 17),
    (16, 27),
    (16, 37),
    (17, 8),
    (17, 18),
    (17, 28),
    (17, 38),
    (18, 9),
    (18, 19),
    (18, 29),
    (18, 39),
    (19, 10),
    (19, 20),
    (19, 30),
    (19, 40),
    (20, 1),
    (20, 11),
    (20, 21),
    (20, 31),
    -- Additional workout relationships to reach 125+
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 6),
    (2, 7),
    (2, 8),
    (3, 9),
    (3, 10),
    (3, 11),
    (4, 12),
    (4, 13),
    (4, 15),
    (5, 16),
    (5, 17),
    (5, 18),
    (6, 19),
    (6, 20),
    (6, 1),
    (7, 2),
    (7, 3),
    (7, 4),
    (8, 5),
    (8, 6),
    (8, 7),
    (9, 8),
    (9, 9),
    (9, 1),
    (10, 2),
    (10, 3),
    (10, 4),
    (11, 5),
    (11, 6),
    (11, 7),
    (12, 8),
    (12, 9),
    (12, 10),
    (13, 1),
    (13, 2),
    (13, 3),
    (14, 1),
    (14, 2),
    (14, 3),
    (15, 1),
    (15, 2),
    (15, 3),
    (16, 1),
    (16, 2),
    (16, 3);

INSERT INTO Meal_Plan (pc_id, recipe_id, quantity) VALUES
    -- Meal plans for various personal constraints
    (1, 1, 2),  -- Busy Ben's meal plan
    (1, 11, 1), -- Busy Ben's meal plan
    (1, 21, 3), -- Busy Ben's meal plan
    (2, 2, 1),
    (2, 12, 2),
    (2, 22, 1),
    (3, 3, 3),
    (3, 13, 2),
    (3, 23, 1),
    (4, 4, 2),
    (4, 14, 1),
    (4, 24, 2),
    (5, 5, 1),
    (5, 15, 2),
    (5, 25, 1),
    (6, 6, 2),
    (6, 16, 1),
    (6, 26, 2),
    (7, 7, 1),
    (7, 17, 2),
    (7, 27, 1),
    (8, 8, 2),
    (8, 18, 1),
    (8, 28, 2),
    (9, 9, 1),
    (9, 19, 2),
    (9, 29, 1),
    (10, 10, 2),
    (10, 20, 1),
    (10, 30, 2),
    (11, 1, 1),
    (11, 11, 2),
    (11, 21, 1),
    (12, 2, 2),
    (12, 12, 1),
    (12, 22, 2),
    (13, 3, 1),
    (13, 13, 2),
    (13, 23, 1),
    (14, 4, 2),
    (14, 14, 1),
    (14, 24, 2),
    (15, 5, 1),
    (15, 15, 2),
    (15, 25, 1),
    (16, 6, 2),
    (16, 16, 1),
    (16, 26, 2),
    (17, 7, 1),
    (17, 17, 2),
    (17, 27, 1);

INSERT INTO Leftover (recipe_id, quantity, is_expired) VALUES
    (1, 2, FALSE),
    (2, 1, TRUE),
    (3, 3, FALSE),
    (4, 1, TRUE),
    (5, 2, FALSE),
    (6, 2, FALSE),
    (7, 1, TRUE),
    (8, 3, FALSE),
    (9, 1, TRUE),
    (10, 2, FALSE),
    (11, 1, FALSE),
    (12, 3, TRUE),
    (13, 1, FALSE),
    (14, 1, TRUE),
    (15, 3, FALSE),
    (16, 2, FALSE),
    (17, 2, TRUE),
    (18, 1, FALSE),
    (19, 2, TRUE),
    (20, 1, FALSE);

INSERT INTO Error_Log (client_id, log_id, message) VALUES
    (1, 1, 'User input error for Busy Ben'),
    (1, 2, 'Scan returned empty result for Busy Ben'),
    (1, 3, 'Barcode checksum mismatch for Busy Ben'),
    (2, 2, 'Barcode checksum mismatch'),
    (2, 4, 'User input error'),
    (2, 6, 'Scan returned empty result'),
    (3, 3, 'Scan returned empty result'),
    (3, 5, 'Database connection lost'),
    (3, 7, 'Ingredient scan failed'),
    (4, 4, 'Timeout during scan'),
    (4, 6, 'Invalid format detected'),
    (4, 8, 'Barcode checksum mismatch'),
    (5, 5, 'Invalid format detected'),
    (5, 7, 'Unrecognized barcode'),
    (5, 9, 'Scan returned empty result'),
    (6, 6, 'Scan returned empty result'),
    (6, 8, 'Expired ingredient scanned'),
    (6, 10, 'User input error'),
    (7, 7, 'Ingredient scan failed'),
    (7, 9, 'Database connection lost'),
    (7, 11, 'Barcode checksum mismatch'),
    (8, 8, 'Barcode checksum mismatch'),
    (8, 10, 'Timeout during scan'),
    (8, 12, 'Scan returned empty result'),
    (9, 9, 'Scan returned empty result'),
    (9, 11, 'Invalid format detected'),
    (9, 13, 'User input error'),
    (10, 10, 'User input error'),
    (10, 12, 'Ingredient scan failed'),
    (10, 14, 'Barcode checksum mismatch'),
    (11, 11, 'Barcode checksum mismatch'),
    (11, 13, 'Scan returned empty result'),
    (11, 15, 'Timeout during scan'),
    (12, 12, 'Scan returned empty result'),
    (12, 14, 'User input error'),
    (12, 16, 'Invalid format detected'),
    (13, 13, 'User input error'),
    (13, 15, 'Ingredient scan failed'),
    (13, 17, 'Barcode checksum mismatch'),
    (14, 14, 'Barcode checksum mismatch'),
    (14, 16, 'Scan returned empty result'),
    (14, 18, 'Database connection lost'),
    (15, 15, 'Timeout during scan'),
    (15, 17, 'Invalid format detected'),
    (15, 19, 'User input error'),
    (16, 16, 'Invalid format detected'),
    (16, 18, 'Ingredient scan failed'),
    (16, 20, 'Barcode checksum mismatch'),
    (17, 17, 'Barcode checksum mismatch'),
    (17, 19, 'Scan returned empty result'),
    (17, 21, 'Timeout during scan'),
    (18, 18, 'Database connection lost'),
    (18, 20, 'User input error'),
    (18, 22, 'Invalid format detected'),
    (19, 19, 'User input error'),
    (19, 21, 'Ingredient scan failed'),
    (19, 23, 'Barcode checksum mismatch'),
    (20, 20, 'Barcode checksum mismatch'),
    (20, 22, 'Scan returned empty result'),
    (20, 24, 'Timeout during scan');