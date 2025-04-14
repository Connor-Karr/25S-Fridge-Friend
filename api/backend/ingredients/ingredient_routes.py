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



