from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def create(username, password):
        password_hash = generate_password_hash(password)
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def find_user(username):
        return User.query.filter_by(username=username).first()


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def create(name):
        product = Product(name=name)
        db.session.add(product)
        db.session.commit()
        return product

    def find(id):
        return Product.query.filter_by(id=id).first()
    
    def find_all(ids):
        return Product.query.filter(Product.id.in_(ids)).all()


class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    products = db.relationship(
        'Product', secondary='warehouse_product', backref='warehouses')

    def create(name, lat, lng):
        warehouse = Warehouse(name=name, lat=lat, lng=lng)
        db.session.add(warehouse)
        db.session.commit()
        return warehouse

    def find(id):
        return Warehouse.query.filter_by(id=id).first()
    
    def set_products(self, products):
        self.products = products
        db.session.commit()
        return self
    


warehouse_product = db.Table('warehouse_product',
                             db.Column('warehouse_id', db.Integer, db.ForeignKey(
                                 'warehouse.id'), primary_key=True),
                             db.Column('product_id', db.Integer, db.ForeignKey(
                                 'product.id'), primary_key=True)
                             )


class Delivery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    products = db.relationship(
        'Product', secondary='delivery_product', backref='deliveries')
    
    def create(lat, lng):
        delivery = Delivery(lat=lat, lng=lng)
        db.session.add(delivery)
        db.session.commit()
        return delivery

    def find(id):
        return Delivery.query.filter_by(id=id).first()
    
    def set_products(self, products):
        self.products = products
        db.session.commit()
        return self


delivery_product = db.Table('delivery_product',
                            db.Column('delivery_id', db.Integer, db.ForeignKey(
                                'delivery.id'), primary_key=True),
                            db.Column('product_id', db.Integer, db.ForeignKey(
                                'product.id'), primary_key=True)
                            )
