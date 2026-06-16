import os
import sys

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

ITFLOW_API_KEY = ''
ITFLOW_DB_URI = ''
ITFLOW_DB_PORT = ''
ITFLOW_DB_NAME = ''
ITFLOW_DB_USER = ''
ITFLOW_DB_PASSWORD = ''

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

app.config['SQLALCHEMY_DATABASE_URI'] = f'mariadb+mariadbconnector:///{ITFLOW_DB_USER}:{ITFLOW_DB_PASSWORD}@{ITFLOW_DB_URI}:{ITFLOW_DB_PORT}/{ITFLOW_DB_NAME}'
app.config['ITFLOW_API_KEY'] = ITFLOW_API_KEY

db = SQLAlchemy(app)

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
    # }
    json = request.json

    ticket_reply = json['ticket_reply']
    ticket_reply_by = json['ticket_reply_by']
    ticket_reply_ticket_id = json['ticket_reply_ticket_id']
    ticket_reply_time_worked = '00:00:00'
    ticket_reply_type = 'Internal'

    with db.engine.connect() as conn:
        reply_id = conn.execute(f"INSERT INTO ticket_replies SET ticket_reply = '{ticket_reply}', ticket_reply_type = '{ticket_reply_type}', ticket_reply_time_worked = '{ticket_reply_time_worked}', ticket_reply_by = {ticket_reply_by}, ticket_reply_ticket_id = {ticket_reply_ticket_id};")

        response = {
            'Reply ID': reply_id,
        }

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

    with db.engine.connect() as conn:
        conn.execute(f"UPDATE tickets SET ticket_category = {category_id} WHERE ticket_id = {ticket_id}")

@app.route('/ticket_categories', methods=['GET'])
def get_ticket_categories():
    # Required filter: SELECT category_id, category_name FROM categories WHERE category_type = 'Ticket' AND category_archived_at IS NULL ORDER BY category_name ASC
    with db.engine.connect() as conn:
        result = conn.execute("SELECT category_id, category_name FROM categories WHERE category_type = 'Ticket' AND category_archived IS NULL ORDER BY category_name ASC")

        response = {
            f'Record {i}': list(row)
            for i, row in enumerate(result, start=1)
        }

    return jsonify(response)

@app.route('/categories', methods=['POST'])
def create_category():
    # Request Body:
    # {
    #   category: 'category',
    #   subcategory: 'subcategory',
    #   description: 'description',
    #   color: 'color',
    # }
    json = request.json

    category = f'{json['category']} - {json['subcategory']}'
    description = json['description']
    color = json['color']

    with db.engine.connect() as conn:
        category_id = conn.execute(f"INSERT INTO categories SET category_name = '{category}', category_description = '{description}', category_type = 'Ticket', category_color = '{color}'")

        response = jsonify(category_id)

    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True)
