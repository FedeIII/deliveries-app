from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.errors import BadRequestError, NotFoundError


class WarehouseRoutes:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
        @app.route('/warehouses', methods=['POST'])
        @jwt_required()
        def add_warehouse():
            name = request.json.get('name', None)
            lat = request.json.get('lat', None)
            lng = request.json.get('lng', None)
            try:
                warehouse = self.deps['warehouse_service'].create(
                    name, lat, lng)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            else:
                return jsonify({"msg": "Warehouse created successfully", "id": warehouse.id}), 201

        @app.route('/warehouses/<warehouse_id>', methods=['GET'])
        @jwt_required()
        def get_warehouse(warehouse_id):
            try:
                warehouse = self.deps['warehouse_service'].get(warehouse_id)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0], "id": warehouse_id}), 404
            else:
                return jsonify({
                    "msg": "Warehouse found",
                    "payload": {
                        "id": warehouse.id,
                        "name": warehouse.name,
                        "latitude": warehouse.lat,
                        "longitude": warehouse.lng
                    }}), 201

        @app.route('/warehouses/<warehouse_id>', methods=['POST'])
        @jwt_required()
        def set_products(warehouse_id):
            product_ids = request.json.get('product_ids', [])

            try:
                warehouse = self.deps['warehouse_service'].set_products(
                    warehouse_id, product_ids)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0], "id": warehouse_id, "product_ids": product_ids}), 404
            else:
                return jsonify({
                    "msg": "Products set in the warehouse successfully",
                    "id": warehouse.id,
                    "product_ids": product_ids
                }), 201

        @app.route('/warehouses/<warehouse_id>/products', methods=['GET'])
        @jwt_required()
        def get_products(warehouse_id):
            try:
                products = self.deps['warehouse_service'].get_products(
                    warehouse_id)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0], "id": warehouse_id}), 404
            else:
                return jsonify({
                    "msg": "Products set in the warehouse successfully",
                    "id": warehouse_id,
                    "product_names": [product.name for product in products]
                }), 201
