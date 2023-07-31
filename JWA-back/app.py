import mysql.connector
from flask import Flask, jsonify, request


app = Flask(__name__)

# database connection parameters with MySQL database credentials
db_config = {
    'host': 'weights',
    'user': 'root',
    'password': 'password',
    'database': 'weights',
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to MySQL:", err)
        return None

def close_db_connection(conn):
    if conn:
        conn.close()

@app.route('/api/weights', methods=['GET', 'POST'])
def handle_weights():
    if request.method == 'GET':
        return get_weights()
    elif request.method == 'POST':
        return save_weight()

def get_weights():
    conn = get_db_connection()
    if not conn:
        return jsonify(error='Database connection error')

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM weights')
        weights = cursor.fetchall()
        return jsonify(weights)
    except mysql.connector.Error as err:
        print("Error executing query:", err)
        return jsonify(error='Error retrieving weights from the database')
    finally:
        cursor.close()
        close_db_connection(conn)

def save_weight():
    weight = request.json['weight']

    conn = get_db_connection()
    if not conn:
        return jsonify(error='Database connection error')

    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO weights (weight) VALUES (%s)', (weight,))
        conn.commit()
        return jsonify(message='Weight saved successfully')
    except mysql.connector.Error as err:
        print("Error executing query:", err)
        conn.rollback()
        return jsonify(error='Error saving weight to the database')
    finally:
        cursor.close()
        close_db_connection(conn)

if __name__ == '__main__':
    app.run(debug=True)
