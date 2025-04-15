from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

ingredients = Blueprint('ingredients', __name__)

@ingredients.route('/', methods=['GET'])
def get_all_ingredients():
    """Get list of all ingredients - Used by Alvin for ingredient management [Alvin-1]"""
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM Ingredient')
    ingredients_data = cursor.fetchall()
    
    response = make_response(jsonify(ingredients_data))
    response.status_code = 200
    return response

@ingredients.route('/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    """Get ingredient details with macronutrients - Used by Nancy for nutritional tracking [Nancy-5]"""
    cursor = db.get_db().cursor()

    # Get ingredient basic info
    cursor.execute('SELECT * FROM Ingredient WHERE ingredient_id = %s', (ingredient_id,))
    ingredient = cursor.fetchone()

    if not ingredient:
        response = make_response(jsonify({"error": "Ingredient not found"}))
        response.status_code = 404
        return response
    
    # Get macronutrients
    cursor.execute('''
        SELECT m.* 
        FROM Macronutrients m
        WHERE m.ingredient_id = %s
    ''', (ingredient_id,))
    macros = cursor.fetchone()
    
    result = {
        "ingredient": ingredient,
        "macronutrients": macros
    }

    response = make_response(jsonify(result))
    response.status_code = 200
    return response



@ingredients.route('/', methods=['POST'])
def add_ingredient():
    """Add new trusted ingredient with macros - Used by Alvin to add trusted food items [Alvin-5]"""
    data = request.json

    name = data.get('name')
    expiration_date = data.get('expiration_date')
    macros = data.get('macros', {})

    if not name:
        response = make_response(jsonify({"error": "Ingredient name is required"}))
        response.status_code = 400
        return response
    
    cursor = db.get_db().cursor()
    try:
        # Insert ingredient
        cursor.execute(
            'INSERT INTO Ingredient (name, expiration_date) VALUES (%s, %s)',
            (name, expiration_date)
        )
        ingredient_id = cursor.lastrowid

        if macros:
            cursor.execute(
                '''INSERT INTO Macronutrients (
                    ingredient_id, protein, fat, fiber, vitamin, sodium, calories, carbs
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                (
                    ingredient_id, 
                    macros.get('protein', 0), 
                    macros.get('fat', 0), 
                    macros.get('fiber', 0),
                    macros.get('vitamin', 0),
                    macros.get('sodium', 0),
                    macros.get('calories', 0),
                    macros.get('carbs', 0)
                )
            )

            db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Ingredient added successfully", 
            "ingredient_id": ingredient_id
        }))
        response.status_code = 201
        return response
    except Exception as e:
        current_app.logger.error(f"Error adding ingredient: {str(e)}")
        response = make_response(jsonify({"error": "Could not add ingredient"}))
        response.status_code = 500
        return response


@ingredients.route('/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    """Update ingredient details or category"""
    data = request.json
    
    cursor = db.get_db().cursor()

    # Check if ingredient exists
    cursor.execute('SELECT * FROM Ingredient WHERE ingredient_id = %s', (ingredient_id,))
    if not cursor.fetchone():
        response = make_response(jsonify({"error": "Ingredient not found"}))
        response.status_code = 404
        return response
    
    name = data.get('name')
    expiration_date = data.get('expiration_date')
    
    update_fields = []
    params = []
    
    if name:
        update_fields.append('name = %s')
        params.append(name)
    
    if expiration_date:
        update_fields.append('expiration_date = %s')
        params.append(expiration_date)

     if not update_fields:
        response = make_response(jsonify({"error": "No fields to update"}))
        response.status_code = 400
        return response
    
    try:
        query = f"UPDATE Ingredient SET {', '.join(update_fields)} WHERE ingredient_id = %s"
        params.append(ingredient_id)
        cursor.execute(query, params)
        db.get_db().commit()
        
        response = make_response(jsonify({"message": "Ingredient updated successfully"}))
        response.status_code = 200
        return response
    
    except Exception as e:
        current_app.logger.error(f"Error updating ingredient: {str(e)}")
        response = make_response(jsonify({"error": "Could not update ingredient"}))
        response.status_code = 500
        return response
    

@ingredients.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    """Delete unused/expired ingredient"""
    cursor = db.get_db().cursor()

    try:
        # Delete from fridge inventory first (foreign key constraint)
        cursor.execute('DELETE FROM Fridge_Inventory WHERE ingredient_id = %s', (ingredient_id,))

         # Delete from macronutrients
        cursor.execute('DELETE FROM Macronutrients WHERE ingredient_id = %s', (ingredient_id,))
        
        # Delete the ingredient
        cursor.execute('DELETE FROM Ingredient WHERE ingredient_id = %s', (ingredient_id,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            response = make_response(jsonify({"error": "Ingredient not found"}))
            response.status_code = 404
            return response
        
        response = make_response(jsonify({"message": "Ingredient deleted successfully"}))
        response.status_code = 200
        return response
    except Exception as e:
        current_app.logger.error(f"Error deleting ingredient: {str(e)}")
        response = make_response(jsonify({"error": "Could not delete ingredient"}))
        response.status_code = 500
        return response
























