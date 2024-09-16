from product import Product

class InventoryManager:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def delete_product(self, name):
        self.products = [product for product in self.products if product.name != name]

    def update_product_category(self, name, new_category):
        for product in self.products:
            if product.name == name:
                product.update_category(new_category)
                break

    def get_all_products(self):
        return self.products

    def get_products_by_category(self, category):
        return [product for product in self.products if product.category == category]
