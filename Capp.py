import time
import json
import os

# ================== PRODUCT DATA ==================
doritos = {
    "variant": ["nacho cheese", "cool ranch", "spicy nacho", "sweet chili"],
    "price": 15000,
    "stock": 10,
    "sold": 0,
    "Product_code": "1DRT421"
}

ben_jerrys = {
    "variant": ["chocolate fudge brownie", "cookie dough", "vanilla", "strawberry cheesecake", "mint chocolate"],
    "price": 30000,
    "stock": 10,
    "sold": 0,
    "Product_code": "1BJR422"
}

ramen = {
    "variant": ["chicken", "beef", "shrimp", "spicy"],
    "price": 8000,
    "stock": 10,
    "sold": 0,
    "Product_code": "1RMN423"
}
# ================== HISTORY ==================
HISTORY_FILE = "sales_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# ================== FUNCTION ==================
def view_products():
    print("=== Doritos ===")
    print(json.dumps(doritos, indent=4))
    print("=== Ben & Jerry's ===")
    print(json.dumps(ben_jerrys, indent=4))
    print("=== Ramen ===")
    print(json.dumps(ramen, indent=4))

def edit_product():
    print("1. Doritos\n2. Ben & Jerry's\n3. Ramen")
    choice = input("Choose product: ")

    if choice == "1":
        product = doritos
        name = "Doritos"
    elif choice == "2":
        product = ben_jerrys
        name = "Ben & Jerry's"
    elif choice == "3":
        product = ramen
        name = "Ramen"
    else:
        print("Invalid choice")
        return

    print("1. Price\n2. Stock\n3. Sold\n4. Variant")
    opt = input("What to edit: ")

    if opt == "1":
        product["price"] = int(input("New price: "))
    elif opt == "2":
        product["stock"] = int(input("New stock: "))
    elif opt == "3":
        product["sold"] = int(input("New sold: "))
    elif opt == "4":
        product["variant"] = input("Variants (comma separated): ").split(",")
    else:
        print("Invalid choice")
        return

    print(f"{name} updated successfully!")

def purchase():
    
    print("1. Doritos\n2. Ben & Jerry's\n3. Ramen")
    choice = input("Choose product: ")

    if choice == "1":
        product =doritos
        name = "Doritos"
    elif choice == "2":
        product = ben_jerrys
        name = "Ben & Jerry's"
    elif choice == "3":
        product = ramen
        name = "Ramen"
    else:
        print("Invalid choice")
        return

    print("Available variants:", ", ".join(product["variant"]))
    variant = input("Choose variant: ")

    if variant not in product["variant"]:
        print("Variant not available!")
        return

    try:
        qty = int(input("Quantity: "))
    except:
        print("Input must be a number!")
        return

    if qty <= 0:
        print("Quantity must be > 0")
        return

    if product["stock"] < qty:
        print("Not enough stock!")
        return

    total = qty * product["price"]

    # update product
    product["stock"] -= qty
    product["sold"] += qty

    # save history
    history = load_history()
    history.append({
        "product": name,
        "variant": variant,
        "qty": qty,
        "price": product["price"],
        "total": total,
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    })
    save_history(history)

    print("\n=== RECEIPT ===")
    print(f"Product : {name}")
    print(f"Variant : {variant}")
    print(f"Qty     : {qty}")
    print(f"Total   : {total}")
    print("==============\n")

def view_history():
    history = load_history()

    if not history:
        print("No sales history found.")
        return

    print("=== SALES HISTORY ===")
    total_all = 0

    for i, h in enumerate(history, 1):
        print(f"{i}. {h['time']} | {h['product']} ({h['variant']}) | {h['qty']} x {h['price']} = {h['total']}")
        total_all += h["total"]

    print(f"\nTotal all purchases: {total_all}")

# ================== MAIN LOOP ==================
while True:
    print("""
=== MENU ===
1. View products
2. Edit products
3. Purchase
4. View sales history
5. Exit
""")

    option = input("Choose option: ")

    if option == "1":
        view_products()
    elif option == "2":
        edit_product()
    elif option == "3":
        purchase()
    elif option == "4":
        view_history()
    elif option == "5":
        print("Bye!")
        break
    else:
        print("Option is not valid.")