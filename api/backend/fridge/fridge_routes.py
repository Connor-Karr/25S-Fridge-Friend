from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

fridge = Blueprint('fridge', __name__)

@fridge.route('/', methods=['GET'])
def get_fridge_inventory():
    """Get current fridge inventory - Used by Busy Ben to view fridge contents [Busy Ben-2]"""
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

@fridge.route('/<int:ingredient_id>', methods=['POST'])
def add_ingredient_to_fridge(ingredient_id):
    """Add new ingredient to fridge"""
    data = request.json
    
    fridge_id = data.get('fridge_id')
    quantity = data.get('quantity', 1)
    
    if not fridge_id:
        response = make_response(jsonify({"error": "Fridge ID is required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    # Check if ingredient already exists in fridge
    cursor.execute(
        'SELECT * FROM Fridge_Inventory WHERE fridge_id = %s AND ingredient_id = %s',
        (fridge_id, ingredient_id)
    )
    existing = cursor.fetchone()
    try:
        if existing:
            # Update quantity
            cursor.execute(
                'UPDATE Fridge_Inventory SET quantity = quantity + %s WHERE fridge_id = %s AND ingredient_id = %s',
                (quantity, fridge_id, ingredient_id)
            )
        else:
            # Insert new entry
            cursor.execute(
                'INSERT INTO Fridge_Inventory (fridge_id, ingredient_id, quantity, is_expired) VALUES (%s, %s, %s, FALSE)',
                (fridge_id, ingredient_id, quantity)
            )
        
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Ingredient added to fridge"}))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error adding ingredient to fridge: {str(e)}")
        response = make_response(jsonify({"error": "Could not add ingredient"}))
        response.status_code = 500
        return response
    
@fridge.route('/', methods=['PUT'])
def update_expired_status():
    """Update expired status of ingredients"""
    cursor = db.get_db().cursor()

    try:
        cursor.execute('''
                UPDATE Fridge_Inventory fi
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
    
@fridge.route('/', methods=['DELETE'])
def remove_expired_ingredients():
    """Remove all expired ingredients"""
    cursor = db.get_db().cursor()
    try:
        cursor.execute('DELETE FROM Fridge_Inventory WHERE is_expired = TRUE')
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