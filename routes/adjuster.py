from flask import Blueprint, jsonify

adjuster_routes = Blueprint("adjuster_routes", __name__)

@adjuster_routes.route('/', methods=['POST'])
def handle_adjuster_questions():
    return jsonify({"message": "Adjuster questions processed successfully"})