import sys
import os
import subprocess
import customtkinter as ctk
from PIL import Image

# Appearance
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

# Base path
script_dir = os.path.dirname(os.path.abspath(__file__))

def load_ctk_image(size, image_path):
    full = os.path.join(script_dir, image_path)
    if not os.path.exists(full):
        raise FileNotFoundError(f"Image not found: {full}")
    img = Image.open(full).resize(size, Image.Resampling.LANCZOS)
    return ctk.CTkImage(light_image=img, size=size)

def create_label_frame(master, text, **kwargs):
    frame = ctk.CTkFrame(master, fg_color=kwargs.get("fg_color", "#748079"),
                         corner_radius=kwargs.get("corner_radius", 10),
                         border_width=2, border_color="white")
    ctk.CTkLabel(frame, text=text, font=kwargs.get("font", ("Arial",15,"bold")),
                 text_color="white", fg_color=frame._fg_color).pack(anchor="nw", padx=30, pady=(5,0))
    container = ctk.CTkFrame(frame, fg_color=frame._fg_color, corner_radius=10)
    container.pack(expand=True, fill="both", padx=30, pady=5)
    frame.container = container
    return frame

def launch_owner():
    window = ctk.CTk()
    window.title("LEASING HOUSES - Welcome Admin")
    window.geometry("1100x800")

    bg_img = load_ctk_image((350,450), "images/united.png")
    ctk.CTkLabel(window, image=bg_img, text="").place(relx=0.75, rely=0.4, anchor="center")

    main_frame = ctk.CTkFrame(window, fg_color="#748079",
                              corner_radius=10, border_width=2,
                              border_color="#fcae79")
    main_frame.place(relx=0.28, rely=0.49, anchor="center")

    # Sections: Lease, Sales, Service, Reports
    sections = [
        ("User Addition", "User_addition.py", "User Addition"),
        ("Properties", "customer_office_details.py", "My Properties"),
        ("Sales", "create_invoice.py", "Generate New Invoice"),
        ("Service", "Service_register.py", "Register Service"),
        ("Reports - Sales", "sales_report.py", "Sale Report"),
        ("Reports - Service", "service_report.py", "Service Report"),
    ]
    for idx, (title, script, btn_text) in enumerate(sections):
        frame = create_label_frame(main_frame, title)
        frame.grid(row=idx, column=0, sticky="news", padx=85, pady=10)
        ctk.CTkButton(
            frame.container,
            text=btn_text,
            font=("Goudy Type", 15, "bold"),
            fg_color="#606060",
            width=200, height=40,
            border_width=2, border_color="#8c4a54",
            command=lambda s=script: subprocess.Popen(
                [sys.executable, os.path.join(script_dir, s)]
            ) or window.destroy()
        ).grid(row=0, column=0, padx=30, pady=5)

    # Bottom controls
    bottom = ctk.CTkFrame(window, fg_color="#4d4d4d", corner_radius=10,
                          border_width=2, border_color="#fdae7a")
    bottom.place(relx=0.75, rely=0.85, anchor="center")
    for txt, tgt in [("Change Password","Change_password_admin.py"),
                     ("Sign-Out","main.py"),
                     ("Exit","main.py")]:
        ctk.CTkButton(
            bottom, text=txt, font=("Arial",15,"bold"),
            command=lambda s=tgt: subprocess.Popen(
                [sys.executable, os.path.join(script_dir, s)]
            ) or window.destroy()
        ).pack(side="left", padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    launch_owner()
