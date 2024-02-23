import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class POSApplication:
    def __init__(self, root):
        self.root = root
        root.title("Burgers on Wheels POS System")

        # Payment Method
        ttk.Label(root, text="Select Payment Method:").grid(column=0, row=0, padx=10, pady=10)
        self.payment_method_var = tk.StringVar()
        payment_methods = ['Cash', 'Credit/Debit Card']
        self.payment_method_combobox = ttk.Combobox(root, textvariable=self.payment_method_var, values=payment_methods, state='readonly')
        self.payment_method_combobox.grid(column=1, row=0)
        self.payment_method_combobox.current(0)

        # Amount
        ttk.Label(root, text="Amount:").grid(column=0, row=1, padx=10, pady=10)
        self.amount_var = tk.StringVar()
        ttk.Entry(root, textvariable=self.amount_var).grid(column=1, row=1)

        # Payment Button
        ttk.Button(root, text="Process Payment", command=self.process_payment).grid(column=0, row=2, columnspan=2, pady=10)

    def process_payment(self):
        # Placeholder for processing payment
        payment_method = self.payment_method_var.get()
        amount = self.amount_var.get()
        # Here you would add the logic to process the payment and interact with the database
        messagebox.showinfo("Payment Processed", f"Payment of {amount} via {payment_method} processed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = POSApplication(root)
    root.mainloop()
