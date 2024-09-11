from gateway import Gateway
from models import db, User, Product, Warehouse, Delivery
from services import UserService, ProductService, WarehouseService, DeliveryService
from routes import UserRoutes, ProductRoutes, WarehouseRoutes, DeliveryRoutes
from flask import Flask
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

db.init_app(app)

user_service = UserService({'User': User})
product_service = ProductService({'Product': Product})
warehouse_service = WarehouseService(
    {'Warehouse': Warehouse, 'Product': Product})
delivery_service = DeliveryService({'Delivery': Delivery, 'Product': Product})

user_routes = UserRoutes({
    'user_service': user_service
})
product_routes = ProductRoutes({
    'product_service': product_service
})
warehouse_routes = WarehouseRoutes({
    'warehouse_service': warehouse_service
})
delivery_routes = DeliveryRoutes({
    'delivery_service': delivery_service
})

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
