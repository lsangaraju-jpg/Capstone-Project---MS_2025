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
from reportlab.pdfgen import canvas  # This stays as `canvas`

def Owner_login():
    subprocess.Popen([sys.executable, "Sale_Service_Emp.py"])
    window.destroy()

# ─── Prepare reports directory ────────────────────────────────────────────────
script_dir  = os.path.dirname(os.path.abspath(__file__))
reports_dir = os.path.join(script_dir, "Sales_Reports")
os.makedirs(reports_dir, exist_ok=True)

# ─── Fetch invoice data ───────────────────────────────────────────────────────
conn = mysql.connector.connect(
         host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
)
cur = conn.cursor()
cur.execute("""
    SELECT Invoice_number, Invoice_date, First_name, Last_name,
           House_Number, Unit_number
      FROM Invoice_Details
     ORDER BY Invoice_date
""")
rows = cur.fetchall()
conn.close()

# ─── Build UI ─────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("Admin - Sales Report")
window.geometry("1300x950")

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
                font=("Arial", 16, "bold"),
                rowheight=50,
                background="white",
                fieldbackground="white",
                foreground="black")
style.configure("Treeview.Heading", font=("Arial", 18, "bold"))

# ─── Table + Scrollbar ────────────────────────────────────────────────────────
table_frame = ctk.CTkFrame(window, fg_color="#E4E4E4", corner_radius=10)
table_frame.pack(pady=20, padx=20, fill="x")

cols   = ["Invoice Number","Invoice Date","First Name","Last Name",
          "House Number","Unit Number","Download"]
widths = [250,250,320,320,250,250,200]
tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
for i,(col,w) in enumerate(zip(cols,widths), start=1):
    tree.column(f"#{i}", width=w, anchor="center")
    tree.heading(f"#{i}", text=col)
for r in rows:
    tree.insert("", "end", values=tuple(r)+("📥",))
vsb = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=vsb.set)
tree.pack(side="left", fill="both", expand=False)
vsb.pack(side="right", fill="y")

# ─── Chart Frame (fixed height, centered) ────────────────────────────────────
chart_frame = ctk.CTkFrame(window, fg_color="#FFFFFF", corner_radius=0)
chart_frame.pack(padx=20, pady=(0,10), fill="x", anchor="center")
chart_frame.configure(height=300)

# ─── Create Figure, Axes & rename the Matplotlib canvas instance ───────────
fig = Figure(figsize=(6,3))
ax = fig.add_subplot(111)
chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)  # renamed!
chart_canvas.get_tk_widget().pack(fill="both", expand=True)

def update_chart():
    dates = [tree.set(i, "Invoice Date") for i in tree.get_children()]
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
    ax.bar(keys, vals)
    ax.set_title("Invoices per Month")
    ax.set_xlabel("Year‑Month")
    ax.set_ylabel("Count")
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels(keys, rotation=0, fontsize=12)

    chart_canvas.draw()  # use the renamed canvas

# ─── Sort toggle on Invoice Date (#2) ────────────────────────────────────────
sort_desc = False
def sort_by_date():
    global sort_desc
    items = [(tree.set(i, "Invoice Date"), i) for i in tree.get_children()]
    def parse(d):
        try:
            return datetime.datetime.strptime(d, "%Y-%m-%d")
        except:
            return datetime.datetime.min
    items.sort(key=lambda x: parse(x[0]), reverse=sort_desc)
    for idx, (_, iid) in enumerate(items):
        tree.move(iid, "", idx)
    sort_desc = not sort_desc
    update_chart()

tree.heading("#2", text="Invoice Date ⇅", command=sort_by_date)

# ─── Download Handler ────────────────────────────────────────────────────────
def download_invoice(inv_no, inv_date):
    conn = mysql.connector.connect(
              host="localhost", user="root",
        password="Nedstark@123", database="BIS698W1700_GRP6"
    )
    c = conn.cursor()
    c.execute("""
        SELECT Invoice_number, Invoice_date, First_name, Last_name,
               House_Number, Unit_number
          FROM Invoice_Details
         WHERE Invoice_number = %s
    """, (inv_no,))
    rec = c.fetchone()
    conn.close()
    if not rec:
        messagebox.showerror("Error", f"No invoice found: {inv_no}")
        return

    rec_ext = rec + ("", "", "")
    headers = ["Invoice Number","Invoice Date","First Name","Last Name",
               "House Number","Unit Number","Price","Taxes","Total"]

    csv_file = f"Invoice_{inv_no}_{inv_date}.csv"
    with open(os.path.join(reports_dir, csv_file), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerow(rec_ext)

    # Now canvas refers to reportlab.pdfgen.canvas
    pdf_file = f"Invoice_{inv_no}_{inv_date}.pdf"
    pdf_path = os.path.join(reports_dir, pdf_file)
    pdf = canvas.Canvas(pdf_path, pagesize=(400,600))
    y = 580
    for h, v in zip(headers, rec_ext):
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(20, y, f"{h}:")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(200, y, str(v))
        y -= 25
    pdf.save()

    # Open the folder
    try:
        os.startfile(reports_dir)
    except:
        subprocess.Popen(["xdg-open", reports_dir])

def on_click(event):
    if tree.identify_region(event.x, event.y) != "cell":
        return
    if tree.identify_column(event.x) != f"#{len(cols)}":
        return
    row = tree.identify_row(event.y)
    if not row:
        return
    inv_no, inv_date = tree.item(row, "values")[:2]
    download_invoice(inv_no, inv_date)

tree.bind("<ButtonRelease-1>", on_click)

# ─── Bottom Buttons ─────────────────────────────────────────────────────────
btn_frame = ctk.CTkFrame(window, fg_color="#E4E4E4", corner_radius=10)
btn_frame.pack(pady=20)
ctk.CTkButton(
    btn_frame, text="Back", width=200,
    font=("Arial",20,"bold"), command=Owner_login,
    fg_color="#d1ffec", text_color="black", border_width=2
).grid(row=0, column=0, padx=60, pady=10)
ctk.CTkButton(
    btn_frame, text="Exit", width=200,
    font=("Arial",20,"bold"), command=window.destroy,
    fg_color="#fcdcdc", text_color="black", border_width=2
).grid(row=0, column=1, padx=60, pady=10)

# ─── Initial Chart Draw ──────────────────────────────────────────────────────
update_chart()

window.mainloop()
