import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    # Replace this path with the location of your dataset
    file_path = 'Dialysis-Facilities-Comprehensive (1).xlsx'
    data = pd.read_excel(file_path)
    data.columns = ['COUNTY', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE', 'HOSPITAL_NAME']
    data = data.iloc[1:]  # Skip the first row with old headers
    return data

# Load data
data = load_data()

# App Title
st.title("Hospital Recommendation System")
st.markdown("Use this app to find dialysis hospitals based on county or specific preferences.")

# Sidebar: Filter by County
st.sidebar.header("Filter Options")
counties = sorted(data['COUNTY'].unique())
selected_county = st.sidebar.selectbox("Select a County:", counties)

# Filter data by selected county
filtered_data = data[data['COUNTY'] == selected_county]

# Additional Search Filters
search_office = st.text_input("Search by NHIF Office (optional):")
if search_office:
    filtered_data = filtered_data[filtered_data['NHIF_OFFICE'].str.contains(search_office, case=False, na=False)]

search_name = st.text_input("Search by Hospital Name (optional):")
if search_name:
    filtered_data = filtered_data[filtered_data['HOSPITAL_NAME'].str.contains(search_name, case=False, na=False)]

# Display Filtered Hospitals
st.subheader(f"Dialysis Hospitals in {selected_county}")
if not filtered_data.empty:
    st.write(filtered_data[['HOSPITAL_NAME', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE']])
else:
    st.write("No hospitals found. Try refining your search.")
