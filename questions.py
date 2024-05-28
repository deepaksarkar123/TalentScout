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
           text += page.extract_text() or ""
       return text.strip()
   except Exception as e:
       st.error(f"Error reading PDF file: {e}")
       return None
 
def read_docx(file):
   try:
       doc = Document(file)
       text = ""
       for paragraph in doc.paragraphs:
           text += paragraph.text + "\n"
       return text.strip()
   except Exception as e:
       st.error(f"Error reading DOCX file: {e}")
       return None
 
async def questionsMain():
   # st.title("Generate Screening Questions")
   st.subheader("Tailored screening questions in an instant!")
 
   # Upload Job Description
   # st.header("Upload Job Description")
   jd_file = st.file_uploader("Upload a job description", type=["pdf", "docx"])
 
   # Upload Candidate Resume
   # st.header("Upload Candidate Resume")
   resume_file = st.file_uploader("Upload a resume", type=["pdf", "docx"])
 
   if st.button("Submit"):
       if jd_file and resume_file:
           jd_text = read_pdf(jd_file) if jd_file.type == "application/pdf" else read_docx(jd_file)
           resume_text = read_pdf(resume_file) if resume_file.type == "application/pdf" else read_docx(resume_file)
 
           if jd_text and resume_text:
               st.text("JD Text:")
               st.write(jd_text[:500])  # Show first 500 characters of JD
               st.text("Resume Text:")
               st.write(resume_text[:500])  # Show first 500 characters of resume
 
               questions_and_responses = generate_questions(jd_text, resume_text)
               if questions_and_responses:
                   display_questions(questions_and_responses)
               #else:
                   #st.error("No questions were generated. Please check the inputs and model configuration.")
           else:
               st.error("Error reading one or both files. Please ensure they are not empty and are properly formatted.")
       else:
           st.error("Please upload both JD and resume files.")
 
def generate_questions(jd_text, resume_text):
   prompt = (
       f"Based on the job description and resume provided below, suggest 5 screening questions that a non-technical recruiter can ask the candidate for the job role."
       f"Instruction: The screening questions should not be technical."
       f"To esnure personalisation, ask probing question in this style: As mentioned in your resume," 
       f"Include recommended responses.\n\n"
       f"Job Description:\n{jd_text}\n\n"
       f"Resume:\n{resume_text}"
   )
   response = model.generate_content(prompt)
   st.text("Model Response:")
   st.write(response.text)  # Show the full response from the model
 
   return parse_questions_and_responses(response.text)
 
def parse_questions_and_responses(text):
   questions = re.findall(r'Question \d+: (.*?) Recommended Response:', text, re.DOTALL)
   responses = re.findall(r'Recommended Response: (.*?)(?=Question \d+:|$)', text, re.DOTALL)
   paired_items = list(zip(questions, responses)) if questions and responses else []
   return paired_items[:5]  # Limit to 5 questions
 
def display_questions(questions_and_responses):
   st.header("Screening Questions")
   if questions_and_responses:
       for i, (question, response) in enumerate(questions_and_responses, 1):
           st.subheader(f"Question {i}")
           st.write(question)
           st.write(f"**Recommended Response:** {response}")
   else:
       st.error("No questions were generated. Please check the inputs and model configuration.")