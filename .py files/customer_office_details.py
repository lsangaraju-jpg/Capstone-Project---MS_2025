import sys
import os
import csv
import requests
import webbrowser
import subprocess

import customtkinter as ctk
from tkinter import messagebox
from tkintermapview import TkinterMapView
from PIL import Image, ImageGrab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path   = os.path.join(script_dir, "properties.csv")
icon_path  = os.path.join(script_dir, "images", "location.png")

OFFICE_INFO = {
    "Office Name": "United Leasing Apartments HQ",
    "Address":     "123 Main St, Mount Pleasant, USA",
    "Phone":       "(555) 123-4567",
    "Email":       "united@leasingapartments.com"
}
OFFICE_HOURS = {
    "Mon":  "09:00 AM - 06:00 PM",
    "Tue":  "09:00 AM - 06:00 PM",
    "Wed":  "09:00 AM - 06:00 PM",
    "Thu":  "09:00 AM - 06:00 PM",
    "Fri":  "09:00 AM - 06:00 PM",
    "Sat":  "10:00 AM - 05:00 PM",
    "Sun":  "Closed"
}

USER_LOC = (43.585867532016835, -84.7729829966881)

properties = []
if os.path.exists(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            properties.append({
                "name":        row["Name"],
                "lat":         float(row["Latitude"]),
                "lng":         float(row["Longitude"]),
                "description": row.get("Description", "")
            })
else:
    fallback = {
        "Mount Pleasant - Downtown": (43.6042366, -84.7737889),
        "Mount Pleasant - East":     (43.6108508, -84.7053924),
        "Mount Pleasant - West":     (43.6011616, -84.8768793),
        "Lansing":                   (42.7626028, -84.4875489),
        "Detroit":                   (42.3486146, -83.0553202),
    }
    for name, (lat, lng) in fallback.items():
        properties.append({
            "name":        name,
            "lat":         lat,
            "lng":         lng,
            "description": f"{name} – premium leasing property."
        })

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("green")

window = ctk.CTk()
window.title("Customer Portal")
window.geometry("1100x650")

# LEFT PANE
left_bg = "#f0f0f0"
left = ctk.CTkFrame(window, width=350, fg_color=left_bg, corner_radius=10)
left.pack(side="left", fill="y", padx=10, pady=10)

# Office Info header
ctk.CTkLabel(left, text="Office Info",
             font=("Arial",16,"bold"), text_color="black", anchor="w")\
    .pack(fill="x", padx=10, pady=(10,3))
# Office Info items
for k, v in OFFICE_INFO.items():
    ctk.CTkLabel(left, text=f"{k}: {v}",
                 font=("Arial",12), text_color="black", anchor="w")\
        .pack(fill="x", padx=10, pady=2)

# Office Hours header
ctk.CTkLabel(left, text="Office Hours",
             font=("Arial",16,"bold"), text_color="black", anchor="w")\
    .pack(fill="x", padx=10, pady=(8,3))
# Office Hours items
for day, h in OFFICE_HOURS.items():
    ctk.CTkLabel(left, text=f"{day}: {h}",
                 font=("Arial",12), text_color="black", anchor="w")\
        .pack(fill="x", padx=10, pady=2)

# Locations header
ctk.CTkLabel(left, text="Locations",
             font=("Arial",16,"bold"), text_color="black", anchor="w")\
    .pack(fill="x", padx=10, pady=(8,3))

# property buttons
window.selected_prop = None
def on_location_selected(prop):
    window.selected_prop = prop
    lat, lng = prop["lat"], prop["lng"]
    map_widget.set_position(lat, lng)
    map_widget.set_zoom(12)
    map_widget.delete_all_marker()
    map_widget.delete_all_path()
    map_widget.set_marker(USER_LOC[0], USER_LOC[1], text="You")
    marker = map_widget.set_marker(lat, lng, text=prop["name"])
    marker.command = lambda: messagebox.showinfo(prop["name"], prop["description"])

for p in properties:
    ctk.CTkButton(left, text=p["name"],
                  font=("Arial",12),
                  width=260,
                  fg_color="#4CAF50", hover_color="#45A049",
                  text_color="black",
                  command=lambda pp=p: on_location_selected(pp))\
        .pack(fill="x", padx=10, pady=3)

# Pin your location 
setting_mode = False
def enable_set_location(_=None):
    global setting_mode
    setting_mode = True
    messagebox.showinfo("Set Location",
        "Click on the map to update your precise 'You' location."
    )

# load icon
if not os.path.exists(icon_path):
    messagebox.showerror("Missing Icon", f"Location icon not found:\n{icon_path}")
    sys.exit(1)
pil_icon = Image.open(icon_path).convert("RGBA")
location_img = ctk.CTkImage(light_image=pil_icon,
                           dark_image=pil_icon,
                           size=(24,24))

set_loc_label = ctk.CTkLabel(
    left,
    image=location_img,
    text=" Pin your location",
    font=("Arial",12),
    text_color="black",
    compound="left",
    fg_color=left_bg
)
set_loc_label.pack(side="bottom", pady=10, padx=10, anchor="w")
set_loc_label.bind("<Button-1>", enable_set_location)

# RIGHT PANE
map_container = ctk.CTkFrame(window, fg_color="black", corner_radius=0)
map_container.pack(side="left", fill="both", expand=True, padx=10, pady=10)

map_widget = TkinterMapView(map_container, corner_radius=0)
map_widget.pack(fill="both", expand=True)
map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")

# initial “You” marker
map_widget.set_marker(USER_LOC[0], USER_LOC[1], text="You")
on_location_selected(properties[0])

def _on_map_click(coord):
    global setting_mode, USER_LOC
    if not setting_mode: return
    USER_LOC = coord
    setting_mode = False
    on_location_selected(window.selected_prop)
    messagebox.showinfo("Location Set",
        f"Your location is now:\n{coord[0]:.6f}, {coord[1]:.6f}"
    )

map_widget.add_left_click_map_command(_on_map_click)

# Get Directions
def get_directions():
    prop = window.selected_prop
    if not prop:
        messagebox.showwarning("No Selection","Select a property first.")
        return
    url = ("https://www.google.com/maps/dir/?api=1"
           f"&origin={USER_LOC[0]},{USER_LOC[1]}"
           f"&destination={prop['lat']},{prop['lng']}"
           "&travelmode=driving")
    webbrowser.open(url)

ctk.CTkButton(map_container, text="Get Directions",
              font=("Arial",12),
              fg_color="#FF9800", hover_color="#F57C00",
              text_color="black",
              command=get_directions,
              corner_radius=0).place(relx=0.1, rely=0.02, anchor="nw")

# Export Map → PNG & PDF
def export_map_view():
    x,y = map_container.winfo_rootx(), map_container.winfo_rooty()
    w,h = map_container.winfo_width(), map_container.winfo_height()
    img = ImageGrab.grab(bbox=(x,y,x+w,y+h))
    png = os.path.join(script_dir, "map_snapshot.png")
    img.save(png)
    pdf = os.path.join(script_dir, "map_snapshot.pdf")
    c = canvas.Canvas(pdf, pagesize=letter)
    c.drawImage(png,50,300,width=500,height=350)
    c.save()
    messagebox.showinfo("Export Complete", f"Saved:\n{png}\n{pdf}")

ctk.CTkButton(map_container, text="Export Map → PNG & PDF",
              font=("Arial",12),
              fg_color="#2196F3", hover_color="#1976D2",
              text_color="black",
              command=export_map_view,
              corner_radius=0).place(relx=0.8, rely=0.02, anchor="nw")

# EXIT button
def exit_to_login():
    subprocess.Popen([sys.executable,
        os.path.join(script_dir, "Customer_login_main.py")
    ])
    window.destroy()

ctk.CTkButton(map_container, text="Exit",
              font=("Arial",12),
              fg_color="#D32F2F", hover_color="#C62828",
              text_color="white",
              command=exit_to_login,
              corner_radius=0).place(relx=0.95, rely=0.98, anchor="se")

window.mainloop()
