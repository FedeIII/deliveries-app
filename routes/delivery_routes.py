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
                return jsonify({"msg": "Delivery created successfully", "id": delivery.id}), 201

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

        @app.route('/deliveries/<delivery_id>', methods=['POST'])
        @jwt_required()
        def set_delivery_products(delivery_id):
            product_ids = request.json.get('product_ids', [])

            try:
                delivery = self.deps['delivery_service'].set_products(
                    delivery_id, product_ids)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0], "id": delivery_id, "product_ids": product_ids}), 404
            else:
                return jsonify({
                    "msg": "Products set in the delivery successfully",
                    "id": delivery.id,
                    "product_ids": product_ids
                }), 201

        @app.route('/deliveries/<delivery_id>/products', methods=['GET'])
        @jwt_required()
        def get_delivery_products(delivery_id):
            try:
                products = self.deps['delivery_service'].get_products(
                    delivery_id)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0], "id": delivery_id}), 404
            else:
                return jsonify({
                    "msg": "Products set in the delivery successfully",
                    "id": delivery_id,
                    "product_names": [product.name for product in products]
                }), 201

        @app.route('/deliveries/route', methods=['GET'])
        @jwt_required()
        def get_delivery_route():
            try:
                delivery_ids = request.json.get('delivery_ids', [])
                route = self.deps['delivery_service'].get_route(
                    delivery_ids)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0]}), 404
            else:
                return jsonify({
                    "msg": "Route calculated successfully",
                    "route": [warehouse for warehouse in route]
                }), 201
