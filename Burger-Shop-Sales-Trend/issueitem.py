import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

class IssueItemsApplication:
    def __init__(self, master):
        self.master = master
        master.title("Issue Items to Kitchen")

        self.conn = sqlite3.connect(r'C:\Users\osandal\Downloads\Tinker Project\Burger-Shop\inventory.db')
        self.c = self.conn.cursor()

        # Fetch inventory items
        self.c.execute('SELECT id, item_name, quantity FROM inventory')
        self.items = self.c.fetchall()

        # Dropdown to select inventory item
        self.item_var = tk.StringVar(master)
        self.item_dropdown = ttk.Combobox(master, textvariable=self.item_var)
        self.item_dropdown['values'] = [item[1] for item in self.items]  # item names
        self.item_dropdown.grid(row=0, column=1, padx=10, pady=10)
        self.item_label = ttk.Label(master, text="Select Item:")
        self.item_label.grid(row=0, column=0, padx=10, pady=10)

        # Entry for quantity to issue
        self.quantity_var = tk.IntVar(master)
        self.quantity_entry = ttk.Entry(master, textvariable=self.quantity_var)
        self.quantity_entry.grid(row=1, column=1, padx=10, pady=10)
        self.quantity_label = ttk.Label(master, text="Quantity to Issue:")
        self.quantity_label.grid(row=1, column=0, padx=10, pady=10)

        # Issue button
        self.issue_button = ttk.Button(master, text="Issue Item", command=self.issue_item)
        self.issue_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def issue_item(self):
        item_name = self.item_var.get()
        quantity_to_issue = self.quantity_var.get()

        # Find the selected item
        item = next((item for item in self.items if item[1] == item_name), None)
        if item and 0 < quantity_to_issue <= item[2]:
            new_quantity = item[2] - quantity_to_issue
            # Update the item in the database
            self.c.execute('UPDATE inventory SET quantity = ? WHERE id = ?', (new_quantity, item[0]))
            self.conn.commit()

            # Generate the PDF report
            self.generate_pdf(item_name, quantity_to_issue)

            messagebox.showinfo("Success", f"Issued {quantity_to_issue} of {item_name}.")
            self.master.destroy()  # Optionally close the window after issuing
        else:
            messagebox.showerror("Error", "Invalid quantity.")

    def generate_pdf(self, item_name, quantity):
        filename = f"{item_name}_issued_report.pdf"
        document = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        flowables = []

        # Company Header
        flowables.append(Paragraph("Burger Hub (Pvt) Ltd", styles['Title']))
        flowables.append(Spacer(1, 12))

        # Address and Contact
        address = """<para align=center>123, Gourmet Street,<br/>Colombo, Sri Lanka<br/>Tel: +94 11 234 5678<br/>Email: info@burgerhub.lk</para>"""
        flowables.append(Paragraph(address, styles["BodyText"]))
        flowables.append(Spacer(1, 12))

        # Issued Item Details
        report_title = Paragraph(f"Material Issue Document - {item_name}", styles['Heading2'])
        flowables.append(report_title)
        flowables.append(Spacer(1, 12))

        data = [['Item Name', 'Quantity Issued'],
                [item_name, quantity]]

        table = Table(data, colWidths=[3*inch, 2*inch])
        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        table.setStyle(table_style)
        flowables.append(table)
        
        document.build(flowables)

        messagebox.showinfo("PDF Generated", f"Professional PDF report for {item_name} has been generated.")

    def on_closing(self):
        self.conn.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = IssueItemsApplication(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
