# main.py

import tkinter as tk
from inventory_manager import InventoryManager
from gui import InventoryGUI

def main():
    # Create the main window
    root = tk.Tk()
    
    # Create an InventoryManager instance
    inventory_manager = InventoryManager()
    
    # Create the GUI instance
    gui = InventoryGUI(root, inventory_manager)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
