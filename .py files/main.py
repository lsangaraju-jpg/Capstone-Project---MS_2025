import customtkinter as ctk
import subprocess
import sys
import os
from PIL import Image

script_dir = os.path.dirname(os.path.abspath(__file__))

def resize_image(size, image_path):
    full_path = os.path.join(script_dir, image_path)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Image not found: {full_path}")
    pil = Image.open(full_path).resize(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=pil, size=size)

def Owner():
    subprocess.Popen([sys.executable, os.path.join(script_dir, "Admin_login_main.py")])
    window.destroy()

def Employee_login():
    subprocess.Popen([sys.executable, os.path.join(script_dir, "Employee_login_main.py")])
    window.destroy()

def Userlogin():
    subprocess.Popen([sys.executable, os.path.join(script_dir, "User_addition_customer.py")])
    window.destroy()


ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")


window = ctk.CTk()
window.title("Welcome to United Apartments")
window.geometry("1100x600")

total_w, total_h = 1150, 600
pane_w = int(total_w * 0.45)   
pane_h = int(total_h * 0.75)   
margin = 20

top_container = ctk.CTkFrame(window, fg_color="transparent")
top_container.pack(pady=(margin, 0))  


img = resize_image((pane_w, pane_h), "images/mainbackground.png")
img_label = ctk.CTkLabel(
    top_container,
    image=img,
    text="",
    width=pane_w,
    height=pane_h
)
img_label.pack(side="left", padx=margin)

# Right: Login frame (same size)
login_frame = ctk.CTkFrame(
    top_container,
    fg_color="transparent",
    corner_radius=10,
    width=pane_w,
    height=pane_h
)
login_frame.pack(side="left", padx=margin)


ctk.CTkLabel(
    login_frame,
    text="Welcome to United Leasing Apartments",
    font=("Kunstler Script", 50, "bold"),  
    text_color="white",
    pady=10,
    wraplength=pane_w - 90
).pack(pady=(20,10), padx=0)

for text, cmd in [
    ("Owner Login", Owner),
    ("Employee Login", Employee_login),
    ("Customer Login", Userlogin),
]:
    ctk.CTkButton(
        login_frame,
        text=text,
        font=("Stencil", 20),
        command=cmd,
        width=220,
        height=50,
        fg_color="#cccccc",
        text_color="black"
    ).pack(pady=10)


footer = ctk.CTkFrame(window, fg_color="transparent")
footer.pack(side="bottom", fill="x", pady=margin)

ctk.CTkLabel(
    footer,
    text="Live Smart, Live Luxuriously with Leasing Apartments",
    font=("Inknut Antiqua", 18, "bold"),
    text_color="#E07F7D",
    fg_color="transparent"
).pack(pady=(0,5))

remaining_text = (
    "United Leasing Apartments is the largest student housing community.\n"
    "We offer an unmatched level of luxury, convenience, and comfort at an affordable price.\n"
    "Leasing Apartments is the place you want to call home!"
)
ctk.CTkLabel(
    footer,
    text=remaining_text,
    font=("Inknut Antiqua", 12, "bold"),
    text_color="#2B87CC",
    fg_color="transparent",
    wraplength=total_w - 40
).pack()

window.mainloop()
