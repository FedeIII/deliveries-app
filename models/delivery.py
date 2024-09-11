from models import db


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
