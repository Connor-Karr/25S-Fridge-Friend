from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

macros = Blueprint('macros', __name__)

@macros.route('/', methods=['GET'])
def get_macronutrients():
    """Get macronutrient data"""
    ingredient_id = request.args.get('ingredient_id')
    
    cursor = db.get_db().cursor()