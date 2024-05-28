
import streamlit as st
import os
from PyPDF2 import PdfReader
from docx import Document
import google.generativeai as genai
import re
from dotenv import load_dotenv
 
# Load environment variables from the .env file
load_dotenv()
 
# Get the API key from environment variables
API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
 
# Ensure the API key is set
if not API_KEY:
    raise ValueError("Google Generative AI API key not found in environment variables")
 
# Configure the generative model
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
 
def read_pdf(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return ""
 
def read_docx(file):
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text
        return text
    except Exception as e:
        st.error(f"Error reading DOCX file: {e}")
        return ""
 
async def atsMain():
    # st.title("Applicant Tracking System")
    st.subheader("Identify the perfect candidate for the role")
 
    # Upload Job Description
    # st.subheader("Upload Job Description")
    jd_file = st.file_uploader("Upload a job description", type=["pdf", "docx"])
 
    # Upload Candidate Resume
    # st.header("Upload Candidate Resume")
    resume_file = st.file_uploader("Upload a resume", type=["pdf", "docx"])
 
    # Screening Questions
    st.subheader("Mandatory Questions")
    work_location = st.selectbox("Preferred Work Location", ["Bangalore", "Chennai", "Hyderabad"])
    work_permit = st.selectbox("Permit to work in India", ["Yes", "No"])
 
    if st.button("Submit"):
        if jd_file and resume_file:
            # Read files
            if jd_file.type == "application/pdf":
                jd_text = read_pdf(jd_file)
            else:
                jd_text = read_docx(jd_file)
           
            if resume_file.type == "application/pdf":
                resume_text = read_pdf(resume_file)
            else:
                resume_text = read_docx(resume_file)
           
            # Analyze and Compare JD and Resume using Google Gemini Pro
            analyze_and_compare(jd_text, resume_text, work_location, work_permit)
        else:
            st.error("Please upload both JD and resume files.")
 
def analyze_and_compare(jd_text, resume_text, work_location, work_permit):
    # Use Google Gemini Pro to perform the analysis
    prompt = (
        f"Analyze the following job description and resume.\n\n"
        f"Job Description:\n{jd_text}\n\n"
        f"Resume:\n{resume_text}\n\n"
        f"Preferred Work Location: {work_location}\n"
        f"Permit to work in India: {work_permit}\n\n"
        f"Determine the match percentage and provide a detailed analysis."
    )
   
    response = model.generate_content(prompt)
    analysis_result = response.text
   
    # Extract the match percentage and decision from the analysis result
    match_percentage = extract_match_percentage(analysis_result)
    decision, detailed_reason = make_decision(match_percentage, work_location, work_permit, analysis_result)
   
    if decision == "Selected":
        st.success("Congrats! You are selected for the interview.")
    else:
        st.error(detailed_reason)
 
def extract_match_percentage(analysis_result):
    # Implement a function to extract the match percentage from the analysis result
    # This function parses the actual response from Google Gemini Pro using a regular expression.
    match = re.search(r'\bmatch percentage\b.*?(\d+)%', analysis_result, re.IGNORECASE)
    if match:
        return float(match.group(1))
    else:
        # If no percentage is found, return 0
        return 0
 
def make_decision(match_percentage, work_location, work_permit, analysis_result):
    # Allowed work locations
    allowed_locations = ["Bangalore", "Chennai"]
   
    reasons = []
    if match_percentage < 70:
        reasons.append(f"Your resume and the job description do not match at the required 70% level. The match percentage for your application is only {match_percentage}%.")
    if work_permit != "Yes":
        reasons.append("You do not have a permit to work in India, which is a mandatory requirement for this role.")
    if work_location not in allowed_locations:
        reasons.append(f"Your preferred work location '{work_location}' is not among the allowed locations {allowed_locations}.")
   
    if not reasons:
        return "Selected", None
    else:
        detailed_reason = generate_rejection_reason(analysis_result, reasons)
        return "Rejected", detailed_reason
 
def generate_rejection_reason(analysis_result, reasons):
    reasons_text = "\n".join(reasons)
    rejection_prompt = (
        f"Generate a detailed rejection message based on the following analysis and reasons, ensuring clarity and accuracy:\n\n"
        f"Analysis:\n{analysis_result}\n\n"
        f"Reasons for rejection:\n{reasons_text}"
    )
    response = model.generate_content(rejection_prompt)
    return response.text