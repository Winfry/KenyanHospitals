import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the machine learning model for diabetes prediction
diabetes_model = joblib.load(open('trained_model.sav', 'rb'))

# Load the dataset
def load_data():
    # Replace this path with the location of your dataset
    file_path = 'Dialysis-Facilities.xlsx'
    data = pd.read_excel(file_path)
    data.columns = ['COUNTY', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE', 'HOSPITAL_NAME']
    data = data.iloc[1:]  # Skip the first row with old headers
    return data
# Load data
data = load_data()

# Function to predict diabetes
def predict_diabetes(features):
    prediction = diabetes_model.predict([features])
    return prediction[0]

# Streamlit app
def main():
    st.title("Unified Health App")


