from .errors import BadRequestError, NotFoundError


class WarehouseService:
    def __init__(self, deps):
        self.deps = deps

    def create(self, name, lat, lng):
        if not name or not lat or not lng:
            raise BadRequestError("Missing warehouse name, lat, or lng")

        warehouse = self.deps['Warehouse'].create(name, lat, lng)
        return warehouse

    def get(self, id):
        if not id:
            raise BadRequestError("Missing warehouse id")

        warehouse = self.deps['Warehouse'].find(id)
        if not warehouse:
            raise NotFoundError("Warehouse not found")
        return warehouse

    def set_products(self, id, product_ids):
        if not product_ids or len(product_ids) == 0:
            raise BadRequestError("Missing product ids")

        warehouse = self.get(id)
        if not warehouse:
            raise NotFoundError("Warehouse not found")
        
        products = self.deps['Product'].find_all(product_ids)
        if len(products) != len(product_ids):
            raise NotFoundError("One or more products not found")
        
        warehouse.set_products(products)
        return warehouse

    def get_products(self, id):
        warehouse = self.get(id)
        if not warehouse:
            raise NotFoundError("Warehouse not found")
        
        if len(warehouse.products) == 0:
            raise NotFoundError("Warehouse without products")
        
        return warehouse.products
        
