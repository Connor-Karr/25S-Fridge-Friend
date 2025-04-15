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