from models import db


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
