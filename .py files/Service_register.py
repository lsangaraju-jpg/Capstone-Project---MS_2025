import sys
import datetime
from tkinter import ttk, messagebox, PhotoImage
import customtkinter as ctk
import mysql.connector
from PIL import Image
import os
import subprocess
from tkcalendar import DateEntry
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import shutil

# Default font setting
default_font = ("Arial", 16, "bold")

# --- Custom CTkLabelFrame if not defined ---
if not hasattr(ctk, "CTkLabelFrame"):
    class CTkLabelFrame(ctk.CTkFrame):
        def __init__(self, master, text="", font=None, **kwargs):
            self.custom_font = font if font is not None else default_font
            super().__init__(master, **kwargs)
            self.title_label = ctk.CTkLabel(self, text=text, text_color="black", font=self.custom_font)
            self.title_label.pack(side="top", anchor="w", padx=2, pady=2)
    ctk.CTkLabelFrame = CTkLabelFrame

# --- Appearance Settings ---
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# --- Main Window Setup ---
window = ctk.CTk()
window.title("Creating Service Request")
window.geometry("1300x1000")

# --- Image Loader with Safety Check ---
def resize_image(size, image_path):
    if not os.path.exists(image_path):
        messagebox.showerror("Error", f"Image not found:\n{image_path}")
        window.destroy()
        exit()
    # Return a CTkImage object for proper scaling on HighDPI displays
    return ctk.CTkImage(light_image=Image.open(image_path), size=size)

logo_path = os.path.join("images", "serviceregister.png")
logo_image = resize_image((200, 200), logo_path)
logo_label = ctk.CTkLabel(window, image=logo_image, text="")
logo_label.image = logo_image
logo_label.place(x=50, y=70)

# --- Navigation Function ---
def main():
    subprocess.Popen([sys.executable, "main.py"])
    window.destroy()
 
def Owner():
    subprocess.Popen([sys.executable, "Owner.py"])
    window.destroy()

def ServiceLoginpage():
    subprocess.Popen([sys.executable, "Sale_Service_Emp.py"])
    window.destroy()

# --- Generate Job Card Number ---
def generate_jobcard_number():
    connection = mysql.connector.connect(
              host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
    )
    mycursor = connection.cursor()
    mycursor.execute('SELECT COUNT(*) FROM ServiceRegister')
    row_count = mycursor.fetchone()[0]
    next_job_number = row_count + 1
    jobno_entry.delete(0, ctk.END)
    jobno_entry.insert(0, str(next_job_number))
    connection.close()

# --- Validate Required Fields ---
def validate_fields():
    # List each field widget with its friendly name.
    required_fields = [
        (jobno_entry, "Job Card Number"),
        (firstname_entry, "First Name"),
        (lastname_entry, "Last Name"),
        (streetaddress_entry, "Street Address"),
        (city_entry, "City"),
        (state_combobox, "State"),
        (phoneno_entry, "Phone Number"),
        (servicedate_entry, "Service Date"),
        (Housenumber_entry, "House Number"),
        (Unitnumber_entry, "Unit Number"),
        (house_purchase_date_entry, "Purchase Date"),
        (servicetype_combobox, "Service Type"),
    ]
    for widget, name in required_fields:
        # Use .get() to retrieve the current value.
        if widget.get().strip() == "":
            messagebox.showerror("Validation Error", f"Please enter a value for '{name}'.")
            widget.focus()
            return False
    return True

# --- Export Service Register Data to CSV with Dynamic File Name ---
def export_to_csv(data):
    # Use job card number (data[0]) and service date (data[7]) for file naming.
    csv_file = f"Servie_Ticket_{data[0]}_{data[7]}.csv"
    headers = [
        "Job Card Number", "First Name", "Last Name", "Street Address",
        "City", "State", "Phone Number", "Service Date", "House Number",
        "Unit Number", "Purchase Date", "Service Type"
    ]
    # Create a new CSV file for this service ticket.
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerow(data)
    
    # Copy CSV file to Desktop and Downloads
    home_dir = os.path.expanduser("~")
    destinations = ["Desktop", "Downloads"]
    for folder in destinations:
        dest_dir = os.path.join(home_dir, folder)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create directory {dest_dir}:\n{e}")
                continue
        dest_file = os.path.join(dest_dir, csv_file)
        try:
            shutil.copy(csv_file, dest_file)
        except Exception as e:
            messagebox.showerror("Error", f"Error copying file to {dest_file}:\n{e}")


def export_to_pdf(data):
    
    pdf_filename = f"Servie_Ticket_{data[0]}_{data[7]}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Service Request Details")
    c.setFont("Helvetica", 12)
    labels = [
        "Job Card Number", "First Name", "Last Name", "Street Address",
        "City", "State", "Phone Number", "Service Date", "House Number",
        "Unit Number", "Purchase Date", "Service Type"
    ]
    y = height - 100
    for label, value in zip(labels, data):
        c.drawString(50, y, f"{label}: {value}")
        y -= 20
    c.save()
    
   
    home_dir = os.path.expanduser("~")
    destinations = ["Desktop", "Downloads"]
    for folder in destinations:
        dest_dir = os.path.join(home_dir, folder)
        if not os.path.exists(dest_dir):
            try:
                os.makedirs(dest_dir)
            except Exception as e:
                messagebox.showerror("Error", f"Cannot create directory {dest_dir}:\n{e}")
                continue
        dest_file = os.path.join(dest_dir, pdf_filename)
        try:
            shutil.copy(pdf_filename, dest_file)
        except Exception as e:
            messagebox.showerror("Error", f"Error copying file to {dest_file}:\n{e}")

