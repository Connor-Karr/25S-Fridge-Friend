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
    """Update user dietary constraints"""
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
    
@users.route('/constraints', methods=['POST'])
def create_constraints():
    """Create personal constraints"""
    data = request.json
    
    budget = data.get('budget')
    dietary_restrictions = data.get('dietary_restrictions')
    personal_diet = data.get('personal_diet')
    age_group = data.get('age_group')
    
    cursor = db.get_db().cursor()
    
    try:
        cursor.execute(
            '''INSERT INTO Personal_Constraints 
               (budget, dietary_restrictions, personal_diet, age_group) 
               VALUES (%s, %s, %s, %s)''',
            (budget, dietary_restrictions, personal_diet, age_group)
        )
        db.get_db().commit()
        
        pc_id = cursor.lastrowid
        
        # If client_id is provided, link these constraints to the client
        client_id = data.get('client_id')
        if client_id:
            cursor.execute(
                'UPDATE Client SET pc_id = %s WHERE client_id = %s',
                (pc_id, client_id)
            )
            db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Personal constraints created successfully",
            "pc_id": pc_id
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating personal constraints: {str(e)}")
        response = make_response(jsonify({"error": "Could not create personal constraints"}))
        response.status_code = 500
        return response
    


@users.route('/auth/student/<int:student_id>', methods=['GET'])
def get_student_auth(student_id):
    """Get student details with their preferences"""
    cursor = db.get_db().cursor()

    # Join User table with Client table to get student information
    query = '''
    SELECT u.user_id, u.f_name as firstName, u.l_name as lastName, 
            c.client_id, pc.personal_diet as dietaryPreferences,
            pc.dietary_restrictions as allergies
    FROM User u
    JOIN Client c ON u.user_id = c.user_id
    LEFT JOIN Personal_Constraints pc ON c.pc_id = pc.pc_id
    WHERE u.user_id = %s
    '''
    
    cursor.execute(query, (student_id,))
    result = cursor.fetchall()
    
    response = make_response(jsonify({"data": result}))
    response.status_code = 200
    return response
    

@users.route('/auth/admin/<int:admin_id>', methods=['GET'])
def get_admin_auth(admin_id):
    """Get admin details"""
    cursor = db.get_db().cursor()
    
    # Join User table with Admin table
    query = '''
    SELECT u.user_id, u.f_name as firstName, u.l_name as lastName, a.admin_id
    FROM User u
    JOIN Admin a ON u.user_id = a.user_id
    WHERE a.admin_id = %s
    '''
    
    cursor.execute(query, (admin_id,))
    result = cursor.fetchall()
    
    response = make_response(jsonify({"data": result}))
    response.status_code = 200
    return response

@users.route('/auth/health/<int:health_id>', methods=['GET'])
def get_health_auth(health_id):
    """Get health advisor details"""
    cursor = db.get_db().cursor()
    
    # Join User table with Health_Advisor table
    query = '''
    SELECT u.user_id, u.f_name as firstName, u.l_name as lastName, ha.advisor_id
    FROM User u
    JOIN Health_Advisor ha ON u.user_id = ha.user_id
    WHERE ha.advisor_id = %s
    '''
    
    cursor.execute(query, (health_id,))
    result = cursor.fetchall()
    
    response = make_response(jsonify({"data": result}))
    response.status_code = 200
    return response

# Add this to your user_routes.py file

@users.route('/fridge/<int:user_id>', methods=['GET'])
def get_user_fridge(user_id):
    """Get a user's fridge ID"""
    cursor = db.get_db().cursor()
    
    query = '''
    SELECT c.fridge_id
    FROM Client c
    WHERE c.user_id = %s
    '''
    
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    
    if not result:
        response = make_response(jsonify({"error": "User not found or no fridge assigned"}))
        response.status_code = 404
        return response
    
    response = make_response(jsonify(result))
    response.status_code = 200
    return response


