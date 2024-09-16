# 🚀 **DELIVERY TEST APP** 🚀

## 🌟 **Overview**

**Delivery Test App** is a server app built in **Flask** to manage **company deliveries**. It stores its data in **SQLite** through **SQLAlchemy**
It allows to create **products, warehouses and deliveries** and scaffolds the optimal route calculation for a specific delivery

---

## ✅ **Tasks Breakdown**

Tasks are estimated based on story points, considering 1 story point as the simplest task possible in the project

**Tasks**:

- **Scaffolding**:
  - [1sp] Create the skeleton of the project running in local with a working database
- **Define routes**:
  - [1sp] API Gateway with the main routes defined
- **Authentication and Authorization**:
  - [2sp] Configure a JWT-based auth system to register and login users
- **Create and retrieve products**:
  - [2sp] Service to create and get Products
- **Create and retrieve warehouses**:
  - [2sp] Service to create and get Wharehouses
- **Create and retrieve deliveries**:
  - [2sp] Service to create and get Deliveries
- **Set and list products in warehouse**:
  - [3sp] set_products and list_products endpoints and Wharehouse service methods
- **Set and list products in delivery**:
  - [3sp] set_prodcuts and list_products endpoints and Delivery service methods
- **Optimal route calculation**:
  - [3sp] Approach definition for the algorithm and time estimation

---

## ✅ **Install and run**

Create and activate a virtual environment:

```console
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```console
pip install -r requirements.txt
```

Create a .env file with the correct values (you can copy the .env.example for local dev)

Run the app:

```console
./run.sh
```

Run the tests:

```console
./run-tests.sh
```

## ✅ **Assuptions and considerations**

### Considerations:

- I was completely unfamiliar with Flask and SQLAlchemy, which I have first used in this exercise. My knowledge of python was very limited and I had to learn and remember lots of things.
- Tests were added for the domain logic (only the `calculate_route` function). I considered that the rest of functionality didn't deserve unit testing (as it was basic framework functionality) and I wasn't considering integration or e2e tests.
- I've implemented a very basic dependency injection system. I'm used to working with these, both custom and existing in a library. I'm unaware whether they are commonly used in python backends.
- To calculate the optimal route, the users pass a list of deliveries by id and expect a list of steps for the route:

```
{
    "id": <ID of the next delivery or warehouse in the route>
    "lat", "lng": <Location of the next step in the route>
    "products": <List of picked products (IDs) for the route>
    "deliveries_left": <List of deliveries (IDs) yet to do>
}
```

### Assumptions:

For the sake of simplicity, as a first iteration to solve the problem, these assumptions were made:

1. It is assumed that if a warehouse has a product, has an unlimited amount of it
2. If the transport passes through a warehouse, all the warehouse's products are picked by it
3. The route starts in a warehouse where the first product of the first delivery exists. I should end in that same warehouse
4. The deliveries are not sorted, their order is defined by the user
5. The next step is picked depending whether the transport has the products for the next delivery available or not:
   - If available, it goes to the next delivery left
   - If not, it goes to the first warehouse found which has the product available

The next iterations for the solution should attack each of these assumptions:

1. Incorporate the concept of multiple items of the same product in warehouses and deliveries.
   This can be done by either adding an "amount" column to both relation tables (delivery_product and warehouse_product) or by adding multiple entries to those tables
2. The transport needs to track the amount of products needed for the delivery, the amount left on it and whether the destination warehouse has enough
3. The optimal route algorithm should output the optimal start location
4. The optimal route algorithm should pick the next delivery (precalculated or dynamically)

## 📈 **Optimal route calculation**

For the optimal route calculation, I would solve it as a **Traveling Salesman Problem** with extra complexity because of the product constraints. These are the different approaches I would try with their story points:

1. [3sp] **Greedy algorithm**: With the same starting point assumption than the current one, pick the next delivery based on proximity. When not enough products are available, pick the nearest warehouse too.
2. [5sp] If a more optimal solution is needed, try with **Google's OR-Tools** or a similar optimization library
3. [13sp] If there are hidden constraints or too difficult to model and extra optimization is needed, **Genetic Algorithms** could leverage those.