# --- Create Service Request ---
def serviceticket():
    # Validate all fields first. If any field is empty, exit early.
    if not validate_fields():
        return

    connection = mysql.connector.connect(
           host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6" )
    mycursor = connection.cursor()
    # Retrieve data from widgets
    Job_cardnumber = jobno_entry.get()
    First_name = firstname_entry.get()
    Last_name = lastname_entry.get()
    Street_address = streetaddress_entry.get()
    City = city_entry.get()
    State = state_combobox.get()
    Phone_number = phoneno_entry.get()
    Service_date = servicedate_entry.get()
    House_number = Housenumber_entry.get()
    Unit_number = Unitnumber_entry.get()
    Purchase_date = house_purchase_date_entry.get()
    Service_Type = servicetype_combobox.get()
    
    query = ("INSERT INTO ServiceRegister "
             "(Job_cardnumber, First_name, Last_name, Street_address, City, State, Phone_number, "
             "Service_date, House_number, Unit_number, Purchase_date, Service_Type) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    values = (Job_cardnumber, First_name, Last_name, Street_address, City, State,
              Phone_number, Service_date, House_number, Unit_number, Purchase_date, Service_Type)
    mycursor.execute(query, values)
    connection.commit()
    connection.close()
    
    # Export the service register details to CSV and PDF using dynamic file names
    export_to_csv(values)
    export_to_pdf(values)
    
    messagebox.showinfo("Message", "Service Ticket Created Successfully")
    subprocess.Popen([sys.executable, "Sale_Service_Emp.py"])
    window.destroy()

# --- Define Clear Form Function ---
def clear_form():
    # Clear Customer Details
    jobno_entry.delete(0, ctk.END)
    firstname_entry.delete(0, ctk.END)
    lastname_entry.delete(0, ctk.END)
    streetaddress_entry.delete(0, ctk.END)
    city_entry.delete(0, ctk.END)
    state_combobox.set("")
    phoneno_entry.delete(0, ctk.END)
    servicedate_entry.set_date(datetime.date.today())
    # Clear House Details
    Housenumber_entry.delete(0, ctk.END)
    Unitnumber_entry.delete(0, ctk.END)
    house_purchase_date_entry.set_date(datetime.date.today())
    # Clear Service Type
    servicetype_combobox.set("")

# --- Build the Main Frame and Panels ---
frame = ctk.CTkFrame(window, fg_color="#d9d9ff")
frame.place(relx=0.5, rely=0.5, anchor="center")

# --- Customer Details Panel ---
SrCustomer_details_frame = ctk.CTkLabelFrame(frame, text="Customer Details", font=("Arial", 16, "bold"), fg_color="#d9d9ff")
SrCustomer_details_frame.grid(row=0, column=0, sticky="news", padx=20, pady=10)

customer_inner = ctk.CTkFrame(SrCustomer_details_frame, fg_color="#d9d9ff")
customer_inner.pack(fill="both", expand=True)

label_width = 130

jobno_label = ctk.CTkLabel(customer_inner, text="Job Card Number:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
jobno_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
jobno_entry = ctk.CTkEntry(customer_inner, width=200, font=("Arial", 14, "bold"))
jobno_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

generate_button = ctk.CTkButton(customer_inner, text="Generate Job Number", font=("Arial", 14, "bold"), fg_color="#FFFFFF", text_color="black", command=generate_jobcard_number)
generate_button.grid(row=0, column=2, padx=10, pady=5)

first_name_label = ctk.CTkLabel(customer_inner, text="First Name:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
first_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
firstname_entry = ctk.CTkEntry(customer_inner, width=200, font=("Arial", 14, "bold"))
firstname_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

last_name_label = ctk.CTkLabel(customer_inner, text="Last Name:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
last_name_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
lastname_entry = ctk.CTkEntry(customer_inner, width=200, font=("Arial", 14, "bold"))
lastname_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

street_address_label = ctk.CTkLabel(customer_inner, text="Street Address:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
street_address_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
streetaddress_entry = ctk.CTkEntry(customer_inner, width=200, font=("Arial", 14, "bold"))
streetaddress_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

city_label = ctk.CTkLabel(customer_inner, text="City:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
city_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
city_entry = ctk.CTkEntry(customer_inner, width=200, font=("Arial", 14, "bold"))
city_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

state_label = ctk.CTkLabel(customer_inner, text="State:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
state_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
state_combobox = ctk.CTkComboBox(customer_inner,
    values=["", "AL", "AK", "AR", "AZ", "CA", "CO", "CT", "DE", "FL",
            "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "MA",
            "MD", "ME", "MI", "MN", "MO", "MS", "MT", "NC", "ND", "NE",
            "NH", "NJ", "NM", "NV", "NY", "OH", "OK", "OR", "PA", "RI",
            "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WI", "WV",
            "WY"], width=170, font=("Arial", 14, "bold"))
state_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

phoneno_label = ctk.CTkLabel(customer_inner, text="Phone Number:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
phoneno_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
phoneno_entry = ctk.CTkEntry(customer_inner, width=200, font=("Arial", 14, "bold"))
phoneno_entry.grid(row=6, column=1, padx=10, pady=5, sticky="w")

servicedate_label = ctk.CTkLabel(customer_inner, text="Service In Date:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
servicedate_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
servicedate_entry = DateEntry(customer_inner, selectmode="day", date_pattern='yyyy-mm-dd', width=18, font=("Arial", 14, "bold"))
servicedate_entry.grid(row=7, column=1, padx=10, pady=5, sticky="w")

for widget in customer_inner.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# --- House Details Panel ---
House_details_frame = ctk.CTkLabelFrame(frame, text="House Details", font=("Arial", 16, "bold"), fg_color="#d9d9ff")
House_details_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

House_inner = ctk.CTkFrame(House_details_frame, fg_color="#d9d9ff")
House_inner.pack(fill="both", expand=True)

Housenumber_label = ctk.CTkLabel(House_inner, text="House Number:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
Housenumber_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
Housenumber_entry = ctk.CTkEntry(House_inner, width=200, font=("Arial", 14, "bold"))
Housenumber_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

Unitnumber_label = ctk.CTkLabel(House_inner, text="Unit Number:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
Unitnumber_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
Unitnumber_entry = ctk.CTkEntry(House_inner, width=200, font=("Arial", 14, "bold"))
Unitnumber_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

house_purchase_date_label = ctk.CTkLabel(House_inner, text="Purchase Date:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
house_purchase_date_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
house_purchase_date_entry = DateEntry(House_inner, selectmode="day", date_pattern='yyyy-mm-dd', width=18, font=("Arial", 14, "bold"))
house_purchase_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

for widget in House_inner.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# --- Service Type Panel ---
Servicetype_details_frame = ctk.CTkLabelFrame(frame, text="Type of Service", font=("Arial", 16, "bold"), fg_color="#d9d9ff")
Servicetype_details_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)

service_inner = ctk.CTkFrame(Servicetype_details_frame, fg_color="#d9d9ff")
service_inner.pack(fill="both", expand=True)

servicetype_label = ctk.CTkLabel(service_inner, text="Service Type:", font=("Arial", 14, "bold"), text_color="black", fg_color="#d9d9ff", width=label_width, anchor="e")
servicetype_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
servicetype_combobox = ctk.CTkComboBox(service_inner, values=["", "Free Service", "Paid Service"], width=170, font=("Arial", 14, "bold"))
servicetype_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# --- Clear Form Button Panel ---
clear_frame = ctk.CTkFrame(frame, fg_color="#d9d9ff")
clear_frame.grid(row=3, column=0, sticky="news", padx=20, pady=0)
clear_form_button = ctk.CTkButton(clear_frame, text="Clear Form", font=("Arial", 14, "bold"),
                                  fg_color="#FFFFFF", text_color="black", command=clear_form)
clear_form_button.pack(padx=10, pady=0)

# --- Action Buttons Panel ---
buttons_frame = ctk.CTkLabelFrame(frame, text="", font=("Arial", 11, "bold"), fg_color="#d9d9ff")
buttons_frame.grid(row=4, column=0, sticky="news", padx=20, pady=10)

buttons_inner = ctk.CTkFrame(buttons_frame, fg_color="#d9d9ff")
buttons_inner.pack(fill="both", expand=True)

btnServiceRequest = ctk.CTkButton(buttons_inner, width=150, text="Create Service Request", font=("Arial", 14, "bold"),
                                  fg_color="#FFFFFF", text_color="black", command=serviceticket)
btnServiceRequest.grid(row=0, column=0, padx=50, pady=10)

btnMainPage = ctk.CTkButton(buttons_inner, width=150, text="Main Page", font=("Arial", 14, "bold"),
                            fg_color="#FFFFFF", text_color="black", command=ServiceLoginpage)
btnMainPage.grid(row=0, column=1, padx=50, pady=10)

btnExit = ctk.CTkButton(buttons_inner, width=150, text="Exit", font=("Arial", 14, "bold"),
                        fg_color="#FFFFFF", text_color="black", command=main)
btnExit.grid(row=0, column=2, padx=50, pady=10)

for widget in buttons_inner.winfo_children():
    widget.grid_configure(padx=50, pady=10)
    

back_icon = resize_image((50, 50), os.path.join("images", "back.png"))
back_btn = ctk.CTkButton(
    window,
    image=back_icon,
    text="Go Back",
    fg_color="#242424",              
    hover_color="#242424",           
    command=Owner         
)
back_btn.image = back_icon           
back_btn.place(x=20, y=20)
back_btn.place(relx=0.98, y=20, anchor="ne")

window.mainloop()
