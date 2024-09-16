# gui.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from inventory_manager import InventoryManager
from product import Product

class InventoryGUI:
    def __init__(self, root, inventory_manager):
        self.root = root
        self.root.title("Generic Inventory Management System")
        self.root.geometry("900x600")  # Enlarged Window

        self.inventory_manager = inventory_manager
        self.category_var = tk.StringVar(value="All")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Category Label
        self.category_label = tk.Label(self.root, text="Select Category")
        self.category_label.grid(row=0, column=0)

        # Category ComboBox
        self.category_combo = ttk.Combobox(self.root, textvariable=self.category_var, values=["All", "Electronics", "Furniture", "Grocery", "Miscellaneous"])
        self.category_combo.grid(row=0, column=1)
        self.category_combo.bind("<<ComboboxSelected>>", self.refresh_products)

        # Product Name Label
        self.name_label = tk.Label(self.root, text="Product Name")
        self.name_label.grid(row=1, column=0)

        # Product Name Entry
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.grid(row=1, column=1)

        # Price Label
        self.price_label = tk.Label(self.root, text="Price")
        self.price_label.grid(row=2, column=0)

        # Price Entry
        self.price_entry = tk.Entry(self.root, width=30)
        self.price_entry.grid(row=2, column=1)

        # Supplier Info Label
        self.supplier_label = tk.Label(self.root, text="Supplier Info")
        self.supplier_label.grid(row=3, column=0)

        # Supplier Info Entry
        self.supplier_entry = tk.Entry(self.root, width=30)
        self.supplier_entry.grid(row=3, column=1)

        # Category Label
        self.product_category_label = tk.Label(self.root, text="Category")
        self.product_category_label.grid(row=4, column=0)

        # Category Entry
        self.product_category_entry = tk.Entry(self.root, width=30)
        self.product_category_entry.grid(row=4, column=1)

        # Additional Attributes Label
        self.attributes_label = tk.Label(self.root, text="Additional Attributes (key:value, comma separated)")
        self.attributes_label.grid(row=5, column=0)

        # Additional Attributes Entry
        self.attributes_entry = tk.Entry(self.root, width=30)
        self.attributes_entry.grid(row=5, column=1)

        # Add Product Button
        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=6, column=1)

        # Create a Frame for Table and Scrollbars
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=7, column=0, columnspan=3, sticky="nsew")

        # Table View
        self.columns = ("Name", "Price", "Supplier", "Inventory Level", "Total Value", "Category", "Additional Info")
        self.tree = ttk.Treeview(self.frame, columns=self.columns, show='headings')
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Define headings
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.heading("Inventory Level", text="Inventory Level")
        self.tree.heading("Total Value", text="Total Value")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Additional Info", text="Additional Info")

        # Adjust column width
        for col in self.columns:
            self.tree.column(col, width=120)

        # Scrollbars
        self.scroll_y = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_y.set)
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.scroll_x = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=self.scroll_x.set)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Initialize product display
        self.refresh_products()

    def add_product(self):
        name = self.name_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
            return
        supplier_info = self.supplier_entry.get()
        category = self.product_category_entry.get()
        additional_attributes = self.attributes_entry.get()

        if not name or not price or not supplier_info or not category:
            messagebox.showwarning("Input Error", "Name, Price, Supplier Info, and Category are required")
            return

        # Convert additional attributes from string to dictionary
        attributes_dict = {}
        if additional_attributes:
            try:
                attributes = additional_attributes.split(',')
                for attribute in attributes:
                    key, value = attribute.split(':')
                    attributes_dict[key.strip()] = value.strip()
            except ValueError:
                messagebox.showwarning("Input Error", "Additional attributes should be in key:value format, separated by commas")
                return

        product = Product(name, price, supplier_info, category, **attributes_dict)
        self.inventory_manager.add_product(product)
        self.refresh_products()

    def refresh_products(self, event=None):
        # Clear previous products in the table
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Filter by category
        category = self.category_var.get()
        if category == "All":
            products = self.inventory_manager.get_all_products()
        else:
            products = self.inventory_manager.get_products_by_category(category)

        # Display all products
        for product in products:
            self.tree.insert("", "end", values=(
                product.name,
                f"${product.price:.2f}",
                product.supplier_info,
                product.get_inventory_level(),
                f"${product.get_total_value():.2f}",
                product.category,
                ', '.join([f"{key}: {value}" for key, value in product.additional_attributes.items()])
            ))

        # Adjust scrolling
        self.tree.update_idletasks()

if __name__ == "__main__":
    import tkinter as tk
    from inventory_manager import InventoryManager
    from product import Product

    def main():
        # Create the main window
        root = tk.Tk()
        
        # Create an InventoryManager instance
        inventory_manager = InventoryManager()
        
        # Add default products
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

    main()
