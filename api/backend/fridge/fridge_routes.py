from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

fridge = Blueprint('fridge', __name__)

@fridge.route('/inventory/<client_id>', methods=['GET'])
def get_fridge_inventory(client_id):