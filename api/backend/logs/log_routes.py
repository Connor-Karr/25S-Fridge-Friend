from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime

logs = Blueprint('logs', __name__)

@logs.route('/scans', methods=['GET'])
def get_scan_history():
    """Get scan history"""
    client_id = request.args.get('client_id')
    
    cursor = db.get_db().cursor()
    query = '''
            SELECT fsl.*, i.name as ingredient_name
            FROM Food_Scan_Log fsl
            JOIN Ingredient i ON fsl.ingredient_id = i.ingredient_id
            JOIN Client c ON c.log_id = fsl.log_id
            WHERE c.client_id = %s
            ORDER BY fsl.timestamp DESC
        '''
    cursor.execute(query, (client_id,))
    scans = cursor.fetchall()
    
    response = make_response(jsonify(scans))
    response.status_code = 200
    return response