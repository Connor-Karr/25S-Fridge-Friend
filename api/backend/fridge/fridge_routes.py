from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

fridge = Blueprint('fridge', __name__)

@fridge.route('/', methods=['GET'])
def get_fridge_inventory():
    """Get current fridge inventory"""
    client_id = request.args.get('client_id')
    
    if not client_id:
        response = make_response(jsonify({"error": "Client ID is required"}))
        response.status_code = 400
        return response

    cursor = db.get_db().cursor()
    query = '''
        SELECT fi.fridge_id, i.name, fi.quantity, i.expiration_date, fi.is_expired
        FROM Fridge_Ingredient fi
        JOIN Client c ON c.fridge_id = fi.fridge_id
        JOIN Ingredient i ON fi.ingredient_id = i.ingredient_id
        WHERE c.client_id = %s
    '''
    cursor.execute(query, (client_id,))
    inventory = cursor.fetchall()
    
    response = make_response(jsonify(inventory))
    response.status_code = 200
    return response
    
@fridge.route('/expired', methods=['PUT'])
def update_expired_status():
    """Update expired status of ingredients"""
    cursor = db.get_db().cursor()

    try:
        cursor.execute('''
                UPDATE Fridge_Ingredient fi
                JOIN Ingredient i ON fi.ingredient_id = i.ingredient_id
                SET fi.is_expired = TRUE
                WHERE i.expiration_date < CURDATE()
            ''')
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Expired ingredients updated"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating expired status: {str(e)}")
        response = make_response(jsonify({"error": "Could not update expired status"}))
        response.status_code = 500
        return response
    
@fridge.route('/expired', methods=['DELETE'])
def remove_expired_ingredients():
    """Remove all expired ingredients"""
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Fridge_Ingredient WHERE is_expired = TRUE')
        db.get_db().commit()
        
        count = cursor.rowcount
        response = make_response(jsonify({"message": f"{count} expired ingredients removed"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error removing expired ingredients: {str(e)}")
        response = make_response(jsonify({"error": "Could not remove expired ingredients"}))
        response.status_code = 500
        return response
