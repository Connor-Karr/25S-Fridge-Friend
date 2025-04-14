from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

ingredients = Blueprint('ingredients', __name__)

@ingredients.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient details"""
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ingredient WHERE ingredient_id = %s', (ingredient_id,))
    ingredient = cursor.fetchone()

    response = make_response(jsonify(ingredients_data))
    response.status_code = 200
    return response

@ingredients.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient details"""
    cursor = db.get_db().cursor()

    # Get ingredient basic info
    cursor.execute('SELECT * FROM Ingredient WHERE ingredient_id = %s', (ingredient_id,))
    ingredient = cursor.fetchone()

    if not ingredient:
        response = make_response(jsonify({"error": "Ingredient not found"}))
        response.status_code = 404
        return response
    
     # Get macronutrients
    cursor.execute('''
        SELECT m.* 
        FROM Macronutrients m
        WHERE m.ingredient_id = %s
    ''', (ingredient_id,))
    macros = cursor.fetchone()
    
    result = {
        "ingredient": ingredient,
        "macronutrients": macros
    }








