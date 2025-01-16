import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Constants
MODEL_PATH = 'trained_model.sav'
DATA_PATH = 'Dialysis-Facilities.xlsx'

# Load the machine learning model
def load_model():
    try:
        return joblib.load(MODEL_PATH)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

# Load hospital dataset
def load_hospital_data():
    try:
        data = pd.read_excel(DATA_PATH)
        data.columns = ['COUNTY', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE', 'HOSPITAL_NAME']
        data = data.iloc[1:]  # Skip the first row with old headers
        return data
    except Exception as e:
        st.error(f"Error loading hospital data: {e}")
        st.stop()

# Prediction function
def predict_diabetes(model, features):
    try:
        prediction = model.predict([features])
        return prediction[0]
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        return None

# Send email function
def send_email(name, email, diagnosis):
    try:
        sender_email = os.getenv("EMAIL_USER")
        sender_password = os.getenv("EMAIL_PASS")

        if not sender_email or not sender_password:
            st.error("Email credentials are not set.")
            return

        subject = "Diabetes Prediction Results"
        body = f"Dear {name},\n\nYour test result: {diagnosis}.\n\nThank you for using our application."

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Streamlit app layout
def main():
    st.set_page_config(page_title="Diabetes Prediction & Hospital Finder", page_icon="🏥", layout="wide")
    st.title("Diabetes Prediction & Hospital Recommendation System 🩺")

    # Sidebar menu
    with st.sidebar:
        menu = st.radio("Menu", ["Home", "Hospital Finder", "Contact"])

    # Load resources
    model = load_model()
    hospital_data = load_hospital_data()

    if menu == "Home":
        st.header("Diabetes Prediction")

        # Input fields
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        gender = st.selectbox("Gender", ["Male", "Female"])

        pregnancies = st.number_input("Pregnancies", min_value=0, step=1)
        glucose = st.number_input("Glucose Level", min_value=0.0, step=1.0)
        blood_pressure = st.number_input("Blood Pressure", min_value=0.0, step=1.0)
        skin_thickness = st.number_input("Skin Thickness", min_value=0.0, step=1.0)
        insulin = st.number_input("Insulin", min_value=0.0, step=1.0)
        bmi = st.number_input("BMI", min_value=0.0, step=0.1)
        diabetes_pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.0, step=0.01)
        age = st.slider("Age", 0, 120, 25)

        if st.button("Predict"):
            features = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, diabetes_pedigree, age]
            diagnosis = predict_diabetes(model, features)

            if diagnosis is not None:
                result = "Diabetic" if diagnosis == 1 else "Non-Diabetic"
                st.success(f"Prediction: {result}")

                # Send email
                send_email(name, email, result)

    elif menu == "Hospital Finder":
        st.header("Find Hospitals in Your Area")
        county = st.selectbox("Select County", sorted(hospital_data['COUNTY'].unique()))
        hospital_type = st.radio("Hospital Type", ["General", "Dialysis"])

        filtered_data = hospital_data[hospital_data['COUNTY'] == county]

        if hospital_type == "Dialysis":
            filtered_data = filtered_data[filtered_data['NHIF_HOSPITAL_CODE'].str.contains("DIALYSIS", na=False)]

        if not filtered_data.empty:
            st.dataframe(filtered_data[['HOSPITAL_NAME', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE']])
            st.download_button("Download Hospital List", data=filtered_data.to_csv(index=False), file_name="hospital_list.csv")
        else:
            st.warning("No hospitals found for the selected criteria.")

    elif menu == "Contact":
        st.header("Contact Us")
        st.write("For inquiries, please email us at: support@example.com")

if __name__ == "__main__":
    main()
