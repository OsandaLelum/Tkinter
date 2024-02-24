import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class PaymentDialog:
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.top.title("Payment Information")
        self.top.geometry("300x200")

        # Card Number
        ttk.Label(self.top, text="Card Number:").grid(row=0, column=0, pady=5, padx=5)
        self.card_number_var = tk.StringVar()
        ttk.Entry(self.top, textvariable=self.card_number_var).grid(row=0, column=1, pady=5, padx=5)

        # Expiry Date
        ttk.Label(self.top, text="Expiry Date (MM/YY):").grid(row=1, column=0, pady=5, padx=5)
        self.exp_date_var = tk.StringVar()
        ttk.Entry(self.top, textvariable=self.exp_date_var).grid(row=1, column=1, pady=5, padx=5)

        # CVV
        ttk.Label(self.top, text="CVV:").grid(row=2, column=0, pady=5, padx=5)
        self.cvv_var = tk.StringVar()
        ttk.Entry(self.top, textvariable=self.cvv_var).grid(row=2, column=1, pady=5, padx=5)

        # Submit Button
        ttk.Button(self.top, text="Submit Payment", command=self.submit_payment).grid(row=3, column=0, columnspan=2, pady=10)

    def submit_payment(self):
        # Placeholder function for payment submission logic
        card_number = self.card_number_var.get()
        exp_date = self.exp_date_var.get()
        cvv = self.cvv_var.get()

        # Validation logic here
        if not (card_number and exp_date and cvv):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Simulate payment process
        messagebox.showinfo("Payment Submitted", "Your payment has been submitted.")
        self.top.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    PaymentDialog(root)  # Directly open the Payment Dialog
    root.mainloop()
