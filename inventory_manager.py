# inventory_manager.py

from product import Product, Electronics, Furniture, Grocery

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def update_inventory(self, product_name, amount):
        for product in self.products:
            if product.product_name == product_name:
                product.update_inventory(amount)
                return
        raise ValueError("Product not found")

    def calculate_total_value(self, category=None):
        total_value = 0
        for product in self.products:
            if category is None or isinstance(product, category):
                total_value += product.get_total_value()
        return total_value

    def get_all_products(self):
        return self.products
