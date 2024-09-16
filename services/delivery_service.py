from .errors import BadRequestError, NotFoundError
from domain.calculate_route import calculate_route


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

    def set_products(self, id, product_ids):
        if not product_ids or len(product_ids) == 0:
            raise BadRequestError("Missing product ids")

        delivery = self.get(id)
        if not delivery:
            raise NotFoundError("Delivery not found")

        products = self.deps['Product'].find_all(product_ids)
        if len(products) != len(product_ids):
            raise NotFoundError("One or more products not found")

        delivery.set_products(products)
        return delivery

    def get_products(self, id):
        delivery = self.get(id)
        if not delivery:
            raise NotFoundError("Delivery not found")

        if len(delivery.products) == 0:
            raise NotFoundError("Delivery without products")

        return delivery.products

    def get_route(self, delivery_ids):
        deliveries = [self.get(id) for id in delivery_ids]
        if len(deliveries) != len(delivery_ids):
            raise NotFoundError("One or more deliveries not found")

        return calculate_route(deliveries)
