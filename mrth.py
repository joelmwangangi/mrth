import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sqlite3
import pandas as pd

# Create and connect to the new database named 'mtrh.db'
conn = sqlite3.connect("mtrh.db")
cursor = conn.cursor()

# Create the patients table with all required columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creation_date TEXT,
    diagnosis_date TEXT,
    diagnosis TEXT,
    healthcare_service_unit TEXT,
    patient_id TEXT,
    mobile_number TEXT,
    gender TEXT,
    age INTEGER
)
""")
conn.commit()

# List of healthcare service units
clinic_names = [
    "S4A OPD Ambulatory", "PW 2 OPD - Consultant Room - MTRH",
    "Ambulatory Consultation - MTRH", "ED - Medical Emergency (Rm 14) - MTRH",
    "Diabetic Clinic - Chandaria - MTRH", "ENT - General - MTRH",
    "Haematology Clinic - Chandaria - MTRH", "MOPC CLINIC - MTRH",
    "Dental- OMFS- Oral & Maxillofacial Clinic - MTRH", "General-Oncology Telemedicine - MTRH"
]

# Function to submit data
def submit_data():
    creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Auto timestamp
    diagnosis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Auto diagnosis date
    diagnosis = diagnosis_entry.get()
    healthcare_unit = healthcare_unit_dropdown.get()
    patient_id = patient_id_entry.get()
    mobile_number = mobile_number_entry.get()
    gender = gender_dropdown.get()
    age = age_entry.get()

    if not diagnosis or not healthcare_unit or not patient_id or not mobile_number or not gender or not age:
        messagebox.showwarning("Warning", "All fields must be filled!")
        return

    data = (creation_date, diagnosis_date, diagnosis, healthcare_unit, patient_id, mobile_number, gender, age)
    cursor.execute("INSERT INTO patients (creation_date, diagnosis_date, diagnosis, healthcare_service_unit, patient_id, mobile_number, gender, age) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", data)
    conn.commit()
    messagebox.showinfo("Success", "Patient data saved successfully!")

# Function to fetch patient data
def view_patient():
    patient_id = patient_id_entry.get()
    
    if not patient_id:
        messagebox.showwarning("Warning", "Please enter a Patient ID!")
        return

    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    record = cursor.fetchone()

    if record:
        result_text.set(
            f"📌 ID: {record[0]}\n"
            f"📅 Creation Date: {record[1]}\n"
            f"🗓 Diagnosis Date: {record[2]}\n"
            f"💉 Diagnosis: {record[3]}\n"
            f"🏥 Healthcare Unit: {record[4]}\n"
            f"📞 Mobile Number: {record[6]}\n"
            f"⚧ Gender: {record[7]}\n"
            f"🎂 Age: {record[8]}"
        )
    else:
        messagebox.showerror("Error", "No record found for the given Patient ID!")

# Function to delete patient record
def delete_patient():
    patient_id = patient_id_entry.get()
    
    if not patient_id:
        messagebox.showwarning("Warning", "Please enter a Patient ID!")
        return

    cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
    conn.commit()
    messagebox.showinfo("Success", "Record deleted successfully!")
    result_text.set("")  # Clear displayed data

# Function to export all data to CSV
def download_data():
    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()

    if not records:
        messagebox.showwarning("Warning", "No records found to download!")
        return

    columns = ["ID", "Creation Date", "Diagnosis Date", "Diagnosis", "Healthcare Unit", "Patient ID", "Mobile", "Gender", "Age"]
    df = pd.DataFrame(records, columns=columns)
    df.to_csv("mtrh_data.csv", index=False)
    messagebox.showinfo("Success", "Data downloaded as 'mtrh_data.csv'!")

# GUI Setup
root = tk.Tk()
root.title("MTRH Healthcare System")
root.geometry("550x450")
root.configure(bg="#f0f0f0")  # Soft background color

# Frames for better layout
frame_top = tk.Frame(root, bg="#f0f0f0")
frame_top.pack(pady=10)
frame_bottom = tk.Frame(root, bg="#f0f0f0")
frame_bottom.pack(pady=10)

# Input Section
tk.Label(frame_top, text="🔍 Enter Patient ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
patient_id_entry = tk.Entry(frame_top, font=("Arial", 12), width=20)
patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

# Submit Section
tk.Label(root, text="Diagnosis:", font=("Arial", 12), bg="#f0f0f0").pack()
diagnosis_entry = tk.Entry(root, font=("Arial", 12), width=30)
diagnosis_entry.pack(pady=5)

tk.Label(root, text="Healthcare Service Unit:", font=("Arial", 12), bg="#f0f0f0").pack()
healthcare_unit_dropdown = ttk.Combobox(root, values=clinic_names, font=("Arial", 12))
healthcare_unit_dropdown.pack(pady=5)
healthcare_unit_dropdown.set(clinic_names[0])  # Default selection

tk.Label(root, text="Mobile Number:", font=("Arial", 12), bg="#f0f0f0").pack()
mobile_number_entry = tk.Entry(root, font=("Arial", 12), width=30)
mobile_number_entry.pack(pady=5)

tk.Label(root, text="Gender:", font=("Arial", 12), bg="#f0f0f0").pack()
gender_dropdown = ttk.Combobox(root, values=["Male", "Female", "Other"], font=("Arial", 12))
gender_dropdown.pack(pady=5)
gender_dropdown.set("Male")  # Default selection

tk.Label(root, text="Age:", font=("Arial", 12), bg="#f0f0f0").pack()
age_entry = tk.Entry(root, font=("Arial", 12), width=10)
age_entry.pack(pady=5)

submit_button = tk.Button(root, text="Submit Data", command=submit_data, font=("Arial", 12), bg="#4CAF50", fg="white", padx=5)
submit_button.pack(pady=10)

# Action Buttons
view_button = tk.Button(frame_top, text="View Patient", command=view_patient, font=("Arial", 10), bg="#4CAF50", fg="white", padx=5)
view_button.grid(row=1, column=0, padx=10, pady=10)

delete_button = tk.Button(frame_top, text="Delete Patient", command=delete_patient, font=("Arial", 10), bg="#E74C3C", fg="white", padx=5)
delete_button.grid(row=1, column=1, padx=10, pady=10)

download_button = tk.Button(frame_bottom, text="Download Data", command=download_data, font=("Arial", 10), bg="#3498DB", fg="white", padx=5)
download_button.pack(pady=10)

# Display Area
result_text = tk.StringVar()
result_label = tk.Label(frame_bottom, textvariable=result_text, font=("Arial", 12), bg="#f0f0f0", fg="#333", width=50, height=7, anchor="w", justify="left", relief="solid", borderwidth=1)
result_label.pack(pady=10)

root.mainloop()
conn.close()
