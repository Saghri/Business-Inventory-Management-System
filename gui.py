# gui.py

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from inventory_manager import InventoryManager
from product import Electronics, Furniture, Grocery

class InventoryGUI:
    def __init__(self, root, inventory_manager):
        self.root = root
        self.root.title("Business Inventory Management System")
        self.root.geometry("800x600")  # Enlarged Window
        self.inventory_manager = inventory_manager

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # Product Name Label
        self.name_label = tk.Label(self.root, text="Product Name")
        self.name_label.grid(row=0, column=0)

        # Product Name Entry
        self.name_entry = tk.Entry(self.root, width=30)
        self.name_entry.grid(row=0, column=1)

        # Price Label
        self.price_label = tk.Label(self.root, text="Price")
        self.price_label.grid(row=1, column=0)

        # Price Entry
        self.price_entry = tk.Entry(self.root, width=30)
        self.price_entry.grid(row=1, column=1)

        # Supplier Info Label
        self.supplier_label = tk.Label(self.root, text="Supplier Info")
        self.supplier_label.grid(row=2, column=0)

        # Supplier Info Entry
        self.supplier_entry = tk.Entry(self.root, width=30)
        self.supplier_entry.grid(row=2, column=1)

        # Category Label
        self.category_label = tk.Label(self.root, text="Category (Electronics/Furniture/Grocery)")
        self.category_label.grid(row=3, column=0)

        # Category Entry
        self.category_entry = tk.Entry(self.root, width=30)
        self.category_entry.grid(row=3, column=1)

        # Additional Info Label
        self.additional_info_label = tk.Label(self.root, text="Additional Info (Warranty/Material/Expiration)")
        self.additional_info_label.grid(row=4, column=0)

        # Additional Info Entry
        self.additional_info_entry = tk.Entry(self.root, width=30)
        self.additional_info_entry.grid(row=4, column=1)

        # Add Product Button
        self.add_product_button = tk.Button(self.root, text="Add Product", command=self.add_product)
        self.add_product_button.grid(row=5, column=1)

        # Inventory Table View
        self.create_table_view()

    def create_table_view(self):
        # Treeview widget (table)
        self.columns = ("Name", "Price", "Supplier", "Category", "Additional Info", "Inventory Level", "Total Value")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show='headings')
        self.tree.grid(row=6, column=0, columnspan=3, sticky="nsew")

        # Define headings
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.heading("Supplier", text="Supplier")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Additional Info", text="Additional Info")
        self.tree.heading("Inventory Level", text="Inventory Level")
        self.tree.heading("Total Value", text="Total Value")

        # Adjust column width
        for col in self.columns:
            self.tree.column(col, width=100)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=6, column=3, sticky="ns")

    def add_product(self):
        product_name = self.name_entry.get()
        try:
            price = float(self.price_entry.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Price must be a number")
            return
        supplier_info = self.supplier_entry.get()
        category = self.category_entry.get().lower()
        additional_info = self.additional_info_entry.get()

        if not product_name or not price or not supplier_info or not category:
            messagebox.showwarning("Input Error", "All fields are required")
            return

        if category == "electronics":
            product = Electronics(product_name, price, supplier_info, additional_info)
        elif category == "furniture":
            product = Furniture(product_name, price, supplier_info, additional_info)
        elif category == "grocery":
            try:
                expiration_date = datetime.strptime(additional_info, "%Y-%m-%d").date()
                product = Grocery(product_name, price, supplier_info, expiration_date)
            except ValueError:
                messagebox.showwarning("Input Error", "Expiration date must be in YYYY-MM-DD format")
                return
        else:
            messagebox.showwarning("Input Error", "Invalid category. Choose from Electronics, Furniture, or Grocery.")
            return

        self.inventory_manager.add_product(product)
        self.refresh_products()

    def refresh_products(self):
        # Clear previous products in the table
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Display all products
        for product in self.inventory_manager.get_all_products():
            self.tree.insert("", "end", values=(product.product_name, f"${product.price:.2f}", product._supplier_info, product.__class__.__name__, product.additional_info, product.get_inventory_level(), f"${product.get_total_value():.2f}"))
