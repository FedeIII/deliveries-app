from .errors import BadRequestError, NotFoundError


class DeliveryService:
    def __init__(self, deps):
        self.deps = deps

    def create(self, lat, lng):
        if not lat or not lng:
            raise BadRequestError("Missing delivery lat or lng")
        delivery = self.deps['Delivery'].create(lat, lng)
        return delivery

    def get(self, id):
        if not id:
            raise BadRequestError("Missing delivery id")
        delivery = self.deps['Delivery'].find(id)
        if not delivery:
            raise NotFoundError("Delivery not found")
        return delivery
