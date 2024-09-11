from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.errors import BadRequestError, NotFoundError


class ProductRoutes:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
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
                return jsonify({"msg": error.args[0], "id": product_id}), 404
            else:
                return jsonify({
                    "msg": "Product found",
                    "payload": {
                        "id": product.id,
                        "name": product.name
                    }}), 201
