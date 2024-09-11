# 🚀 **DELIVERY TEST APP** 🚀

## 🌟 **Overview**

**Delivery Test App** is a server app built in **Flask** to manage **company deliveries**. It stores its data in **SQLite** through **SQLAlchemy**
It allows to create **products, warehouses and deliveries** and scaffolds the optimal route calculation for a specific delivery

---

## ✅ **Tasks Breakdown**

Tasks are estimated based on story points, considering 1 story point as the simplest task possible in the project

**Tasks**:  
- **Scaffolding**: [1sp] Create the skeleton of the project running in local with a working database
- **Define routes**: [1sp] API Gateway with the main routes defined
- **Auth and Aunthentication**: [2sp] Configure a JWT-based auth system to register and login users
- **Create and retrieve products**: [2sp] Service to create and get Products
- **Create and retrieve warehouses**: [2sp] Service to create and get Wharehouses
- **Create and retrieve deliveries**: [2sp] Service to create and get Deliveries
- **List products in warehouse**: [2sp] list_products method in Wharehouse service
- **List products in delivery**: [2sp] list_products method in Delivery service
- **Optimal route calculation**: [3sp] Approach definition for the algorithm and time estimation

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