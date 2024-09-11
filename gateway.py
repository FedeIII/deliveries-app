
from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from services.errors import BadRequestError, NotFoundError


class Gateway:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
        self.deps['user_routes'].set_routes(app)
        self.deps['product_routes'].set_routes(app)
        self.deps['warehouse_routes'].set_routes(app)
        self.deps['delivery_routes'].set_routes(app)
