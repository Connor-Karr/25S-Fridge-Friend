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

@logs.route('/scans', methods=['POST'])
def log_food_scan():
    """Log new food scan - Used by Alvin to track scanning issues [Alvin-6]"""
    data = request.json
    
    ingredient_id = data.get('ingredient_id')
    status = data.get('status')

    if not all([ingredient_id, status]):
        response = make_response(jsonify({"error": "Ingredient ID and status are required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO Food_Scan_Log (ingredient_id, status, timestamp) VALUES (%s, %s, %s)',
            (ingredient_id, status, datetime.now())
        )
        db.get_db().commit()
        
        log_id = cursor.lastrowid
        
        if status == 'FAILED':
            message = data.get('message', 'Unknown error during scan')
            client_id = data.get('client_id')
            
            if client_id:
                cursor.execute(
                    'INSERT INTO Error_Log (client_id, log_id, message, timestamp) VALUES (%s, %s, %s, %s)',
                    (client_id, log_id, message, datetime.now())
                )
                db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Food scan logged successfully", 
            "log_id": log_id
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error logging food scan: {str(e)}")
        response = make_response(jsonify({"error": "Could not log food scan"}))
        response.status_code = 500
        return response

@logs.route('/errors', methods=['GET'])
def get_error_logs():
    """Get error logs - Used by Alvin to diagnose system issues [Alvin-6]"""
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

@logs.route('/errors', methods=['POST'])
def log_error():
    """Create new error log entry"""
    data = request.json
    
    client_id = data.get('client_id')
    log_id = data.get('log_id')
    message = data.get('message')

    if not all([client_id, message]):
        response = make_response(jsonify({"error": "Client ID and message are required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    
    try:
        cursor.execute(
            'INSERT INTO Error_Log (client_id, log_id, message, timestamp) VALUES (%s, %s, %s, %s)',
            (client_id, log_id, message, datetime.now())
        )
        db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Error logged successfully", 
            "error_id": cursor.lastrowid
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating error log: {str(e)}")
        response = make_response(jsonify({"error": "Could not create error log"}))
        response.status_code = 500
        return response