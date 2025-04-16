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

INSERT INTO User (
    f_name, l_name, username, password, email
) VALUES 
    ('Heather', 'Bradford', 'heather231', 'g6ASy6N4(2', 'heather.bradford@example.com'),
    ('Nicholas', 'Miller', 'nicholas928', 't4DSCGrg)I', 'nicholas.miller@example.com'),
    ('George', 'Hall', 'george636', '(lHN^3AyN1', 'george.hall@example.com'),
    ('Kelly', 'Thomas', 'kelly742', '_d31KO@p+!', 'kelly.thomas@example.com'),
    ('Olivia', 'Hernandez', 'olivia693', '5a2FykmV*H', 'olivia.hernandez@example.com'),
    ('James', 'Porter', 'james817', '(9zKCkpvfp', 'james.porter@example.com'),
    ('Donald', 'Alvarez', 'donald903', 'XbY&0Jqm_5', 'donald.alvarez@example.com'),
    ('Steve', 'Barnes', 'steve492', '_R8HNVlE34', 'steve.barnes@example.com'),
    ('Timothy', 'Cowan', 'timothy874', 'EP6Mup0_M!', 'timothy.cowan@example.com'),
    ('Emily', 'Grimes', 'emily866', 'I^k18H4vLk', 'emily.grimes@example.com'),
    ('Virginia', 'Rogers', 'virginia559', 'cD_#2Aem!k', 'virginia.rogers@example.com'),
    ('Olivia', 'Johnson', 'olivia366', 'E)3sK&n6@y', 'olivia.johnson@example.com'),
    ('Isaac', 'Hurley', 'isaac147', 'T1VmsQ69@)', 'isaac.hurley@example.com'),
    ('Aaron', 'Adams', 'aaron126', '+LVC35rzn2', 'aaron.adams@example.com'),
    ('Kendra', 'Jefferson', 'kendra510', 'zp#nzeNe%8', 'kendra.jefferson@example.com'),
    ('Michelle', 'Armstrong', 'michelle561', '_9zEUw9BT2', 'michelle.armstrong@example.com'),
    ('Courtney', 'Jones', 'courtney264', '5*^v5UirjQ', 'courtney.jones@example.com'),
    ('Steven', 'Murphy', 'steven560', 'Qi(3eSm3X0', 'steven.murphy@example.com'),
    ('Michael', 'Burns', 'michael737', '5@xY3k!j%*', 'michael.burns@example.com'),
    ('Caleb', 'Blankenship', 'caleb199', '+M*9Cu)P2q', 'caleb.blankenship@example.com'),
    ('Brittney', 'Gilmore', 'brittney509', 'm1_i5MtD(7', 'brittney.gilmore@example.com'),
    ('Brittney', 'Rivera', 'brittney544', 'Z17GtsiGM&', 'brittney.rivera@example.com'),
    ('Robert', 'Roman', 'robert428', 'B2)53H4n%y', 'robert.roman@example.com'),
    ('Tina', 'Jennings', 'tina825', 'T)2#e3AwY4', 'tina.jennings@example.com'),
    ('Edward', 'Valenzuela', 'edward846', ')+YD3XSoF8', 'edward.valenzuela@example.com'),
    ('Tara', 'Patterson', 'tara479', 'v+)43ODn(X', 'tara.patterson@example.com'),
    ('Cynthia', 'Miller', 'cynthia729', '(7uKl&9kEt', 'cynthia.miller@example.com'),
    ('Kelsey', 'Porter', 'kelsey313', '+v_i)SYS%2', 'kelsey.porter@example.com'),
    ('Daniel', 'Foster', 'daniel761', '#1IFlO6vGj', 'daniel.foster@example.com'),
    ('Aaron', 'Smith', 'aaron690', '@0O_w@zn%9', 'aaron.smith@example.com'),
    ('David', 'Serrano', 'david572', 's#_7Xwj!Z6', 'david.serrano@example.com'),
    ('Patricia', 'Cox', 'patricia336', 'f3NU0C)s)a', 'patricia.cox@example.com'),
    ('Christopher', 'Meadows', 'christopher164', 'zD0Tmn#p%p', 'christopher.meadows@example.com'),
    ('Jason', 'Taylor', 'jason401', ')U26AunhDv', 'jason.taylor@example.com'),
    ('Ryan', 'Lopez', 'ryan737', 'ufFsUnn6&8', 'ryan.lopez@example.com'),
    ('Roger', 'Valencia', 'roger652', '*IsZWMqp3d', 'roger.valencia@example.com'),
    ('Patricia', 'Jimenez', 'patricia197', '9t#A#1Hq_k', 'patricia.jimenez@example.com'),
    ('Todd', 'Howell', 'todd513', 'jpHilSk+%4', 'todd.howell@example.com'),
    ('Heather', 'Rogers', 'heather174', 'h5uQc4Z8#D', 'heather.rogers@example.com'),
    ('Jared', 'Park', 'jared210', 'Q_8UFyiGmS', 'jared.park@example.com');

