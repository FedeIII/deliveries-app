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
