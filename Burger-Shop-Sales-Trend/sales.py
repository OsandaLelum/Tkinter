import tkinter as tk
from tkinter import ttk
import sqlite3
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

class SalesAnalyticsApp:
    def __init__(self, master):
        self.master = master
        master.title("Sales Analytics")

        # Create Tabs
        tab_control = ttk.Notebook(master)
        self.sales_trend_canvas = None
        tab_control = ttk.Notebook(master)

        self.analytics_tab = ttk.Frame(tab_control)
        self.data_tab = ttk.Frame(tab_control)  
        self.item_analytics_tab = ttk.Frame(tab_control)
        self.sales_chart_tab = ttk.Frame(tab_control)
        

        tab_control.add(self.analytics_tab, text='Analytics')
        tab_control.add(self.data_tab, text='Raw Data')
        tab_control.add(self.item_analytics_tab, text='Item Analytics')
        tab_control.add(self.sales_chart_tab, text='Sales Chart')
        tab_control.pack(expand=1, fill="both")

        # Initialize UI components
        self.setup_analytics_tab()
        self.setup_data_tab()
        self.setup_item_analytics_tab()
        self.setup_sales_chart_tab()

    def setup_analytics_tab(self):
        # KPIs
        self.total_sales_var = tk.StringVar()
        self.total_items_var = tk.StringVar()
        self.avg_sale_var = tk.StringVar()

        ttk.Label(self.analytics_tab, text="Total Sales:").grid(column=0, row=0, sticky='w')
        ttk.Label(self.analytics_tab, textvariable=self.total_sales_var).grid(column=1, row=0, sticky='e')

        ttk.Label(self.analytics_tab, text="Total Items Sold:").grid(column=0, row=1, sticky='w')
        ttk.Label(self.analytics_tab, textvariable=self.total_items_var).grid(column=1, row=1, sticky='e')

        ttk.Label(self.analytics_tab, text="Average Sale Amount:").grid(column=0, row=2, sticky='w')
        ttk.Label(self.analytics_tab, textvariable=self.avg_sale_var).grid(column=1, row=2, sticky='e')

        ttk.Button(self.analytics_tab, text="Refresh Analytics", command=self.load_analytics).grid(column=0, row=3, columnspan=2, pady=10)
        self.load_analytics()

    def setup_data_tab(self):
    # Create a frame for the treeview and the refresh button to allow using pack
        tree_frame = ttk.Frame(self.data_tab)
        tree_frame.pack(expand=True, fill="both", side="top")

    # Set up the Treeview in the frame
        self.tree = ttk.Treeview(tree_frame, columns=("sale_id", "item_name", "quantity", "total_price", "sale_date"), show="headings")
        self.tree.heading("sale_id", text="Sale ID")
        self.tree.heading("item_name", text="Item Name")
        self.tree.heading("quantity", text="Quantity")
        self.tree.heading("total_price", text="Total Price")
        self.tree.heading("sale_date", text="Sale Date")
        self.tree.pack(expand=True, fill="both", side="top")

    # Refresh Data button below the treeview
        refresh_button = ttk.Button(self.data_tab, text="Refresh Data", command=self.load_sales_data)
        refresh_button.pack(side="bottom", fill="x")

    # Load initial sales data
        self.load_sales_data()


    def load_analytics(self):
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute("SELECT SUM(total_price), SUM(quantity), AVG(total_price) FROM sales")
        total_sales, total_items, avg_sale = c.fetchone()
        conn.close()

        self.total_sales_var.set(f"${total_sales:,.2f}")
        self.total_items_var.set(f"{total_items}")
        self.avg_sale_var.set(f"${avg_sale:,.2f}")

    def load_sales_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)  # Clear the table

        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute("SELECT * FROM sales")
        for row in c.fetchall():
            self.tree.insert('', 'end', values=row)
        conn.close()

    def setup_item_analytics_tab(self):
        # Create Treeview for item-wise analytics
        self.item_tree = ttk.Treeview(self.item_analytics_tab, columns=("item_name", "total_quantity", "total_sales"), show="headings")
        self.item_tree.heading("item_name", text="Item Name")
        self.item_tree.heading("total_quantity", text="Total Quantity Sold")
        self.item_tree.heading("total_sales", text="Total Sales")
        
        # Adjust column widths and alignment
        self.item_tree.column("item_name", anchor='w', width=200)
        self.item_tree.column("total_quantity", anchor='center', width=150)
        self.item_tree.column("total_sales", anchor='center', width=150)

        self.item_tree.pack(expand=True, fill="both", padx=5, pady=5)

        # Button to refresh item analytics
        ttk.Button(self.item_analytics_tab, text="Refresh Item Analytics", command=self.load_item_analytics).pack(pady=10)
        ttk.Button(self.item_analytics_tab, text="Show Pie Chart", command=self.show_pie_chart).pack(pady=10)

        self.load_item_analytics()  # Load analytics initially

    def load_item_analytics(self):
        # Clear existing data in the treeview
        for i in self.item_tree.get_children():
            self.item_tree.delete(i)

        # Query the database for item-wise sales data
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute("""
            SELECT item_name, SUM(quantity) as total_quantity, SUM(total_price) as total_sales
            FROM sales
            GROUP BY item_name
            ORDER BY total_sales DESC
        """)
        
        for row in c.fetchall():
            self.item_tree.insert('', 'end', values=row)
        
        conn.close()

    def show_pie_chart(self):
        # Fetch item-wise sales data
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute("""
            SELECT item_name, SUM(total_price) as total_sales
            FROM sales
            GROUP BY item_name
        """)
        data = c.fetchall()
        conn.close()

        item_names = [row[0] for row in data]
        sales = [row[1] for row in data]

        # Create a pie chart
        fig = Figure(figsize=(6, 6), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        plot.pie(sales, labels=item_names, autopct='%1.1f%%', startangle=140)
        plot.set_title('Item-wise Sales Distribution')

        # Embed the pie chart into the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=self.item_analytics_tab)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def setup_sales_chart_tab(self):
        # Button to show the sales trend line chart
        ttk.Button(self.sales_chart_tab, text="Show Sales Trend", command=self.show_sales_trend).pack(pady=10)

    def show_sales_trend(self):
        # Clear the previous chart if it exists
        if self.sales_trend_canvas is not None:
            self.sales_trend_canvas.get_tk_widget().destroy()

        # Proceed with fetching data and creating the chart as before
        conn = sqlite3.connect('sales.db')
        c = conn.cursor()
        c.execute("""
            SELECT strftime('%Y-%m-%d', sale_date) AS sale_date, SUM(total_price) as total_sales
            FROM sales
            GROUP BY strftime('%Y-%m-%d', sale_date)
            ORDER BY sale_date ASC
        """)
        data = c.fetchall()
        conn.close()

        dates = [datetime.strptime(row[0], '%Y-%m-%d').date() for row in data]
        sales = [row[1] for row in data]

        fig = Figure(figsize=(8, 4), dpi=100)
        plot = fig.add_subplot(1, 1, 1)
        plot.plot(dates, sales, marker='o', linestyle='-', color='b')

        plot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plot.xaxis.set_major_locator(mdates.DayLocator(interval=max(len(dates)//10, 1)))
        fig.autofmt_xdate()

        plot.set_title('Date-wise Total Sales Trend')
        plot.set_xlabel('Date')
        plot.set_ylabel('Total Sales')

        # Create a new canvas for the chart and store its reference
        self.sales_trend_canvas = FigureCanvasTkAgg(fig, master=self.sales_chart_tab)
        self.sales_trend_canvas.draw()
        self.sales_trend_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesAnalyticsApp(root)
    root.geometry("800x600")  # Adjust as needed
    root.mainloop()