INSERT INTO Admin (user_id) VALUES 
    (1), (2), (3), (4), (5),
    (6), (7), (8), (9), (10),
    (11), (12), (13), (14), (15),
    (16), (17), (18), (19), (20),
    (21), (22), (23), (24), (25),
    (26), (27), (28), (29), (30),
    (31), (32), (33), (34), (35),
    (36), (37), (38), (39), (40);

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
    (89.4, 'tree nuts,none', 'vegetarian', 'senior'),
    (93.88, 'none', 'vegetarian', 'child'),
    (190.58, 'dairy', 'vegetarian', 'adult'),
    (89.44, 'none', 'paleo', 'adult'),
    (141.37, 'none', 'balanced', 'teen'),
    (71.89, 'sesame', 'vegetarian', 'teen'),
    (199.86, 'soy', 'paleo', 'child'),
    (60.56, 'none,soy', 'low-carb', 'adult'),
    (63.13, 'tree nuts,dairy,shellfish', 'vegetarian', 'senior'),
    (51.33, 'tree nuts,fish,sesame', 'vegetarian', 'teen'),
    (182.57, 'sesame', 'paleo', 'child'),
    (66.45, 'gluten,fish', 'paleo', 'senior'),
    (186.62, 'soy,gluten', 'vegetarian', 'senior'),
    (132.17, 'none', 'vegetarian', 'child'),
    (89.63, 'none,tree nuts,gluten', 'vegetarian', 'senior'),
    (156.61, 'soy,egg,fish', 'vegan', 'senior'),
    (198.62, 'dairy,soy', 'paleo', 'child'),
    (166.76, 'peanuts', 'vegetarian', 'adult'),
    (189.94, 'gluten,egg,sesame', 'paleo', 'adult'),
    (188.31, 'gluten,fish', 'vegan', 'teen'),
    (107.33, 'shellfish', 'low-carb', 'teen'),
    (139.92, 'tree nuts,peanuts', 'balanced', 'senior'),
    (108.1, 'none', 'low-carb', 'adult'),
    (150.95, 'gluten,tree nuts,peanuts', 'low-carb', 'senior'),
    (176.78, 'shellfish', 'paleo', 'senior'),
    (51.78, 'none', 'keto', 'child'),
    (193.75, 'peanuts', 'low-carb', 'senior'),
    (104.51, 'egg,sesame,peanuts', 'low-carb', 'teen'),
    (127.26, 'none', 'low-carb', 'teen'),
    (190.53, 'sesame,peanuts,soy', 'keto', 'child');

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
    ('Running', 27, NULL, 320),
    ('Cycling', 76, NULL, 579),
    ('Boxing', 51, 30.22, 513),
    ('Running', 63, NULL, 172),
    ('Pilates', 33, NULL, 329),
    ('Jump Rope', 60, NULL, 274),
    ('Swimming', 80, NULL, 286),
    ('Boxing', 36, 101.84, 569),
    ('Jump Rope', 57, NULL, 394),
    ('Swimming', 84, NULL, 305),
    ('Dancing', 46, NULL, 435),
    ('Cycling', 36, NULL, 530),
    ('HIIT', 21, NULL, 187),
    ('Cycling', 24, NULL, 597),
    ('Jump Rope', 31, NULL, 173),
    ('Dancing', 70, NULL, 416),
    ('Yoga', 57, NULL, 250),
    ('Dancing', 23, NULL, 367),
    ('Yoga', 64, NULL, 275),
    ('Pilates', 34, NULL, 572);

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
    ('Black Beans', '2026-03-12'),
    ('Tofu', '2025-07-18'),
    ('Oats', '2026-01-22'),
    ('Blueberries', '2025-06-08'),
    ('Chia Seeds', '2026-04-15'),
    ('Olive Oil', '2025-11-30'),
    ('Peanut Butter', '2025-09-07'),
    ('Almond Milk', '2025-07-29'),
    ('Kale', '2025-05-14'),
    ('Tuna', '2026-02-18'),
    ('Turkey Breast', '2025-08-04'),
    ('Quinoa Flour', '2026-01-15'),
    ('Coconut Oil', '2025-12-10'),
    ('Cauliflower', '2025-06-05'),
    ('Tempeh', '2025-07-14'),
    ('Hemp Seeds', '2025-10-22'),
    ('Hummus', '2025-06-30'),
    ('Sweet Potatoes', '2025-11-15'),
    ('Zucchini', '2025-06-12'),
    ('Nutritional Yeast', '2026-03-28');

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
    ('Herself Salad', 'Course also college north wait anyone author cup social how news.'),
    ('Huge Salad', 'Magazine adult assume economy born imagine care society tonight song.'),
    ('Social Skillet', 'That Mrs themselves us something short pretty treatment top character green.'),
    ('Sea Salad', 'Community anyone form probably human investment investment down.'),
    ('Star Skillet', 'Energy third heart speech program card hear design truth bar produce popular street top require character.'),
    ('Blood Skillet', 'Your his total use apply glass finally direction establish cell glass generation response.'),
    ('Through Salad', 'Real region not case hope term crime scientist health instead brother market to conference.'),
    ('Report Skillet', 'Floor window science technology home cause live mind so difficult could.'),
    ('Third Salad', 'Maybe within watch wrong decide necessary feeling reduce hair against environment.'),
    ('Our Stew', 'Physical free meet prepare serious though majority better major step thing.'),
    ('Message Bowl', 'Society statement drive class Republican own feeling police report cause range happy near fire happy.'),
    ('Collection Bowl', 'Establish foreign international area chance well case.'),
    ('Them Stew', 'Her me dream particularly next possible lead process.'),
    ('Rock Stew', 'Perhaps approach seem local appear wonder model person as factor.'),
    ('Later Stew', 'Risk knowledge inside last left pay eat.'),
    ('Remain Salad', 'Fund training economy represent strategy spend over gas total tend cup each.'),
    ('Course Bowl', 'Different brother a matter stage care else young even television possible send plan.'),
    ('Player Skillet', 'Discussion since Mrs help wonder they sit nice laugh call ground case.'),
    ('Already Salad', 'Baby least table agent change him represent need short fish or line run lot program compare.'),
    ('Cup Stew', 'Eight money should new recent model fear entire but federal themselves language fine.'),
    ('Type Stew', 'None high camera goal skin raise wind little without store sister expert avoid that medical us.'),
    ('Job Stew', 'Religious foot difficult police computer lay establish.'),
    ('Work Wrap', 'East control report maybe expect oil card seek between.'),
    ('Fund Bowl', 'Bag your institution energy need he radio especially note community sport go position foreign firm fear.'),
    ('Imagine Bowl', 'Away son benefit population himself science share citizen fine everyone get.'),
    ('While Skillet', 'Blue for morning lawyer public section politics Congress popular rule against threat third prepare.'),
    ('Until Bowl', 'Establish hospital price thank fund child gas product career want picture sign get this Mrs.'),
    ('Bar Skillet', 'Scene start two wrong big friend beat every amount stock.'),
    ('Quite Stew', 'Describe assume wait forward pick someone while newspaper fine national all once leader executive.'),
    ('Student Stew', 'Surface attention answer seven physical friend operation inside against difference soon yourself could opportunity prepare season.');

