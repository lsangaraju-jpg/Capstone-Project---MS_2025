import sys
from tkinter import ttk, PhotoImage, messagebox
import customtkinter as ctk
from tkcalendar import DateEntry
import mysql.connector
from PIL import Image
import os
import subprocess
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# --- Appearance Settings ---
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# --- Main Window Setup ---
window = ctk.CTk()
window.title("Create an Invoice")
window.geometry("1000x1200")

# --- DateEntry Font Style ---
style = ttk.Style()
style.configure("Custom.DateEntry", font=("Arial", 14))

# --- Image Loader with Safety Check ---
def resize_image(size, image_path):
    if not os.path.exists(image_path):
        messagebox.showerror("Error", f"Image not found:\n{image_path}")
        window.destroy()
        exit()
    return ctk.CTkImage(light_image=Image.open(image_path), size=size)

# --- Audit Image ---
audit_image = resize_image((150, 150), os.path.join("images", "audit.png"))
audit_label = ctk.CTkLabel(window, image=audit_image, text="")
audit_label.place(relx=0.21, rely=0.02, anchor="ne")

# --- Navigation Function ---
def Admin_login_main():
    subprocess.Popen([sys.executable, "Sale_Service_Emp.py"])
    window.destroy()

# --- Generate Invoice Number ---
def generate_invoice_number():
    connection = mysql.connector.connect(
              host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
    )
    mycursor = connection.cursor()
    mycursor.execute('SELECT COUNT(*) FROM Invoice_Details')
    row_count = mycursor.fetchone()[0]
    next_invoice_number = row_count + 1
    invoiceno_entry.delete(0, ctk.END)
    invoiceno_entry.insert(0, str(next_invoice_number))
    connection.close()

# --- Validate Required Fields ---
def validate_fields():
    required_fields = [
        (firstname_entry, "First Name"),
        (lastname_entry, "Last Name"),
        (gender_combobox, "Gender"),
        (dob_entry, "DOB"),
        (streetaddress_entry, "Street Address"),
        (city_entry, "City"),
        (state_combobox, "State"),
        (phoneno_entry, "Phone Number"),
        (invoiceno_entry, "Invoice Number"),
        (invoicedate_entry, "Invoice Date"),
        (House_number_entry, "House Number"),
        (unit_number_entry, "Unit Number")
    ]
    for widget, name in required_fields:
        if widget.get().strip() == "":
            messagebox.showerror("Validation Error", f"Please enter a value for '{name}'.")
            return False
    return True

# --- Export Invoice Data to CSV with Dynamic File Name ---
def export_to_csv(data):
    # The file name is in the format: Invoice_<InvoiceNumber>_<InvoiceDate>.csv
    csv_file = f"Invoice_{data[8]}_{data[9]}.csv"
    headers = [
        "First Name", "Last Name", "Gender", "DOB", "Street Address",
        "City", "State", "Phone Number", "Invoice Number", "Invoice Date",
        "House Number", "Unit Number"
    ]
    # Write a new CSV file for the current invoice.
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerow(data)

# --- Export Invoice Data to PDF using ReportLab with Dynamic File Name ---
def export_to_pdf(data):
    
    pdf_filename = f"Invoice_{data[8]}_{data[9]}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Invoice Details")
    c.setFont("Helvetica", 12)
    labels = [
        "First Name", "Last Name", "Gender", "DOB", "Street Address",
        "City", "State", "Phone Number", "Invoice Number", "Invoice Date",
        "House Number", "Unit Number"
    ]
    y = height - 100
    for label, value in zip(labels, data):
        c.drawString(50, y, f"{label}: {value}")
        y -= 20
    c.save()

# --- Create Invoice ---
def create_invoice():
    if not validate_fields():
        return

    data = (
        firstname_entry.get(), lastname_entry.get(), gender_combobox.get(), dob_entry.get(),
        streetaddress_entry.get(), city_entry.get(), state_combobox.get(), phoneno_entry.get(),
        invoiceno_entry.get(), invoicedate_entry.get(), House_number_entry.get(), unit_number_entry.get()
    )
    
    connection = mysql.connector.connect(
        host="localhost", 
        user="root", 
        password="Nedstark@123", 
        database="BIS698W1700_GRP6"
    )
    mycursor = connection.cursor()
    mycursor.execute(
        "INSERT INTO Invoice_Details (First_name, Last_name, Gender, BirthDate, StreetAddress, City, State, Phonenumber, Invoice_number, Invoice_date, House_Number, Unit_Number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
        data
    )
    connection.commit()
    connection.close()
    
    export_to_csv(data)
    export_to_pdf(data)
    
    messagebox.showinfo("Message", "Created Invoice Successfully")
    subprocess.Popen([sys.executable, "Sale_Service_Admin.py"])
    window.destroy()

# --- Clear Form Function ---
def clear_form():
    for widget in [
        firstname_entry, lastname_entry, streetaddress_entry, city_entry, phoneno_entry,
        invoiceno_entry, House_number_entry, unit_number_entry
    ]:
        widget.delete(0, ctk.END)
    gender_combobox.set(" ")
    state_combobox.set("")
    dob_entry.set_date("")
    invoicedate_entry.set_date("")

# --- Field Generator ---
def create_label_entry(parent, text, row, column, label_width=140):
    label = ctk.CTkLabel(parent, text=text, font=("Arial", 14, 'bold'), text_color="black", width=label_width, anchor="w")
    label.grid(row=row, column=column, padx=(10, 0), pady=5, sticky="w")
    entry = ctk.CTkEntry(parent, width=250, font=("Arial", 14))
    entry.grid(row=row, column=column+1, padx=10, pady=5, sticky="w")
    return entry

