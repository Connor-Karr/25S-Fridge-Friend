from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime, timedelta

leftovers = Blueprint('leftovers', __name__)

@leftovers.route('/', methods=['GET'])
def get_leftovers():
    """Get all leftovers"""
    recipe_id = request.args.get('recipe_id')
    
    cursor = db.get_db().cursor()
    
    if recipe_id:
        cursor.execute('''
            SELECT l.*, r.name as recipe_name
            FROM Leftover l
            JOIN Recipe r ON l.recipe_id = r.recipe_id
            WHERE l.recipe_id = %s
        ''', (recipe_id,))
    else:
        cursor.execute('''
            SELECT l.*, r.name as recipe_name
            FROM Leftover l
            JOIN Recipe r ON l.recipe_id = r.recipe_id
        ''')
    
    leftovers = cursor.fetchall()
    
    response = make_response(jsonify(leftovers))
    response.status_code = 200
    return response

@leftovers.route('/<int:leftover_id>', methods=['GET'])
def get_leftover(leftover_id):
    """Get specific leftover details"""
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT l.*, r.name as recipe_name, r.instructions
        FROM Leftover l
        JOIN Recipe r ON l.recipe_id = r.recipe_id
        WHERE l.leftover_id = %s
    ''', (leftover_id,))
    
    leftover = cursor.fetchone()
    
    if not leftover:
        response = make_response(jsonify({"error": "Leftover not found"}))
        response.status_code = 404
        return response
    
    response = make_response(jsonify(leftover))
    response.status_code = 200
    return response

@leftovers.route('/', methods=['POST'])
def add_leftover():
    """Add new leftover"""
    data = request.json
    
    recipe_id = data.get('recipe_id')
    quantity = data.get('quantity', 1)
    
    if not recipe_id:
        response = make_response(jsonify({"error": "Recipe ID is required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    
    # Check if recipe exists
    cursor.execute('SELECT * FROM Recipe WHERE recipe_id = %s', (recipe_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "Recipe not found"}))
        response.status_code = 404
        return response
    
    try:
        # Calculate expiration date (e.g., 5 days from now)
        expiration_date = datetime.now() + timedelta(days=5)
        
        cursor.execute(
            'INSERT INTO Leftover (recipe_id, quantity, is_expired) VALUES (%s, %s, FALSE)',
            (recipe_id, quantity)
        )
        db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Leftover added successfully",
            "leftover_id": cursor.lastrowid
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error adding leftover: {str(e)}")
        response = make_response(jsonify({"error": "Could not add leftover"}))
        response.status_code = 500
        return response
