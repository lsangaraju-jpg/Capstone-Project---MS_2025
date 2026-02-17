import sys
import os
import subprocess
import customtkinter as ctk
import mysql.connector
from PIL import Image
from tkinter import messagebox

# ─── Configuration ──────────────────────────────────────────────────────────────
IMAGE_W     = 350   # image width in pixels
IMAGE_H     = 400   # image height in pixels
IMAGE_PADX  = 20    # horizontal gap between image and form
IMAGE_PADY  = 20    # vertical gap above the image and form
FRAME_PADX  = 10    # horizontal gap between frame and image
FRAME_PADY  = 50    # vertical gap above the frame

# ─── Helpers ────────────────────────────────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))

def resize_image(size, image_path):
    full = os.path.join(script_dir, image_path)
    if not os.path.exists(full):
        raise FileNotFoundError(f"Image not found: {full}")
    pil = Image.open(full).resize(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=pil, size=size)

def main_page():
    subprocess.Popen([sys.executable, os.path.join(script_dir, "main.py")])
    window.destroy()

def toggle_password_visibility():
    if show_password_var.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

def clear_form():
    userid_entry.delete(0, "end")
    password_entry.delete(0, "end")

def Employee_login_main():
    conn = mysql.connector.connect(
        host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
        )
    cur = conn.cursor()
    query = (
        "SELECT * FROM usercredentials "
        "WHERE Username=%s AND user_password=%s "
        "AND Department IN (%s, %s)"
    )
    cur.execute(query, (
        userid_entry.get(), password_entry.get(),
        'Employee - Sales', 'Employee - Service'
    ))
    if cur.fetchone():
        messagebox.showinfo(title="Message", message="Login Successful")
        subprocess.Popen([sys.executable, os.path.join(script_dir, "Sale_Service_Emp.py")])
        window.destroy()
    else:
        invalid_msg.place(relx=0.53, rely=0.52)
    cur.close()
    conn.close()

# ─── CTk Appearance ─────────────────────────────────────────────────────────────
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# ─── Main Window ────────────────────────────────────────────────────────────────
window = ctk.CTk()
window.title("Welcome to United Apartments - Employee Login")
window.geometry("1000x500")

top_frame = ctk.CTkFrame(window, fg_color="transparent")
top_frame.pack(pady=(IMAGE_PADY, 0))

emp_img   = resize_image((IMAGE_W, IMAGE_H), "images/employeeloginmain.png")
img_label = ctk.CTkLabel(
    top_frame,
    image=emp_img,
    text="",
    width=IMAGE_W,
    height=IMAGE_H
)
img_label.pack(side="left", padx=(IMAGE_PADX, 0))

frame = ctk.CTkFrame(
    top_frame,
    fg_color="#FFD485",
    corner_radius=10,
    width=IMAGE_W,
    height=IMAGE_H
)
frame.pack(
    side="left",
    padx=(FRAME_PADX, 0),   # horizontal offset from image
    pady=(FRAME_PADY, 0)    # vertical offset down from top_frame
)

# ─── Inside Login Frame ─────────────────────────────────────────────────────────
user_info_frame = ctk.CTkFrame(frame, fg_color="#d1873d", corner_radius=10)
user_info_frame.grid(row=0, column=0, padx=20, pady=30)

ctk.CTkLabel(
    user_info_frame, text="User ID:",
    font=("Arial", 16, 'bold'), text_color="white"
).grid(row=0, column=0, padx=(10,2), pady=5, sticky="e")
ctk.CTkLabel(
    user_info_frame, text="Password:",
    font=("Arial", 16, 'bold'), text_color="white"
).grid(row=1, column=0, padx=(10,2), pady=5, sticky="e")

userid_entry = ctk.CTkEntry(
    user_info_frame, font=("Arial", 16),
    width=300, placeholder_text="Enter Email"
)
userid_entry.grid(row=0, column=1, padx=(10,10), pady=5, sticky="w")

password_entry = ctk.CTkEntry(
    user_info_frame, show="*",
    font=("Arial", 16), width=300,
    placeholder_text="Enter Password"
)
password_entry.grid(row=1, column=1, padx=(10,10), pady=5, sticky="w")

control_frame = ctk.CTkFrame(user_info_frame, fg_color="transparent")
control_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="e")

ctk.CTkButton(
    control_frame, text="Clear Form", command=clear_form,
    font=("Arial", 10, "bold"), fg_color="#005e2e",
    text_color="white", width=100, height=30
).pack(side="right", padx=(0,20))

show_password_var = ctk.BooleanVar()
ctk.CTkCheckBox(
    control_frame, text="Show Password",
    variable=show_password_var,
    command=toggle_password_visibility,
    font=("Arial", 12, "bold"),
    fg_color="#d1873d", width=140
).pack(side="right", padx=5)

invalid_msg = ctk.CTkLabel(
    window, text="Invalid Credentials! Please Try again.",
    font=("Arial", 16, 'bold'), text_color="#C20A0A",
    fg_color="#FFD485"
)
invalid_msg.place_forget()

buttons_frame = ctk.CTkFrame(frame, fg_color="#d1873d", corner_radius=30)
buttons_frame.grid(row=3, column=0, padx=20, pady=20)

ctk.CTkButton(
    buttons_frame, text="Sign-In", font=("Arial", 16, 'bold'),
    command=Employee_login_main, fg_color="#005e2e",
    text_color="white", width=120, height=40
).grid(row=0, column=0, padx=20, pady=20)

ctk.CTkButton(
    buttons_frame, text="Main page", font=("Arial", 16, 'bold'),
    command=main_page, fg_color="#005e2e",
    text_color="white", width=120, height=40
).grid(row=0, column=1, padx=20, pady=20)

ctk.CTkButton(
    buttons_frame, text="Exit", font=("Arial", 16, 'bold'),
    command=window.destroy, fg_color="#005e2e",
    text_color="white", width=120, height=40
).grid(row=0, column=2, padx=20, pady=20)

# ─── Back to Home Link ──────────────────────────────────────────────────────────
back_icon   = resize_image((50, 50), "images/back.png")
back_button = ctk.CTkLabel(window, image=back_icon, text="", fg_color="transparent")
back_button.place(relx=0.95, rely=0.02, anchor="ne")
back_button.bind("<Button-1>", lambda e: main_page())

ctk.CTkLabel(
    window, text="Back to Home", font=("Arial", 12),
    text_color="white", fg_color="transparent"
).place(relx=0.98, rely=0.12, anchor="ne")

window.mainloop()
