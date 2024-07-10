from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'user',
    'password': 'userpassword',
    'database': 'my_database'
}
return_data_num = 10

last_checked_data = None

@app.route('/api/set-return-num/<int:num>', methods=['GET'])
def set_return_num(num):
    global return_data_num
    return_data_num = num
    return jsonify({'message': f'Successfully set the number of records to return to {num}'})

@app.route('/api/should-reload', methods=['GET'])
def test_should_reload():

    global last_checked_data
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        # total number of records in the database 
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM transactions ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        records = cursor.fetchall()
        

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT COUNT(*) FROM transactions"
        cursor.execute(query)
        total_records = cursor.fetchall()
        count = total_records[0]['COUNT(*)']


        # Closing the cursor and connection
        cursor.close()
        connection.close()
        print (f"last_checked_data: {last_checked_data}, count: {count}")
        if last_checked_data != count:
            last_checked_data = count
            return jsonify({'reload': True}), 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return jsonify({'reload': False}), 500, {'Access-Control-Allow-Origin': '*'}
    except Error as e:
        print(f"Error: {e}")
        return jsonify({'Error': True}), 500, {'Access-Control-Allow-Origin': '*'}
#
#   


def get_db_connection():
    """Function to get a database connection."""
    try:
        mydb = mysql.connector.connect(
                host="localhost",
                user="user",
                password="userpassword",
                database="my_database"
            )
        connection = mydb
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/api/last-10-records', methods=['GET'])
def get_last_10_records():
    global last_checked_data
    """Endpoint to get the last 10 records from the database."""
    connection = get_db_connection()
    if connection is None:
        return jsonify({'error': 'Failed to connect to the database'}), 500

    cursor = connection.cursor(dictionary=True)

    try:
        limit = return_data_num
        query = "SELECT * FROM transactions ORDER BY id DESC LIMIT %s" % limit
        cursor.execute(query)
        records = cursor.fetchall()

        # Closing the cursor and connection
        cursor.close()
        connection.close()

        # total number of records in the database 
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT COUNT(*) FROM transactions"
        cursor.execute(query)
        total_records = cursor.fetchall()
        count = total_records[0]['COUNT(*)']
        last_checked_data = count

        return jsonify(records)

    except Error as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Failed to fetch data'}), 500
# print("Server is running", get_last_10_records())
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3308)
