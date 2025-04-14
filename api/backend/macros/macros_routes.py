from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

macros = Blueprint('macros', __name__)

@macros.route('/', methods=['GET'])
def get_macronutrients():
    """Get macronutrient data"""
    ingredient_id = request.args.get('ingredient_id')
    
    cursor = db.get_db().cursor()
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
    
    response = make_response(jsonify(macros))
    response.status_code = 200
    return response