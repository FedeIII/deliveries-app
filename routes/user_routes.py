from flask import request, jsonify
from flask_jwt_extended import create_access_token
from services.errors import BadRequestError


class UserRoutes:
    def __init__(self, deps):
        self.deps = deps

    def set_routes(self, app):
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
