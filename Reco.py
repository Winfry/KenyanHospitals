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

# Function to predict diabetes
def predict_diabetes(features):
    prediction = diabetes_model.predict([features])
    return prediction[0]

# Function to recommend hospitals based on user input
def recommend_hospitals(county, hospital_type):
    if hospital_type == "Dialysis":
        hospitals = dialysis_hospitals
    else:
        hospitals = general_hospitals

    return hospitals[hospitals['County'].str.contains(county, case=False, na=False)]

# Streamlit app
def main():
    st.title("Unified Health App")

    # Sidebar for navigation
    menu = ["Diabetes Prediction", "Hospital Recommendation"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Diabetes Prediction":
        st.header("Diabetes Prediction")
        st.write("Enter your details below to predict if you might have diabetes.")

        # Input features
        pregnancies = st.number_input("Number of Pregnancies", min_value=0)
        glucose = st.number_input("Glucose Level", min_value=0)
        blood_pressure = st.number_input("Blood Pressure (mm Hg)", min_value=0)
        skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0)
        insulin = st.number_input("Insulin Level (IU/mL)", min_value=0)
        bmi = st.number_input("BMI", min_value=0.0, format="%.1f")
        dpf = st.number_input("Diabetes Pedigree Function", min_value=0.0, format="%.3f")
        age = st.number_input("Age", min_value=0)

        if st.button("Predict"):
            features = [pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]
            prediction = predict_diabetes(features)

            if prediction == 1:
                st.warning("You might have diabetes. Please consult a healthcare provider.")
            else:
                st.success("You are unlikely to have diabetes. Maintain a healthy lifestyle!")

    elif choice == "Hospital Recommendation":
        st.header("Hospital Recommendation")
        st.write("Find hospitals based on your location and preference.")

        county = st.text_input("Enter your County")
        hospital_type = st.radio("Select Hospital Type", ["General", "Dialysis"])

        if st.button("Search Hospitals"):
            recommendations = recommend_hospitals(county, hospital_type)

            if recommendations.empty:
                st.error("No hospitals found for the selected criteria.")
            else:
                st.write("### Recommended Hospitals:")
                st.dataframe(recommendations)

if __name__ == '__main__':
    main()
