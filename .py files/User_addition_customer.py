import os
import subprocess
import sys
import mysql.connector
from PIL import Image
from tkinter import messagebox

import customtkinter as ctk

# ─── Define script directory ────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

def resize_image(size, image_path):
    """Load & resize for high-DPI via CTkImage."""
    full = os.path.join(script_dir, image_path)
    pil = Image.open(full).resize(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=pil, size=size)

def Ownerlogin():
    subprocess.Popen([sys.executable, os.path.join(script_dir, "customer_office_details.py")])
    window.destroy()

def go_to_customer_login(event=None):
    target = os.path.join(script_dir, "Customer_login_main.py")
    subprocess.Popen([sys.executable, target])
    window.destroy()

def clear_form():
    userid_entry.delete(0, "end")
    password_entry.delete(0, "end")

def toggle_password_visibility():
    if show_password_var.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

def user_addition():
    Username      = userid_entry.get()
    user_password = password_entry.get()
    Department    = department_combobox.get()  # always "Customer"
    final_dept    = Department

    if not Username or not user_password:
        messagebox.showerror("Error", "User ID and Password cannot be empty.")
        return

    conn = mysql.connector.connect(
        host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
    )
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usercredentials (Username, user_password, Department) VALUES (%s, %s, %s)",
        (Username, user_password, final_dept)
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "ID Created Successfully")
    subprocess.Popen([sys.executable, os.path.join(script_dir, "Customer_login_main.py")])
    window.destroy()

# ─── Main Window ─────────────────────────────────────────────────────────────
window = ctk.CTk()
window.title("User Addition - Customer")
window.geometry("700x600")

# Background image
bg_image = resize_image((150, 150), os.path.join("images", "Useraddition.png"))
ctk.CTkLabel(window, image=bg_image, text="")\
    .place(relx=0, rely=-0.31, relwidth=1, relheight=1)

# Container frames
main_frame = ctk.CTkFrame(window, fg_color="transparent", corner_radius=10)
main_frame.place(relx=0.5, rely=0.65, anchor="center")
form_frame = ctk.CTkFrame(main_frame, fg_color="#50C878")
form_frame.pack(padx=40, pady=30)

# Username
ctk.CTkLabel(
    form_frame, text="User Name:",
    font=("Arial", 20), text_color="#000"
).grid(row=0, column=0, sticky="w", padx=10, pady=10)
userid_entry = ctk.CTkEntry(form_frame, width=300)
userid_entry.grid(row=0, column=1, padx=10, pady=10)

# Password
ctk.CTkLabel(
    form_frame, text="Password:",
    font=("Arial", 20), text_color="#000"
).grid(row=1, column=0, sticky="w", padx=10, pady=10)
password_entry = ctk.CTkEntry(form_frame, show="*", width=300)
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Show & Clear controls
show_password_var = ctk.BooleanVar()
control_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
control_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)

ctk.CTkCheckBox(
    control_frame,
    text="Show Password",
    variable=show_password_var,
    command=toggle_password_visibility,
    font=("Arial", 12, "bold"),
    fg_color="#50C878",
    text_color="#000"
).pack(side="left", padx=(0,15))

ctk.CTkButton(
    control_frame,
    text="Clear Form",
    command=clear_form,
    font=("Arial", 10, "bold"),
    fg_color="#005e2e",
    text_color="white",
    width=100,
    height=30
).pack(side="left")

# Department dropdown (only Customer)
ctk.CTkLabel(
    form_frame, text="Department:",
    font=("Arial", 20), text_color="#000"
).grid(row=3, column=0, sticky="w", padx=10, pady=10)
department_combobox = ctk.CTkComboBox(
    form_frame,
    values=["Customer"],
    width=300,
    font=("Arial", 14, "bold")
)
department_combobox.set("Customer")
department_combobox.grid(row=3, column=1, padx=10, pady=10)

# Action buttons
button_frame = ctk.CTkFrame(main_frame, fg_color="#50C878")
button_frame.pack(pady=20)

ctk.CTkButton(
    button_frame,
    width=150,
    text="Create User",
    font=("Arial", 20, "bold"),
    text_color="#000",
    fg_color=("#00d0bc", "#00d0bc"),
    command=user_addition,
    border_color="#00d0bc",
    border_width=2
).grid(row=0, column=0, padx=20, pady=10)

ctk.CTkButton(
    button_frame,
    width=150,
    text="Main Page",
    font=("Arial", 20, "bold"),
    text_color="#000",
    fg_color=("#00d0bc", "#00d0bc"),
    command=Ownerlogin,
    border_color="#00d0bc",
    border_width=2
).grid(row=0, column=1, padx=20, pady=10)

ctk.CTkButton(
    button_frame,
    width=150,
    text="Exit",
    font=("Arial", 20, "bold"),
    text_color="#000",
    fg_color=("#00d0bc", "#00d0bc"),
    command=window.destroy,
    border_color="#00d0bc",
    border_width=2
).grid(row=0, column=2, padx=20, pady=10)

# ─── Already-have-an-account Link ─────────────────────────────────────────────
link_frame = ctk.CTkFrame(window, fg_color="transparent", corner_radius=0)
link_frame.place(relx=0.5, rely=0.77, anchor="center")

ctk.CTkLabel(
    link_frame,
    text="Already have an account?",
    font=("Arial", 16),
    text_color="#BBBBBB"
).pack(side="left")

sign_in_label = ctk.CTkLabel(
    link_frame,
    text=" Sign in",
    font=("Arial", 16, "underline"),
    text_color="#007AFF",
    cursor="hand2"
)
sign_in_label.pack(side="left")
sign_in_label.bind("<Button-1>", go_to_customer_login)

window.mainloop()
