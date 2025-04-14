from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

macros = Blueprint('macros', __name__)