INSERT INTO Recipe_Ingredient (
    recipe_id, ingredient_id, quantity, unit
) VALUES 
    (20, 23, 1.21, 'whole'),
    (38, 35, 1.60, 'piece'),
    (22, 22, 1.05, 'pound'),
    (18, 20, 2.65, 'gallon'),
    (8, 20, 2.19, 'gallon'),
    (27, 32, 3.00, 'piece'),
    (35, 9, 0.99, 'cup'),
    (40, 19, 2.87, 'cup'),
    (28, 6, 2.49, 'piece'),
    (24, 15, 0.80, 'oz'),
    (23, 14, 2.91, 'bag'),
    (23, 35, 2.05, 'pound'),
    (18, 34, 1.57, 'bag'),
    (34, 30, 1.01, 'pound'),
    (21, 32, 1.79, 'piece'),
    (35, 15, 1.62, 'whole'),
    (17, 23, 0.82, 'oz'),
    (39, 24, 0.75, 'whole'),
    (25, 24, 2.07, 'oz'),
    (27, 5, 0.96, 'whole'),
    (3, 38, 1.07, 'scoop'),
    (40, 20, 2.93, 'whole'),
    (5, 31, 2.93, 'whole'),
    (26, 33, 0.62, 'cup'),
    (40, 35, 2.68, 'piece'),
    (5, 27, 1.44, 'gallon'),
    (10, 22, 2.93, 'bag'),
    (23, 39, 2.99, 'scoop'),
    (27, 33, 2.95, 'piece'),
    (5, 16, 1.28, 'cup'),
    (15, 21, 2.31, 'oz'),
    (7, 35, 1.41, 'scoop'),
    (32, 36, 1.04, 'cup'),
    (32, 16, 0.87, 'scoop'),
    (28, 35, 2.59, 'bag'),
    (28, 7, 1.79, 'whole'),
    (3, 2, 2.29, 'pound'),
    (34, 13, 1.33, 'pound'),
    (16, 40, 0.68, 'whole'),
    (26, 30, 2.82, 'scoop'),
    (24, 20, 1.73, 'cup'),
    (30, 22, 2.49, 'oz'),
    (21, 15, 2.07, 'bag'),
    (22, 36, 1.10, 'piece'),
    (2, 11, 0.96, 'scoop'),
    (11, 1, 1.85, 'oz'),
    (10, 11, 2.97, 'scoop'),
    (37, 10, 2.89, 'gallon'),
    (39, 4, 1.69, 'pound'),
    (35, 33, 1.28, 'gallon'),
    (2, 40, 1.68, 'piece'),
    (17, 17, 1.86, 'scoop'),
    (39, 36, 2.97, 'gallon'),
    (39, 15, 0.77, 'pound'),
    (38, 39, 1.57, 'piece'),
    (36, 11, 0.97, 'piece'),
    (19, 28, 1.81, 'cup'),
    (37, 36, 1.40, 'pound'),
    (34, 6, 0.73, 'piece'),
    (8, 34, 2.76, 'bag'),
    (28, 20, 2.43, 'cup'),
    (39, 3, 0.78, 'pound'),
    (18, 6, 2.75, 'cup'),
    (4, 13, 1.49, 'oz'),
    (1, 22, 1.46, 'scoop'),
    (22, 24, 1.93, 'cup'),
    (18, 36, 1.31, 'pound'),
    (23, 17, 2.95, 'whole'),
    (31, 40, 2.09, 'whole'),
    (6, 4, 1.37, 'oz'),
    (13, 9, 2.82, 'piece'),
    (1, 29, 1.91, 'bag'),
    (16, 31, 2.58, 'whole'),
    (23, 36, 2.12, 'scoop'),
    (9, 19, 2.35, 'scoop'),
    (24, 7, 1.36, 'bag'),
    (32, 25, 1.69, 'gallon'),
    (3, 33, 1.81, 'scoop'),
    (17, 4, 1.78, 'whole'),
    (10, 16, 1.86, 'gallon'),
    (35, 2, 2.75, 'oz'),
    (9, 20, 2.80, 'pound'),
    (10, 10, 2.29, 'piece'),
    (29, 17, 2.40, 'cup'),
    (35, 31, 1.81, 'bag'),
    (29, 15, 1.45, 'bag'),
    (18, 26, 1.27, 'scoop'),
    (26, 6, 2.17, 'scoop'),
    (27, 13, 1.63, 'cup'),
    (7, 18, 0.60, 'pound'),
    (39, 16, 1.92, 'gallon'),
    (1, 31, 2.70, 'whole'),
    (24, 25, 1.38, 'whole'),
    (24, 22, 0.92, 'cup'),
    (27, 6, 2.12, 'scoop'),
    (20, 40, 1.73, 'cup'),
    (6, 39, 0.99, 'oz'),
    (14, 5, 2.83, 'oz'),
    (31, 4, 2.31, 'cup'),
    (12, 39, 1.70, 'scoop'),
    (11, 26, 1.62, 'cup'),
    (25, 31, 0.63, 'gallon'),
    (16, 26, 1.68, 'pound'),
    (2, 33, 1.36, 'piece'),
    (2, 7, 2.68, 'oz'),
    (4, 11, 1.96, 'scoop'),
    (38, 16, 2.47, 'whole'),
    (25, 11, 1.51, 'whole'),
    (27, 19, 2.02, 'piece'),
    (6, 36, 0.78, 'whole'),
    (40, 28, 1.53, 'piece'),
    (36, 7, 2.08, 'pound'),
    (5, 18, 2.71, 'cup'),
    (14, 2, 1.17, 'scoop'),
    (14, 3, 1.64, 'whole'),
    (15, 12, 2.37, 'whole'),
    (32, 19, 1.20, 'pound'),
    (32, 8, 1.30, 'whole'),
    (11, 9, 0.69, 'bag'),
    (12, 38, 1.20, 'gallon'),
    (13, 19, 2.08, 'scoop'),
    (10, 9, 1.69, 'bag'),
    (2, 10, 0.94, 'cup'),
    (25, 6, 2.63, 'bag'),
    (30, 30, 2.98, 'cup');

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
    (21, 24.2, 12.57, 6.3, 6.62, 111.06, 313, 67.85),
    (22, 18.1, 2.65, 8.06, 42.12, 119.5, 301, 57.87),
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
    (35, 23.25, 5.96, 0.79, 80.51, 99.47, 212, 79.72),
    (36, 21.17, 8.55, 6.17, 12.67, 199.49, 231, 51.27),
    (37, 5.56, 2.69, 9.66, 1.49, 151.26, 175, 8.75),
    (38, 14.38, 2.68, 5.14, 20.04, 119.13, 347, 59.19),
    (39, 27.96, 6.67, 1.28, 64.98, 94.34, 208, 75.82),
    (40, 10.42, 5.67, 5.1, 75.53, 116.18, 290, 47.29);

INSERT INTO Ingredient_Macronutrient (
    ingredient_id, macro_id
) VALUES 
    (7, 25), (30, 1), (11, 11), (7, 13), (25, 38),
    (33, 19), (24, 19), (39, 24), (12, 40), (5, 12),
    (14, 5), (11, 14), (3, 13), (13, 22), (14, 17),
    (1, 38), (22, 17), (26, 35), (38, 15), (13, 37),
    (8, 38), (34, 20), (36, 18), (16, 30), (25, 29),
    (32, 23), (24, 39), (31, 38), (17, 15), (32, 36),
    (27, 12), (9, 11), (32, 9), (34, 30), (36, 13),
    (24, 2), (35, 38), (40, 22), (2, 38), (26, 24),
    (39, 23), (16, 39), (31, 32), (26, 2), (23, 22),
    (26, 13), (25, 15), (8, 19), (20, 16), (7, 40),
    (11, 35), (10, 21), (28, 28), (38, 9), (37, 38),
    (19, 18), (9, 35), (29, 28), (22, 39), (24, 27),
    (25, 22), (20, 28), (15, 18), (29, 37), (32, 40),
    (8, 14), (35, 3), (32, 7), (9, 22), (15, 17),
    (39, 36), (13, 8), (13, 6), (24, 32), (39, 3),
    (36, 40), (12, 5), (2, 22), (4, 16), (16, 32),
    (18, 9), (20, 27), (16, 25), (34, 3), (29, 18),
    (39, 13), (16, 12), (24, 7), (26, 17), (30, 10),
    (23, 15), (8, 16), (18, 8), (36, 16), (17, 4),
    (1, 12), (28, 39), (33, 27), (5, 23), (19, 21),
    (11, 6), (17, 10), (37, 29), (17, 23), (13, 3),
    (34, 6), (18, 5), (28, 25), (3, 33), (20, 7),
    (16, 21), (20, 25), (17, 6), (7, 24), (1, 6),
    (16, 13), (13, 39), (5, 29), (32, 16), (3, 9),
    (34, 7), (19, 35), (21, 30), (4, 17), (6, 16);

