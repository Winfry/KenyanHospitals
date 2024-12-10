import streamlit as st
import pandas as pd

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

# App Title
st.title("Hospital Recommendation System")
st.markdown("Use this app to find dialysis hospitals based on county or specific preferences.")

# Sidebar: Filter by County
st.sidebar.header("🔍 Filter Options")
st.sidebar.markdown("""
    Use the filters below to customize your search for dialysis hospitals in Kenya. 
    Narrow down your options based on county, NHIF office, or hospital name.
""")
counties = sorted(data['COUNTY'].unique())
selected_county = st.sidebar.selectbox("🏙️ Select a County:", 
                                           counties,  
                                       help="Choose the county where you want to find a dialysis hospital." )

# Filter data by selected county
filtered_data = data[data['COUNTY'] == selected_county]

# Additional Search Filters
search_office = st.text_input("🏢 Search by NHIF Office (optional):")
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
    
# Add a footer or contact section
st.markdown("""
    ---
    ### Need Help? 💬
    - **Contact Us**: For further assistance, email us at [support@hospitalfinder.com](mailto:support@hospitalfinder.com).
    - **Frequently Asked Questions (FAQs)**: Visit our [FAQ page](https://hospitalfinder.com/faqs) for common queries.
    - **Feedback**: We value your input! Let us know how we can improve by filling out [this form](https://hospitalfinder.com/feedback).
    
    ---
    #### ❤️ Thank You for Using Our App!
    We are committed to making healthcare accessible and seamless. 
    Stay healthy and take care! 😊
""")
    
