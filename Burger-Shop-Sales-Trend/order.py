import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

class BurgerOrderingSystem:
    def __init__(self, master):  # Corrected from _init_ to __init__
        self.master = master
        master.title("Burger Order Funnel")

        self.burgers = {
            "Classic Burger": 1200,
            "Cheese Burger": 2000,
            "Veggie Burger": 1000,
            "Chicken Burger": 1500,
            "Fish Burger": 1400,
            "Double Cheese Burger": 2000,
            "Bacon Burger": 2200,
            "Spicy Burger": 1800,
            "Mushroom Swiss Burger": 1200,
            "BBQ Burger": 1800,
        }

        self.cart = []
        self.create_widgets()

    def create_widgets(self):
        burgers_list = list(self.burgers.items())
        for index, (burger, price) in enumerate(burgers_list):
            column_offset = (index % 2) * 3
            row = index // 2

            image_path = f"images/{burger.lower().replace(' ', '_')}.png"
            try:
                image = Image.open(image_path)
            except FileNotFoundError:
                image_path = image_path.replace('.png', '.jpg')
                try:
                    image = Image.open(image_path)
                except FileNotFoundError:
                    print(f"Image not found for {burger}, using placeholder")
                    image = Image.new('RGB', (200, 200), color='gray')

            image = image.resize((150, 150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            image_label = ttk.Label(self.master, image=photo)
            image_label.image = photo
            image_label.grid(column=column_offset, row=row, padx=5, pady=5)

            ttk.Label(self.master, text=f"{burger} - LKR{price}").grid(column=column_offset+1, row=row, sticky=tk.W, padx=5, pady=5)

            add_button = ttk.Button(self.master, text="Add to Cart", command=lambda b=burger: self.add_to_cart(b))
            add_button.grid(column=column_offset+2, row=row, padx=5, pady=5)

        last_row = len(burgers_list) // 2 if len(burgers_list) % 2 == 0 else len(burgers_list) // 2 + 1

        self.cart_label = ttk.Label(self.master, text="Cart: 0 items")
        self.cart_label.grid(column=0, row=last_row, columnspan=2, sticky=tk.W, padx=5, pady=5)

        checkout_button = ttk.Button(self.master, text="Checkout", command=self.checkout)
        checkout_button.grid(column=2, row=last_row, columnspan=2, padx=5, pady=5)

    def add_to_cart(self, burger):
        self.cart.append(burger)
        self.cart_label.configure(text=f"Cart: {len(self.cart)} items")
        messagebox.showinfo("Added to Cart", f"{burger} added to cart!")

    
    def checkout(self):
        if not self.cart:
            messagebox.showinfo("Checkout", "Your cart is empty!")
        else:
            ordered_items = '\n'.join(self.cart)
            messagebox.showinfo("Checkout", f"You have ordered: {ordered_items}")
            self.cart.clear()
            self.cart_label.configure(text="Cart: 0 items")
            conn = sqlite3.connect('sales.db')
            c = conn.cursor()
            from datetime import datetime
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('''
                  INSERT INTO sales (item_name, quantity, total_price, sale_date) VALUES (?, ?, ?, ?)
                ''', (item_name, quantity, total_price, current_time))
            conn.commit()
            conn.close()
            messagebox.showinfo("Checkout Successful", "Your order has been saved.")


 


            

if __name__ == "__main__":  # Corrected from _name_ == "_main_"
    root = tk.Tk()
    app = BurgerOrderingSystem(root)
    root.geometry("800x600")  # Adjust the window size as needed
    root.mainloop()