# --- Calendar Icon ---
calendar_icon_path = os.path.join("images", "calendar_icon.png")
try:
    from tkinter import PhotoImage  # Ensure PhotoImage is available
    calendar_icon = PhotoImage(file=calendar_icon_path)
except Exception:
    messagebox.showerror("Error", f"Calendar icon not found:\n{calendar_icon_path}")
    calendar_icon = None

# --- Container Frame ---
frame = ctk.CTkFrame(window, fg_color="#E4E4E4", width=1000, height=1000, corner_radius=10)
frame.place(relx=0.58, rely=0.5, anchor="center")

# --- Customer Details Frame ---
Customer_details_frame = ctk.CTkFrame(frame, fg_color="#E4E4E4", corner_radius=10)
Customer_details_frame.grid(row=0, column=0, padx=20, pady=0, sticky="w")

ctk.CTkLabel(Customer_details_frame, text="Customer Details", text_color="#2fa572", font=("Arial", 20, 'bold'))\
    .grid(row=0, columnspan=2, pady=10, sticky="w")

firstname_entry = create_label_entry(Customer_details_frame, "First Name:", 1, 0)
lastname_entry = create_label_entry(Customer_details_frame, "Last Name:", 2, 0)

ctk.CTkLabel(Customer_details_frame, text="Gender:", font=("Arial", 14, 'bold'), text_color="black", width=140, anchor="w")\
    .grid(row=3, column=0, padx=(10, 0), pady=5, sticky="w")
gender_combobox = ctk.CTkComboBox(Customer_details_frame, values=[" ", "Male", "Female", "Unknown"], width=250, font=("Arial", 14, 'bold'))
gender_combobox.grid(row=3, column=1, padx=10, pady=5, sticky="w")

ctk.CTkLabel(Customer_details_frame, text="DOB:", font=("Arial", 14, 'bold'), text_color="black", width=140, anchor="w")\
    .grid(row=4, column=0, padx=(10, 0), pady=5, sticky="w")
dob_entry = DateEntry(Customer_details_frame, selectmode="day", date_pattern='yyyy-mm-dd', width=20, style="Custom.DateEntry", font=("Arial", 14), buttonimage=calendar_icon)
dob_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

streetaddress_entry = create_label_entry(Customer_details_frame, "Street Address:", 5, 0)
city_entry = create_label_entry(Customer_details_frame, "City:", 6, 0)

ctk.CTkLabel(Customer_details_frame, text="State:", font=("Arial", 14, 'bold'), text_color="black", width=140, anchor="w")\
    .grid(row=7, column=0, padx=(10, 0), pady=5, sticky="w")
state_combobox = ctk.CTkComboBox(Customer_details_frame,
    values=["", "AL", "AK", "AR", "AZ", "CA", "CO", "CT", "DE", "FL",
            "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA",
            "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
            "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
            "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WI", "WV",
            "WY"], width=170, font=("Arial", 11))
state_combobox.grid(row=7, column=1, padx=10, pady=5, sticky="w")

phoneno_entry = create_label_entry(Customer_details_frame, "Phone Number:", 8, 0)

# --- House Details Frame ---
House_details_frame = ctk.CTkFrame(frame, fg_color="#E4E4E4", corner_radius=10)
House_details_frame.grid(row=1, column=0, padx=20, pady=0, sticky="w")

ctk.CTkLabel(House_details_frame, text="House Details", text_color="#2fa572", font=("Arial", 20, 'bold'))\
    .grid(row=0, columnspan=2, pady=10, sticky="w")

invoiceno_entry = create_label_entry(House_details_frame, "Invoice Number:", 1, 0)
generate_button = ctk.CTkButton(House_details_frame, text="Generate Invoice Number", font=("Arial", 10, 'bold'), command=generate_invoice_number)
generate_button.grid(row=1, column=2, padx=10, sticky="w")

ctk.CTkLabel(House_details_frame, text="Invoice Date:", font=("Arial", 14, 'bold'), text_color="black", width=140, anchor="w")\
    .grid(row=2, column=0, padx=(10, 0), pady=5, sticky="w")
invoicedate_entry = DateEntry(House_details_frame, selectmode="day", date_pattern='yyyy-mm-dd', width=20, style="Custom.DateEntry", font=("Arial", 14), buttonimage=calendar_icon)
invoicedate_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

House_number_entry = create_label_entry(House_details_frame, "House Number:", 3, 0)
unit_number_entry = create_label_entry(House_details_frame, "Unit Number:", 4, 0)

clear_form_button = ctk.CTkButton(
    House_details_frame,
    text="Clear Form",
    font=("Arial", 12, 'bold'),
    command=clear_form,
    width=80,
    height=25
)
clear_form_button.grid(row=4, column=2, padx=10, pady=5, sticky="w")

# --- Action Buttons Frame ---
buttons_frame = ctk.CTkFrame(frame, fg_color="#E4E4E4", corner_radius=10)
buttons_frame.grid(row=2, column=0, padx=10, pady=20)

ctk.CTkButton(buttons_frame, width=100, text="Create Invoice", font=("Arial", 14, 'bold'), command=create_invoice)\
    .grid(row=0, column=0, padx=30, pady=10)
ctk.CTkButton(buttons_frame, width=100, text="Main Page", font=("Arial", 14, 'bold'), command=Admin_login_main)\
    .grid(row=0, column=1, padx=30, pady=10)
ctk.CTkButton(buttons_frame, width=100, text="Exit", font=("Arial", 14, 'bold'), command=window.destroy)\
    .grid(row=0, column=2, padx=30, pady=10)

window.mainloop()
