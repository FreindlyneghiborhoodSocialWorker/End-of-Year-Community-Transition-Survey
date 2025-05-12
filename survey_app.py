import streamlit as st
from datetime import datetime

# Google Sheets imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authorize and open sheet
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name("gs_creds.json", scope)
gc = gspread.authorize(creds)
sh = gc.open("End-of-Year Community Transition Survey")  # exact name of your Google Sheet
worksheet = sh.sheet1  # first tab

# --- Streamlit UI ---
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

def save_to_sheet(row):
    """Append a single row to Google Sheets."""
    worksheet.append_row(row)

if st.button("Submit Feedback"):
    ts = datetime.now().isoformat()
    serv = "; ".join(services)
    row = [ts, teacher_name, school_district, serv, good, improve, rating]
    save_to_sheet(row)
    st.success("✅ Thank you for your feedback!")

# --- QR Code Generation ---
import qrcode
import io

# Replace this with your real Streamlit app link
qr_url = "https://your-username-streamlit-survey.streamlit.app"

# Create the QR code
qr = qrcode.make(qr_url)

# Convert to bytes
buf = io.BytesIO()
qr.save(buf, format="PNG")
buf.seek(0)

# Display the QR code in Streamlit
st.markdown("---")
st.subheader("Want to share this survey?")
st.image(buf, caption="Scan to open the survey", use_container_width=True)