INSERT INTO Brand (
    brand_id, name, is_trusted
) VALUES 
    (1, 'Kirkland Signature', TRUE),
    (2, '365 Everyday Value', FALSE),
    (3, 'Trader Joe''s', FALSE),
    (4, 'Great Value', TRUE),
    (5, 'Organic Valley', TRUE),
    (6, 'Annie''s', FALSE),
    (7, 'Amy''s', FALSE),
    (8, 'Green Giant', FALSE),
    (9, 'Horizon Organic', FALSE),
    (10, 'Chobani', FALSE),
    (11, 'Siggi''s', FALSE),
    (12, 'Fage', TRUE),
    (13, 'Tillamook', TRUE),
    (14, 'Stonyfield', FALSE),
    (15, 'Daiya', FALSE),
    (16, 'Gardein', FALSE),
    (17, 'MorningStar Farms', FALSE),
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
    (32, 'Bob''s Red Mill', FALSE),
    (33, 'Barilla', TRUE),
    (34, 'Rao''s Homemade', TRUE),
    (35, 'Prego', FALSE),
    (36, 'Classico', TRUE),
    (37, 'Hunt''s', FALSE),
    (38, 'Hellmann''s', TRUE),
    (39, 'Sir Kensington''s', TRUE),
    (40, 'Generic Brand', TRUE);

INSERT INTO Recipe_Brand (
    recipe_id, brand_id
) VALUES 
    (37, 8), (14, 28), (7, 15), (40, 1), (35, 31),
    (32, 24), (16, 10), (7, 1), (25, 8), (8, 22),
    (34, 24), (24, 1), (38, 12), (2, 22), (21, 31),
    (22, 19), (27, 5), (1, 37), (25, 14), (28, 6),
    (7, 14), (5, 17), (33, 10), (7, 13), (1, 14),
    (40, 26), (29, 34), (14, 4), (3, 11), (10, 14),
    (39, 18), (8, 15), (23, 20), (26, 3), (4, 13),
    (5, 18), (28, 4), (10, 33), (28, 30), (27, 29),
    (22, 21), (12, 12), (15, 15), (23, 2), (36, 27),
    (32, 13), (34, 10), (38, 3), (17, 30), (22, 14),
    (2, 39), (33, 17), (5, 23), (7, 28), (14, 27),
    (33, 26), (22, 17), (13, 26), (16, 39), (40, 34),
    (40, 36), (10, 35), (34, 21), (10, 11), (14, 31),
    (15, 26), (28, 35), (14, 25), (13, 27), (29, 25),
    (28, 11), (24, 3), (6, 3), (39, 35), (21, 26),
    (30, 38), (17, 25), (1, 15), (21, 20), (24, 28),
    (28, 32), (2, 30), (37, 33), (15, 32), (18, 15),
    (25, 9), (30, 9), (23, 14), (10, 17), (21, 19),
    (30, 15), (13, 13), (22, 11), (33, 34), (1, 20),
    (38, 19), (16, 3), (16, 32), (10, 26), (17, 18),
    (31, 3), (39, 10), (13, 12), (24, 33), (20, 28),
    (6, 25), (35, 24), (20, 23), (11, 37), (27, 24),
    (9, 32), (10, 23), (27, 23), (11, 17), (38, 30),
    (14, 33), (34, 3), (34, 25), (21, 30), (3, 39),
    (6, 29), (20, 36), (4, 30), (4, 9), (6, 8);

INSERT INTO Fridge_Inventory (
    fridge_id
) VALUES 
    (1), (2), (3), (4), (5),
    (6), (7), (8), (9), (10),
    (11), (12), (13), (14), (15),
    (16), (17), (18), (19), (20),
    (21), (22), (23), (24), (25),
    (26), (27), (28), (29), (30),
    (31), (32), (33), (34), (35),
    (36), (37), (38), (39), (40);

INSERT INTO Shopping_List (list_id) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20),
(21), (22), (23), (24), (25), (26), (27), (28), (29), (30),
(31), (32), (33), (34), (35), (36), (37), (38), (39), (40);

INSERT INTO ShoppingList_Ingredient (list_id, ingredient_id, quantity, unit, cost)
VALUES
(19, 5, 2.67, 'gallon', 3.92),
(17, 22, 3.96, 'cup', 5.54),
(30, 24, 3.70, 'gallon', 1.90),
(13, 28, 3.92, 'pound', 7.05),
(5, 30, 2.84, 'whole', 5.45),
(31, 29, 2.59, 'gallon', 7.97),
(10, 26, 3.18, 'piece', 1.73),
(14, 17, 4.40, 'piece', 9.51),
(22, 10, 2.55, 'scoop', 8.81),
(2, 31, 2.59, 'whole', 7.99),
(18, 20, 4.96, 'scoop', 0.93),
(13, 31, 4.75, 'scoop', 5.25),
(11, 20, 2.03, 'scoop', 3.70),
(15, 38, 2.30, 'cup', 5.46),
(22, 5, 1.14, 'oz', 5.86),
(3, 24, 4.29, 'bag', 4.92),
(40, 9, 4.58, 'cup', 1.48),
(38, 3, 1.03, 'bag', 7.50),
(9, 19, 2.15, 'pound', 7.25),
(11, 34, 4.34, 'gallon', 2.34),
(27, 31, 3.31, 'oz', 4.70),
(17, 8, 3.91, 'bag', 9.79),
(15, 35, 2.04, 'gallon', 1.32),
(27, 7, 1.89, 'oz', 6.36),
(32, 34, 1.19, 'whole', 4.88),
(7, 33, 3.24, 'oz', 2.05),
(4, 29, 1.64, 'oz', 8.00),
(6, 17, 4.03, 'oz', 8.46),
(3, 25, 3.19, 'whole', 5.53),
(8, 35, 2.36, 'pound', 1.63),
(36, 11, 3.25, 'scoop', 3.09),
(19, 3, 2.10, 'gallon', 2.94),
(18, 19, 3.10, 'scoop', 8.36),
(22, 20, 2.37, 'cup', 4.55),
(36, 38, 2.14, 'pound', 6.96),
(26, 16, 2.60, 'piece', 8.54),
(33, 33, 4.64, 'bag', 5.38),
(36, 19, 2.67, 'bag', 9.74),
(26, 32, 4.06, 'pound', 8.57),
(34, 32, 3.45, 'scoop', 6.34),
(30, 26, 4.15, 'whole', 9.53),
(5, 27, 4.00, 'gallon', 4.22),
(32, 4, 1.79, 'piece', 7.23),
(39, 11, 3.12, 'whole', 0.81),
(10, 18, 3.01, 'gallon', 8.77),
(13, 26, 1.87, 'cup', 1.30),
(15, 40, 4.56, 'pound', 7.09),
(8, 21, 1.57, 'oz', 8.17),
(5, 26, 1.77, 'piece', 2.47),
(20, 21, 3.69, 'piece', 5.05),
(10, 8, 1.60, 'cup', 1.23),
(9, 22, 1.56, 'cup', 6.56),
(8, 10, 3.07, 'gallon', 6.22),
(7, 37, 2.45, 'scoop', 5.59),
(7, 16, 2.31, 'cup', 7.42),
(13, 1, 4.46, 'bag', 1.94),
(17, 37, 4.89, 'cup', 3.94),
(4, 2, 3.72, 'piece', 1.79),
(4, 31, 2.97, 'gallon', 7.35),
(7, 26, 4.09, 'scoop', 6.44),
(5, 8, 1.89, 'oz', 1.50),
(25, 24, 2.70, 'gallon', 8.19),
(30, 20, 2.86, 'scoop', 9.79),
(36, 9, 2.67, 'scoop', 7.67),
(29, 32, 1.01, 'oz', 4.38),
(26, 38, 1.49, 'cup', 9.30),
(15, 3, 1.95, 'gallon', 2.81),
(17, 6, 2.42, 'oz', 3.56),
(32, 9, 1.21, 'whole', 6.88),
(9, 16, 3.92, 'whole', 9.79),
(32, 7, 1.74, 'pound', 5.98),
(2, 20, 3.70, 'bag', 3.86),
(24, 5, 4.69, 'gallon', 6.46),
(31, 9, 4.64, 'oz', 3.06),
(14, 15, 2.94, 'bag', 6.37),
(37, 33, 2.32, 'piece', 7.79),
(22, 27, 4.53, 'cup', 5.00),
(24, 19, 2.20, 'piece', 7.46),
(26, 21, 3.09, 'pound', 5.30),
(21, 7, 4.95, 'oz', 2.31),
(35, 5, 1.25, 'gallon', 9.76),
(31, 26, 4.29, 'pound', 5.51),
(26, 11, 4.72, 'oz', 2.93),
(29, 20, 4.50, 'cup', 3.93),
(13, 22, 1.73, 'scoop', 4.88),
(37, 32, 4.73, 'gallon', 6.02),
(36, 31, 3.50, 'pound', 3.51),
(11, 7, 2.93, 'whole', 5.07),
(33, 27, 2.78, 'whole', 2.61),
(10, 25, 1.93, 'gallon', 5.39),
(8, 3, 4.16, 'bag', 8.80),
(32, 31, 4.20, 'cup', 0.65),
(27, 36, 2.19, 'cup', 2.27),
(14, 29, 3.45, 'scoop', 8.28),
(3, 20, 3.69, 'oz', 4.26),
(32, 1, 3.36, 'piece', 5.28),
(27, 33, 1.29, 'whole', 0.98),
(9, 25, 2.83, 'whole', 4.30),
(8, 9, 3.94, 'scoop', 7.31),
(5, 36, 1.83, 'gallon', 4.96),
(17, 3, 1.90, 'oz', 7.50),
(31, 18, 4.93, 'oz', 7.15),
(6, 16, 2.12, 'gallon', 8.53),
(27, 22, 4.54, 'pound', 0.79),
(25, 1, 3.99, 'gallon', 2.19),
(23, 4, 1.78, 'gallon', 5.10),
(1, 20, 2.16, 'gallon', 2.34),
(23, 19, 2.08, 'scoop', 6.77),
(32, 23, 3.78, 'gallon', 4.21),
(18, 26, 2.00, 'whole', 7.67),
(15, 33, 4.76, 'whole', 1.99),
(25, 4, 3.94, 'oz', 3.19),
(31, 19, 3.14, 'cup', 8.77),
(17, 29, 1.87, 'oz', 4.98),
(19, 37, 4.94, 'oz', 3.91),
(3, 32, 4.17, 'oz', 0.82),
(8, 26, 3.29, 'cup', 4.54),
(32, 27, 1.25, 'cup', 4.15),
(5, 14, 3.19, 'oz', 1.46),
(16, 17, 3.03, 'bag', 8.21),
(36, 5, 4.81, 'pound', 7.77),
(4, 10, 3.81, 'scoop', 9.28),
(38, 15, 1.71, 'oz', 2.07),
(34, 37, 2.62, 'gallon', 5.80),
(25, 39, 4.99, 'piece', 4.31);

