from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

fridge = Blueprint('fridge', __name__)

@fridge.route('/', methods=['GET'])
def get_fridge_inventory():
    """Get current fridge inventory"""

@fridge.route('/<int:ingredient_id>', methods=['GET'])
def get_fridge_ingredient(ingredient_id):
    """Get details for a specific ingredient"""
    fridge_id = request.args.get('fridge_id')
    
    if not fridge_id:
        response = make_response(jsonify({"error": "Fridge ID is required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    query = '''
        SELECT fi.fridge_id, i.name, fi.quantity, i.expiration_date, fi.is_expired
        FROM Fridge_Inventory fi
        JOIN Ingredient i ON fi.ingredient_id = i.ingredient_id
        WHERE fi.fridge_id = %s AND fi.ingredient_id = %s
    '''
    cursor.execute(query, (fridge_id, ingredient_id))
    ingredient = cursor.fetchone()
    
    if not ingredient:
        response = make_response(jsonify({"error": "Ingredient not found in fridge"}))
        response.status_code = 404
        return response
    
    response = make_response(jsonify(ingredient))
    response.status_code = 200
    return response
