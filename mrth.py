import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# Connect to the database
conn = sqlite3.connect("mtrh.db", check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
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

# Clinic options
clinic_names = [
    "S4A OPD Ambulatory", "PW 2 OPD - Consultant Room - MTRH",
    "Ambulatory Consultation - MTRH", "ED - Medical Emergency (Rm 14) - MTRH",
    "Diabetic Clinic - Chandaria - MTRH", "ENT - General - MTRH",
    "Haematology Clinic - Chandaria - MTRH", "MOPC CLINIC - MTRH",
    "Dental- OMFS- Oral & Maxillofacial Clinic - MTRH", "General-Oncology Telemedicine - MTRH"
]

# App title
st.title("🏥 MTRH Healthcare System")

# Patient ID entry (used in multiple actions)
st.subheader("🔍 Enter Patient ID")
patient_id = st.text_input("Patient ID", max_chars=50)

# --- Submit Section ---
st.subheader("📋 Enter Patient Details")

diagnosis = st.text_input("Diagnosis")
healthcare_unit = st.selectbox("Healthcare Service Unit", clinic_names)
mobile_number = st.text_input("Mobile Number")
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
age = st.number_input("Age", min_value=0, max_value=120, step=1)

if st.button("✅ Submit Data"):
    if not all([patient_id, diagnosis, healthcare_unit, mobile_number, gender, age]):
        st.warning("⚠️ All fields must be filled!")
    else:
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        diagnosis_date = creation_date
        data = (creation_date, diagnosis_date, diagnosis, healthcare_unit, patient_id, mobile_number, gender, age)
        cursor.execute("""
            INSERT INTO patients (creation_date, diagnosis_date, diagnosis, healthcare_service_unit, patient_id, mobile_number, gender, age)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        st.success("✅ Patient data saved successfully!")

# --- View Section ---
if st.button("🔍 View Patient"):
    if not patient_id:
        st.warning("⚠️ Please enter a Patient ID!")
    else:
        cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
        record = cursor.fetchone()
        if record:
            st.info(f"""
📌 ID: {record[0]}
📅 Creation Date: {record[1]}
🗓 Diagnosis Date: {record[2]}
💉 Diagnosis: {record[3]}
🏥 Healthcare Unit: {record[4]}
🆔 Patient ID: {record[5]}
📞 Mobile Number: {record[6]}
⚧ Gender: {record[7]}
🎂 Age: {record[8]}
""")
        else:
            st.error("❌ No record found for the given Patient ID!")

# --- Delete Section ---
if st.button("🗑 Delete Patient"):
    if not patient_id:
        st.warning("⚠️ Please enter a Patient ID!")
    else:
        cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
        conn.commit()
        st.success("🗑 Record deleted successfully!")

# --- Download Section ---
if st.button("⬇️ Download All Data as CSV"):
    cursor.execute("SELECT * FROM patients")
    records = cursor.fetchall()
    if records:
        df = pd.DataFrame(records, columns=[
            "ID", "Creation Date", "Diagnosis Date", "Diagnosis",
            "Healthcare Unit", "Patient ID", "Mobile", "Gender", "Age"
        ])
        csv = df.to_csv(index=False)
        st.download_button("📥 Download CSV", data=csv, file_name="mtrh_data.csv", mime="text/csv")
    else:
        st.warning("⚠️ No records found to download.")
