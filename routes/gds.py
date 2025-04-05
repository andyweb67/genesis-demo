from flask import Blueprint, jsonify

gds_routes = Blueprint("gds_routes", __name__)

@gds_routes.route('/', methods=['POST'])
def generate_gds():
    return jsonify({"message": "GDS generated successfully"})
