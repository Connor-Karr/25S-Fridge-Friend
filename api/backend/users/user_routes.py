from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def get_all_users():
    """Get list of all users"""
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id, f_name, l_name, username, email FROM User')
    users_data = cursor.fetchall()
    
    response = make_response(jsonify(users_data))
    response.status_code = 200
    return response


@users.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user profile details"""
    cursor = db.get_db().cursor()
    cursor.execute('SELECT user_id, f_name, l_name, username, email FROM User WHERE user_id = %s', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        response = make_response(jsonify({"error": "User not found"}))
        response.status_code = 404
        return response
    
    response = make_response(jsonify(user_data))
    response.status_code = 200
    return response

@users.route('/', methods=['POST'])
def create_user():
    """Create a new user account"""
    user_data = request.json
    
    f_name = user_data.get('f_name')
    l_name = user_data.get('l_name')
    username = user_data.get('username')
    password = user_data.get('password')
    email = user_data.get('email')
    
    if not all([f_name, l_name, username, password, email]):
        response = make_response(jsonify({"error": "Missing required fields"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    try:
        cursor.execute(
            'INSERT INTO User (f_name, l_name, username, password, email) VALUES (%s, %s, %s, %s, %s)',
            (f_name, l_name, username, password, email)
        )
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "User created successfully", "user_id": cursor.lastrowid}))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating user: {str(e)}")
        response = make_response(jsonify({"error": "Could not create user"}))
        response.status_code = 500
        return response
    
@users.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user profile or mark user as inactive"""
    user_data = request.json
    
    cursor = db.get_db().cursor()
    
    # Check if user exists
    cursor.execute('SELECT * FROM User WHERE user_id = %s', (user_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "User not found"}))
        response.status_code = 404
        return response
        
    # Build update query dynamically based on provided fields
    update_fields = []
    params = []
    
    if 'f_name' in user_data:
        update_fields.append('f_name = %s')
        params.append(user_data['f_name'])
        
    if 'l_name' in user_data:
        update_fields.append('l_name = %s')
        params.append(user_data['l_name'])
        
    if 'email' in user_data:
        update_fields.append('email = %s')
        params.append(user_data['email'])
        
    if 'username' in user_data:
        update_fields.append('username = %s')
        params.append(user_data['username'])
    
    if not update_fields:
        response = make_response(jsonify({"error": "No fields to update"}))
        response.status_code = 400
        return response
        
    query = f"UPDATE User SET {', '.join(update_fields)} WHERE user_id = %s"
    params.append(user_id)
    
    try:
        cursor.execute(query, params)
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "User updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating user: {str(e)}")
        response = make_response(jsonify({"error": "Could not update user"}))
        response.status_code = 500
        return response
    
@users.route('/constraints/<int:pc_id>', methods=['PUT'])
def update_constraints(pc_id):
    """Update user dietary constraints - Used by Nancy to manage client diets [Nancy-1, Nancy-4]"""
    data = request.json
    
    cursor = db.get_db().cursor()
    
    # Check if personal constraints exist
    cursor.execute('SELECT * FROM Personal_Constraints WHERE pc_id = %s', (pc_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "Personal constraints not found"}))
        response.status_code = 404
        return response
    
    update_fields = []
    params = []
    
    if 'budget' in data:
        update_fields.append('budget = %s')
        params.append(data['budget'])
    
    if 'dietary_restrictions' in data:
        update_fields.append('dietary_restrictions = %s')
        params.append(data['dietary_restrictions'])
    
    if 'personal_diet' in data:
        update_fields.append('personal_diet = %s')
        params.append(data['personal_diet'])
    
    if 'age_group' in data:
        update_fields.append('age_group = %s')
        params.append(data['age_group'])
    
    if not update_fields:
        response = make_response(jsonify({"error": "No fields to update"}))
        response.status_code = 400
        return response
    
    query = f"UPDATE Personal_Constraints SET {', '.join(update_fields)} WHERE pc_id = %s"
    params.append(pc_id)
    
    try:
        cursor.execute(query, params)
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Personal constraints updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating personal constraints: {str(e)}")
        response = make_response(jsonify({"error": "Could not update personal constraints"}))
        response.status_code = 500
        return response