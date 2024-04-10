from flask import Blueprint, jsonify, request
import json
import os

transaction_blueprint = Blueprint('transactions', __name__)

# Helper function to load transactions data from JSON file
import os

# Define the path to transactions.json relative to the current script
transactions_file_path = os.path.join(os.path.dirname(__file__), 'transactions.json')

# Helper function to load transactions data from JSON file
def load_transactions():
    if os.path.exists(transactions_file_path):
        with open(transactions_file_path, 'r') as file:
            return json.load(file)
    else:
        return {}

# Helper function to save transactions data to JSON file
def save_transactions(transactions_data):
    with open(transactions_file_path, 'w') as file:
        json.dump(transactions_data, file, indent=4)


@transaction_blueprint.route('/transaction/<id>', methods=['GET'])
def get_transaction(id):
    transactions_data = load_transactions()
    transaction = transactions_data.get(id)
    if transaction:
        return jsonify(transaction), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404

@transaction_blueprint.route('/transaction', methods=['POST'])
def add_transaction():
    transaction_data = request.get_json()
    if not transaction_data or 'description' not in transaction_data or 'amount' not in transaction_data or 'date' not in transaction_data:
        return jsonify({'error': 'Incomplete transaction data'}), 400

    transactions_data = load_transactions()
    transaction_id = str(len(transactions_data) + 1)
    transaction_data['id'] = transaction_id
    transactions_data[transaction_id] = transaction_data
    save_transactions(transactions_data)

    return jsonify(transaction_data), 201

@transaction_blueprint.route('/transaction/<id>', methods=['PUT'])
def update_transaction(id):
    transaction_data = request.get_json()
    if not transaction_data:
        return jsonify({'error': 'No data provided for update'}), 400

    transactions_data = load_transactions()
    if id in transactions_data:
        transactions_data[id].update(transaction_data)
        save_transactions(transactions_data)
        return jsonify(transactions_data[id]), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404

@transaction_blueprint.route('/transaction/<id>', methods=['DELETE'])
def delete_transaction(id):
    transactions_data = load_transactions()
    if id in transactions_data:
        del transactions_data[id]
        save_transactions(transactions_data)
        return jsonify({'message': 'Transaction deleted'}), 200
    else:
        return jsonify({'message': 'Transaction not found'}), 404

@transaction_blueprint.route('/transactions', methods=['GET'])
def get_all_transactions():
    transactions_data = load_transactions()
    return jsonify(list(transactions_data.values())), 200