INSERT INTO Food_Scan_Log (ingredient_id, status)
VALUES
(29, 'SUCCESS'),
(9, 'SUCCESS'),
(17, 'FAILED'),
(16, 'FAILED'),
(7, 'SUCCESS'),
(12, 'SUCCESS'),
(39, 'SUCCESS'),
(1, 'SUCCESS'),
(7, 'SUCCESS'),
(26, 'SUCCESS'),
(11, 'FAILED'),
(34, 'SUCCESS'),
(17, 'SUCCESS'),
(26, 'SUCCESS'),
(18, 'SUCCESS'),
(37, 'FAILED'),
(34, 'FAILED'),
(1, 'SUCCESS'),
(20, 'FAILED'),
(7, 'SUCCESS'),
(23, 'FAILED'),
(19, 'FAILED'),
(35, 'SUCCESS'),
(26, 'SUCCESS'),
(35, 'SUCCESS'),
(7, 'SUCCESS'),
(18, 'FAILED'),
(24, 'FAILED'),
(24, 'FAILED'),
(29, 'SUCCESS'),
(37, 'SUCCESS'),
(7, 'FAILED'),
(7, 'SUCCESS'),
(5, 'SUCCESS'),
(7, 'FAILED'),
(32, 'SUCCESS'),
(7, 'SUCCESS'),
(13, 'SUCCESS'),
(31, 'SUCCESS'),
(28, 'SUCCESS');

INSERT INTO Client (user_id, pc_id, fridge_id, list_id, log_id, flag)
VALUES
(1, 1, 1, 1, 2, 0),
(2, 2, 2, 2, 3, 0),
(3, 3, 3, 3, 4, 0),
(4, 4, 4, 4, 5, 1),
(5, 5, 5, 5, 6, 1),
(6, 6, 6, 6, 7, 1),
(7, 7, 7, 7, 8, 1),
(8, 8, 8, 8, 9, 0),
(9, 9, 9, 9, 10, 0),
(10, 10, 10, 10, 11, 0),
(11, 11, 11, 11, 12, 1),
(12, 12, 12, 12, 13, 1),
(13, 13, 13, 13, 14, 0),
(14, 14, 14, 14, 15, 1),
(15, 15, 15, 15, 16, 0),
(16, 16, 16, 16, 17, 0),
(17, 17, 17, 17, 18, 0),
(18, 18, 18, 18, 19, 0),
(19, 19, 19, 19, 20, 1),
(20, 20, 20, 20, 21, 0),
(21, 21, 21, 21, 22, 1),
(22, 22, 22, 22, 23, 1),
(23, 23, 23, 23, 24, 1),
(24, 24, 24, 24, 25, 1),
(25, 25, 25, 25, 26, 0),
(26, 26, 26, 26, 27, 1),
(27, 27, 27, 27, 28, 0),
(28, 28, 28, 28, 29, 1),
(29, 29, 29, 29, 30, 0),
(30, 30, 30, 30, 31, 0),
(31, 31, 31, 31, 32, 1),
(32, 32, 32, 32, 33, 1),
(33, 33, 33, 33, 34, 0),
(34, 34, 34, 34, 35, 1),
(35, 35, 35, 35, 36, 0),
(36, 36, 36, 36, 37, 0),
(37, 37, 37, 37, 38, 1),
(38, 38, 38, 38, 39, 1),
(39, 39, 39, 39, 40, 1),
(40, 40, 40, 40, 1, 1);

