import os
import sys

import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Check for required environment variables
ITFLOW_API_KEY = os.getenv('ITFLOW_API_KEY') or 'none'
if ITFLOW_API_KEY == 'none':
    sys.exit('Error: IFLOW_API_KEY not provided.')

ITFLOW_DB_URI = os.getenv('ITFLOW_DB_URI') or 'none'
if ITFLOW_DB_URI == 'none':
    sys.exit('Error: ITFLOW_DB_URI not provided.')

ITFLOW_DB_PORT = os.getenv('ITFLOW_DB_PORT') or 'none'
if ITFLOW_DB_PORT == 'none':
    sys.exit('Error: ITFLOW_DB_PORT not provided.')

ITFLOW_DB_NAME = os.getenv('ITFLOW_DB_NAME') or 'none'
if ITFLOW_DB_NAME == 'none':
    sys.exit('Error: ITFLOW_DB_NAME not provided.')

ITFLOW_DB_USER = os.getenv('ITFLOW_DB_USER') or 'none'
if ITFLOW_DB_USER == 'none':
    sys.exit('Error: ITFLOW_DB_USER not provided.')

ITFLOW_DB_PASSWORD = os.getenv('ITFLOW_DB_PASSWORD') or 'none'
if ITFLOW_DB_PASSWORD == 'none':
    sys.exit('Error: ITFLOW_DB_PASSWORD not provided.')


@app.route('/ping', methods=['GET'])
def ping():  # put application's code here
    return 'Pong!'


@app.route('/ticket_replies', methods=['POST'])
def create_ticket_reply():
    # Request Body:
    # {
    #   ticket_reply: 'ticket reply',
    #   ticket_reply_by: contact or user id,
    #   ticket_reply_ticket_id: ticket id,
    #   ticket_reply_type: Internal | Client
    # }
    json = request.json

    ticket_reply = json['ticket_reply']
    ticket_reply_by = json['ticket_reply_by']
    ticket_reply_ticket_id = json['ticket_reply_ticket_id']
    ticket_reply_time_worked = '00:00:00'
    ticket_reply_type = json['ticket_reply_type']

    conn = mysql.connector.connect(
        host=ITFLOW_DB_URI,
        port=ITFLOW_DB_PORT,
        user=ITFLOW_DB_USER,
        password=ITFLOW_DB_PASSWORD,
        database=ITFLOW_DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO ticket_replies SET ticket_reply = '{ticket_reply}', ticket_reply_type = '{ticket_reply_type}', ticket_reply_time_worked = '{ticket_reply_time_worked}', ticket_reply_by = {ticket_reply_by}, ticket_reply_ticket_id = {ticket_reply_ticket_id}")
    conn.commit()

    row = cursor.fetchone()
    conn.close()
    return jsonify(row)


@app.route('/ticket_statuses', methods=['POST'])
def set_ticket_status():
    # Request Body:
    # {
    #   status_id: 'status_id',
    #   ticket_id: 'ticket_id',
    # }
    json = request.json

    status_id = json['status_id']
    ticket_id = json['ticket_id']

    conn = mysql.connector.connect(
        host=ITFLOW_DB_URI,
        port=ITFLOW_DB_PORT,
        user=ITFLOW_DB_USER,
        password=ITFLOW_DB_PASSWORD,
        database=ITFLOW_DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute(f'UPDATE tickets SET ticket_status = {status_id} WHERE ticket_id = {ticket_id}')
    conn.commit()
    conn.close()

    return jsonify({'success': 'True'})


@app.route('/ticket_statuses', methods=['GET'])
def get_ticket_statuses():
    conn = mysql.connector.connect(
        host=ITFLOW_DB_URI,
        port=ITFLOW_DB_PORT,
        user=ITFLOW_DB_USER,
        password=ITFLOW_DB_PASSWORD,
        database=ITFLOW_DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute('SELECT ticket_status_id, ticket_status_name FROM ticket_statuses')

    response = []

    for result in cursor.fetchall():
        ticket_status_id = result[0]
        ticket_status_name = result[1]

        response.append({'ticket_status_id': ticket_status_id, 'ticket_status_name': ticket_status_name})

    conn.close()
    return jsonify(response)


@app.route('/ticket_categories', methods=['POST'])
def add_ticket_category():
    # Request Body:
    # {
    #   category_id: 'category_id'
    #   ticket_id: 'ticket_id'
    # }
    json = request.json

    category_id = json['category_id']
    ticket_id = json['ticket_id']

    conn = mysql.connector.connect(
        host=ITFLOW_DB_URI,
        port=ITFLOW_DB_PORT,
        user=ITFLOW_DB_USER,
        password=ITFLOW_DB_PASSWORD,
        database=ITFLOW_DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute(f"UPDATE tickets SET ticket_category = {category_id} WHERE ticket_id = {ticket_id}")
    conn.commit()
    conn.close()

    return "done"


@app.route('/ticket_categories', methods=['GET'])
def get_ticket_categories():
    conn = mysql.connector.connect(
        host=ITFLOW_DB_URI,
        port=ITFLOW_DB_PORT,
        user=ITFLOW_DB_USER,
        password=ITFLOW_DB_PASSWORD,
        database=ITFLOW_DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute(
        "SELECT category_id, category_name, category_color, category_type FROM categories WHERE category_type = 'Ticket' AND category_archived_at IS NULL ORDER BY category_name ASC")

    response = []
    for result in cursor.fetchall():
        category_id = result[0]
        category_name = result[1]
        category_color = result[2]
        category_type = result[3]

        response.append({'category_id': category_id, 'category_name': category_name, 'category_color': category_color,
                         'category_type': category_type})

    conn.close()
    return jsonify(response)


@app.route('/categories', methods=['POST'])
def create_category():
    # Request Body:
    # {
    #   category: 'category',
    #   description: 'description',
    #   color: 'color',
    # }
    json = request.json

    category = json['category']
    description = json['description']
    color = json['color']

    conn = mysql.connector.connect(
        host=ITFLOW_DB_URI,
        port=ITFLOW_DB_PORT,
        user=ITFLOW_DB_USER,
        password=ITFLOW_DB_PASSWORD,
        database=ITFLOW_DB_NAME
    )

    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO categories SET category_name = '{category}', category_description = '{description}', category_type = 'Ticket', category_color = '{color}'")
    conn.commit()
    conn.close()

    return "done"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
