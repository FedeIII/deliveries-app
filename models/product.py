from models import db


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