INSERT INTO Meal_Plan (pc_id, recipe_id, quantity)
VALUES
(21, 13, 3),
(7, 3, 1),
(9, 22, 3),
(10, 37, 3),
(32, 12, 2),
(22, 12, 2),
(31, 12, 2),
(17, 5, 1),
(12, 24, 2),
(33, 27, 3),
(15, 35, 2),
(13, 7, 2),
(32, 1, 1),
(6, 29, 1),
(23, 37, 1),
(28, 8, 2),
(20, 20, 2),
(28, 3, 2),
(17, 1, 2),
(25, 38, 3),
(25, 16, 2),
(17, 31, 3),
(1, 32, 1),
(38, 9, 2),
(32, 14, 3),
(12, 32, 1),
(30, 18, 1),
(23, 6, 1),
(28, 30, 2),
(9, 8, 3),
(27, 21, 2),
(18, 24, 3),
(37, 24, 2),
(5, 25, 1),
(2, 15, 2),
(39, 19, 1),
(39, 18, 3),
(12, 19, 3),
(34, 40, 2),
(20, 38, 2);

INSERT INTO Leftover (leftover_id, recipe_id, quantity, is_expired) VALUES
(1001, 324, 2.5, FALSE),
(1002, 118, 1.0, TRUE),
(1003, 256, 3.2, FALSE),
(1004, 193, 0.5, TRUE),
(1005, 287, 1.8, FALSE),
(1006, 341, 2.0, FALSE),
(1007, 129, 1.5, TRUE),
(1008, 275, 3.0, FALSE),
(1009, 182, 0.7, TRUE),
(1010, 301, 2.2, FALSE),
(1011, 156, 1.3, FALSE),
(1012, 245, 2.7, TRUE),
(1013, 137, 0.8, FALSE),
(1014, 298, 1.1, TRUE),
(1015, 219, 3.5, FALSE),
(1016, 163, 2.4, FALSE),
(1017, 227, 1.7, TRUE),
(1018, 345, 0.9, FALSE),
(1019, 112, 2.3, TRUE),
(1020, 291, 1.4, FALSE),
(1021, 173, 3.1, FALSE),
(1022, 267, 2.6, TRUE),
(1023, 143, 1.2, FALSE),
(1024, 329, 0.6, TRUE),
(1025, 205, 2.1, FALSE),
(1026, 318, 1.9, FALSE),
(1027, 241, 3.3, TRUE),
(1028, 126, 0.4, FALSE),
(1029, 283, 2.8, TRUE),
(1030, 197, 1.6, FALSE),
(1031, 314, 3.7, FALSE),
(1032, 152, 2.9, TRUE),
(1033, 261, 0.3, FALSE),
(1034, 186, 1.3, TRUE),
(1035, 337, 3.4, FALSE),
(1036, 221, 2.0, FALSE),
(1037, 308, 1.5, TRUE),
(1038, 179, 3.8, FALSE),
(1039, 295, 0.2, TRUE),
(1040, 132, 2.7, FALSE);

INSERT INTO Nutrition_Tracking (client_id, protein, fat, fiber, sodium, vitamins, calories, carbs) VALUES
(1, 170.03, 66.62, 11.31, 1967.95, 137.14, 1593, 122.1),
(2, 104.34, 23.49, 24.17, 2448.23, 104.72, 1917, 345.58),
(3, 81.09, 60.12, 6.32, 2042.2, 103.67, 1890, 141.35),
(4, 193.32, 73.02, 19.56, 2963.24, 105.24, 1822, 283.47),
(5, 80.21, 70.32, 15.81, 2218.55, 74.02, 2021, 181.25),
(6, 74.88, 72.39, 16.94, 2541.82, 101.93, 2071, 380.89),
(7, 64.33, 20.83, 11.26, 1183.25, 142.17, 2934, 153.39),
(8, 64.72, 78.01, 16.77, 1270.61, 74.91, 1837, 203.5),
(9, 74.03, 56.31, 11.02, 1089.48, 78.76, 1778, 203.12),
(10, 60.13, 58.15, 13.25, 1264.48, 123.31, 2428, 163.6),
(11, 53.13, 45.21, 17.87, 2432.25, 67.25, 2109, 154.5),
(12, 72.47, 48.14, 23.85, 1709.51, 114.63, 1794, 339.93),
(13, 130.67, 90.28, 22.68, 1071.46, 148.2, 2389, 261.09),
(14, 90.8, 62.78, 11.93, 1179.1, 76.44, 2108, 289.29),
(15, 88.78, 77.67, 14.01, 1942.52, 113.75, 2539, 300.95),
(16, 110.21, 46.44, 15.33, 2890.34, 142.08, 2774, 369.82),
(17, 164.25, 45.73, 16.54, 1331.03, 139.38, 2998, 312.37),
(18, 159.89, 79.19, 18.99, 2879.69, 131.97, 2817, 387.49),
(19, 97.52, 25.98, 14.5, 2420.92, 66.36, 1592, 172.93),
(20, 83.69, 24.72, 17.15, 2311.79, 134.63, 1652, 149.15),
(21, 61.26, 70.73, 16.94, 1027.22, 96.58, 2481, 393.23),
(22, 65.09, 39.97, 6.14, 1588.98, 147.6, 1945, 159.78),
(23, 173.8, 77.55, 7.61, 2075.28, 100.64, 2352, 289.87),
(24, 152.35, 94.22, 19.78, 2225.39, 119.44, 2485, 372.23),
(25, 195.36, 72.6, 13.79, 2825.29, 100.01, 2237, 252.55),
(26, 57.44, 20.84, 20.38, 2623.89, 81.45, 1733, 264.36),
(27, 135.01, 92.83, 6.89, 2623.13, 122.39, 2692, 349.04),
(28, 50.19, 64.68, 6.29, 1651.45, 56.63, 1532, 149.75),
(29, 167.85, 75.14, 12.23, 1749.96, 71.83, 2188, 120.48),
(30, 109.04, 98.45, 18.55, 2806.9, 113.03, 2943, 368.46),
(31, 177.56, 56.81, 13.56, 2782.72, 117.77, 2932, 322.22),
(32, 167.33, 43.44, 11.71, 1321.28, 78.89, 2870, 316.27),
(33, 94.62, 27.25, 23.84, 2054.71, 107.62, 2141, 222.66),
(34, 53.55, 57.82, 11.56, 2227.98, 119.04, 2212, 141.75),
(35, 188.33, 81.88, 17.7, 2772.88, 77.32, 1727, 298.7),
(36, 55.25, 60.9, 15.04, 1679.52, 144.55, 1828, 170.61),
(37, 188.05, 23.59, 22.55, 2321.64, 83.12, 2564, 368.37),
(38, 187.91, 40.38, 7.41, 2358.22, 142.63, 2815, 286.42),
(39, 158.97, 89.22, 21.2, 1650.37, 128.77, 1788, 227.32),
(40, 162.84, 74.85, 12.75, 2440.17, 65.83, 1972, 132.18);

