import tkinter as tk
from inventory_manager import InventoryManager
from gui import InventoryGUI
from product import Product

def main():
    # Create the main window
    root = tk.Tk()
    
    # Create an InventoryManager instance
    inventory_manager = InventoryManager()
    
    # Add default products with category
    default_products = [
        Product(name="Laptop", price=999.99, supplier_info="Tech Supplier Co.", category="Electronics", brand="BrandX", warranty="2 years"),
        Product(name="Sofa", price=499.99, supplier_info="Home Furnishings Inc.", category="Furniture", material="Leather", dimensions="3x2x1.5 m"),
        Product(name="Organic Apples", price=2.99, supplier_info="Fresh Farms", category="Grocery", expiration_date="2024-12-01"),
        Product(name="Smartphone", price=699.99, supplier_info="Gadget World", category="Electronics", brand="BrandY", warranty="1 year"),
        Product(name="Dining Table", price=299.99, supplier_info="Furniture HQ", category="Furniture", material="Wood", dimensions="1.8x1 m")
    ]
    
    for product in default_products:
        inventory_manager.add_product(product)
    
    # Create the GUI instance
    gui = InventoryGUI(root, inventory_manager)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
