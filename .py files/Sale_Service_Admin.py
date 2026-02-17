import customtkinter as ctk
import subprocess
import sys
from PIL import Image, ImageTk

default_font = ("Arial", 16, "bold")

def resize_image(size, image_path):
    """Resize the image to the specified size."""
    image = Image.open(image_path)
    try:
        resized_image = image.resize(size, Image.Resampling.LANCZOS)
    except AttributeError:
        resized_image = image.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(resized_image)

if not hasattr(ctk, "CTkLabelFrame"):
    class CTkLabelFrame(ctk.CTkFrame):
        def __init__(self, master, text="", font=None, **kwargs):
            self.custom_font = font if font is not None else default_font
            super().__init__(master, **kwargs)
            self.title_label = ctk.CTkLabel(self, text=text, text_color="black", font=self.custom_font)
            self.title_label.pack(side="top", anchor="w", padx=2, pady=2)
    ctk.CTkLabelFrame = CTkLabelFrame

# ----------------- Service Login Functions ----------------- #
def Service_Request():
    subprocess.Popen([sys.executable, "Service_register.py"])
    root.destroy()

def Service_User_login():
    subprocess.Popen([sys.executable, "Employee_login_main.py"])
    root.destroy()

def Service_Report():
    subprocess.Popen([sys.executable, "service_report.py"])
    root.destroy()

def Service_Change_pass():
    subprocess.Popen([sys.executable, "Change_password_Emp.py"])
    root.destroy()

# ----------------- Sale Login Functions ----------------- #
def Sale_User_login():
    subprocess.Popen([sys.executable, "Employee_login_main.py"])
    root.destroy()

def Create_Invoice():
    subprocess.Popen([sys.executable, "create_invoice.py"])
    root.destroy()

def Sale_Report():
    subprocess.Popen([sys.executable, "sales_report.py"])
    root.destroy()

def Sale_Change_pass():
    subprocess.Popen([sys.executable, "Change_password_Emp.py"])
    root.destroy()

# ----------------- Main Window Setup ----------------- #
root = ctk.CTk()
root.title("Welcome to Sales and Service Management - Admin")

# Set container color to #242424 (can be changed as needed)
container = ctk.CTkFrame(root, fg_color="#242424")
container.pack(padx=5, pady=45)

container.grid_columnconfigure(0, weight=1)
container.grid_columnconfigure(1, weight=1)

# ----------------- Service Login Frame (Left Column) ----------------- #
service_frame = ctk.CTkFrame(
    container,
    fg_color="#ffffb8",
    border_width=2,
    border_color="black",
    corner_radius=10
)
service_frame.grid(row=0, column=0, sticky="n", padx=45, pady=45)

service_inner = ctk.CTkFrame(service_frame, fg_color="#ffffb8")
service_inner.pack(padx=25, pady=25)

servicetasks_frame = ctk.CTkLabelFrame(
    service_inner,
    text="Service Tasks",
    fg_color="#ffffb8",
    corner_radius=10,
    font=default_font
)
servicetasks_frame.pack(pady=2)
if hasattr(servicetasks_frame, "title_label"):
    servicetasks_frame.title_label.configure(text_color="black", font=default_font)

btnServiceTicket = ctk.CTkButton(
    servicetasks_frame,
    text="Create Service Ticket",
    width=200,
    fg_color="#ffff6b",
    command=Service_Request,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnServiceTicket.pack(pady=20, padx=20)

btnServiceReport = ctk.CTkButton(
    servicetasks_frame,
    text="Generate Service Report",
    width=200,
    fg_color="#ffff6b",
    command=Service_Report,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnServiceReport.pack(pady=2, padx=2)

# ----------------- Sale Login Frame (Right Column) ----------------- #
sale_frame = ctk.CTkFrame(
    container,
    fg_color="#ffffb8",
    border_width=2,
    border_color="black",
    corner_radius=10
)
sale_frame.grid(row=0, column=1, sticky="n", padx=45, pady=45)

sale_inner = ctk.CTkFrame(sale_frame, fg_color="#ffffb8")
sale_inner.pack(padx=25, pady=25)

saletasks_frame = ctk.CTkLabelFrame(
    sale_inner,
    text="Sale Tasks",
    fg_color="#ffffb8",
    corner_radius=10,
    font=default_font
)
saletasks_frame.pack(pady=2)
if hasattr(saletasks_frame, "title_label"):
    saletasks_frame.title_label.configure(text_color="black", font=default_font)

btnSaleInvoice = ctk.CTkButton(
    saletasks_frame,
    text="Create Invoice",
    width=200,
    fg_color="#ffff6b",
    command=Create_Invoice,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnSaleInvoice.pack(pady=20, padx=20)

btnSaleReport = ctk.CTkButton(
    saletasks_frame,
    text="Generate Sale Report",
    width=200,
    fg_color="#ffff6b",
    command=Sale_Report,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnSaleReport.pack(pady=2, padx=2)

# ----------------- Bottom Frame for Service Buttons ----------------- #
bottom_frame = ctk.CTkLabelFrame(
    container,
    fg_color="#242424",
    border_width=2,
    border_color="#242424",
    corner_radius=10,
    font=default_font
)
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=30, pady=10)

inner_bottom_frame = ctk.CTkFrame(bottom_frame, fg_color="#242424")
inner_bottom_frame.pack(padx=10, pady=0, fill="x", expand=True)

btnServiceChangepass = ctk.CTkButton(
    inner_bottom_frame,
    text="Change Password",
    width=180,
    fg_color="#ffff6b",
    command=Service_Change_pass,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnServiceChangepass.pack(side="left", padx=20, pady=20)

btnServiceSignout = ctk.CTkButton(
    inner_bottom_frame,
    text="Sign out",
    width=180,
    fg_color="#ffff6b",
    command=Service_User_login,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnServiceSignout.pack(side="left", padx=20, pady=20)

btnServiceExit = ctk.CTkButton(
    inner_bottom_frame,
    text="Exit",
    width=180,
    fg_color="#ffff6b",
    command=root.destroy,
    text_color="black",
    border_width=2,
    border_color="black",
    font=default_font
)
btnServiceExit.pack(side="left", padx=20, pady=20)

root.geometry("1000x600")

# ----------------- Back Button Integration ----------------- #
back_icon = resize_image((50, 50), "images/back.png")
back_button = ctk.CTkLabel(root, image=back_icon, text="", fg_color="#242424")
back_button.place(relx=0.51, rely=0.5, anchor="ne")

def on_back_click(event):
    subprocess.Popen([sys.executable, 'Owner.py'])
    root.destroy()

back_button.bind("<Button>", on_back_click)

back_text_label = ctk.CTkLabel(root, text="Click Arrow to Go Back", font=default_font, text_color="white", fg_color="#242424")
back_text_label.place(relx=0.59, rely=0.57, anchor="ne")

# ----------------- House Icon Integration ----------------- #
house_icon = resize_image((90, 90), "images/houseicon.png")
house_button = ctk.CTkLabel(root, image=house_icon, text="", fg_color="#242424")
house_button.place(relx=0.53, rely=0.75, anchor="ne")

house_text_label = ctk.CTkLabel(root, text="Go Home", font=default_font, text_color="white", fg_color="#242424")
house_text_label.place(relx=0.535, rely=0.87, anchor="ne")

def on_house_click(event):
    subprocess.Popen([sys.executable, 'main.py'])
    root.destroy()

house_button.bind("<Button>", on_house_click)

root.mainloop()