INSERT INTO Health_Advisor (advisor_id, experience_years, client_id) VALUES 
(1, 7, 1),
(2, 11, 2),
(3, 10, 3),
(4, 7, 4),
(5, 3, 5),
(6, 9, 6),
(7, 13, 7),
(8, 2, 8),
(9, 4, 9),
(10, 17, 10),
(11, 15, 11),
(12, 13, 12),
(13, 13, 13),
(14, 13, 14),
(15, 7, 15),
(16, 17, 16),
(17, 11, 17),
(18, 18, 18),
(19, 1, 19),
(20, 6, 20),
(21, 13, 21),
(22, 8, 22),
(23, 11, 23),
(24, 19, 24),
(25, 2, 25),
(26, 8, 26),
(27, 9, 27),
(28, 18, 28),
(29, 13, 29),
(30, 8, 30),
(31, 18, 31),
(32, 6, 32),
(33, 17, 33),
(34, 8, 34),
(35, 7, 35),
(36, 15, 36),
(37, 20, 37),
(38, 19, 38),
(39, 8, 39),
(40, 14, 40);

INSERT INTO Client_Health_Advisor (client_id, advisor_id) VALUES
(35, 31), (5, 22), (38, 10), (20, 23), (30, 26), (36, 25), (19, 21), (16, 31),
(27, 40), (21, 6), (29, 10), (2, 23), (13, 1), (15, 1), (33, 38), (5, 16),
(34, 8), (30, 27), (22, 14), (40, 15), (27, 25), (38, 30), (35, 10), (23, 3),
(4, 8), (29, 8), (16, 6), (23, 1), (23, 40), (18, 29), (2, 7), (31, 32),
(1, 36), (17, 31), (28, 39), (26, 38), (16, 2), (4, 22), (11, 34), (8, 7),
(16, 32), (28, 25), (22, 3), (11, 27), (18, 10), (31, 20), (15, 31), (16, 30),
(39, 15), (14, 40), (33, 7), (22, 4), (18, 36), (5, 8), (40, 1), (39, 17),
(9, 10), (12, 22), (23, 19), (39, 28), (36, 38), (4, 17), (16, 10), (8, 15),
(33, 17), (2, 33), (10, 10), (16, 14), (22, 1), (39, 40), (5, 40), (28, 17),
(16, 11), (14, 12), (23, 37), (14, 26), (35, 2), (8, 25), (4, 9), (29, 9),
(13, 19), (6, 24), (25, 8), (35, 29), (13, 13), (29, 39), (21, 26), (31, 38),
(36, 7), (27, 20), (26, 35), (26, 13), (12, 5), (31, 9), (2, 34), (11, 26),
(19, 19), (19, 7), (29, 22), (3, 4), (13, 38), (9, 26), (4, 31), (1, 8),
(2, 10), (18, 17), (33, 12), (21, 24), (23, 39), (28, 24), (23, 12), (27, 32),
(40, 33), (26, 10), (1, 14), (17, 28), (22, 22), (14, 38), (32, 16), (5, 38),
(5, 7), (40, 17), (23, 16), (29, 35), (2, 14);

INSERT INTO Client_Workout (client_id, workout_id) VALUES
(31, 17), (22, 16), (2, 11), (2, 3), (22, 31), (35, 20), (21, 2), (16, 37),
(21, 33), (21, 34), (23, 40), (13, 37), (34, 25), (20, 26), (25, 13), (36, 18),
(19, 28), (3, 10), (29, 35), (16, 24), (6, 19), (24, 34), (23, 39), (18, 1),
(40, 9), (2, 10), (13, 1), (31, 33), (20, 12), (26, 35), (19, 26), (22, 15),
(3, 21), (30, 22), (21, 9), (27, 38), (11, 30), (8, 37), (38, 12), (9, 29),
(19, 16), (10, 5), (4, 22), (25, 5), (15, 4), (37, 13), (19, 37), (2, 13),
(34, 28), (5, 33), (32, 2), (24, 25), (1, 1), (39, 21), (31, 19), (12, 40),
(7, 3), (17, 33), (16, 39), (30, 26), (15, 25), (25, 21), (34, 30), (26, 7),
(4, 26), (34, 34), (30, 11), (21, 21), (12, 31), (6, 9), (9, 12), (5, 12),
(40, 6), (16, 10), (39, 31), (25, 34), (4, 38), (14, 5), (18, 39), (21, 22),
(2, 40), (31, 35), (33, 6), (38, 23), (20, 9), (35, 6), (32, 3), (26, 14),
(38, 25), (37, 5), (18, 22), (26, 2), (34, 27), (21, 27), (19, 25), (39, 3),
(19, 19), (12, 3), (19, 22), (24, 33), (12, 17), (5, 24), (9, 1), (17, 40),
(6, 2), (3, 39), (33, 26), (9, 14), (36, 3), (24, 28), (4, 8), (38, 40),
(14, 22), (7, 33), (28, 4), (39, 34), (27, 39), (29, 12), (1, 4), (37, 24),
(23, 37), (25, 36), (2, 9), (35, 33), (15, 13);

INSERT INTO Error_Log (client_id, log_id, message) VALUES
(17, 34, 'Barcode checksum mismatch'),
(15, 26, 'User input error'),
(6, 7, 'Barcode checksum mismatch'),
(10, 8, 'Scan returned empty result'),
(2, 6, 'User input error'),
(23, 17, 'Scan returned empty result'),
(18, 30, 'Access denied'),
(6, 17, 'Invalid format detected'),
(26, 40, 'Timeout during scan'),
(23, 5, 'Timeout during scan'),
(7, 22, 'Barcode checksum mismatch'),
(5, 14, 'Invalid format detected'),
(22, 34, 'Access denied'),
(9, 20, 'Database connection lost'),
(14, 26, 'Database connection lost'),
(29, 1, 'Scan returned empty result'),
(37, 9, 'User input error'),
(32, 20, 'Barcode checksum mismatch'),
(12, 36, 'Scan returned empty result'),
(14, 30, 'Invalid format detected'),
(32, 15, 'Database connection lost'),
(38, 13, 'Invalid format detected'),
(36, 29, 'Ingredient scan failed'),
(20, 6, 'Scan returned empty result'),
(3, 3, 'Expired ingredient scanned'),
(11, 13, 'User input error'),
(17, 28, 'Database connection lost'),
(5, 16, 'Ingredient scan failed'),
(30, 31, 'Scan returned empty result'),
(27, 32, 'User input error'),
(18, 5, 'Expired ingredient scanned'),
(18, 2, 'Ingredient scan failed'),
(12, 25, 'Database connection lost'),
(25, 17, 'Expired ingredient scanned'),
(39, 7, 'Unrecognized barcode'),
(13, 32, 'Database connection lost'),
(6, 3, 'User input error'),
(27, 9, 'Timeout during scan'),
(12, 40, 'Expired ingredient scanned'),
(36, 4, 'Expired ingredient scanned'),
(5, 12, 'Invalid format detected'),
(34, 14, 'Scan returned empty result'),
(27, 13, 'Invalid format detected'),
(30, 4, 'Barcode checksum mismatch'),
(35, 26, 'Barcode checksum mismatch'),
(3, 13, 'Timeout during scan'),
(25, 2, 'Scan returned empty result'),
(7, 3, 'Access denied'),
(31, 21, 'Ingredient scan failed'),
(21, 23, 'Invalid format detected'),
(32, 18, 'Expired ingredient scanned'),
(18, 16, 'Ingredient scan failed'),
(9, 35, 'Database connection lost'),
(19, 1, 'Database connection lost'),
(14, 5, 'Ingredient scan failed'),
(30, 7, 'Unrecognized barcode'),
(19, 21, 'Invalid format detected'),
(3, 22, 'Database connection lost'),
(7, 25, 'Ingredient scan failed'),
(8, 34, 'Barcode checksum mismatch');

