import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import subprocess

class BurgerOrderingSystem:
    def __init__(self, master):
        self.master = master
        master.title("Burger Order Funnel")

        self.burgers = {
            "Classic Burger": {"price": 1200, "desc": "A classic beef burger with lettuce, tomato, and sauce", "calories": "300 kcal"},
            "Cheese Burger": {"price": 2000, "desc": "Beef burger topped with creamy cheese", "calories": "350 kcal"},
            "Veggie Burger": {"price": 1000, "desc": "Made with fresh vegetables and beans", "calories": "250 kcal"},
            "Chicken Burger": {"price": 1500, "desc": "Grilled chicken breast with lettuce and mayo", "calories": "400 kcal"},
            "Fish Burger": {"price": 1400, "desc": "Crispy fish fillet with tartar sauce", "calories": "370 kcal"},
            "Double Cheese Burger": {"price": 2000, "desc": "Double beef patties with double cheese", "calories": "450 kcal"},
            "Bacon Burger": {"price": 2200, "desc": "Beef burger with crispy bacon strips", "calories": "420 kcal"},
            "Spicy Burger": {"price": 1800, "desc": "Spicy beef burger with jalapenos", "calories": "390 kcal"},
            "Mushroom Swiss Burger": {"price": 1200, "desc": "Beef burger with mushrooms and Swiss cheese", "calories": "310 kcal"},
            "BBQ Burger": {"price": 1800, "desc": "Beef burger with BBQ sauce and onion rings", "calories": "430 kcal"},
        }

        self.cart = []
        self.create_widgets()

    def create_widgets(self):
        burgers_list = list(self.burgers.items())

        for index, (burger, details) in enumerate(burgers_list):
            # Create a frame for each burger
            burger_frame = ttk.Frame(self.master)
            burger_frame.grid(row=index // 5, column=index % 5, sticky='nsew', padx=5, pady=5)

            # Load and display the burger image
            image_path = f"images/{burger.lower().replace(' ', '_')}.png"
            try:
                image = Image.open(image_path)
            except FileNotFoundError:
                image_path = image_path.replace('.png', '.jpg')
                try:
                    image = Image.open(image_path)
                except FileNotFoundError:
                    print(f"Image not found for {burger}, using placeholder")
                    image = Image.new('RGB', (150, 150), color='gray')

            image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = ttk.Label(burger_frame, image=photo)
            image_label.image = photo  # Keep a reference
            image_label.pack(side='top')

            # Display burger name, price, description, and calories
            info_text = f"{burger}\nLKR {details['price']}\n{details['desc']}\nCalories: {details['calories']}"
            info_label = ttk.Label(burger_frame, text=info_text, justify='left')
            info_label.pack(side='top', fill='x', expand=True)

            # Add to Cart button
            add_button = ttk.Button(burger_frame, text="Add to Cart", command=lambda b=burger: self.add_to_cart(b))
            add_button.pack(side='top')

        # Cart label
        self.cart_label = ttk.Label(self.master, text="Cart: 0 items")
        self.cart_label.grid(column=0, row=2, columnspan=5, sticky=tk.W, padx=5, pady=5)

        # View Bill button
        view_bill_button = ttk.Button(self.master, text="View Bill", command=self.view_bill)
        view_bill_button.grid(column=0, row=3, columnspan=5, padx=5, pady=5)

        # Checkout button
        checkout_button = ttk.Button(self.master, text="Checkout", command=self.checkout)
        checkout_button.grid(column=0, row=4, columnspan=5, padx=5, pady=5)

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
            subprocess.run(["python", "payment.py"], check=True)


    def view_bill(self):
        if not self.cart:
            messagebox.showinfo("View Bill", "Your cart is empty!")
            return
        
        total_price = 0
        total_calories = 0  # Initialize total calories
        bill_text = f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        bill_text += "Item\t\tQty\tPrice\tCalories\tOrder Date\n"
        for item in self.cart:
            details = self.burgers[item]
            price = details['price']
            calories = int(details['calories'].split()[0])  # Extract calories as integer
            total_calories += calories
            total_price += price
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            bill_text += f"{item}\t1\tLKR {price}\t{calories} kcal\t{order_date}\n"
        
        bill_text += f"\nTotal Calories: {total_calories} kcal\nTotal Price: LKR {total_price}"
        messagebox.showinfo("View Bill", bill_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = BurgerOrderingSystem(root)
    root.geometry("1400x800")  # Adjust the window size as needed
    root.mainloop()
