from flask import Flask, request, jsonify
import sqlite3
import pickle
import os

app = Flask(__name__)

def get_db():
    return sqlite3.connect('users.db')

@app.route('/users', methods=['GET'])
def get_user():
    username = request.args.get('username')
    conn = get_db()
    cursor = conn.cursor()

    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    return jsonify({"user": result})


@app.route('/load_data', methods=['POST'])
def load_data():

    data = pickle.loads(request.data)
    return jsonify({"data": data})

# Vulnerable to Path Traversal
@app.route('/get_file', methods=['GET'])
def get_file():
    filename = request.args.get('filename')

    file_path = os.path.join('files', filename)
    with open(file_path, 'r') as f:
        content = f.read()
    return content

# Vulnerable to Mass Assignment
@app.route('/create_user', methods=['POST'])
def create_user():
    user_data = request.get_json()
    conn = get_db()
    cursor = conn.cursor()
    fields = ','.join(user_data.keys())
    values = ','.join([f"'{v}'" for v in user_data.values()])
    query = f"INSERT INTO users ({fields}) VALUES ({values})"
    cursor.execute(query)
    conn.commit()
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True)  # Debug mode enabled in production
