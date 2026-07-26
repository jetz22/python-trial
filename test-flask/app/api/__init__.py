from flask import Blueprint, jsonify, request

api_bp = Blueprint('api', __name__)

@api_bp.route('/users', methods=['GET'])
def get_users():
    return jsonify({"users": ["Alice", "Bob", "Charlie"]})

@api_bp.route('/hello', methods=['POST'])
def hello():
    data = request.get_json() or {}
    name = data.get('name', 'Guest')
    return jsonify({"message": f"Hello, {name}!"})
