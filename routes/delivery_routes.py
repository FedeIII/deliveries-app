from flask import request, jsonify
from flask_jwt_extended import jwt_required


class DeliveryRoutes:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
        @app.route('/deliveries', methods=['POST'])
        @jwt_required()
        def add_delivery():
            lat = request.json.get('lat', None)
            lng = request.json.get('lng', None)
            return jsonify({"lat": lat, "lng": lng}), 200

        @app.route('/deliveries/<delivery_id>', methods=['GET'])
        @jwt_required()
        def get_delivery(delivery_id):
            return jsonify({"delivery_id": delivery_id}), 200
