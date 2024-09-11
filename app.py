from gateway import Gateway
from services.user_service import UserService
from services.product_service import ProductService
from services.warehouse_service import WarehouseService
from routes.user_routes import UserRoutes
from routes.product_routes import ProductRoutes
from routes.warehouse_routes import WarehouseRoutes
from routes.delivery_routes import DeliveryRoutes
from flask import Flask
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv
from models import User, Product, Warehouse, db

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

db.init_app(app)

user_service = UserService({'User': User})
product_service = ProductService({'Product': Product})
warehouse_service = WarehouseService({'Warehouse': Warehouse})

user_routes = UserRoutes({
    'user_service': user_service
})
product_routes = ProductRoutes({
    'product_service': product_service
})
warehouse_routes = WarehouseRoutes({
    'warehouse_service': warehouse_service
})
delivery_routes = DeliveryRoutes({})

gateway = Gateway({
    'user_routes': user_routes,
    'product_routes': product_routes,
    'warehouse_routes': warehouse_routes,
    'delivery_routes': delivery_routes,
})
gateway.set_routes(app)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