@users.route('/nutritionist/<int:advisor_id>/clients', methods=['GET'])
def get_nutritionist_clients(advisor_id):
    """Get all clients assigned to a health advisor (nutritionist)"""
    cursor = db.get_db().cursor()
    
    try:
        query = '''
        SELECT c.client_id, u.f_name, u.l_name, pc.age_group, 
               pc.dietary_restrictions, pc.personal_diet, pc.budget
        FROM Client_Health_Advisor cha
        JOIN Client c ON cha.client_id = c.client_id
        JOIN User u ON c.user_id = u.user_id
        LEFT JOIN Personal_Constraints pc ON c.pc_id = pc.pc_id
        WHERE cha.advisor_id = %s
        ORDER BY u.l_name, u.f_name
        '''
        
        cursor.execute(query, (advisor_id,))
        clients = cursor.fetchall()
        
        response = make_response(jsonify(clients))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error fetching nutritionist clients: {str(e)}")
        response = make_response(jsonify({"error": "Could not fetch clients"}))
        response.status_code = 500
        return response

@users.route('/nutritionist/<int:advisor_id>/dietary-alerts', methods=['GET'])
def get_dietary_alerts(advisor_id):
    """Get dietary alerts for clients of a health advisor"""
    cursor = db.get_db().cursor()
    
    try:
        # This query identifies clients with nutrition tracking issues
        query = '''
        SELECT c.client_id, u.f_name, u.l_name, 
               CASE 
                   WHEN nt.sodium > 2300 THEN 'High sodium intake detected'
                   WHEN nt.protein < 50 THEN 'Low protein intake detected'
                   WHEN nt.calories < 1500 THEN 'Low calorie intake detected'
                   ELSE 'Unknown alert'
               END as alert_message,
               CASE 
                   WHEN nt.sodium > 2300 THEN 'Medium'
                   WHEN nt.protein < 50 THEN 'High'
                   WHEN nt.calories < 1500 THEN 'Medium'
                   ELSE 'Low'
               END as priority
        FROM Client_Health_Advisor cha
        JOIN Client c ON cha.client_id = c.client_id
        JOIN User u ON c.user_id = u.user_id
        JOIN Nutrition_Tracking nt ON c.client_id = nt.client_id
        WHERE cha.advisor_id = %s
        AND (nt.sodium > 2300 OR nt.protein < 50 OR nt.calories < 1500)
        ORDER BY 
            CASE priority
                WHEN 'High' THEN 1
                WHEN 'Medium' THEN 2
                WHEN 'Low' THEN 3
                ELSE 4
            END
        '''
        
        cursor.execute(query, (advisor_id,))
        alerts = cursor.fetchall()
        
        response = make_response(jsonify(alerts))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error fetching dietary alerts: {str(e)}")
        response = make_response(jsonify({"error": "Could not fetch dietary alerts"}))
        response.status_code = 500
        return response

@users.route('/nutritionist/<int:advisor_id>/nutrition-summary', methods=['GET'])
def get_nutrition_summary(advisor_id):
    """Get nutrition tracking summary for a health advisor's clients"""
    cursor = db.get_db().cursor()
    
    try:
        query = '''
        SELECT 
            pc.personal_diet as diet_type,
            AVG(nt.protein) as avg_protein,
            AVG(nt.carbs) as avg_carbs,
            AVG(nt.fat) as avg_fat
        FROM Client_Health_Advisor cha
        JOIN Client c ON cha.client_id = c.client_id
        JOIN Personal_Constraints pc ON c.pc_id = pc.pc_id
        JOIN Nutrition_Tracking nt ON c.client_id = nt.client_id
        WHERE cha.advisor_id = %s
        GROUP BY pc.personal_diet
        '''
        
        cursor.execute(query, (advisor_id,))
        nutrition_summary = cursor.fetchall()
        
        response = make_response(jsonify(nutrition_summary))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error fetching nutrition summary: {str(e)}")
        response = make_response(jsonify({"error": "Could not fetch nutrition summary"}))
        response.status_code = 500
        return response


