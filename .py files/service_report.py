import sys
import os
import subprocess
import datetime
import mysql.connector
import customtkinter as ctk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from reportlab.pdfgen import canvas  # ReportLab canvas for PDF export

def Ownerlogin():
    subprocess.Popen([sys.executable, "Sale_Service_Emp.py"])
    window.destroy()


script_dir  = os.path.dirname(os.path.abspath(__file__))
reports_dir = os.path.join(script_dir, "Service_Reports")
os.makedirs(reports_dir, exist_ok=True)


conn = mysql.connector.connect(
        host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6")
cursor = conn.cursor()
cursor.execute("""
    SELECT Job_cardnumber, Service_date, First_name, Last_name,
           House_number, Unit_number, Purchase_date, Service_Type
      FROM ServiceRegister
     ORDER BY Service_date
""")
tickets = cursor.fetchall()
conn.close()


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Service Report")
window.geometry("1400x950")

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
                font=("Arial", 16, "bold"),
                rowheight=50,
                background="white",
                fieldbackground="white",
                foreground="black")
style.configure("Treeview.Heading", font=("Arial", 18, "bold"))


table_frame = ctk.CTkFrame(window, fg_color="#E4E4E4", corner_radius=10)
table_frame.pack(padx=20, pady=(20,10), fill="x")

cols = [
    "Job Card Number","Service Date","First Name","Last Name",
    "House Number","Unit Number","Purchase Date","Service Type","Download"
]
widths = [230,210,210,210,210,210,210,210,150]

tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=10)
for i,(col,w) in enumerate(zip(cols,widths), start=1):
    tree.column(f"#{i}", width=w, anchor="center")
    tree.heading(f"#{i}", text=col)
for row in tickets:
    tree.insert('', 'end', values=tuple(row)+("📥",))

vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.pack(side="left", fill="both", expand=False)
vsb.pack(side="right", fill="y")


chart_frame = ctk.CTkFrame(window, fg_color="#FFFFFF", corner_radius=0)
chart_frame.pack(padx=20, pady=(0,10), fill="x", anchor="center")
chart_frame.configure(height=300)


fig = Figure(figsize=(8,3))
ax = fig.add_subplot(111)
chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
chart_canvas.get_tk_widget().pack(fill="both", expand=True)

def update_chart():
    dates = [tree.set(item, "Service Date") for item in tree.get_children()]
    counts = {}
    for d in dates:
        try:
            dt = datetime.datetime.strptime(d, "%Y-%m-%d")
            key = dt.strftime("%Y-%m")
        except:
            key = "Unknown"
        counts[key] = counts.get(key, 0) + 1

    keys = sorted(counts.keys())
    vals = [counts[k] for k in keys]

    ax.clear()
    ax.bar(keys, vals, color="#4CAF50")
    ax.set_title("Service Requests per Month")
    ax.set_xlabel("Year‑Month")
    ax.set_ylabel("Count")
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(keys, rotation=0, fontsize=12)

    chart_canvas.draw()

# ─── Sort toggle for Service Date ────────────────────────────────────────────
sort_desc = False
def sort_by_service_date():
    global sort_desc
    items = [(tree.set(i, "Service Date"), i) for i in tree.get_children()]
    def parse(d):
        try:
            return datetime.datetime.strptime(d, '%Y-%m-%d')
        except:
            return datetime.datetime.min
    items.sort(key=lambda x: parse(x[0]), reverse=sort_desc)
    for idx, (_, iid) in enumerate(items):
        tree.move(iid, '', idx)
    sort_desc = not sort_desc
    update_chart()

tree.heading("#2", text="Service Date ⇅", command=sort_by_service_date)

# ─── Download handler ────────────────────────────────────────────────────────
def download_report(jobno, service_date):
    conn = mysql.connector.connect(
        host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"    )
    cur = conn.cursor()
    cur.execute("""
        SELECT Job_cardnumber, First_name, Last_name, Street_address,
               City, State, Phone_number, Service_date,
               House_number, Unit_number, Purchase_date, Service_Type
          FROM ServiceRegister
         WHERE Job_cardnumber = %s
    """, (jobno,))
    rec = cur.fetchone()
    conn.close()
    if not rec:
        messagebox.showerror("Error", f"No record found for {jobno}")
        return

    # Write CSV
    csv_name = f"Service_Ticket_{jobno}_{service_date}.csv"
    csv_path = os.path.join(reports_dir, csv_name)
    headers = ["Job Number", "First Name", "Last Name", "Street", "City", "State", "Phone",
               "Service Date","House Number", "Unit Number", "Purchase Date", "Type"]
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerow(rec)

    # Write PDF
    pdf_name = f"Service_Ticket_{jobno}_{service_date}.pdf"
    pdf_path = os.path.join(reports_dir, pdf_name)
    pdf = canvas.Canvas(pdf_path, pagesize=(400,600))
    y = 580
    for h, v in zip(headers, rec):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(20, y, f"{h}:")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, y, str(v))
        y -= 25
    pdf.save()

    
    try:
        os.startfile(reports_dir)           
    except OSError:
        subprocess.Popen(["xdg-open", reports_dir])  

def on_click(event):
    if tree.identify_region(event.x, event.y) != "cell":
        return
    if tree.identify_column(event.x) != f"#{len(cols)}":
        return
    row = tree.identify_row(event.y)
    if not row:
        return
    vals = tree.item(row, "values")
    download_report(vals[0], vals[1])

tree.bind("<ButtonRelease-1>", on_click)

# ─── Bottom Buttons ─────────────────────────────────────────────────────────
buttons_frame = ctk.CTkFrame(window, fg_color="#E4E4E4", corner_radius=10)
buttons_frame.pack(pady=(10,30))
ctk.CTkButton(
    buttons_frame, text="Back", width=200,
    font=("Arial",20,"bold"), command=Ownerlogin,
    fg_color="#d1ffec", text_color="black", border_width=2
).grid(row=0, column=0, padx=40, pady=10)
ctk.CTkButton(
    buttons_frame, text="Exit", width=200,
    font=("Arial",20,"bold"), command=window.destroy,
    fg_color="#fcdcdc", text_color="black", border_width=2
).grid(row=0, column=1, padx=40, pady=10)

# ─── Initial render ──────────────────────────────────────────────────────────
update_chart()
window.mainloop()
