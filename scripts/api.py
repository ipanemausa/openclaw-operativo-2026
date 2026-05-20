from flask import Blueprint, jsonify

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/status')
def status():
    return jsonify({"status": "active", "message": "API Blueprint is working!"})
