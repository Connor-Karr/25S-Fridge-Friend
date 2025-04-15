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


@meal_plans.route('/<int:meal_id>', methods=['GET'])
def get_meal_plan(meal_id):
    """Get specific meal plan details"""
    cursor = db.get_db().cursor()
    
    query = '''
        SELECT mp.meal_id, mp.pc_id, mp.recipe_id, mp.quantity, r.name AS recipe_name, r.instructions
        FROM Meal_Plan mp
        JOIN Recipe r ON mp.recipe_id = r.recipe_id
        WHERE mp.meal_id = %s
    '''
    cursor.execute(query, (meal_id,))
    meal_plan = cursor.fetchone()
    
    if not meal_plan:
        response = make_response(jsonify({"error": "Meal plan not found"}))
        response.status_code = 404
        return response
    
    response = make_response(jsonify(meal_plan))
    response.status_code = 200
    return response



@meal_plans.route('/', methods=['POST'])
def create_meal_plan():
    """Create new meal plan"""
    data = request.json
    
    pc_id = data.get('pc_id')
    recipe_id = data.get('recipe_id')
    quantity = data.get('quantity', 1)
    
    if not all([pc_id, recipe_id]):
        response = make_response(jsonify({"error": "Personal constraint ID and recipe ID are required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO Meal_Plan (pc_id, recipe_id, quantity) VALUES (%s, %s, %s)',
            (pc_id, recipe_id, quantity)
        )
        db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Meal plan created successfully", 
            "meal_id": cursor.lastrowid
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating meal plan: {str(e)}")
        response = make_response(jsonify({"error": "Could not create meal plan"}))
        response.status_code = 500
        return response

@meal_plans.route('/<int:meal_id>', methods=['PUT'])
def update_meal_plan(meal_id):
    """Update meal plan details"""
    data = request.json
    
    quantity = data.get('quantity')
    
    if not quantity:
        response = make_response(jsonify({"error": "No fields to update"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    
    # Check if meal plan exists
    cursor.execute('SELECT * FROM Meal_Plan WHERE meal_id = %s', (meal_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "Meal plan not found"}))
        response.status_code = 404
        return response
    
    try:
        cursor.execute(
            'UPDATE Meal_Plan SET quantity = %s WHERE meal_id = %s',
            (quantity, meal_id)
        )
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Meal plan updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating meal plan: {str(e)}")
        response = make_response(jsonify({"error": "Could not update meal plan"}))
        response.status_code = 500
        return response

@meal_plans.route('/<int:meal_id>', methods=['DELETE'])
def delete_meal_plan(meal_id):
    """Delete specific meal plan"""
    cursor = db.get_db().cursor()
    
    try:
        cursor.execute('DELETE FROM Meal_Plan WHERE meal_id = %s', (meal_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            response = make_response(jsonify({"error": "Meal plan not found"}))
            response.status_code = 404
            return response
        
        response = make_response(jsonify({"message": "Meal plan deleted successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error deleting meal plan: {str(e)}")
        response = make_response(jsonify({"error": "Could not delete meal plan"}))
        response.status_code = 500
        return response
    
@meal_plans.route('/', methods=['DELETE'])
def delete_outdated_meal_plans():
    """Delete outdated meal plans"""
    recipe_id = request.args.get('recipe_id')
    
    if not recipe_id:
        response = make_response(jsonify({"error": "Recipe ID is required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    
    try:
        cursor.execute('DELETE FROM Meal_Plan WHERE recipe_id = %s', (recipe_id,))
        db.get_db().commit()
        
        count = cursor.rowcount
        response = make_response(jsonify({"message": f"{count} meal plans deleted"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error deleting meal plans: {str(e)}")
        response = make_response(jsonify({"error": "Could not delete meal plans"}))
        response.status_code = 500
        return response

