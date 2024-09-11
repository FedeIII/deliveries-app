from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .product import Product
from .warehouse import Warehouse
from .delivery import Delivery
