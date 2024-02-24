import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime

class InventoryApplication:
    def __init__(self, master):
        self.master = master
        master.title("Inventory Management")

        self.conn = sqlite3.connect('inventory.db')
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY,
                item_name TEXT NOT NULL,
                unit_price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL
            )
        ''')
        self.conn.commit()

        # Frame for Inventory Table
        self.table_frame = ttk.Frame(master)
        self.table_frame.grid(row=0, column=0, columnspan=3, sticky='ew')

        # Inventory Table with Headers
        self.inventory_tree = ttk.Treeview(self.table_frame, columns=("Item Name", "Unit Price", "Quantity", "Total Price"), show="headings")
        self.inventory_tree.heading("Item Name", text="Item Name")
        self.inventory_tree.heading("Unit Price", text="Unit Price")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Total Price", text="Total Price")
        self.inventory_tree.column("Item Name", anchor='center')
        self.inventory_tree.column("Unit Price", anchor='center')
        self.inventory_tree.column("Quantity", anchor='center')
        self.inventory_tree.column("Total Price", anchor='center')
        self.inventory_tree.pack(side="top", fill="x")

        # Entry Frame for Adding New Items
        self.entry_frame = ttk.Frame(master)
        self.entry_frame.grid(row=1, column=0, columnspan=3, pady=10)

        # Item Name Entry
        self.item_name_label = ttk.Label(self.entry_frame, text="Item Name:")
        self.item_name_label.grid(row=0, column=0, sticky=tk.W)
        self.item_name_entry = ttk.Entry(self.entry_frame)
        self.item_name_entry.grid(row=0, column=1)

        # Unit Price Entry
        self.unit_price_label = ttk.Label(self.entry_frame, text="Unit Price:")
        self.unit_price_label.grid(row=1, column=0, sticky=tk.W)
        self.unit_price_entry = ttk.Entry(self.entry_frame)
        self.unit_price_entry.grid(row=1, column=1)

        # Quantity Entry
        self.quantity_label = ttk.Label(self.entry_frame, text="Quantity:")
        self.quantity_label.grid(row=2, column=0, sticky=tk.W)
        self.quantity_entry = ttk.Entry(self.entry_frame)
        self.quantity_entry.grid(row=2, column=1)

        # Add Item Button
        self.add_item_button = ttk.Button(self.entry_frame, text="Add Item", command=self.add_item)
        self.add_item_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Total Inventory Value Display
        self.total_inventory_label = ttk.Label(master, text="Total Inventory Value: LKR 0")
        self.total_inventory_label.grid(row=2, column=0, columnspan=3, pady=10)

        # Generate Report Button
        self.generate_report_button = ttk.Button(master, text="Generate Report", command=self.generate_inventory_report)
        self.generate_report_button.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        self.refresh_inventory_list()

    def add_item(self):
        item_name = self.item_name_entry.get()
        unit_price = self.unit_price_entry.get()
        quantity = self.quantity_entry.get()
        try:
            unit_price = float(unit_price)
            quantity = int(quantity)
            total_price = unit_price * quantity
            self.c.execute('INSERT INTO inventory (item_name, unit_price, quantity, total_price) VALUES (?, ?, ?, ?)', (item_name, unit_price, quantity, total_price))
            self.conn.commit()
            self.item_name_entry.delete(0, tk.END)
            self.unit_price_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)
            self.refresh_inventory_list()
            messagebox.showinfo("Success", "Item added to inventory.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid unit price and quantity.")

    def refresh_inventory_list(self):
        for i in self.inventory_tree.get_children():
            self.inventory_tree.delete(i)
        self.c.execute('SELECT item_name, unit_price, quantity, total_price FROM inventory')
        total_value = 0
        for row in self.c.fetchall():
            self.inventory_tree.insert("", tk.END, values=row)
            total_value += row[3]
        self.total_inventory_label.config(text=f"Total Inventory Value: LKR {total_value}")   

    def generate_inventory_report(self):
        # Fetch inventory items
        self.c.execute('SELECT item_name, unit_price, quantity, total_price FROM inventory')
        inventory_items = self.c.fetchall()
        
        # Define the CSV file name with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f'inventory_report_{timestamp}.csv'
        
        # Writing to CSV
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Writing the headers
            writer.writerow(['Item Name', 'Unit Price', 'Quantity', 'Total Price'])
            
            # Writing inventory data
            for item in inventory_items:
                writer.writerow(item)
            
            # Optionally, calculate and write totals
            total_units = sum(item[2] for item in inventory_items)
            total_value = sum(item[3] for item in inventory_items)
            writer.writerow([])
            writer.writerow(['Total Units', '', total_units, ''])
            writer.writerow(['Total Inventory Value', '', '', total_value])
        
        messagebox.showinfo("Report Generated", f"Inventory report has been generated: {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApplication(root)
    root.geometry("600x600")  # Adjust the window size as needed
    root.mainloop()

