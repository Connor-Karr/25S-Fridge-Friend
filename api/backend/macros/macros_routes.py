from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

macros = Blueprint('macros', __name__)

@macros.route('/', methods=['GET'])
def get_macronutrients():
    """Get macronutrient data"""
    ingredient_id = request.args.get('ingredient_id')
    
    cursor = db.get_db().cursor()
    
    if ingredient_id:
        cursor.execute('''
            SELECT * 
            FROM Macronutrients 
            WHERE ingredient_id = %s
        ''', (ingredient_id,))
        macros = cursor.fetchone()
        
        if not macros:
            response = make_response(jsonify({"error": "Macronutrients not found for this ingredient"}))
            response.status_code = 404
            return response
    else:
        cursor.execute('''
            SELECT m.*, i.name as ingredient_name
            FROM Macronutrients m
            JOIN Ingredient i ON m.ingredient_id = i.ingredient_id
        ''')
        macros = cursor.fetchall()
    
    response = make_response(jsonify(macros))
    response.status_code = 200
    return response

@macros.route('/<int:macro_id>', methods=['PUT'])
def update_macronutrients(macro_id):
    """Update macronutrient values"""
    data = request.json
    
    protein = data.get('protein')
    fat = data.get('fat')
    fiber = data.get('fiber')
    vitamin = data.get('vitamin')
    sodium = data.get('sodium')
    calories = data.get('calories')
    carbs = data.get('carbs')

    update_fields = []
    params = []

    if protein is not None:
        update_fields.append('protein = %s')
        params.append(protein)

    if fat is not None:
        update_fields.append('fat = %s')
        params.append(fat)

    if fiber is not None:
        update_fields.append('fiber = %s')
        params.append(fiber)

    if vitamin is not None:
        update_fields.append('vitamin = %s')
        params.append(vitamin)