INSERT INTO Fridge_Ingredient (fridge_id, ingredient_id, quantity, unit, is_expired) VALUES
(5, 4, 4.44, 'piece', TRUE),
(16, 28, 3.8, 'bag', TRUE),
(26, 3, 9.03, 'cup', FALSE),
(30, 11, 4.6, 'scoop', TRUE),
(21, 12, 3.17, 'whole', TRUE),
(35, 24, 7.01, 'pound', TRUE),
(16, 37, 6.9, 'oz', TRUE),
(22, 8, 4.99, 'scoop', FALSE),
(2, 38, 7.95, 'pound', TRUE),
(8, 30, 5.12, 'whole', TRUE),
(29, 34, 9.02, 'piece', FALSE),
(5, 37, 5.63, 'oz', FALSE),
(13, 4, 7.31, 'bag', TRUE),
(33, 36, 4.0, 'cup', FALSE),
(1, 40, 7.93, 'cup', FALSE),
(12, 3, 3.66, 'oz', TRUE),
(30, 38, 4.64, 'cup', TRUE),
(1, 32, 9.04, 'oz', TRUE),
(11, 14, 7.66, 'gallon', TRUE),
(20, 9, 3.08, 'piece', TRUE),
(2, 3, 6.51, 'oz', FALSE),
(16, 30, 5.0, 'cup', TRUE),
(33, 22, 3.88, 'whole', TRUE),
(22, 3, 5.99, 'gallon', FALSE),
(2, 33, 4.81, 'oz', FALSE),
(31, 4, 3.17, 'pound', FALSE),
(1, 6, 2.26, 'pound', TRUE),
(14, 1, 8.02, 'cup', FALSE),
(18, 11, 6.44, 'whole', TRUE),
(37, 5, 2.68, 'cup', TRUE),
(30, 15, 3.11, 'pound', TRUE),
(6, 30, 9.85, 'gallon', FALSE),
(33, 27, 1.24, 'pound', FALSE),
(30, 24, 8.55, 'pound', FALSE),
(11, 40, 1.53, 'piece', TRUE),
(33, 26, 6.2, 'whole', TRUE),
(24, 21, 7.99, 'whole', TRUE),
(35, 6, 7.64, 'gallon', TRUE),
(8, 35, 0.57, 'pound', FALSE),
(2, 31, 6.96, 'scoop', TRUE),
(14, 6, 5.02, 'scoop', FALSE),
(27, 22, 3.6, 'cup', TRUE),
(32, 9, 2.14, 'cup', FALSE),
(1, 39, 6.07, 'oz', FALSE),
(20, 23, 7.67, 'cup', FALSE),
(11, 23, 4.83, 'gallon', FALSE),
(10, 1, 9.48, 'piece', FALSE),
(1, 38, 0.94, 'oz', TRUE),
(6, 5, 6.46, 'piece', FALSE),
(13, 3, 8.74, 'gallon', FALSE),
(18, 8, 8.44, 'pound', TRUE),
(24, 28, 3.89, 'scoop', FALSE),
(36, 8, 3.38, 'piece', TRUE),
(33, 19, 5.37, 'whole', TRUE),
(21, 14, 4.04, 'piece', FALSE),
(10, 22, 2.65, 'cup', FALSE),
(27, 27, 7.85, 'bag', TRUE),
(20, 10, 4.62, 'gallon', FALSE),
(27, 36, 9.83, 'gallon', TRUE),
(26, 28, 7.91, 'oz', FALSE),
(1, 10, 8.8, 'gallon', FALSE),
(8, 25, 0.51, 'pound', FALSE),
(5, 6, 1.85, 'piece', TRUE),
(35, 25, 0.94, 'scoop', TRUE),
(37, 2, 2.02, 'cup', TRUE),
(25, 13, 0.8, 'whole', TRUE),
(40, 1, 8.85, 'whole', TRUE),
(27, 35, 5.76, 'cup', TRUE),
(29, 24, 4.38, 'whole', FALSE),
(10, 33, 7.58, 'bag', TRUE),
(32, 19, 7.51, 'pound', TRUE),
(22, 14, 9.25, 'cup', TRUE),
(34, 5, 6.9, 'piece', TRUE),
(20, 28, 2.02, 'gallon', FALSE),
(3, 16, 6.94, 'piece', TRUE),
(35, 13, 7.36, 'gallon', FALSE),
(3, 9, 9.21, 'bag', FALSE),
(13, 40, 5.75, 'bag', FALSE),
(19, 10, 3.12, 'pound', TRUE),
(37, 32, 5.62, 'pound', TRUE),
(32, 1, 7.12, 'piece', TRUE),
(25, 26, 5.0, 'cup', FALSE),
(2, 9, 3.86, 'gallon', FALSE),
(5, 28, 8.73, 'bag', TRUE),
(15, 11, 0.7, 'scoop', FALSE),
(15, 2, 6.37, 'scoop', FALSE),
(39, 39, 6.23, 'whole', FALSE),
(12, 13, 6.15, 'piece', FALSE),
(37, 37, 7.95, 'cup', TRUE),
(5, 33, 6.76, 'gallon', TRUE),
(33, 14, 8.69, 'pound', TRUE),
(10, 18, 5.98, 'oz', TRUE),
(39, 29, 4.89, 'gallon', TRUE),
(32, 18, 6.41, 'bag', FALSE),
(14, 32, 7.1, 'gallon', TRUE),
(22, 34, 5.84, 'cup', TRUE),
(33, 33, 0.93, 'scoop', TRUE),
(32, 16, 7.15, 'cup', TRUE),
(9, 4, 2.44, 'scoop', TRUE),
(12, 37, 7.24, 'whole', TRUE),
(21, 34, 9.97, 'whole', TRUE),
(22, 36, 2.97, 'cup', TRUE),
(18, 12, 9.08, 'cup', TRUE),
(38, 35, 9.89, 'piece', FALSE),
(23, 38, 4.12, 'piece', TRUE),
(5, 10, 9.16, 'pound', TRUE),
(39, 2, 8.67, 'pound', FALSE),
(3, 2, 1.71, 'piece', TRUE),
(3, 19, 9.78, 'whole', TRUE),
(2, 12, 5.03, 'pound', TRUE),
(18, 25, 3.42, 'pound', FALSE),
(33, 20, 9.21, 'oz', TRUE),
(23, 23, 9.52, 'whole', TRUE),
(4, 32, 4.74, 'whole', FALSE),
(4, 11, 1.36, 'piece', FALSE),
(16, 31, 9.42, 'cup', FALSE),
(34, 38, 8.38, 'piece', TRUE),
(21, 29, 2.78, 'gallon', FALSE),
(36, 34, 0.88, 'bag', FALSE),
(10, 20, 7.58, 'bag', FALSE),
(35, 17, 0.94, 'oz', TRUE),
(16, 38, 7.76, 'oz', FALSE),
(3, 37, 4.07, 'gallon', TRUE),
(40, 15, 0.67, 'scoop', FALSE),
(31, 21, 8.22, 'gallon', FALSE);

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