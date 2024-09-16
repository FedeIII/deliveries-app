import unittest
from domain.calculate_route import calculate_route


class Product:
    def __init__(self, id):
        self.id = id


class Warehouse:
    def __init__(self, id, lat, lng, products):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.products = products


class Delivery:
    def __init__(self, id, lat, lng, products):
        self.id = id
        self.lat = lat
        self.lng = lng
        self.products = products


class TestCalculateRoute(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product1 = Product(1)
        cls.product2 = Product(2)
        cls.product3 = Product(3)

        cls.warehouse1 = Warehouse(1, 15, 16, [cls.product1, cls.product2])
        cls.warehouse2 = Warehouse(2, 17, 18, [cls.product2, cls.product3])

        cls.delivery1 = Delivery(1, 10, 11, [cls.product3])
        cls.delivery2 = Delivery(2, 12, 13, [cls.product2])
        cls.delivery3 = Delivery(3, 12, 13, [cls.product1])

        cls.product1.warehouses = [cls.warehouse1]
        cls.product2.warehouses = [cls.warehouse1, cls.warehouse2]
        cls.product3.warehouses = [cls.warehouse2]

    def test_calculate_route(self):
        route = calculate_route(
            [self.delivery1, self.delivery2, self.delivery3])
        step_ids = [step["id"] for step in route]
        self.assertEqual(step_ids, [
                         'warehouse-2', 'delivery-1', 'delivery-2', 'warehouse-1', 'delivery-3', 'warehouse-2'])


if __name__ == '__main__':
    unittest.main()
