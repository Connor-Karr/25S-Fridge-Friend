from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db
from datetime import datetime, timedelta

leftovers = Blueprint('leftovers', __name__)
