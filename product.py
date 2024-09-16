class Product:
    def __init__(self, name, price, supplier_info, category, **kwargs):
        self.name = name
        self.price = price
        self.supplier_info = supplier_info
        self.category = category
        self._inventory_level = 0
        self.additional_attributes = kwargs

    def update_inventory(self, amount):
        self._inventory_level += amount

    def get_inventory_level(self):
        return self._inventory_level

    def get_total_value(self):
        return self._inventory_level * self.price

    def update_category(self, new_category):
        self.category = new_category

    def __str__(self):
        attributes = ', '.join([f"{key}: {value}" for key, value in self.additional_attributes.items()])
        return f"{self.name} | ${self.price:.2f} | {self._inventory_level} units | {self.category} | {attributes}"
