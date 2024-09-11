
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from services.errors import BadRequestError, NotFoundError


class Gateway:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
        # User
        @app.route('/register', methods=['POST'])
        def register_user():
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            try:
                self.deps['user_service'].register(username, password)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            else:
                return jsonify({"msg": f"User {username} created successfully"}), 201

        @app.route('/login', methods=['POST'])
        def login_user():
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            if self.deps['user_service'].check_password(username, password):
                access_token = create_access_token(identity=username)
                return jsonify(access_token=access_token), 200
            return jsonify({"msg": "Bad username or password"}), 401

        # Product
        @app.route('/products', methods=['POST'])
        @jwt_required()
        def add_product():
            name = request.json.get('name', None)
            try:
                product = self.deps['product_service'].create(name)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            else:
                return jsonify({"msg": "Product created successfully", "id": product.id}), 201

        @app.route('/products/<product_id>', methods=['GET'])
        def get_product(product_id):
            try:
                product = self.deps['product_service'].get(product_id)
            except BadRequestError as error:
                return jsonify({"msg": error.args[0]}), 400
            except NotFoundError as error:
                return jsonify({"msg": error.args[0]}), 404
            else:
                return jsonify({
                    "msg": "Product found",
                    "payload": {
                        "id": product.id,
                        "name": product.name
                    }}), 201

        # Warehouse
        @app.route('/warehouses', methods=['POST'])
        @jwt_required()
        def add_warehouse():
            name = request.json.get('name', None)
            lat = request.json.get('lat', None)
            lng = request.json.get('lng', None)
            return jsonify({"name": name, "lat": lat, "lng": lng}), 200

        @app.route('/warehouses/<warehouse_id>', methods=['GET'])
        @jwt_required()
        def get_warehouse(warehouse_id):
            return jsonify({"warehouse_id": warehouse_id}), 200

        # Delivery
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
