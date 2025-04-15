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

    if sodium is not None:
        update_fields.append('sodium = %s')
        params.append(sodium)

    if calories is not None:
        update_fields.append('calories = %s')
        params.append(calories)

    if carbs is not None:
        update_fields.append('carbs = %s')
        params.append(carbs)

    if not update_fields:
        response = make_response(jsonify({"error": "No fields to update"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Macronutrients WHERE macro_id = %s', (macro_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "Macronutrients not found"}))
        response.status_code = 404
        return response
    
    try:
        query = f"UPDATE Macronutrients SET {', '.join(update_fields)} WHERE macro_id = %s"
        params.append(macro_id)
        cursor.execute(query, params)
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Macronutrients updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating macronutrients: {str(e)}")
        response = make_response(jsonify({"error": "Could not update macronutrients"}))
        response.status_code = 500
        return response