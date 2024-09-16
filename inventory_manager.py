# inventory_manager.py

from product import Product

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def update_inventory(self, product_name, amount):
        for product in self.products:
            if product.name == product_name:
                product.update_inventory(amount)
                return
        raise ValueError("Product not found")

    def calculate_total_value(self):
        total_value = 0
        for product in self.products:
            total_value += product.get_total_value()
        return total_value

    def get_products_by_category(self, category):
        return [product for product in self.products if product.category == category]

    def get_all_products(self):
        return self.products
