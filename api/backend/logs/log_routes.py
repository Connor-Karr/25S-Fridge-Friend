from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime

logs = Blueprint('logs', __name__)