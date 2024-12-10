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
st.image("Dialysis_Center.jpg", caption="Keeping The Kidneys Healthy!", use_column_width=True)
st.markdown("""
    # Welcome to the Hospital Finder App! 🏥

    This app is designed to help you easily find dialysis hospitals across Kenya, tailored to your specific needs and preferences. Whether you're looking for a hospital based on its **county**, **NHIF office**, or **hospital name**, we've got you covered.

    ## How It Works:
    - **Filter by County**: Select your preferred county, and we'll show you all dialysis hospitals in that area.
    - **Filter by NHIF Office**: If you have a specific NHIF office in mind, you can filter hospitals by their affiliated NHIF office for easier access.
    - **Search by Hospital Name**: If you already know the name of the hospital, you can quickly find it using the search functionality.

    ## Features:
    - **Personalized Recommendations**: Based on your preferences, we will suggest the best dialysis hospitals that meet your criteria.
    - **Easy Navigation**: With an intuitive user interface, you can quickly find the information you need without any hassle.
    - **Comprehensive Data**: The database includes detailed information on hospitals, including their names, locations, and NHIF affiliations.

    ## Why Use This App?
    Finding a dialysis facility that fits your specific needs has never been easier! This app simplifies your search, ensuring that you can access the best hospitals in your area or any part of Kenya.

    **Your health is important, and we’re here to help you make informed decisions for your well-being.**

    Let's get started—just choose your preferences and let us help you find the perfect dialysis hospital for you!
""")


# Custom Sidebar
st.sidebar.header("🔍 Filter Options")

# Sidebar introduction
st.sidebar.markdown("""
    Use the filters below to customize your search for dialysis hospitals in Kenya. 
    Narrow down your options based on county, NHIF office, or hospital name.
""")

# County Selection
counties = sorted(data['COUNTY'].unique())
county = st.sidebar.selectbox(
    "🏙️ Select County:",
    options=["All", "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"],  # Replace with actual counties in your dataset
    help="Choose the county where you want to find a dialysis hospital."
)
# Filter data by selected county
filtered_data = data[data['COUNTY'] == county]


# NHIF Office Filter
nhif_offices = sorted(filtered_data['NHIF_OFFICE'].unique())
selected_office = st.sidebar.selectbox(
    "🏢 Select NHIF Office:",
    "Select NHIF Office (optional):", ['All Offices'] + nhif_offices)

if selected_office != 'All Offices':
    filtered_data = filtered_data[filtered_data['NHIF_OFFICE'] == selected_office]


# Search for hospital name
search_name = st.sidebar.text_input("🏥Search by Hospital Name (optional):")
if search_name:
    filtered_data = filtered_data[filtered_data['HOSPITAL_NAME'].str.contains(search_name, case=False, na=False)]

# Display Results with Enhanced UI
st.subheader(f"Dialysis Hospitals in {county}")

# If no hospitals are found, show a message
if filtered_data.empty:
    st.warning("No hospitals found with the selected filters. Try refining your search.")
    
# Add a reset button
if st.sidebar.button("🔄 Reset Filters"):
    # Simulate resetting by reloading the app
    st.experimental_rerun()    
 
# Sidebar footer with an icon or note
st.sidebar.markdown("""
    ---
    🤝 **Tip**: Use multiple filters together for a more refined search!
""")    

# Display the hospitals in a table
st.markdown("### 🏥 Recommended Dialysis Hospitals")
st.markdown("""
    Below is a list of dialysis hospitals based on your selected filters. 
    Click on column headers to sort data or use the search options for a more refined view.
""")
st.dataframe(filtered_data[['HOSPITAL_NAME', 'NHIF_OFFICE', 'NHIF_HOSPITAL_CODE']], 
             use_container_width=True,
            height=400 
            )


# Add a footer or contact section
st.markdown("""
    ---
    If you need assistance, feel free to reach out to us at **support@hospitalfinder.com**.
    """)
