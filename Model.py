import streamlit as st
import pandas as pd
import joblib
import numpy as np
from streamlit_option_menu import option_menu
import pickle
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the machine learning model for diabetes prediction
diabetes_model = joblib.load(open('trained_model.sav', 'rb'))


# Load the dataset
def load_data():
    file_path = 'Dialysis-Facilities.xlsx'
    data = pd.read_excel(file_path)
    data.columns = ['COUNTY', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE', 'HOSPITAL_NAME']
    data = data.iloc[1:]  # Skip the first row with old headers
    return data

# Function to predict diabetes
def predict_diabetes(features):
    logging.info(f"Features received for prediction: {features}")
    try:
        prediction = diabetes_model.predict([features])
        logging.info(f"Prediction result: {prediction}")
        return prediction[0]
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return "Error"

# Function to send a thank-you email with test result and contact details
def send_thank_you_email(name, email, diagnosis):
    sender_name = "Winfry Nyarangi"
    sender_email = "Winfrynyarangi@gmail.com"  
    sender_password = "zglj lqmq jqkw cioy"  

    linkedin_profile = "https://www.linkedin.com/in/winfry-nyarangi-213a20225/"
    webpapp_url = "https://diabetespredictionsystem-by-akshay.streamlit.app/"
    
    banner = """<img src="{}" alt="Banner Image" style="max-width: 100%; height: auto; margin-top: 20px;">""".format('https://d2jx2rerrg6sh3.cloudfront.net/images/Article_Images/ImageForArticle_22744_16565132428524067.jpg')
    
    # Additional tips for diabetic patients and prevention
    additional_tips = """<p><strong><u>Tips for Diabetic Patients:</u></strong></p><ol>...</ol><p><strong><u>Tips for Diabetes Prevention:</u></strong></p><ol>...</ol>"""
    
    subject = "Thank You for Visiting Diabetes Prediction Web Application!"
    color = "red" if diagnosis == "Diabetic" else "green"
    body = f"Dear {name},<br><br>Thank you for visiting the Diabetes Prediction Web Application!<br><br><b>Test Result:</b> <b style='color:{color}'>{diagnosis}</b>{banner}{additional_tips}<br><br>WebApp URL: {webpapp_url}<br><br>Connect: {linkedin_profile}<br><br><br>Best regards,<br>Akshay Ravella"

    message = MIMEMultipart()
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

# Streamlit app
def main():
    st.set_page_config(page_title="Diabetes Prediction & Hospital Recommendation", page_icon="🏥", layout="wide")
    st.title("Diabetes Prediction & Hospital Recommendation System 🩺🐞")

    with st.sidebar:
        selected = option_menu("Menu", ["Home", 'Others'], icons=['house', 'three-dots'], default_index=0)

    if selected == 'Home':
        st.title('Diabetes Prediction Web App')
        st.write('This web application is designed to predict whether a person is diabetic or not.')

        # Input fields
        name = st.text_input('Enter Your Name')
        email = st.text_input('Enter Your Email')

        #Input fields validation
        if not name or not email:
            st.warning('Please enter both Name and Email to proceed!', icon="⚠️")
            st.stop()

        if not email.endswith('@gmail.com'):
            st.error("Invalid email address!", icon="❌")
            st.stop()

        sex = st.selectbox('Gender',('Male','Female'))
        Pregnancies = st.text_input('Number of Pregnancies (Enter 0 if Male)')
        Glucose = st.text_input('Glucose Level')
        BloodPressure = st.text_input('BloodPressure Value')
        SkinThickness = st.text_input('Skin Thickness Value')
        Insulin = st.text_input('Insulin Level')
        BMI = st.text_input('BMI Value')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
        Age = st.slider('Choose your Age', 1, 100)

        # Check if the entered values are numeric
        if not all(value.replace('.', '', 1).isdigit() for value in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction]):
            st.error("❗Please enter valid numerical values for the input fields.")
            st.stop()
            
        #Prediction Button
        if st.button('Predict'):
            features = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness), 
                        float(Insulin), float(BMI), float(DiabetesPedigreeFunction), Age]
            diagnosis = predict_diabetes(features)
            
            
            
            # Send a thank-you email with the test result and contact details
            send_thank_you_email(name, email, diagnosis)

            # Display the test result
            with st.spinner('Please wait, loading...'):
                time.sleep(2)
            
            # Display prediction
            st.subheader("Prediction Result")
            if diagnosis == "Diabetic":
               st.error("Prediction: You are likely Diabetic.")
               
               # Hospital Recommendation
               st.header("Hospital Recommendation")
               st.markdown("""
               Based on your diabetes prediction, here are hospital recommendations. Select your county to filter results.
               """)

               counties = sorted(load_data()['COUNTY'].unique())
               selected_county = st.selectbox("Select County:", counties)

               # Display hospitals based on the prediction
               filtered_hospitals = load_data()[
                   (load_data()['COUNTY'] == selected_county)
               ]
               if filtered_hospitals.empty:
                   st.warning("No dialysis hospitals found in the selected county.")
               else:
                  st.dataframe(filtered_hospitals[['HOSPITAL_NAME', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE']], use_container_width=True)
               
            else:
               st.success("Prediction: Great! You are not Diabetic.")
    
            
            st.info('Do check your email for more details, Thank You.', icon="ℹ️")

        
        
    elif selected == 'Others':
        tab1, tab2, tab3 = st.tabs(["❓Help", "💬 Feedback", "📩 Contact"])

        with tab1:
            st.header("Welcome to the Help Page!", divider='rainbow')
            st.write("This application predicts diabetes based on inputs like pregnancies, glucose level, blood pressure, etc.")
            st.write("It works with 90% accuracy, providing insights for better health management.")
        
        with tab2:
            st.subheader("Your Feedback is Valuable!", divider='rainbow')
            user_message = st.text_area("Have questions or suggestions? I'd love to hear from you.", height=80, placeholder="Type here...")
            if st.button("Send"):
                formspree_endpoint = "https://formspree.io/f/mbjnrbvv"
                data = {"message": user_message}
                response = requests.post(formspree_endpoint, data=data)
                
                if response.status_code == 200:
                    st.success("Message sent successfully!")
                else:
                    st.error("Failed to send message, Please try again.")
        
        with tab3:
            st.write("Connect: [LinkedIn Profile](https://www.linkedin.com/in/winfry-nyarangi-213a20225/)")
            st.write("Email: [Winfrynyarangi@gmail.com](mailto:Winfrynyarangi@gmail.com)")
            st.image('https://pngimg.com/d/thank_you_PNG88.png', width=220)
            st.markdown("""<div style="position: fixed; bottom: 7.6px; left: 10px; right: 10px; text-align: left; color: grey; font-size: 14px;">Made by <span style="font-weight: bold; color: grey;">Akshay</span>🎈</div>""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
