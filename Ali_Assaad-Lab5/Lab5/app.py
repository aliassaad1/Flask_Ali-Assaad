from flask import Flask, jsonify, request

from flask_cors import CORS
from Database import create_table
from Database import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to the User Management API!"

@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/add', methods=['POST'])
def api_insert_user():
    user_data = request.get_json()
    return jsonify(insert_user(user_data))

@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user_by_id(user_id):
    return jsonify(get_user_by_id(user_id))

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user_data = request.get_json()
    return jsonify(update_user(user_data))

@app.route('/api/users/delete/<int:user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))


def get_users():
    users = []
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()
        users = [dict(row) for row in rows]
    except Exception as e:
        print(f"Error getting users: {e}")
    finally:
        conn.close()
    return users

def insert_user(user):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)",
                    (user['name'], user['email'], user['phone'], user['address'], user['country']))
        conn.commit()
        return get_user_by_id(cur.lastrowid)
    except Exception as e:
        print(f"Error inserting user: {e}")
        conn.rollback()
    finally:
        conn.close()

def get_user_by_id(user_id):
    user = {}
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = dict(cur.fetchone())
    except Exception as e:
        print(f"Error getting user by id: {e}")
    finally:
        conn.close()
    return user

def update_user(user):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id =?",
                    (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"]))
        conn.commit()
        return get_user_by_id(user["user_id"])
    except Exception as e:
        print(f"Error updating user: {e}")
        conn.rollback()
    finally:
        conn.close()

def delete_user(user_id):
    message = {}
    try:
        conn = get_db_connection()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except Exception as e:
        print(f"Error deleting user: {e}")
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()
    return message

if __name__ == '__main__':
    create_table()  # Ensure the table is created upon startup
    app.run(debug=True)