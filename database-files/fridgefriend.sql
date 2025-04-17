
-- Create database
DROP DATABASE IF EXISTS fridgefriend;
CREATE DATABASE fridgefriend;
USE fridgefriend;


-- First, create all tables
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


CREATE TABLE Fridge_Inventory (
  fridge_id INT AUTO_INCREMENT PRIMARY KEY
);


CREATE TABLE Shopping_List (
  list_id INT AUTO_INCREMENT PRIMARY KEY
);


CREATE TABLE Food_Scan_Log (
  log_id INT AUTO_INCREMENT PRIMARY KEY,
  ingredient_id INT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  status VARCHAR(50),
  FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id)
);


CREATE TABLE Brand (
  brand_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  is_trusted BOOLEAN DEFAULT TRUE
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


CREATE TABLE Health_Advisor (
  advisor_id INT AUTO_INCREMENT PRIMARY KEY,
  experience_years INT,
  user_id INT,
  FOREIGN KEY (user_id) REFERENCES User(user_id)
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


CREATE TABLE Ingredient_Macronutrient (
  ingredient_id INT,
  macro_id INT,
  PRIMARY KEY (ingredient_id, macro_id),
  FOREIGN KEY (ingredient_id) REFERENCES Ingredient(ingredient_id),
  FOREIGN KEY (macro_id) REFERENCES Macronutrients(macro_id)
);


CREATE TABLE Recipe_Brand (
  recipe_id INT,
  brand_id INT,
  PRIMARY KEY (recipe_id, brand_id),
  FOREIGN KEY (recipe_id) REFERENCES Recipe(recipe_id),
  FOREIGN KEY (brand_id) REFERENCES Brand(brand_id)
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


-- Now start inserting data in the correct order
-- First, insert into independent tables (no foreign key dependencies)


-- 1. Insert User data (40 rows - strong entity)
INSERT INTO User (f_name, l_name, username, password, email) VALUES
-- Clients (1-15)
('Busy', 'Ben', 'busyben', 'g6ASy6N4(2', 'busy.ben@example.com'),
('Nicholas', 'Miller', 'nicholas928', 't4DSCGrg)I', 'nicholas.miller@example.com'),
('George', 'Hall', 'george636', '(lHN^3AyN1', 'george.hall@example.com'),
('Kelly', 'Thomas', 'kelly742', '_d31KO@p+!', 'kelly.thomas@example.com'),
('Olivia', 'Hernandez', 'olivia693', '5a2FykmV*H', 'olivia.hernandez@example.com'),
('James', 'Porter', 'james817', '(9zKCkpvfp', 'james.porter@example.com'),
('Donald', 'Alvarez', 'donald903', 'XbY&0Jqm_5', 'donald.alvarez@example.com'),
('Steve', 'Barnes', 'steve492', '_R8HNVlE34', 'steve.barnes@example.com'),
('Timothy', 'Cowan', 'timothy874', 'EP6Mup0_M!', 'timothy.cowan@example.com'),
('Emily', 'Grimes', 'emily866', 'I^k18H4vLk', 'emily.grimes@example.com'),
('Sarah', 'Johnson', 'sarah123', 'P@ssw0rd123', 'sarah.johnson@example.com'),
('Michael', 'Williams', 'mike456', 'Secur3P@ss', 'michael.williams@example.com'),
('Jennifer', 'Brown', 'jenbrown', 'Br0wnJ3n!', 'jennifer.brown@example.com'),
('David', 'Jones', 'davejones', 'J0n3sD@v3', 'david.jones@example.com'),
('Lisa', 'Garcia', 'lisag', 'G@rc1@L1sa', 'lisa.garcia@example.com'),
-- Admins (16-25)
('Alvin', 'Admin', 'alvinadmin', 'cD_#2Aem!k', 'alvin.admin@example.com'),
('Olivia', 'Johnson', 'olivia366', 'E)3sK&n6@y', 'olivia.johnson@example.com'),
('Isaac', 'Hurley', 'isaac147', 'T1VmsQ69@)', 'isaac.hurley@example.com'),
('Aaron', 'Adams', 'aaron126', '+LVC35rzn2', 'aaron.adams@example.com'),
('Kendra', 'Jefferson', 'kendra510', 'zp#nzeNe%8', 'kendra.jefferson@example.com'),
('Michelle', 'Armstrong', 'michelle561', '_9zEUw9BT2', 'michelle.armstrong@example.com'),
('Courtney', 'Jones', 'courtney264', '5*^v5UirjQ', 'courtney.jones@example.com'),
('Steven', 'Murphy', 'steven560', 'Qi(3eSm3X0', 'steven.murphy@example.com'),
('Michael', 'Burns', 'michael737', '5@xY3k!j%*', 'michael.burns@example.com'),
('Caleb', 'Blankenship', 'caleb199', '+M*9Cu)P2q', 'caleb.blankenship@example.com'),
-- Health Advisors (26-40)
('Riley', 'Runner', 'rileyrunner', 'm1_i5MtD(7', 'riley.runner@example.com'),
('Nancy', 'Nutritionist', 'nancynutri', 'Z17GtsiGM&', 'nancy.nutritionist@example.com'),
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


-- New Admin Users (41-80)
('Amanda', 'Gordon', 'amandagordon', 'P@ssw0rd51', 'amanda.gordon@example.com'),
('Brian', 'Hughes', 'brianhughes', 'P@ssw0rd52', 'brian.hughes@example.com'),
('Carly', 'Ingram', 'carlyingram', 'P@ssw0rd53', 'carly.ingram@example.com'),
('Derek', 'Johnson', 'derekj', 'P@ssw0rd54', 'derek.johnson@example.com'),
('Emma', 'Kennedy', 'emmak', 'P@ssw0rd55', 'emma.kennedy@example.com'),
('Frank', 'Lewis', 'frankl', 'P@ssw0rd56', 'frank.lewis@example.com'),
('Grace', 'Mitchell', 'gracem', 'P@ssw0rd57', 'grace.mitchell@example.com'),
('Henry', 'Norton', 'henryn', 'P@ssw0rd58', 'henry.norton@example.com'),
('Irene', 'Oliver', 'ireneo', 'P@ssw0rd59', 'irene.oliver@example.com'),
('Jack', 'Parker', 'jackp', 'P@ssw0rd60', 'jack.parker@example.com'),
('Karen', 'Quinn', 'karenq', 'P@ssw0rd61', 'karen.quinn@example.com'),
('Lance', 'Roberts', 'lancer', 'P@ssw0rd62', 'lance.roberts@example.com'),
('Megan', 'Smith', 'megans', 'P@ssw0rd63', 'megan.smith@example.com'),
('Nathan', 'Thomas', 'nathant', 'P@ssw0rd64', 'nathan.thomas@example.com'),
('Olivia', 'Underwood', 'oliviau', 'P@ssw0rd65', 'olivia.underwood@example.com'),
('Peter', 'Vincent', 'peterv', 'P@ssw0rd66', 'peter.vincent@example.com'),
('Quinn', 'Williams', 'quinnw', 'P@ssw0rd67', 'quinn.williams@example.com'),
('Rachel', 'Xavier', 'rachelx', 'P@ssw0rd68', 'rachel.xavier@example.com'),
('Scott', 'Young', 'scotty', 'P@ssw0rd69', 'scott.young@example.com'),
('Tina', 'Zhang', 'tinaz', 'P@ssw0rd70', 'tina.zhang@example.com'),
('Ulysses', 'Adams', 'uadams', 'P@ssw0rd71', 'ulysses.adams@example.com'),
('Victoria', 'Bell', 'vbell', 'P@ssw0rd72', 'victoria.bell@example.com'),
('William', 'Cortez', 'wcortez', 'P@ssw0rd73', 'william.cortez@example.com'),
('Xander', 'Diaz', 'xdiaz', 'P@ssw0rd74', 'xander.diaz@example.com'),
('Yasmine', 'Evans', 'yevans', 'P@ssw0rd75', 'yasmine.evans@example.com'),
('Zachary', 'Fisher', 'zfisher', 'P@ssw0rd76', 'zachary.fisher@example.com'),
('Anna', 'Garcia', 'agarcia', 'P@ssw0rd77', 'anna.garcia@example.com'),
('Benjamin', 'Harris', 'bharris', 'P@ssw0rd78', 'benjamin.harris@example.com'),
('Catherine', 'Ingles', 'cingles', 'P@ssw0rd79', 'catherine.ingles@example.com'),
('Daniel', 'Johnson', 'djohnson', 'P@ssw0rd80', 'daniel.johnson@example.com'),
('Eleanor', 'Kim', 'ekim', 'P@ssw0rd81', 'eleanor.kim@example.com'),
('Francisco', 'Lee', 'flee', 'P@ssw0rd82', 'francisco.lee@example.com'),
('Gabriela', 'Martinez', 'gmartinez', 'P@ssw0rd83', 'gabriela.martinez@example.com'),
('Hector', 'Nelson', 'hnelson', 'P@ssw0rd84', 'hector.nelson@example.com'),
('Isabel', 'Ortiz', 'iortiz', 'P@ssw0rd85', 'isabel.ortiz@example.com'),
('Jonathan', 'Perry', 'jperry', 'P@ssw0rd86', 'jonathan.perry@example.com'),
('Kimberly', 'Quinn', 'kquinn', 'P@ssw0rd87', 'kimberly.quinn@example.com'),
('Lucas', 'Rodriguez', 'lrodriguez', 'P@ssw0rd88', 'lucas.rodriguez@example.com'),
('Maria', 'Stevens', 'mstevens', 'P@ssw0rd89', 'maria.stevens@example.com'),
('Nicholas', 'Thompson', 'nthompson', 'P@ssw0rd90', 'nicholas.thompson@example.com'),


-- New Health Advisor Users (81-95)
('Olivia', 'Udell', 'oudell', 'P@ssw0rd91', 'olivia.udell@example.com'),
('Patrick', 'Vasquez', 'pvasquez', 'P@ssw0rd92', 'patrick.vasquez@example.com'),
('Quincy', 'Wong', 'qwong', 'P@ssw0rd93', 'quincy.wong@example.com'),
('Rebecca', 'Xu', 'rxu', 'P@ssw0rd94', 'rebecca.xu@example.com'),
('Samuel', 'Young', 'syoung', 'P@ssw0rd95', 'samuel.young@example.com'),
('Theresa', 'Zhang', 'tzhang', 'P@ssw0rd96', 'theresa.zhang@example.com'),
('Uri', 'Anderson', 'uanderson', 'P@ssw0rd97', 'uri.anderson@example.com'),
('Veronica', 'Baker', 'vbaker', 'P@ssw0rd98', 'veronica.baker@example.com'),
('Walter', 'Chang', 'wchang', 'P@ssw0rd99', 'walter.chang@example.com'),
('Xiomara', 'Davis', 'xdavis', 'P@ssw0rd100', 'xiomara.davis@example.com'),
('Yosef', 'Edwards', 'yedwards', 'P@ssw0rd101', 'yosef.edwards@example.com'),
('Zara', 'Franklin', 'zfranklin', 'P@ssw0rd102', 'zara.franklin@example.com'),
('Adam', 'Gordon', 'agordon', 'P@ssw0rd103', 'adam.gordon@example.com'),
('Brenda', 'Henderson', 'bhenderson', 'P@ssw0rd104', 'brenda.henderson@example.com'),
('Chris', 'Ingram', 'cingram', 'P@ssw0rd105', 'chris.ingram@example.com'),


-- New Client Users (96-115)
('Delia', 'Jackson', 'djackson', 'P@ssw0rd106', 'delia.jackson@example.com'),
('Efrain', 'Knight', 'eknight', 'P@ssw0rd107', 'efrain.knight@example.com'),
('Fiona', 'Lopez', 'flopez', 'P@ssw0rd108', 'fiona.lopez@example.com'),
('Gabriel', 'Mendoza', 'gmendoza', 'P@ssw0rd109', 'gabriel.mendoza@example.com'),
('Hannah', 'Nakamura', 'hnakamura', 'P@ssw0rd110', 'hannah.nakamura@example.com'),
('Ian', 'Oliveira', 'ioliveira', 'P@ssw0rd111', 'ian.oliveira@example.com'),
('Julie', 'Peterson', 'jpeterson', 'P@ssw0rd112', 'julie.peterson@example.com'),
('Kevin', 'Quinn', 'kquinn2', 'P@ssw0rd113', 'kevin.quinn@example.com'),
('Lena', 'Robinson', 'lrobinson', 'P@ssw0rd114', 'lena.robinson@example.com'),
('Marco', 'Sanchez', 'msanchez', 'P@ssw0rd115', 'marco.sanchez@example.com'),
('Nina', 'Turner', 'nturner', 'P@ssw0rd116', 'nina.turner@example.com'),
('Oscar', 'Unger', 'ounger', 'P@ssw0rd117', 'oscar.unger@example.com'),
('Penelope', 'Vasquez', 'pvasquez2', 'P@ssw0rd118', 'penelope.vasquez@example.com'),
('Quentin', 'Washington', 'qwashington', 'P@ssw0rd119', 'quentin.washington@example.com'),
('Rosa', 'Xiong', 'rxiong', 'P@ssw0rd120', 'rosa.xiong@example.com'),
('Stefan', 'Yamamoto', 'syamamoto', 'P@ssw0rd121', 'stefan.yamamoto@example.com'),
('Talia', 'Zimmerman', 'tzimmerman', 'P@ssw0rd122', 'talia.zimmerman@example.com'),
('Ulrich', 'Abbott', 'uabbott', 'P@ssw0rd123', 'ulrich.abbott@example.com'),
('Valerie', 'Blackwell', 'vblackwell', 'P@ssw0rd124', 'valerie.blackwell@example.com'),
('Wesley', 'Carter', 'wcarter', 'P@ssw0rd125', 'wesley.carter@example.com'),

('Alexis', 'Dawson', 'adawson', 'P@ssw0rd126', 'alexis.dawson@example.com'),
('Brandon', 'Elliott', 'belliott', 'P@ssw0rd127', 'brandon.elliott@example.com'),
('Cassandra', 'Freeman', 'cfreeman', 'P@ssw0rd128', 'cassandra.freeman@example.com'),
('Dominic', 'Grant', 'dgrant', 'P@ssw0rd129', 'dominic.grant@example.com'),
('Elizabeth', 'Harmon', 'eharmon', 'P@ssw0rd130', 'elizabeth.harmon@example.com'),
('Felix', 'Irving', 'firving', 'P@ssw0rd131', 'felix.irving@example.com'),
('Gabrielle', 'Jimenez', 'gjimenez', 'P@ssw0rd132', 'gabrielle.jimenez@example.com'),
('Harrison', 'Kelly', 'hkelly', 'P@ssw0rd133', 'harrison.kelly@example.com'),
('Isabella', 'Lawson', 'ilawson', 'P@ssw0rd134', 'isabella.lawson@example.com'),
('Jasper', 'Mitchell', 'jmitchell', 'P@ssw0rd135', 'jasper.mitchell@example.com'),
('Kiara', 'Newman', 'knewman', 'P@ssw0rd136', 'kiara.newman@example.com'),
('Landon', 'Osborn', 'losborn', 'P@ssw0rd137', 'landon.osborn@example.com'),
('Mia', 'Peterson', 'mpeterson', 'P@ssw0rd138', 'mia.peterson@example.com'),
('Noah', 'Quinn', 'nquinn', 'P@ssw0rd139', 'noah.quinn@example.com'),
('Olivia', 'Richards', 'orichards', 'P@ssw0rd140', 'olivia.richards@example.com'),
('Parker', 'Stone', 'pstone', 'P@ssw0rd141', 'parker.stone@example.com'),
('Quinn', 'Torres', 'qtorres', 'P@ssw0rd142', 'quinn.torres@example.com'),
('Riley', 'Underwood', 'runderwood', 'P@ssw0rd143', 'riley.underwood@example.com'),
('Sebastian', 'Vargas', 'svargas', 'P@ssw0rd144', 'sebastian.vargas@example.com'),
('Taylor', 'Wallace', 'twallace', 'P@ssw0rd145', 'taylor.wallace@example.com'),
('Uma', 'Xiong', 'uxiong', 'P@ssw0rd146', 'uma.xiong@example.com'),
('Vincent', 'Yates', 'vyates', 'P@ssw0rd147', 'vincent.yates@example.com'),
('Willow', 'Zhang', 'wzhang', 'P@ssw0rd148', 'willow.zhang@example.com'),
('Xavier', 'Anderson', 'xanderson', 'P@ssw0rd149', 'xavier.anderson@example.com'),
('Yasmine', 'Benson', 'ybenson', 'P@ssw0rd150', 'yasmine.benson@example.com');;


-- 2. Insert Personal_Constraints (35 rows - strong entity)
INSERT INTO Personal_Constraints (budget, dietary_restrictions, personal_diet, age_group) VALUES
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
(142.50, 'none', 'balanced', 'adult'),
(178.30, 'gluten,dairy', 'vegan', 'young adult'),
(165.20, 'peanuts', 'paleo', 'adult'),
(95.75, 'shellfish', 'mediterranean', 'senior'),
(210.45, 'none', 'keto', 'adult'),
(125.60, 'tree nuts', 'vegetarian', 'teen'),
(185.90, 'dairy', 'balanced', 'adult'),
(140.25, 'fish', 'pescatarian', 'child'),
(195.30, 'none', 'low-carb', 'adult'),
(110.85, 'soy,eggs', 'vegan', 'senior'),
(175.40, 'gluten', 'high-protein', 'young adult'),
(155.15, 'none', 'mediterranean', 'adult'),
(120.70, 'peanuts,tree nuts', 'keto', 'teen'),
(190.55, 'shellfish,fish', 'pescatarian', 'adult'),
(130.95, 'dairy', 'balanced', 'senior'),
(170.30, 'none', 'paleo', 'adult'),
(105.80, 'soy', 'vegetarian', 'child'),
(160.65, 'gluten', 'high-protein', 'teen'),
(135.10, 'none', 'balanced', 'adult'),
(180.75, 'dairy,eggs', 'vegan', 'senior'),
(155.25, 'none', 'balanced', 'adult'),
(172.40, 'gluten', 'mediterranean', 'young adult'),
(128.95, 'dairy', 'keto', 'teen'),
(162.50, 'shellfish', 'paleo', 'senior'),
(145.75, 'peanuts', 'vegetarian', 'adult'),
(193.20, 'tree nuts', 'high-protein', 'young adult'),
(118.40, 'soy', 'vegan', 'teen'),
(175.60, 'fish', 'pescatarian', 'adult'),
(132.85, 'none', 'low-carb', 'senior'),
(165.30, 'gluten,dairy', 'balanced', 'adult');


-- 3. Insert Workout data (35 rows - strong entity)
INSERT INTO Workout (name, quantity, weight, calories_burnt) VALUES
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
('Circuit Training', 40, NULL, 400);


-- 4. Insert Ingredient data (40 rows - strong entity)
INSERT INTO Ingredient (name, expiration_date) VALUES
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
('Garlic', '2025-08-15');


-- 5. Insert Recipe data (35 rows - strong entity)
INSERT INTO Recipe (name, instructions) VALUES
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
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20),
(21), (22), (23), (24), (25), (26), (27), (28), (29), (30),
(31), (32), (33), (34), (35), (36), (37), (38), (39), (40),
(41), (42), (43), (44), (45), (46), (47), (48), (49), (50);


-- 7. Insert Shopping_List data (30 rows)
INSERT INTO Shopping_List (list_id) VALUES
(1), (2), (3), (4), (5), (6), (7), (8), (9), (10),
(11), (12), (13), (14), (15), (16), (17), (18), (19), (20),
(21), (22), (23), (24), (25), (26), (27), (28), (29), (30),
(31), (32), (33), (34), (35), (36), (37), (38), (39), (40),
(41), (42), (43), (44), (45), (46), (47), (48), (49), (50);

-- 8. Insert Food_Scan_Log data (60 rows - weak entity)
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
(26, 'SUCCESS'),
(27, 'FAILED'),
(28, 'SUCCESS'),
(29, 'SUCCESS'),
(30, 'FAILED'),
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


-- 9. Insert Brand data (35 rows)
INSERT INTO Brand (name, is_trusted) VALUES
('Kirkland Signature', TRUE),
('365 Everyday Value', FALSE),
('Trader Joe''s', TRUE),
('Great Value', TRUE),
('Organic Valley', TRUE),
('Annie''s', FALSE),
('Amy''s', FALSE),
('Green Giant', FALSE),
('Horizon Organic', TRUE),
('Chobani', FALSE),
('Siggi''s', FALSE),
('Fage', TRUE),
('Tillamook', TRUE),
('Stonyfield', FALSE),
('Daiya', FALSE),
('Gardein', FALSE),
('MorningStar Farms', TRUE),
('Beyond Meat', TRUE),
('Impossible Foods', FALSE),
('Field Roast', FALSE),
('Applegate', TRUE),
('Boca', FALSE),
('Earth Balance', FALSE),
('Lightlife', TRUE),
('Nature''s Path', FALSE),
('Kind', TRUE),
('Clif Bar', TRUE),
('RXBAR', TRUE),
('LÄRABAR', TRUE),
('Nature Valley', TRUE),
('Quaker', FALSE),
('Bob''s Red Mill', TRUE),
('Barilla', TRUE),
('Rao''s Homemade', TRUE),
('Prego', FALSE);


INSERT INTO Admin (user_id) VALUES
-- Original admin user_ids (16-25)
(16), (17), (18), (19), (20),
(21), (22), (23), (24), (25),
-- New admin user_ids (41-90)
(41), (42), (43), (44), (45),
(46), (47), (48), (49), (50),
(51), (52), (53), (54), (55),
(56), (57), (58), (59), (60),
(61), (62), (63), (64), (65),
(66), (67), (68), (69), (70),
(71), (72), (73), (74), (75),
(76), (77), (78), (79), (80),
(81), (82), (83), (84), (85),
(86), (87), (88), (89), (90);


-- 11. Insert Macronutrients data (40 rows)
INSERT INTO Macronutrients (ingredient_id, protein, fat, fiber, vitamin, sodium, calories, carbs) VALUES
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
(40, 10.42, 5.67, 5.1, 75.53, 116.18, 290, 47.29);


INSERT INTO Client (user_id, pc_id, fridge_id, list_id, log_id, flag) VALUES
-- Use user_ids 1-15 (original clients)
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
(11, 11, 11, 11, 11, 0),
(12, 12, 12, 12, 12, 1),
(13, 13, 13, 13, 13, 0),
(14, 14, 14, 14, 14, 1),
(15, 15, 15, 15, 15, 0),
-- Use user_ids 96-125 (new clients)
(96, 16, 16, 16, 16, 1),  -- Delia Jackson
(97, 17, 17, 17, 17, 0),  -- Efrain Knight
(98, 18, 18, 18, 18, 1),  -- Fiona Lopez
(99, 19, 19, 19, 19, 0),  -- Gabriel Mendoza
(100, 20, 20, 20, 20, 1), -- Hannah Nakamura
(101, 21, 21, 21, 21, 0), -- Ian Oliveira
(102, 22, 22, 22, 22, 1), -- Julie Peterson
(103, 23, 23, 23, 23, 0), -- Kevin Quinn
(104, 24, 24, 24, 24, 1), -- Lena Robinson
(105, 25, 25, 25, 25, 0), -- Marco Sanchez
(106, 26, 26, 26, 26, 1), -- Nina Turner
(107, 27, 27, 27, 27, 0), -- Oscar Unger
(108, 28, 28, 28, 28, 1), -- Penelope Vasquez
(109, 29, 29, 29, 29, 0), -- Quentin Washington
(110, 30, 30, 30, 30, 1), -- Rosa Xiong
(111, 31, 31, 31, 31, 0), -- Stefan Yamamoto
(112, 32, 32, 32, 32, 1), -- Talia Zimmerman
(113, 33, 33, 33, 33, 0), -- Ulrich Abbott
(114, 34, 34, 34, 34, 1), -- Valerie Blackwell
(115, 35, 35, 35, 35, 0),
-- Using 5 more user_ids from new client range (96-125) for remaining rows
(96, 46, 46, 46, 46, 1),
(97, 47, 47, 47, 47, 0),
(98, 48, 48, 48, 48, 1),
(99, 49, 49, 49, 49, 0),
(100, 50, 50, 50, 50, 1),
(116, 36, 36, 36, 36, 0),
(117, 37, 37, 37, 37, 1),
(118, 38, 38, 38, 38, 0),
(119, 39, 39, 39, 39, 1),
(120, 40, 40, 40, 40, 0),
(121, 41, 41, 41, 41, 1),
(122, 42, 42, 42, 42, 0),
(123, 43, 43, 43, 43, 1),
(124, 44, 44, 44, 44, 0),
(125, 45, 45, 45, 45, 1),
(126, 46, 46, 46, 46, 0),
(127, 47, 47, 47, 47, 1),
(128, 48, 48, 48, 48, 0),
(129, 49, 49, 49, 49, 1),
(130, 50, 50, 50, 50, 0),
(131, 51, 1, 1, 1, 1),  -- Reusing existing fridge/list/log IDs since they exist
(132, 52, 2, 2, 2, 0),
(133, 53, 3, 3, 3, 1),
(134, 54, 4, 4, 4, 0),
(135, 55, 5, 5, 5, 1),
(136, 56, 6, 6, 6, 0),
(137, 57, 7, 7, 7, 1),
(138, 58, 8, 8, 8, 0),
(139, 59, 9, 9, 9, 1),
(140, 60, 10, 10, 10, 0);


INSERT INTO Health_Advisor (experience_years, user_id) VALUES
-- Original health advisor user_ids (26-40)
(7, 26),  -- Riley Runner
(11, 27), -- Nancy Nutritionist
(10, 28),
(7, 29),
(3, 30),
(9, 31),
(13, 32),
(2, 33),
(4, 34),
(17, 35),
(5, 36),
(8, 37),
(12, 38),
(6, 39),
(9, 40),
-- New health advisor user_ids (81-95) - changed from 91-105 to avoid overlap with clients
(10, 81),
(8, 82),
(12, 83),
(7, 84),
(15, 85),
(6, 86),
(9, 87),
(11, 88),
(5, 89),
(13, 90),
(4, 91),
(16, 92),
(8, 93),
(14, 94),
(9, 95);


-- Now with those dependencies established, we can insert data into the relationship tables


-- 14. Insert Recipe_Ingredient data (75 rows - weak entity)
INSERT INTO Recipe_Ingredient (recipe_id, ingredient_id, quantity, unit) VALUES
-- Recipe 1 ingredients (Event Stew)
(1, 1, 1.5, 'pound'),   -- Chicken Breast
(1, 5, 2.0, 'cup'),     -- Lentils
(1, 6, 3.0, 'whole'),   -- Broccoli
(1, 7, 2.0, 'whole'),   -- Sweet Potato
(1, 26, 2.0, 'tbsp'),   -- Olive Oil
(1, 40, 3.0, 'clove'),  -- Garlic for Event Stew


-- Recipe 2 ingredients (Rest Bowl)
(2, 3, 1.0, 'cup'),     -- Quinoa
(2, 19, 1.0, 'whole'),  -- Avocado
(2, 20, 2.0, 'cup'),    -- Spinach
(2, 16, 0.5, 'whole'),  -- Cucumber
(2, 28, 2.0, 'whole'),  -- Tomatoes
(2, 26, 1.0, 'tbsp'),   -- Olive Oil for Rest Bowl


-- Recipe 3 ingredients (Wide Bowl)
(3, 4, 1.5, 'cup'),     -- Brown Rice
(3, 21, 8.0, 'oz'),     -- Tofu
(3, 29, 1.0, 'cup'),    -- Carrots
(3, 17, 1.0, 'whole'),  -- Bell Pepper
(3, 30, 2.0, 'cup'),    -- Kale
(3, 26, 2.0, 'tbsp'),   -- Olive Oil for Wide Bowl


-- Recipe 4 ingredients (Glass Wrap)
(4, 38, 2.0, 'slice'),  -- Whole Wheat Bread
(4, 2, 0.25, 'pound'),  -- Ground Beef
(4, 10, 2.0, 'slice'),  -- Cheddar Cheese
(4, 28, 2.0, 'slice'),  -- Tomatoes
(4, 20, 0.5, 'cup'),    -- Spinach


-- Recipe 5 ingredients (That Skillet)
(5, 2, 1.0, 'pound'),   -- Ground Beef
(5, 40, 2.0, 'clove'),  -- Garlic
(5, 10, 0.5, 'cup'),    -- Cheddar Cheese
(5, 29, 1.0, 'cup'),    -- Carrots
(5, 17, 1.0, 'whole'),  -- Bell Pepper


-- Recipe 6 ingredients (Every Salad)
(6, 20, 4.0, 'cup'),    -- Spinach
(6, 19, 1.0, 'whole'),  -- Avocado
(6, 28, 1.0, 'cup'),    -- Tomatoes
(6, 16, 1.0, 'whole'),  -- Cucumber
(6, 12, 0.25, 'cup'),   -- Almonds
(6, 26, 2.0, 'tbsp'),   -- Olive Oil for Every Salad


-- Recipe 7 ingredients (Too Wrap)
(7, 38, 2.0, 'slice'),  -- Whole Wheat Bread
(7, 37, 2.0, 'tbsp'),   -- Peanut Butter
(7, 25, 1.0, 'whole'),  -- Banana
(7, 15, 1.0, 'tbsp'),   -- Honey
(7, 36, 1.0, 'tsp'),    -- Chia Seeds


-- Recipe 8 ingredients (Never Skillet)
(8, 1, 1.0, 'pound'),   -- Chicken Breast
(8, 17, 2.0, 'whole'),  -- Bell Pepper
(8, 40, 3.0, 'clove'),  -- Garlic
(8, 26, 2.0, 'tbsp'),   -- Olive Oil
(8, 4, 1.0, 'cup'),     -- Brown Rice


-- Recipe 9 ingredients (Line Bowl)
(9, 4, 1.0, 'cup'),     -- Brown Rice
(9, 22, 1.0, 'cup'),    -- Black Beans
(9, 19, 1.0, 'whole'),  -- Avocado
(9, 17, 1.0, 'whole'),  -- Bell Pepper
(9, 28, 0.5, 'cup'),    -- Tomatoes
(9, 31, 0.5, 'pound'),  -- Shrimp for Line Bowl
(9, 40, 2.0, 'clove'),  -- Garlic for Line Bowl


-- Recipe 10 ingredients (Already Wrap)
(10, 38, 2.0, 'slice'), -- Whole Wheat Bread
(10, 31, 4.0, 'oz'),    -- Shrimp
(10, 20, 1.0, 'cup'),   -- Spinach
(10, 28, 2.0, 'slice'), -- Tomatoes
(10, 19, 0.5, 'whole'), -- Avocado
(10, 9, 2.0, 'tbsp'),   -- Milk for Already Wrap
(10, 26, 1.0, 'tbsp'),  -- Olive Oil for Already Wrap


-- Recipe 11 ingredients (Quinoa Power Bowl)
(11, 3, 1.0, 'cup'),    -- Quinoa
(11, 6, 1.0, 'cup'),    -- Broccoli
(11, 7, 1.0, 'whole'),  -- Sweet Potato
(11, 19, 1.0, 'whole'), -- Avocado
(11, 12, 2.0, 'tbsp');  -- Almonds


-- 15. Insert Ingredient_Macronutrient data (125+ rows - bridge table)
-- Add in smaller batches with separate INSERT statements to avoid constraint errors
INSERT INTO Ingredient_Macronutrient (ingredient_id, macro_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
(6, 6), (7, 7), (8, 8), (9, 9), (10, 10),
(11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 20),
(21, 21), (22, 22), (23, 23), (24, 24), (25, 25),
(26, 26), (27, 27), (28, 28), (29, 29), (30, 30),
(31, 31), (32, 32), (33, 33), (34, 34), (35, 35),
(36, 36), (37, 37), (38, 38), (39, 39), (40, 40);


-- Add 40 more rows (total now 80)
INSERT INTO Ingredient_Macronutrient (ingredient_id, macro_id) VALUES
(1, 2), (1, 3), (2, 3), (2, 4), (3, 4),
(3, 5), (4, 5), (4, 6), (5, 6), (5, 7),
(6, 7), (6, 8), (7, 8), (7, 9), (8, 9),
(8, 10), (9, 10), (9, 11), (10, 11), (10, 12),
(11, 12), (11, 13), (12, 13), (12, 14), (13, 14),
(13, 15), (14, 15), (14, 16), (15, 16), (15, 17),
(16, 17), (16, 18), (17, 18), (17, 19), (18, 19),
(18, 20), (19, 20), (19, 21), (20, 21), (20, 22);


-- Add 45 more rows (total now 125+)
INSERT INTO Ingredient_Macronutrient (ingredient_id, macro_id) VALUES
(21, 22), (21, 23), (22, 23), (22, 24), (23, 24),
(23, 25), (24, 25), (24, 26), (25, 26), (25, 27),
(26, 27), (26, 28), (27, 28), (27, 29), (28, 29),
(28, 30), (29, 30), (29, 31), (30, 31), (30, 32),
(31, 32), (31, 33), (32, 33), (32, 34), (33, 34),
(33, 35), (34, 35), (34, 36), (35, 36), (35, 37),
(36, 37), (36, 38), (37, 38), (37, 39), (38, 39),
(38, 40), (39, 40), (39, 1), (40, 1), (40, 2),
(1, 10), (2, 11), (3, 12), (4, 13), (5, 14);


-- 16. Insert Recipe_Brand data (125+ rows - bridge table)
-- First batch of 75 rows
INSERT INTO Recipe_Brand (recipe_id, brand_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
(4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
(5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
(6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
(7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
(8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
(9, 6), (9, 7), (9, 8), (9, 9), (9, 10),
(10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
(11, 11), (11, 12), (11, 13), (11, 14), (11, 15),
(12, 11), (12, 12), (12, 13), (12, 14), (12, 15),
(13, 11), (13, 12), (13, 13), (13, 14), (13, 15),
(14, 11), (14, 12), (14, 13), (14, 14), (14, 15),
(15, 11), (15, 12), (15, 13), (15, 14), (15, 15);


-- Second batch to reach 125+ rows
INSERT INTO Recipe_Brand (recipe_id, brand_id) VALUES
(16, 16), (16, 17), (16, 18), (16, 19), (16, 20),
(17, 16), (17, 17), (17, 18), (17, 19), (17, 20),
(18, 16), (18, 17), (18, 18), (18, 19), (18, 20),
(19, 16), (19, 17), (19, 18), (19, 19), (19, 20),
(20, 16), (20, 17), (20, 18), (20, 19), (20, 20),
(21, 21), (21, 22), (21, 23), (21, 24), (21, 25),
(22, 21), (22, 22), (22, 23), (22, 24), (22, 25),
(23, 21), (23, 22), (23, 23), (23, 24), (23, 25),
(24, 21), (24, 22), (24, 23), (24, 24), (24, 25),
(25, 21), (25, 22), (25, 23), (25, 24), (25, 25);


-- 17. Insert Fridge_Ingredient data (65 rows - weak entity)
INSERT INTO Fridge_Ingredient (fridge_id, ingredient_id, quantity, unit, is_expired) VALUES
-- Fridge 1
(1, 1, 2.5, 'pound', FALSE),
(1, 2, 1.0, 'pound', FALSE),
(1, 3, 1.5, 'cup', FALSE),
(1, 6, 2.0, 'piece', FALSE),
(1, 8, 12.0, 'whole', FALSE),


-- Fridge 2
(2, 3, 3.0, 'cup', FALSE),
(2, 7, 2.0, 'piece', FALSE),
(2, 11, 32.0, 'oz', FALSE),
(2, 15, 16.0, 'oz', FALSE),
(2, 19, 3.0, 'whole', FALSE),


-- Fridge 3
(3, 4, 2.0, 'cup', FALSE),
(3, 8, 6.0, 'whole', FALSE),
(3, 12, 8.0, 'oz', FALSE),
(3, 16, 1.0, 'whole', FALSE),
(3, 20, 10.0, 'oz', FALSE),


-- Fridge 4
(4, 5, 1.5, 'cup', TRUE),
(4, 9, 0.5, 'gallon', FALSE),
(4, 13, 6.0, 'oz', FALSE),
(4, 17, 3.0, 'whole', TRUE),
(4, 21, 16.0, 'oz', FALSE),


-- Fridge 5
(5, 6, 2.0, 'piece', FALSE),
(5, 10, 8.0, 'oz', FALSE),
(5, 14, 4.0, 'whole', FALSE),
(5, 18, 1.0, 'pound', TRUE),
(5, 22, 2.0, 'cup', FALSE),


-- Fridge 6
(6, 7, 3.0, 'piece', FALSE),
(6, 11, 16.0, 'oz', TRUE),
(6, 15, 12.0, 'oz', FALSE),
(6, 19, 2.0, 'whole', FALSE),
(6, 23, 1.5, 'cup', FALSE),


-- Fridge 7
(7, 8, 12.0, 'whole', FALSE),
(7, 12, 12.0, 'oz', FALSE),
(7, 16, 2.0, 'whole', TRUE),
(7, 20, 6.0, 'oz', FALSE),
(7, 24, 1.0, 'pint', FALSE),


-- Fridge 8
(8, 9, 1.0, 'gallon', FALSE),
(8, 13, 8.0, 'oz', FALSE),
(8, 17, 2.0, 'whole', FALSE),
(8, 21, 14.0, 'oz', TRUE),
(8, 25, 3.0, 'whole', FALSE),


-- Fridge 9
(9, 10, 8.0, 'oz', FALSE),
(9, 14, 5.0, 'whole', FALSE),
(9, 18, 1.5, 'pound', FALSE),
(9, 22, 3.0, 'cup', TRUE),
(9, 26, 16.0, 'oz', FALSE),


-- Fridge 10
(10, 1, 1.0, 'pound', TRUE),
(10, 5, 2.0, 'cup', FALSE),
(10, 10, 16.0, 'oz', FALSE),
(10, 15, 8.0, 'oz', FALSE),
(10, 20, 8.0, 'oz', TRUE),


-- Additional fridges
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
(14, 10, 12.0, 'oz', TRUE),


(15, 11, 2.0, 'cup', FALSE),
(15, 16, 3.0, 'whole', FALSE);


-- 18. Insert ShoppingList_Ingredient data (65 rows - weak entity)
INSERT INTO ShoppingList_Ingredient (list_id, ingredient_id, quantity, unit, cost) VALUES
-- Shopping List 1
(1, 11, 2.0, 'cup', 3.99),
(1, 12, 1.0, 'pound', 7.99),
(1, 13, 0.5, 'pound', 4.49),
(1, 14, 6.0, 'whole', 3.99),
(1, 15, 1.0, 'bottle', 6.99),


-- Shopping List 2
(2, 13, 0.5, 'pound', 5.99),
(2, 14, 3.0, 'whole', 2.49),
(2, 15, 0.5, 'bottle', 4.99),
(2, 16, 2.0, 'whole', 1.99),
(2, 17, 3.0, 'whole', 2.99),


-- Shopping List 3
(3, 14, 6.0, 'whole', 4.99),
(3, 15, 0.75, 'bottle', 5.49),
(3, 16, 1.0, 'whole', 0.99),
(3, 17, 2.0, 'whole', 1.99),
(3, 18, 1.0, 'pound', 12.99),


-- Shopping List 4
(4, 15, 1.0, 'bottle', 8.99),
(4, 16, 2.0, 'whole', 1.99),
(4, 17, 3.0, 'whole', 2.99),
(4, 18, 1.5, 'pound', 18.99),
(4, 19, 2.0, 'whole', 1.50),


-- Shopping List 5
(5, 16, 2.0, 'whole', 1.99),
(5, 17, 3.0, 'whole', 2.99),
(5, 18, 1.0, 'pound', 12.99),
(5, 19, 3.0, 'whole', 2.25),
(5, 20, 1.0, 'bag', 3.99),


-- Shopping List 6
(6, 17, 3.0, 'whole', 2.99),
(6, 18, 1.0, 'pound', 12.99),
(6, 19, 2.0, 'whole', 1.50),
(6, 20, 2.0, 'bag', 7.98),
(6, 21, 1.0, 'package', 2.99),


-- Shopping List 7
(7, 18, 1.0, 'pound', 12.99),
(7, 19, 2.0, 'whole', 1.50),
(7, 20, 1.0, 'bag', 3.99),
(7, 21, 2.0, 'package', 5.98),
(7, 22, 1.0, 'can', 1.49),


-- Shopping List 8
(8, 19, 2.0, 'whole', 1.50),
(8, 20, 1.0, 'bag', 3.99),
(8, 21, 1.0, 'package', 2.99),
(8, 22, 2.0, 'can', 2.98),
(8, 23, 1.0, 'package', 4.99),


-- Shopping List 9
(9, 20, 1.0, 'bag', 3.99),
(9, 21, 1.0, 'package', 2.99),
(9, 22, 1.0, 'can', 1.49),
(9, 23, 1.0, 'package', 4.99),
(9, 24, 1.0, 'container', 3.99),


-- Shopping List 10
(10, 21, 1.0, 'package', 2.99),
(10, 22, 1.0, 'can', 1.49),
(10, 23, 1.0, 'package', 4.99),
(10, 24, 2.0, 'container', 7.98),
(10, 25, 1.0, 'bunch', 2.49),


-- Additional shopping lists
(11, 25, 2.0, 'bunch', 4.98),
(11, 26, 1.0, 'bottle', 8.99),
(11, 27, 1.0, 'carton', 3.49),


(12, 28, 4.0, 'whole', 3.99),
(12, 29, 1.0, 'bag', 2.49),
(12, 30, 1.0, 'bunch', 3.99),


(13, 31, 1.0, 'pound', 9.99),
(13, 32, 1.0, 'pound', 7.99),
(13, 33, 1.0, 'bunch', 2.99);


-- 19. Insert Client_Health_Advisor data (125+ rows - bridge table)
-- First 50 rows
INSERT INTO Client_Health_Advisor (client_id, advisor_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
(4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
(5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
(6, 1), (6, 2), (6, 3), (6, 4), (6, 5),
(7, 1), (7, 2), (7, 3), (7, 4), (7, 5),
(8, 1), (8, 2), (8, 3), (8, 4), (8, 5),
(9, 1), (9, 2), (9, 3), (9, 4), (9, 5),
(10, 1), (10, 2), (10, 3), (10, 4), (10, 5);

-- Next 50 rows
INSERT INTO Client_Health_Advisor (client_id, advisor_id) VALUES
(11, 1), (11, 2), (11, 3), (11, 4), (11, 5),
(12, 1), (12, 2), (12, 3), (12, 4), (12, 5),
(13, 1), (13, 2), (13, 3), (13, 4), (13, 5),
(14, 1), (14, 2), (14, 3), (14, 4), (14, 5),
(15, 1), (15, 2), (15, 3), (15, 4), (15, 5),
(16, 1), (16, 2), (16, 3), (16, 4), (16, 5),
(17, 1), (17, 2), (17, 3), (17, 4), (17, 5),
(18, 1), (18, 2), (18, 3), (18, 4), (18, 5),
(19, 1), (19, 2), (19, 3), (19, 4), (19, 5),
(20, 1), (20, 2), (20, 3), (20, 4), (20, 5);


-- Additional rows to exceed 125 total
INSERT INTO Client_Health_Advisor (client_id, advisor_id) VALUES
(1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
(2, 6), (2, 7), (2, 8), (2, 9), (2, 10),
(3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
(4, 6), (4, 7), (4, 8), (4, 9), (4, 10),
(5, 6), (5, 7), (5, 8), (5, 9), (5, 10),
(11, 6), (11, 7), (11, 8), (11, 9), (11, 10),
(12, 6), (12, 7), (12, 8), (12, 9), (12, 10);


-- 20. Insert Client_Workout data (125+ rows - bridge table)
-- First batch of 50 rows
INSERT INTO Client_Workout (client_id, workout_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5),
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
(4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
(5, 1), (5, 2), (5, 3), (5, 4), (5, 5),
(6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
(7, 6), (7, 7), (7, 8), (7, 9), (7, 10),
(8, 6), (8, 7), (8, 8), (8, 9), (8, 10),
(9, 6), (9, 7), (9, 8), (9, 9), (9, 10),
(10, 6), (10, 7), (10, 8), (10, 9), (10, 10);


-- Second batch of 50 rows
INSERT INTO Client_Workout (client_id, workout_id) VALUES
(11, 11), (11, 12), (11, 13), (11, 14), (11, 15),
(12, 11), (12, 12), (12, 13), (12, 14), (12, 15),
(13, 11), (13, 12), (13, 13), (13, 14), (13, 15),
(14, 11), (14, 12), (14, 13), (14, 14), (14, 15),
(15, 11), (15, 12), (15, 13), (15, 14), (15, 15),
(16, 16), (16, 17), (16, 18), (16, 19), (16, 20),
(17, 16), (17, 17), (17, 18), (17, 19), (17, 20),
(18, 16), (18, 17), (18, 18), (18, 19), (18, 20),
(19, 16), (19, 17), (19, 18), (19, 19), (19, 20),
(20, 16), (20, 17), (20, 18), (20, 19), (20, 20);


-- Third batch of rows to exceed 125 total
INSERT INTO Client_Workout (client_id, workout_id) VALUES
(1, 21), (1, 22), (1, 23), (1, 24), (1, 25),
(2, 21), (2, 22), (2, 23), (2, 24), (2, 25),
(3, 21), (3, 22), (3, 23), (3, 24), (3, 25),
(4, 21), (4, 22), (4, 23), (4, 24), (4, 25),
(5, 21), (5, 22), (5, 23), (5, 24), (5, 25),
(6, 26), (6, 27), (6, 28), (6, 29), (6, 30);


-- 21. Insert Meal_Plan data (50 rows - weak entity)
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
(17, 17, 2);


-- 22. Insert Leftover data (35 rows - for recipes that exist)
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
(20, 1, FALSE),
(21, 2, TRUE),
(22, 1, FALSE),
(23, 3, TRUE),
(24, 2, FALSE),
(25, 1, TRUE),
(26, 3, FALSE),
(27, 2, TRUE),
(28, 1, FALSE),
(29, 3, TRUE),
(30, 2, FALSE),
(31, 1, TRUE),
(32, 3, FALSE),
(33, 2, TRUE),
(34, 1, FALSE),
(35, 2, TRUE),
(1, 1, TRUE),
(2, 2, FALSE),
(3, 1, TRUE),
(4, 3, FALSE),
(5, 1, TRUE),
(6, 3, FALSE),
(7, 2, TRUE),
(8, 1, FALSE),
(9, 3, TRUE),
(10, 1, FALSE),
(11, 2, TRUE),
(12, 1, FALSE),
(13, 3, TRUE),
(14, 2, FALSE),
(15, 1, TRUE),
(16, 3, TRUE),
(17, 1, FALSE),
(18, 2, TRUE),
(19, 3, FALSE),
(20, 2, TRUE),
(21, 1, FALSE),
(22, 3, TRUE),
(23, 2, FALSE),
(24, 1, TRUE),
(25, 3, FALSE),
(26, 2, TRUE),
(27, 1, FALSE),
(28, 3, TRUE),
(29, 2, FALSE),
(30, 1, TRUE);


-- 23. Insert Nutrition_Tracking data (30 rows - for all clients)
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
(20, 115.67, 52.34, 13.65, 1934.56, 97.43, 2234, 244.32),
(21, 78.45, 43.21, 15.67, 1546.78, 123.45, 1876, 213.45),
(22, 92.67, 56.34, 14.32, 1843.56, 105.67, 2145, 233.67),
(23, 104.34, 48.76, 16.45, 1765.43, 98.45, 2034, 187.65),
(24, 89.56, 53.21, 13.78, 1632.45, 110.23, 1923, 203.45),
(25, 116.78, 45.67, 18.23, 1954.32, 87.65, 2187, 254.32),
(26, 95.43, 50.23, 15.43, 1845.67, 105.43, 1965, 215.67),
(27, 86.54, 48.76, 14.32, 1765.43, 98.67, 1895, 195.43),
(28, 107.65, 54.32, 17.54, 1923.45, 115.67, 2145, 234.56),
(29, 93.45, 51.23, 16.78, 1834.56, 102.34, 1987, 213.45),
(30, 101.23, 57.65, 15.32, 1954.32, 97.54, 2076, 223.45),
(31, 92.43, 48.76, 15.32, 1765.43, 105.32, 1965, 210.45),
(32, 104.32, 53.21, 16.76, 1845.67, 96.54, 2034, 223.67),
(33, 87.65, 45.87, 14.32, 1632.45, 112.34, 1876, 193.45),
(34, 95.43, 52.34, 17.65, 1923.45, 103.56, 2045, 218.54),
(35, 110.76, 56.87, 15.43, 1845.67, 98.76, 2187, 234.56),
(36, 88.32, 47.65, 13.54, 1723.45, 106.54, 1945, 207.65),
(37, 103.45, 51.23, 16.87, 1934.54, 94.32, 2076, 226.45),
(38, 96.54, 53.76, 14.21, 1832.45, 108.76, 1987, 214.32),
(39, 112.32, 58.54, 17.43, 2054.32, 91.45, 2143, 239.76),
(40, 89.54, 46.32, 15.65, 1754.32, 109.87, 1932, 201.54),
(41, 105.67, 54.32, 16.54, 1876.54, 97.43, 2134, 227.65),
(42, 93.21, 50.76, 14.87, 1723.45, 113.54, 1965, 209.43),
(43, 108.76, 55.43, 18.32, 1954.32, 95.67, 2187, 236.54),
(44, 90.43, 49.21, 13.76, 1687.65, 110.32, 1923, 197.65),
(45, 102.54, 52.87, 16.32, 1843.21, 99.54, 2076, 224.32),
(46, 97.65, 51.32, 15.76, 1765.43, 105.87, 2013, 216.54),
(47, 113.21, 59.76, 17.87, 2076.54, 90.21, 2165, 242.32),
(48, 91.32, 47.65, 14.32, 1732.43, 107.65, 1954, 204.32),
(49, 106.54, 53.21, 16.76, 1954.32, 96.87, 2123, 230.76),
(50, 99.87, 52.43, 15.32, 1865.43, 104.32, 2032, 220.54);

-- 24. Insert Error_Log data (60 rows - weak entity)
INSERT INTO Error_Log (client_id, log_id, message) VALUES
(1, 1, 'User input error for Busy Ben'),
(1, 2, 'Scan returned empty result for Busy Ben'),
(1, 3, 'Barcode checksum mismatch for Busy Ben'),
(2, 1, 'Barcode checksum mismatch'),
(2, 2, 'User input error'),
(2, 3, 'Scan returned empty result'),
(3, 1, 'Scan returned empty result'),
(3, 2, 'Database connection lost'),
(3, 3, 'Ingredient scan failed'),
(4, 4, 'Timeout during scan'),
(4, 5, 'Invalid format detected'),
(4, 6, 'Barcode checksum mismatch'),
(5, 5, 'Invalid format detected'),
(5, 6, 'Unrecognized barcode'),
(5, 7, 'Scan returned empty result'),
(6, 6, 'Scan returned empty result'),
(6, 7, 'Expired ingredient scanned'),
(6, 8, 'User input error'),
(7, 7, 'Ingredient scan failed'),
(7, 8, 'Database connection lost'),
(7, 9, 'Barcode checksum mismatch'),
(8, 8, 'Barcode checksum mismatch'),
(8, 9, 'Timeout during scan'),
(8, 10, 'Scan returned empty result'),
(9, 9, 'Scan returned empty result'),
(9, 10, 'Invalid format detected'),
(9, 11, 'User input error'),
(10, 10, 'User input error'),
(10, 11, 'Ingredient scan failed'),
(10, 12, 'Barcode checksum mismatch'),
(11, 11, 'Barcode checksum mismatch'),
(11, 12, 'Scan returned empty result'),
(11, 13, 'Timeout during scan'),
(12, 12, 'Scan returned empty result'),
(12, 13, 'User input error'),
(12, 14, 'Invalid format detected'),
(13, 13, 'User input error'),
(13, 14, 'Ingredient scan failed'),
(13, 15, 'Barcode checksum mismatch'),
(14, 14, 'Barcode checksum mismatch'),
(14, 15, 'Scan returned empty result'),
(14, 16, 'Database connection lost'),
(15, 15, 'Timeout during scan'),
(15, 16, 'Invalid format detected'),
(15, 17, 'User input error'),
(16, 16, 'Invalid format detected'),
(16, 17, 'Ingredient scan failed'),
(16, 18, 'Barcode checksum mismatch'),
(17, 17, 'Barcode checksum mismatch'),
(17, 18, 'Scan returned empty result'),
(17, 19, 'Timeout during scan'),
(18, 18, 'Database connection lost'),
(18, 19, 'User input error'),
(18, 20, 'Invalid format detected'),
(19, 19, 'User input error'),
(19, 20, 'Ingredient scan failed'),
(19, 21, 'Barcode checksum mismatch'),
(20, 20, 'Barcode checksum mismatch'),
(20, 21, 'Scan returned empty result'),
(20, 22, 'Timeout during scan');

