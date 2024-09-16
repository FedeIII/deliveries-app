def remove_elements_from_list(list, elements):
    return [element for element in list if element not in elements]


def get_first_missing_product(next_delivery_products, route_products):
    return next(
        (product_id for product_id in next_delivery_products if product_id not in route_products), None)


def get_product_warehouses(deliveries):
    product_warehouses = {}

    products_set = set(
        product for delivery in deliveries for product in delivery.products)
    unique_products = list(products_set)

    for product in unique_products:
        product_warehouses[product.id] = product.warehouses

    return product_warehouses


def get_warehouse_for_product(product_warehouses, product_id):
    # TO DO: pick the nearest warehouse for the product, instead of the first one in the list
    return product_warehouses[product_id][0]


def get_warehouse_product_ids(warehouse):
    return [product.id for product in warehouse.products]

def get_next_delivery(deliveries_left, delivery_map):
    # TO DO: pick the following delivery as the nearest one, instead of the first of the ones left
    next_delivery_id = deliveries_left[0]
    return delivery_map[next_delivery_id]

def get_first_step(product_warehouses, deliveries):
    # TO DO: pick as starting warehouse one with ALL or THE MOST products of ANY delivery
    first_product_id = deliveries[0].products[0].id
    first_warehouse = product_warehouses[first_product_id][0]
    return {
        "id": f"warehouse-{first_warehouse.id}",
        "lat": first_warehouse.lat,
        "lng": first_warehouse.lng,
        "products": get_warehouse_product_ids(first_warehouse),
        "deliveries_left": [delivery.id for delivery in deliveries]
    }


def get_next_delivery_step(next_delivery, previous_step):
    return {
        "id": f"delivery-{next_delivery.id}",
        "lat": next_delivery.lat,
        "lng": next_delivery.lng,
        "products": previous_step["products"],
        "deliveries_left": remove_elements_from_list(previous_step["deliveries_left"], [next_delivery.id])
    }


def get_next_warehouse_step(next_delivery_products, route_products, product_warehouses, previous_step):
    missing_product_id = get_first_missing_product(
        next_delivery_products, route_products)
    warehouse_for_missing_product = get_warehouse_for_product(
        product_warehouses, missing_product_id)
    return {
        "id": f"warehouse-{warehouse_for_missing_product.id}",
        "lat": warehouse_for_missing_product.lat,
        "lng": warehouse_for_missing_product.lng,
        "products": list(set(previous_step["products"] + get_warehouse_product_ids(warehouse_for_missing_product))),
        "deliveries_left": previous_step["deliveries_left"]
    }


def get_last_step(first_step, previous_step):
    last_step = first_step.copy()
    last_step.update({
        "products": previous_step["products"],
        "deliveries_left": previous_step["deliveries_left"]
    })
    return last_step


def calculate_route(deliveries):
    delivery_map = {delivery.id: delivery for delivery in deliveries}
    route = []
    product_warehouses = get_product_warehouses(deliveries)

    first_step = get_first_step(product_warehouses, deliveries)
    route.append(first_step)

    next_step = first_step.copy()

    while (len(next_step["deliveries_left"]) != 0):
        next_delivery = get_next_delivery(next_step["deliveries_left"], delivery_map)

        next_delivery_products = set(
            [product.id for product in next_delivery.products])
        route_products = set(next_step["products"])

        if (next_delivery_products.issubset(route_products)):
            next_step = get_next_delivery_step(next_delivery, next_step)
        else:
            next_step = get_next_warehouse_step(
                next_delivery_products, route_products, product_warehouses, next_step)

        route.append(next_step)

    last_step = get_last_step(first_step, next_step)
    route.append(last_step)

    return route
