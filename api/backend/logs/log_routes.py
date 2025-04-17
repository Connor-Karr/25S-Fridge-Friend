from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime

logs = Blueprint('logs', __name__)

@logs.route('/scans', methods=['GET'])
def get_scan_history():
    """Get scan history - Used by Alvin to track food scanning patterns [Alvin-6]"""
    client_id = request.args.get('client_id')
    
    cursor = db.get_db().cursor()
    
    if client_id:
        query = '''
            SELECT fsl.*, i.name as ingredient_name
            FROM Food_Scan_Log fsl
            JOIN Ingredient i ON fsl.ingredient_id = i.ingredient_id
            JOIN Client c ON c.log_id = fsl.log_id
            WHERE c.client_id = %s
            ORDER BY fsl.timestamp DESC
        '''
        cursor.execute(query, (client_id,))
    else:
        query = '''
            SELECT fsl.*, i.name as ingredient_name
            FROM Food_Scan_Log fsl
            JOIN Ingredient i ON fsl.ingredient_id = i.ingredient_id
            ORDER BY fsl.timestamp DESC
        '''
        cursor.execute(query)

    scans = cursor.fetchall()

    response = make_response(jsonify(scans))
    response.status_code = 200
    return response


@logs.route('/errors', methods=['GET'])
def get_error_logs():
    """Get error logs"""
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT el.*, fsl.status as scan_status, i.name as ingredient_name
        FROM Error_Log el
        JOIN Food_Scan_Log fsl ON el.log_id = fsl.log_id
        JOIN Ingredient i ON fsl.ingredient_id = i.ingredient_id
        ORDER BY el.timestamp DESC
    ''')
    
    errors = cursor.fetchall()
    
    response = make_response(jsonify(errors))
    response.status_code = 200
    return response


@logs.route('/nutrition/<int:client_id>', methods=['GET'])
def get_nutrition_logs(client_id):
    """Get nutrition tracking logs"""
    cursor = db.get_db().cursor()
    
    cursor.execute('''
        SELECT nt.*
        FROM Nutrition_Tracking nt
        WHERE nt.client_id = %s
        ORDER BY nt.tracking_id DESC
    ''', (client_id,))
    
    nutrition_logs = cursor.fetchall()
    
    response = make_response(jsonify(nutrition_logs))
    response.status_code = 200
    return response

