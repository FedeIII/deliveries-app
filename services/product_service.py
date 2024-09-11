from .errors import BadRequestError, NotFoundError


class ProductService:
    def __init__(self, deps):
        self.deps = deps

    def create(self, name):
        if not name:
            raise BadRequestError("Missing product name")
        product = self.deps['Product'].create(name)
        return product

    def get(self, id):
        if not id:
            raise BadRequestError("Missing product id")
        product = self.deps['Product'].find(id)
        if not product:
            raise NotFoundError("Product not found")
        return product