# Add this to user_routes.py

@users.route('/client/<int:client_id>/workouts', methods=['GET'])
def get_client_workouts(client_id):
    """Get workouts for a specific client"""
    cursor = db.get_db().cursor()
    
    try:
        query = '''
        SELECT w.workout_id, w.name, w.quantity, w.weight, w.calories_burnt
        FROM Client_Workout cw
        JOIN Workout w ON cw.workout_id = w.workout_id
        WHERE cw.client_id = %s
        ORDER BY w.workout_id
        '''
        
        cursor.execute(query, (client_id,))
        workouts = cursor.fetchall()
        
        response = make_response(jsonify(workouts))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error fetching client workouts: {str(e)}")
        response = make_response(jsonify({"error": "Could not fetch workouts"}))
        response.status_code = 500
        return response



# Add these routes to user_routes.py

@users.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout"""
    data = request.json
    
    name = data.get('name')
    quantity = data.get('quantity')  # Duration in minutes
    weight = data.get('weight')      # Weight used if applicable
    calories_burnt = data.get('calories_burnt')
    
    if not name:
        response = make_response(jsonify({"error": "Workout name is required"}))
        response.status_code = 400
        return response

    cursor = db.get_db().cursor()
    try:
        # Insert workout
        cursor.execute(
            'INSERT INTO Workout (name, quantity, weight, calories_burnt) VALUES (%s, %s, %s, %s)',
            (name, quantity, weight, calories_burnt)
        )
        workout_id = cursor.lastrowid
        
        # Associate with client if client_id is provided
        client_id = data.get('client_id')
        if client_id:
            cursor.execute(
                'INSERT INTO Client_Workout (client_id, workout_id) VALUES (%s, %s)',
                (client_id, workout_id)
            )
            
        db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Workout created successfully", 
            "workout_id": workout_id
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error creating workout: {str(e)}")
        response = make_response(jsonify({"error": "Could not create workout"}))
        response.status_code = 500
        return response

@users.route('/workouts/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    """Update a workout"""
    data = request.json
    
    cursor = db.get_db().cursor()
    
    # Check if workout exists
    cursor.execute('SELECT * FROM Workout WHERE workout_id = %s', (workout_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "Workout not found"}))
        response.status_code = 404
        return response
    
    # Build update query dynamically
    update_fields = []
    params = []
    
    if 'name' in data:
        update_fields.append('name = %s')
        params.append(data['name'])
    
    if 'quantity' in data:
        update_fields.append('quantity = %s')
        params.append(data['quantity'])
    
    if 'weight' in data:
        update_fields.append('weight = %s')
        params.append(data['weight'])
    
    if 'calories_burnt' in data:
        update_fields.append('calories_burnt = %s')
        params.append(data['calories_burnt'])
    
    if not update_fields:
        response = make_response(jsonify({"error": "No fields to update"}))
        response.status_code = 400
        return response
    
    try:
        query = f"UPDATE Workout SET {', '.join(update_fields)} WHERE workout_id = %s"
        params.append(workout_id)
        cursor.execute(query, params)
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Workout updated successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error updating workout: {str(e)}")
        response = make_response(jsonify({"error": "Could not update workout"}))
        response.status_code = 500
        return response

@users.route('/workouts/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    """Delete a workout"""
    cursor = db.get_db().cursor()
    
    try:
        # First delete from Client_Workout (foreign key constraint)
        cursor.execute('DELETE FROM Client_Workout WHERE workout_id = %s', (workout_id,))
        
        # Then delete the workout
        cursor.execute('DELETE FROM Workout WHERE workout_id = %s', (workout_id,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            response = make_response(jsonify({"error": "Workout not found"}))
            response.status_code = 404
            return response
        
        response = make_response(jsonify({"message": "Workout deleted successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error deleting workout: {str(e)}")
        response = make_response(jsonify({"error": "Could not delete workout"}))
        response.status_code = 500
        return response