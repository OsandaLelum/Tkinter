import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import subprocess

import sqlite3
import subprocess
from tkinter import messagebox

def login(username, password):
    conn = sqlite3.connect(r'C:\Users\osandal\Downloads\Tinker Project\Burger-Shop\customer.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    if result:
        messagebox.showinfo("Success", "Login Successful")
        if username.lower() == 'admin':
            try:
                # Open the Items Inventory page if the user is 'admin'
                subprocess.run(["python", "inventory.py"], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to start the inventory process: {e}")
        elif username.lower() == 'admink':
            try:
                # Open the Issue Items page if the user is 'adminK'
                subprocess.run(["python", "issueitem.py"], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to start the issue item process: {e}")
        elif username.lower() == 'salesmanager':
            try:
                # Open the Issue Items page if the user is 'adminK'
                subprocess.run(["python", "sales.py"], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to start the issue item process: {e}")
        else:
            try:
                # Open the Order page for other users
                subprocess.run(["python", "neworder.py"], check=True)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Failed to start the order process: {e}")
        return username
    else:
        messagebox.showerror("Error", "Invalid username or password")
    conn.close()




# Function to handle signup
def signup(username, password):
    conn = sqlite3.connect('customer.db')
    if not username or not password:
        messagebox.showerror("Error", "Username and password are required")
        return
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")
    conn.close()

# Function to create login window
def create_login_window():
    window = tk.Toplevel()
    window.title("Login")
    window.configure(bg="lightblue")  # Set background color

    tk.Label(window, text="Username", bg="lightblue", fg="white", font=("Helvetica", 14)).grid(row=0)  # Change font size and color
    tk.Label(window, text="Password", bg="lightblue", fg="white", font=("Helvetica", 14)).grid(row=1)  # Change font size and color

    username = tk.Entry(window, font=("Helvetica", 14))  # Change font size
    password = tk.Entry(window, show="*", font=("Helvetica", 14))  # Change font size
    username.grid(row=0, column=1)
    password.grid(row=1, column=1)

    tk.Button(window, text="Login", bg="green", fg="white", font=("Helvetica", 14), command=lambda: login(username.get(), password.get())).grid(columnspan=2)

# Function to create signup window
def create_signup_window():
    window = tk.Toplevel()
    window.title("Signup")
    window.configure(bg="lightblue")  # Set background color

    tk.Label(window, text="Username", bg="lightblue", fg="white", font=("Helvetica", 14)).grid(row=0)  # Change font size and color
    tk.Label(window, text="Password", bg="lightblue", fg="white", font=("Helvetica", 14)).grid(row=1)  # Change font size and color

    username = tk.Entry(window, font=("Helvetica", 14))  # Change font size
    password = tk.Entry(window, show="*", font=("Helvetica", 14))  # Change font size
    username.grid(row=0, column=1)
    password.grid(row=1, column=1)

    tk.Button(window, text="Signup", bg="green", fg="white", font=("Helvetica", 14), command=lambda: signup(username.get(), password.get())).grid(columnspan=2)
# login.py

def get_logged_in_user():
    # ... your login logic here
    return username  # Assuming 'username' is the logged-in user's name


# Main window
root = tk.Tk()
root.title("Customer Login System")

# Add text label
text_label = tk.Label(root, text="Welcome to the Burger Tuk Ordering System", bg="lightblue", fg="white", font=("Helvetica", 20, "bold"))  # Change font size, color, and style
text_label.pack()
text_label = tk.Label(root, text="Dewmi-Kavindya")
text_label.pack()

# Load image
image_path = "images/burger_image.png"  # Replace with your image path
image = Image.open(image_path)
image = image.resize((500, 500), Image.LANCZOS)  # Resize the image
photo = ImageTk.PhotoImage(image)

# Create a label for the image
image_label = tk.Label(root, image=photo)
image_label.image = photo  # Keep a reference

# Add image label to the window
image_label.pack()

login_image = Image.open("images/login_image.png")  # Replace with the path to your login button image
login_image = login_image.resize((100, 100), Image.LANCZOS)  # Resize the image
login_photo = ImageTk.PhotoImage(login_image)
login_button = tk.Button(root, image=login_photo, bg="lightblue", borderwidth=0, command=create_login_window)
login_button.image = login_photo
login_button.pack(side=tk.LEFT ,padx=30, pady=30)

signup_image = Image.open("images/signup_image.png")  # Replace with the path to your signup button image
signup_image = signup_image.resize((100, 100), Image.LANCZOS)  # Resize the image
signup_photo = ImageTk.PhotoImage(signup_image)
signup_button = tk.Button(root, image=signup_photo, bg="lightblue", borderwidth=0, command=create_signup_window)
signup_button.image = signup_photo
signup_button.pack(side=tk.RIGHT,padx=30, pady=30)
root.mainloop()