import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import qrcode
import io

# --- GOOGLE SHEETS SETUP ---
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_file("gs_creds.json", scopes=SCOPES)
client = gspread.authorize(creds)
sheet = client.open("End-of-Year Community Transition Survey").sheet1  # Use your actual Sheet name

# --- STREAMLIT UI ---
st.title("End-of-Year Community Transition Survey")
st.write("Thank you for taking a few minutes to provide feedback on our services this year.")

teacher_name = st.text_input("Your Name (optional)")
school_district = st.text_input("School District")

services = st.multiselect(
    "Which services did I provide this year? (Select all that apply)",
    [
        "Job Placement",
        "Classroom Support",
        "Group Lessons (Job Readiness)",
        "Group Lessons (Self Advocacy)",
        "Group Lessons (Independent Living)",
        "Pre-ETS Activities",
        "Life Skills Coaching"
    ]
)

good = st.text_area("What went well this past year? Share any successes.")
improve = st.text_area("Where can I improve? (e.g., IEP support, family connections)")
rating = st.slider("Overall satisfaction (1 = low, 5 = high)", 1, 5, 3)

# --- FUNCTION TO SAVE TO GOOGLE SHEET ---
def save_to_sheet(row):
    sheet.append_row(row)

# --- FORM SUBMISSION ---
if st.button("Submit Feedback"):
    timestamp = datetime.now().isoformat()
    service_str = "; ".join(services)
    row = [timestamp, teacher_name, school_district, service_str, good, improve, rating]
    save_to_sheet(row)
    st.success("✅ Thank you for your feedback!")

# --- QR CODE GENERATION ---
st.markdown("---")
st.subheader("Want to share this survey?")

# 🔁 Replace this URL with the actual link to your Streamlit survey app:
survey_url = "https://your-username-your-app-name.streamlit.app"

# Create QR code
qr = qrcode.make(survey_url)
buf = io.BytesIO()
qr.save(buf, format="PNG")
buf.seek(0)

st.image(buf, caption="Scan to open the survey", use_container_width=True)

