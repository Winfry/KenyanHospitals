import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    file_path = 'Dialysis-Facilities-Comprehensive (1).xlsx'
    data = pd.read_excel(file_path)
    data.columns = ['COUNTY', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE', 'HOSPITAL_NAME']
    data = data.iloc[1:]  # Skip the first row with old headers
    return data

# Load data
data = load_data()

# App Title and Description
st.set_page_config(page_title="Hospital Recommendation", page_icon="🏥", layout="wide")
st.title("Welcome to the Hospital Recommendation System 🏥")
st.markdown("""
    This app helps you find dialysis hospitals in Kenya based on the county and your preferences.
    Filter hospitals by county, NHIF office, or hospital name, and get the perfect recommendation for your needs!
""")

# Custom Sidebar
st.sidebar.header("🔍 Filter Options")

# Add an image to the sidebar
st.sidebar.image('https://example.com/your_image.png', width=200)  # Replace with a real image URL or file path

# County Selection
counties = sorted(data['COUNTY'].unique())
selected_county = st.sidebar.selectbox("Select a County:", counties)

# Filter data by selected county
filtered_data = data[data['COUNTY'] == selected_county]

# NHIF Office Filter
nhif_offices = sorted(filtered_data['NHIF_OFFICE'].unique())
selected_office = st.sidebar.selectbox("Select NHIF Office (optional):", ['All Offices'] + nhif_offices)

if selected_office != 'All Offices':
    filtered_data = filtered_data[filtered_data['NHIF_OFFICE'] == selected_office]

# Search for hospital name
search_name = st.sidebar.text_input("Search by Hospital Name (optional):")
if search_name:
    filtered_data = filtered_data[filtered_data['HOSPITAL_NAME'].str.contains(search_name, case=False, na=False)]

# Display Results with Enhanced UI
st.subheader(f"Dialysis Hospitals in {selected_county}")

# If no hospitals are found, show a message
if filtered_data.empty:
    st.warning("No hospitals found with the selected filters. Try refining your search.")

# Display the hospitals in a table
st.dataframe(filtered_data[['HOSPITAL_NAME', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE']], use_container_width=True)

# Add a footer or contact section
st.markdown("""
    ---
    If you need assistance, feel free to reach out to us at **support@hospitalfinder.com**.
    """)
