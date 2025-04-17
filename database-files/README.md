# `database-files` Folder

# FridgeFriend Database

# The Tables

The following is a summary of what each of the tables in our database represents:

User: Stores basic user information including first name, last name, username, password, and email. This serves as the foundation for all user types in the system.

Admin: Represents system administrators who have elevated permissions. References the User table through a foreign key.

Personal_Constraints: Stores user-specific dietary and budget information including budget limits, dietary restrictions, personal diet preferences, and age group.

Workout: Contains information about different types of workouts, including name, quantity, weight, and calories burned.
Ingredient: Stores details about food ingredients including name and expiration date.

Recipe: Contains recipe information including name and preparation instructions.

Fridge_Inventory: Represents a user's virtual refrigerator where ingredients are stored.

Shopping_List: Represents a user's shopping list for grocery planning.

Food_Scan_Log: Tracks when ingredients are scanned into the system, including timestamp and status.

Brand: Stores information about food brands, including whether they are trusted.

Macronutrients: Contains nutritional information for ingredients including protein, fat, fiber, vitamins, sodium, calories, and carbohydrates.

Client: Represents regular users of the application with references to their personal constraints, fridge inventory, shopping list, and food scan log.

Health_Advisor: Represents nutrition and fitness professionals who can provide guidance to clients.

Recipe_Ingredient: A bridge table that connects recipes to their required ingredients, including quantities and units.

Ingredient_Macronutrient: A bridge table that connects ingredients to their nutritional information.

Recipe_Brand: A bridge table that associates recipes with recommended brands.

Fridge_Ingredient: A weak entity that tracks specific ingredients in a user's fridge, including quantity, unit, and expiration status.

ShoppingList_Ingredient: A weak entity that tracks ingredients on a user's shopping list, including quantity, unit, and estimated cost.

Meal_Plan: Associates personal constraints with recommended recipes and quantities.

Leftover: Tracks leftover portions of prepared recipes, including quantity and expiration status.

Nutrition_Tracking: Monitors clients' nutritional intake including protein, fat, fiber, sodium, vitamins, calories, and carbohydrates.

Client_Health_Advisor: A bridge table that connects clients to their health advisors.

Client_Workout: A bridge table that associates clients with their workout routines.

Error_Log: Records system errors related to clients and food scanning, including error messages and timestamps.

# To re-bootstrap the database, do the following:

Drop the existing database by using the command:

DROP DATABASE IF EXISTS fridgefriend;

Create the database:

CREATE DATABASE fridgefriend;
USE fridgefriend;

Execute the CREATE TABLE statements in the correct order (starting with strong entities first) to recreate the schema.
Insert the data with the INSERT INTO statements, following the same order to respect foreign key constraints.
Verify the data using SQL queries to ensure all relationships are properly established.
