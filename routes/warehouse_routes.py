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
                    "msg": "Product found",
                    "payload": {
                        "id": warehouse.id,
                        "name": warehouse.name,
                        "latitude": warehouse.lat,
                        "longitude": warehouse.lng
                    }}), 201
