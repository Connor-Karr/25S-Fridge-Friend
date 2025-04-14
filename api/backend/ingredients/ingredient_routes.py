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

    response = make_response(jsonify(result))
    response.status_code = 200
    return response


@ingredients.route('/', methods=['POST'])
def add_ingredient():
    """Add new trusted ingredient with macros"""
    data = request.json

    name = data.get('name')
    expiration_date = data.get('expiration_date')
    macros = data.get('macros', {})

    if not name:
        response = make_response(jsonify({"error": "Ingredient name is required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    try:
        # Insert ingredient
        cursor.execute(
            'INSERT INTO Ingredient (name, expiration_date) VALUES (%s, %s)',
            (name, expiration_date)
        )
        ingredient_id = cursor.lastrowid

        if macros:
            cursor.execute(
                '''INSERT INTO Macronutrients (
                    ingredient_id, protein, fat, fiber, vitamin, sodium, calories, carbs
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (
                    ingredient_id, 
                    macros.get('protein', 0), 
                    macros.get('fat', 0), 
                    macros.get('fiber', 0),
                    macros.get('vitamin', 0),
                    macros.get('sodium', 0),
                    macros.get('calories', 0),
                    macros.get('carbs', 0)
                )
            )

            db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Ingredient added successfully", 
            "ingredient_id": ingredient_id
        }))
        response.status_code = 201
        return response













