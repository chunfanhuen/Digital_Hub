from fpdf import FPDF
import os
from tkinter import Tk, filedialog

# Create a sample dictionary with placeholder data
invoice_data = {
    'invoice_id': [1001],
    'order_id': [1],
    'order_number': [101],
    'store_id': [1],
    'store_location': ['City A'],
    'product_id': [101],
    'product_name': ['Product X'],
    'product_brand': ['Brand A'],
    'quantity_sold': [2],
    'order_date': ['2023-07-01'],
    'delivery_date': ['2023-07-05'],
    'sale_amount': [200.00],
    'customer_id': [10001],
    'customer_name': ['Alice'],
    'invoice_date': ['2023-07-01'],
    'invoice_total': [300.00]
}

# Create a class for generating a PDF invoice
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'INVOICE', 0, 1, 'C')
        self.set_font('Arial', 'I', 12)
        self.cell(0, 10, 'Company Name', 0, 1, 'C')
        self.cell(0, 10, 'Address Line 1', 0, 1, 'C')
        self.cell(0, 10, 'Address Line 2', 0, 1, 'C')
        self.cell(0, 10, 'Phone: (000) 000-0000', 0, 1, 'C')
        self.cell(0, 10, 'Email: info@company.com', 0, 1, 'C')
        self.ln(10)

    def invoice_body(self, invoice_data):
        self.set_font('Arial', '', 12)

        # Invoice Information
        self.cell(100, 10, f'Invoice ID: {invoice_data["invoice_id"][0]}', 0, 0)
        self.cell(0, 10, f'Invoice Date: {invoice_data["invoice_date"][0]}', 0, 1)
        self.cell(100, 10, f'Order ID: {invoice_data["order_id"][0]}', 0, 0)
        self.cell(0, 10, f'Order Number: {invoice_data["order_number"][0]}', 0, 1)
        self.cell(100, 10, f'Store Location: {invoice_data["store_location"][0]}', 0, 0)
        self.cell(0, 10, f'Order Date: {invoice_data["order_date"][0]}', 0, 1)
        self.ln(10)

        # Customer Information
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Customer Information', 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Customer ID: {invoice_data["customer_id"][0]}', 0, 1)
        self.cell(0, 10, f'Customer Name: {invoice_data["customer_name"][0]}', 0, 1)
        self.ln(10)

        # Product Information
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Product Details', 0, 1)
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'Product ID: {invoice_data["product_id"][0]}', 0, 1)
        self.cell(0, 10, f'Product Name: {invoice_data["product_name"][0]}', 0, 1)
        self.cell(0, 10, f'Product Brand: {invoice_data["product_brand"][0]}', 0, 1)
        self.cell(0, 10, f'Quantity Sold: {invoice_data["quantity_sold"][0]}', 0, 1)
        self.cell(0, 10, f'Sale Amount: ${invoice_data["sale_amount"][0]:.2f}', 0, 1)
        self.ln(10)

        # Totals
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Total Invoice Amount: ${invoice_data["invoice_total"][0]:.2f}', 0, 1)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Create a PDF object
pdf = PDF()
pdf.add_page()
pdf.invoice_body(invoice_data)

# Use Tkinter to open a file dialog to let the user choose where to save the file
root = Tk()
root.withdraw()  # Hide the root window
file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

if file_path:
    pdf.output(file_path)
    print(f"Invoice saved as {file_path}")
else:
    print("Save operation cancelled")
import datetime
print(dir(datetime))
