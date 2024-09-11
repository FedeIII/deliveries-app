from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.errors import BadRequestError, NotFoundError


class DeliveryRoutes:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
        @app.route('/deliveries', methods=['POST'])
        @jwt_required()
        def add_delivery():
            lat = request.json.get('lat', None)
            lng = request.json.get('lng', None)
            try:
                delivery = self.deps['delivery_service'].create(lat, lng)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            else:
                return jsonify({"msg": "Warehouse created successfully", "id": delivery.id}), 201

        @app.route('/deliveries/<delivery_id>', methods=['GET'])
        @jwt_required()
        def get_delivery(delivery_id):
            try:
                delivery = self.deps['delivery_service'].get(delivery_id)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0], "id": delivery_id}), 404
            else:
                return jsonify({
                    "msg": "Delivery found",
                    "payload": {
                        "id": delivery.id,
                        "latitude": delivery.lat,
                        "longitude": delivery.lng
                    }}), 201
