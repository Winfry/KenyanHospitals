import streamlit as st
import pandas as pd
import joblib

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

# Function to recommend hospitals based on user input
def recommend_hospitals(county, hospital_type):
    if hospital_type == "Dialysis":
        hospitals = data
    else:
        hospitals = data

    return hospitals[hospitals['County'].str.contains(county, case=False, na=False)]

# Streamlit app
def main():
    st.title("Unified Health App")

# creating a function for prediction
def diabetes_prediction(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)
    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)
    if prediction[0] == 0:
        return 'Not Diabetic'
    else:
        return 'Diabetic'
    
