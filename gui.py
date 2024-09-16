import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
from inventory_manager import InventoryManager
from product import Product

class InventoryGUI:
    def __init__(self, root, inventory_manager):
        self.root = root
        self.root.title("Generic Inventory Management System")
        self.root.geometry("900x600")  # Enlarged Window

        self.inventory_manager = inventory_manager
        self.selected_product_name = None  # Track the selected product for deletion or updating

        # Categories list
        self.categories = ["Electronics", "Furniture", "Grocery", "Miscellaneous"]

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Category Label
        self.category_label = tk.Label(self.root, text="Select Category")
        self.category_label.grid(row=0, column=0, padx=10, pady=10)

        # Category ComboBox
        self.category_combo = ttk.Combobox(self.root, values=self.categories)
        self.category_combo.grid(row=0, column=1, padx=10, pady=10)
        self.category_combo.set("Select Category")
        self.category_combo.bind("<<ComboboxSelected>>", self.on_category_selected)

        # Add New Category Button
        self.add_category_button = tk.Button(self.root, text="Add New Category", command=self.add_new_category)
        self.add_category_button.grid(row=0, column=2, padx=10, pady=10)

        # Product Name Label
        self.name_label = tk.Label(self.root, text="Product Name")
        self.name_label.grid(row=1, column=0, padx=10, pady=10)

        # Product Name Entry
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.grid(row=1, column=1, padx=10, pady=10)

        # Price Label
        self.price_label = tk.Label(self.root, text="Price")
        self.price_label.grid(row=2, column=0, padx=10, pady=10)

        # Price Entry
        self.price_entry = tk.Entry(self.root, width=30)
        self.price_entry.grid(row=2, column=1, padx=10, pady=10)

        # Supplier Info Label
        self.supplier_label = tk.Label(self.root, text="Supplier Info")
        self.supplier_label.grid(row=3, column=0, padx=10, pady=10)

        # Supplier Info Entry
        self.supplier_entry = tk.Entry(self.root, width=30)
        self.supplier_entry.grid(row=3, column=1, padx=10, pady=10)

        # Additional Attributes Label
        self.attributes_label = tk.Label(self.root, text="Additional Attributes (key:value, comma separated)")
        self.attributes_label.grid(row=4, column=0, padx=10, pady=10)

        # Additional Attributes Entry
        self.attributes_entry = tk.Entry(self.root, width=30)
        self.attributes_entry.grid(row=4, column=1, padx=10, pady=10)

        # Add Product Button
        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=5, column=1, padx=10, pady=10)

        # Delete Product Button
        self.delete_product_button = tk.Button(self.root, text="Delete Product", command=self.delete_product)
        self.delete_product_button.grid(row=6, column=1, padx=10, pady=10)

        # Change Category Button
        self.change_category_button = tk.Button(self.root, text="Change Category", command=self.change_category)
        self.change_category_button.grid(row=7, column=1, padx=10, pady=10)

        # Create a Frame for Table and Scrollbars
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=8, column=0, columnspan=3, sticky="nsew")

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

        # Bind item selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_item_selected)

        # Initialize product display
        self.refresh_products()

    def on_category_selected(self, event):
        # When category is selected, refresh product list
        self.refresh_products()

    def add_new_category(self):
        new_category = simpledialog.askstring("New Category", "Enter the new category name:")
        if new_category and new_category not in self.categories:
            self.categories.append(new_category)
            self.category_combo['values'] = self.categories
            self.category_combo.set(new_category)

    def add_product(self):
        name = self.name_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
            return
        supplier_info = self.supplier_entry.get()
        category = self.category_combo.get()
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

    def delete_product(self):
        if self.selected_product_name:
            self.inventory_manager.delete_product(self.selected_product_name)
            self.refresh_products()
            self.selected_product_name = None  # Reset selection
        else:
            messagebox.showwarning("Selection Error", "No product selected for deletion")

    def change_category(self):
        if self.selected_product_name:
            new_category = simpledialog.askstring("Change Category", "Enter new category for the selected product:")
            if new_category:
                self.inventory_manager.update_product_category(self.selected_product_name, new_category)
                self.refresh_products()
        else:
            messagebox.showwarning("Selection Error", "No product selected for category change")

    def on_item_selected(self, event):
        selected_item = self.tree.selection()[0]
        self.selected_product_name = self.tree.item(selected_item, 'values')[0]

    def refresh_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        category = self.category_combo.get()
        if category == "Select Category":
            products = self.inventory_manager.get_all_products()
        else:
            products = self.inventory_manager.get_products_by_category(category)

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

