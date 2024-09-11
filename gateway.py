
from flask import request, jsonify
            
class Gateway:
    def __init__(self, deps):
        self.deps = deps
        
    def set_routes(self, app):
        # User
        @app.route('/register', methods=['POST'])
        def register_user():
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            return jsonify({"username": username, "password": password}), 200
        
        @app.route('/login', methods=['POST'])
        def login_user():
            username = request.json.get('username', None)
            password = request.json.get('password', None)
            return jsonify({"username": username, "password": password}), 200
        
        # Product
        @app.route('/products', methods=['POST'])
        def add_product():
            name = request.json.get('name', None)
            return jsonify({"name": name}), 200
        
        @app.route('/products/<product_id>', methods=['GET'])
        def get_product(product_id):
            return jsonify({"product_id": product_id}), 200
        
        # Warehouse
        @app.route('/warehouses', methods=['POST'])
        def add_warehouse():
            name = request.json.get('name', None)
            lat = request.json.get('lat', None)
            lng = request.json.get('lng', None)
            return jsonify({"name": name, "lat": lat, "lng": lng}), 200
        
        @app.route('/warehouses/<warehouse_id>', methods=['GET'])
        def get_warehouse(warehouse_id):
            return jsonify({"warehouse_id": warehouse_id}), 200
        
        # Delivery
        @app.route('/deliveries', methods=['POST'])
        def add_delivery():
            lat = request.json.get('lat', None)
            lng = request.json.get('lng', None)
            return jsonify({"lat": lat, "lng": lng}), 200
        
        @app.route('/deliveries/<delivery_id>', methods=['GET'])
        def get_delivery(delivery_id):
            return jsonify({"delivery_id": delivery_id}), 200