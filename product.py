# product.py

class Product:
    def __init__(self, product_name, price, supplier_info):
        self.product_name = product_name
        self.price = price
        self._supplier_info = supplier_info  # Sensitive info
        self._inventory_level = 0  # Protected attribute

    def update_inventory(self, amount):
        self._inventory_level += amount

    def get_inventory_level(self):
        return self._inventory_level

    def get_total_value(self):
        return self._inventory_level * self.price

    def __str__(self):
        return f"{self.product_name} | ${self.price:.2f} | {self._inventory_level} units"

class Electronics(Product):
    def __init__(self, product_name, price, supplier_info, warranty_period):
        super().__init__(product_name, price, supplier_info)
        self.warranty_period = warranty_period

    def __str__(self):
        return f"{super().__str__()} | Warranty: {self.warranty_period} months"

class Furniture(Product):
    def __init__(self, product_name, price, supplier_info, material):
        super().__init__(product_name, price, supplier_info)
        self.material = material

    def __str__(self):
        return f"{super().__str__()} | Material: {self.material}"

class Grocery(Product):
    def __init__(self, product_name, price, supplier_info, expiration_date):
        super().__init__(product_name, price, supplier_info)
        self.expiration_date = expiration_date

    def __str__(self):
        return f"{super().__str__()} | Expiration: {self.expiration_date}"
