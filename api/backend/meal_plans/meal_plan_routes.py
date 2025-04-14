from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

meal_plans = Blueprint('meal_plans', __name__)

@meal_plans.route('/', methods=['GET'])
def get_all_meal_plans():
    """Get all meal plans"""
    client_id = request.args.get('client_id')
    
    cursor = db.get_db().cursor()
    
    if client_id:
        query = '''
            SELECT mp.meal_id, mp.pc_id, mp.recipe_id, mp.quantity, r.name AS recipe_name
            FROM Meal_Plan mp
            JOIN Client c ON mp.pc_id = c.pc_id
            JOIN Recipe r ON mp.recipe_id = r.recipe_id
            WHERE c.client_id = %s
        '''
        cursor.execute(query, (client_id,))
    else:
        query = '''
            SELECT mp.meal_id, mp.pc_id, mp.recipe_id, mp.quantity, r.name AS recipe_name
            FROM Meal_Plan mp
            JOIN Recipe r ON mp.recipe_id = r.recipe_id
        '''
        cursor.execute(query)
        
    meal_plans = cursor.fetchall()
    
    response = make_response(jsonify(meal_plans))
    response.status_code = 200
    return response

