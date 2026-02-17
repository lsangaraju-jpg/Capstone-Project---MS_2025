import customtkinter as ctk
import subprocess
import mysql.connector
from PIL import Image, ImageTk
import sys
import os
from tkinter import messagebox  

# --- Utility Function to Resize Images ---
def resize_image(size, image_path):
    """Resize the image to the specified size."""
    image = Image.open(image_path)
    resized_image = image.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(resized_image)

# --- Navigation Functions ---
def Admin_login_main():
    subprocess.Popen(["python", "Employee_login_main.py"])
    window.destroy()

def toggle_password_visibility():
    if show_password_var.get():
        newpassword_entry.configure(show="")
    else:
        newpassword_entry.configure(show="*")

def change_password():
    connection = mysql.connector.connect(
        host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
        )
    mycursor = connection.cursor()
    query = (
        "UPDATE usercredentials "
        "SET user_password = %s "
        "WHERE Username = %s"
    )
    
    mycursor.execute(query, (newpassword_entry.get(), userid_entry.get()))
    connection.commit()
    connection.close()

    messagebox.showinfo("Message", "Password Changed successfully")
    subprocess.Popen(["python", "Employee_login_main.py"])
    window.destroy()

def exit_program():
    subprocess.Popen(["python", "main.py"])
    window.destroy()

# --- Appearance Setup ---
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# --- Create Main Window ---
window = ctk.CTk()
window.title("Change Password - Employee")
window.geometry("800x600")

# --- Background Image Setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
bg_path = os.path.join(script_dir, "images", "changepassword.png")
print(f"Looking for background image at: {bg_path}")
if not os.path.exists(bg_path):
    raise FileNotFoundError(f"Background image not found: {bg_path}")

bg_image = resize_image((1000, 700), bg_path)
bg_label = ctk.CTkLabel(window, image=bg_image, text="")
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --- Form Frame ---
form_frame = ctk.CTkFrame(window, fg_color="#d68f24", width=500, height=250, corner_radius=10)
form_frame.place(relx=0.65, rely=0.2, anchor="center")

# --- Change Password Form ---
changepass_frame = ctk.CTkFrame(form_frame, fg_color="#d68f24", corner_radius=10)
changepass_frame.grid(row=0, column=0, padx=10, pady=25)

# Increase vertical spacing for the new password row
userid_label = ctk.CTkLabel(
    changepass_frame, text="User ID:", font=("Arial", 15, "bold"),
    text_color="black", fg_color="#d68f24"
)
userid_label.grid(row=0, column=0, padx=40, pady=40, sticky="e")

userid_entry = ctk.CTkEntry(
    changepass_frame, font=("Arial", 15), width=300,
    placeholder_text="Enter User ID"
)
userid_entry.grid(row=0, column=1, padx=10, pady=10)

# Increase vertical padding between rows by setting a larger pady for the new password label
newpassword_label = ctk.CTkLabel(
    changepass_frame, text="New Password:", font=("Arial", 15, "bold"),
    text_color="black", fg_color="#d68f24"
)
newpassword_label.grid(row=1, column=0, padx=10, pady=30, sticky="e")

newpassword_entry = ctk.CTkEntry(
    changepass_frame, show="*", font=("Arial", 15), width=300,
    placeholder_text="Enter New Password"
)
newpassword_entry.grid(row=1, column=1, padx=10, pady=10)

show_password_var = ctk.BooleanVar()
show_password_checkbox = ctk.CTkCheckBox(
    changepass_frame, text="Show Password",
    variable=show_password_var, command=toggle_password_visibility,
    font=("Arial", 12, "bold"), fg_color="#d68f24", text_color="black"
)
show_password_checkbox.grid(row=2, column=1, sticky="w", padx=10, pady=20)

for widget in changepass_frame.winfo_children():
    widget.grid_configure(padx=5, pady=5)

# --- Buttons Frame ---
buttons_frame = ctk.CTkFrame(form_frame, fg_color="#d68f24", corner_radius=10)
buttons_frame.grid(row=1, column=0, padx=30, pady=15)

btnChangePassword = ctk.CTkButton(
    buttons_frame, text="Change Password",
    font=("Arial", 12, "bold"), command=change_password,
    fg_color="#748079", text_color="white", width=120, height=40
)
btnChangePassword.grid(row=0, column=0, padx=15, pady=5)

btnMainPage = ctk.CTkButton(
    buttons_frame, text="Main Page",
    font=("Arial", 12, "bold"), command=Admin_login_main,
    fg_color="#748079", text_color="white", width=120, height=40
)
btnMainPage.grid(row=0, column=1, padx=15, pady=5)

btnExit = ctk.CTkButton(
    buttons_frame, text="Exit",
    font=("Arial", 12, "bold"), command=exit_program,
    fg_color="#748079", text_color="white", width=120, height=40
)
btnExit.grid(row=0, column=2, padx=15, pady=5)

for widget in buttons_frame.winfo_children():
    widget.grid_configure(padx=15, pady=5)

key_image_path = os.path.join(script_dir, "images", "key.png")  
if os.path.exists(key_image_path):
    # Resize and place the image
    key_image = resize_image((200, 200), key_image_path)
    key_label = ctk.CTkLabel(window, image=key_image, text="")
    # Position the image just below the form frame
    key_label.place(relx=0.85, rely=0.51, anchor="center")
else:
    print(f"Optional key image not found at: {key_image_path}. Skipping additional image.")

window.mainloop()