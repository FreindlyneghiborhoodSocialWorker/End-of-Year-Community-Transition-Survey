import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Use credentials from Streamlit secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
client = gspread.authorize(creds)

# Open your exact Google Sheet
sheet = client.open("End-of-Year Community Transition Survey").sheet1  # Ensure this name matches exactly

# Streamlit app layout
st.title("End-of-Year Community Transition Survey")
st.write("Thank you for taking a few minutes to provide feedback on our services this year.")

# Survey questions
name = st.text_input("Your Name (optional)")
district = st.text_input("School District")

services = st.multiselect(
    "Which services did I provide this year? (Select all that apply)",
    ["Classroom Support", "Job Placement", "IEP Meetings", "Family Communication", "Other"]
)

successes = st.text_area("What went well this past year? Share any successes.")
improvements = st.text_area("Where can I improve? (e.g., IEP support, family connections)")

satisfaction = st.slider("Overall satisfaction (1 = low, 5 = high)", 1, 5, 3)

# Submit button
if st.button("Submit"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    services_str = ", ".join(services)
    row = [timestamp, name, district, services_str, successes, improvements, satisfaction]
    sheet.append_row(row)
    st.success("✅ Thank you! Your response has been recorded.")