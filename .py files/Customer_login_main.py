import sys
import subprocess
import mysql.connector
import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
import os

# ─── Configuration ──────────────────────────────────────────────────────────────
IMAGE_W     = 400   # image width in pixels
IMAGE_H     = 450   # image height in pixels
IMAGE_PADX  = 20    # horizontal gap between image and frame
IMAGE_PADY  = 30    # vertical gap above the image and form
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

def main():
    subprocess.Popen([sys.executable, os.path.join(script_dir, "Owner.py")])
    window.destroy()

def toggle_password_visibility():
    if show_password_var.get():
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

def clear_form():
    userid_entry.delete(0, "end")
    password_entry.delete(0, "end")

def User_login_page():
    try:
        conn = mysql.connector.connect(
                   host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
        )
    except mysql.connector.Error as err:
        messagebox.showerror("DB Error", f"Could not connect:\n{err}")
        return

    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM usercredentials "
        "WHERE Username=%s AND user_password=%s AND Department='Customer';",
        (userid_entry.get(), password_entry.get())
    )
    result = cur.fetchone()
    conn.close()

    if result:
        messagebox.showinfo("Success", "Login Successful")
        subprocess.Popen([sys.executable, os.path.join(script_dir, "customer_office_details.py")])
        window.destroy()
    else:
        invalid_msg.place(relx=0.55, rely=0.55)

# ─── CTk Appearance ─────────────────────────────────────────────────────────────
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# ─── Main Window ────────────────────────────────────────────────────────────────
window = ctk.CTk()
window.title("Welcome to United Apartments - Customer")
window.geometry("1000x500")

# ─── Top frame for bg image + login form ────────────────────────────────────────
top_frame = ctk.CTkFrame(window, fg_color="transparent")
top_frame.pack(pady=(IMAGE_PADY, 0))

# Background image
bg_img = resize_image((IMAGE_W, IMAGE_H), "images/userloginmain.png")
bg_label = ctk.CTkLabel(
    top_frame,
    image=bg_img,
    text="",
    width=IMAGE_W,
    height=IMAGE_H
)
bg_label.pack(side="left", padx=(IMAGE_PADX, 0))

# Login frame, same height as image
frame = ctk.CTkFrame(
    top_frame,
    fg_color="#FFD485",
    corner_radius=10,
    width=IMAGE_W,
    height=IMAGE_H
)
frame.pack(
    side="left",
    padx=(FRAME_PADX, 0),
    pady=(FRAME_PADY, 0)
)

# ─── Inside Login Frame ─────────────────────────────────────────────────────────
user_info = ctk.CTkFrame(frame, fg_color="#d1873d", corner_radius=10)
user_info.grid(row=0, column=0, padx=20, pady=30)

ctk.CTkLabel(user_info, text="User ID:",  font=("Arial",16,"bold"), text_color="white")\
    .grid(row=0, column=0, sticky="e", padx=(10,2), pady=5)
ctk.CTkLabel(user_info, text="Password:",font=("Arial",16,"bold"), text_color="white")\
    .grid(row=1, column=0, sticky="e", padx=(10,2), pady=5)

userid_entry = ctk.CTkEntry(user_info, width=300, placeholder_text="Enter Email", font=("Arial",16))
userid_entry.grid(row=0, column=1, padx=10, pady=5)
password_entry = ctk.CTkEntry(user_info, width=300, show="*", placeholder_text="Enter Password", font=("Arial",16))
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Show / Clear controls
ctrl = ctk.CTkFrame(user_info, fg_color="transparent")
ctrl.grid(row=2, column=0, columnspan=2, sticky="e", padx=(0,20), pady=10)

ctk.CTkButton(
    ctrl, text="Clear Form", command=clear_form,
    fg_color="#005e2e", text_color="white", font=("Arial",10,"bold"),
    width=100, height=30
).pack(side="right", padx=(0,20))

show_password_var = ctk.BooleanVar()
ctk.CTkCheckBox(
    ctrl, text="Show Password", variable=show_password_var,
    command=toggle_password_visibility, font=("Arial",12,"bold"),
    fg_color="#d1873d", text_color="white", width=140
).pack(side="right", padx=5)

invalid_msg = ctk.CTkLabel(
    window, text="Invalid Credentials! Please Try Again.",
    font=("Arial",16,"bold"), text_color="#C20A0A",
    fg_color="#FFD485"
)
invalid_msg.place_forget()

# Buttons row
btn_frame = ctk.CTkFrame(frame, fg_color="#d1873d", corner_radius=30)
btn_frame.grid(row=3, column=0, padx=20, pady=30)

ctk.CTkButton(btn_frame, text="Sign-In", command=User_login_page,
              fg_color="#005e2e", text_color="white",
              font=("Arial",16,"bold"), width=120, height=40)\
    .grid(row=0, column=0, padx=20, pady=20)
ctk.CTkButton(btn_frame, text="Main page", command=main,
              fg_color="#005e2e", text_color="white",
              font=("Arial",16,"bold"), width=120, height=40)\
    .grid(row=0, column=1, padx=20, pady=20)
ctk.CTkButton(btn_frame, text="Exit", command=window.destroy,
              fg_color="#005e2e", text_color="white",
              font=("Arial",16,"bold"), width=120, height=40)\
    .grid(row=0, column=2, padx=20, pady=20)

# ─── Back to Home Link ──────────────────────────────────────────────────────────
back_icon = resize_image((50,50), "images/back.png")
back_btn  = ctk.CTkLabel(window, image=back_icon, text="", fg_color="transparent")
back_btn.place(relx=0.95, rely=0.02, anchor="ne")
back_btn.bind("<Button-1>", lambda e: (subprocess.Popen([sys.executable, os.path.join(script_dir, "main.py")]), window.destroy()))

ctk.CTkLabel(
    window, text="Back to Home", font=("Arial",12),
    text_color="white", fg_color="transparent"
).place(relx=0.98, rely=0.13, anchor="ne")

window.mainloop()
