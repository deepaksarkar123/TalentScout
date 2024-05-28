
import os
import streamlit as st
from google.generativeai import GenerativeModel, ChatSession, configure
from dotenv import load_dotenv
 
# Load environment variables from .env file
load_dotenv()
 
# Configure API access
api_key = os.getenv("GOOGLE_GENAI_API_KEY")
# chat=None
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()
 
configure(api_key=api_key)
 
# Initialize the Gemini Pro model and start chat session
try:
    model = GenerativeModel('gemini-pro')
    chat = model.start_chat()
except Exception as e:
    st.error(f"Failed to initialize the Gemini Pro model. Error: {e}")
    st.stop()

jd=""
def handleGenSubmit():
    st.session_state.jdGenSubmit=True
def setEnrichClicked():
    st.session_state.isEnrichClicked=True
def generate_initial_jd(role, min_exp, max_exp, requirements):
    # Generate a job description considering a range of experiences and specific requirements
    prompt = (
        f"Draft a job description for a {role}. Thoroughly and carefully adjust the required skillsets and work exprience in the job description for {min_exp} to {max_exp} years of experience. Requirements: {requirements}"
        f"Style the job description that reflects a work culture of an IT startup: mordern and vibrant."
        f"Mandatory instructions. Include these two paragraphs in the generated job description. About MINDSPRINT We help businesses with solutions for their transformation journeys and technology innovations. With deep domain knowledge and experience of over three decades, Mindsprint is a breeding ground for innovators, technology experts, business strategists, as well as young, fresh minds who think and breathe customer-centricity. WHY JOIN MINDSPRINT"
        f"Freedom to innovate with a talented team People-oriented inclusive work culture Global exposure with infinite opportunities to grow Opportunity to work on advanced technologies A workplace that makes you feel at home"
        f"Include, learn more about MINDSPRINT (https://www.mindsprint.org/)"
    )
    # try:
    #     model = GenerativeModel('gemini-pro')
    #     chat = model.start_chat()
    # except Exception as e:
    #     st.error(f"Failed to initialize the Gemini Pro model. Error: {e}")
    #     st.stop()
    response = chat.send_message(prompt)
    st.session_state['history'] = [prompt, response.text]
    return response.text
 
def chat_interaction(user_query):
    # Send the user's query to the chat model and maintain the conversation history
    # try:
    #     model = GenerativeModel('gemini-pro')
    #     chat = model.start_chat()
    # except Exception as e:
    #     st.error(f"Failed to initialize the Gemini Pro model. Error: {e}")
    #     st.stop()
    response = chat.send_message(user_query)
    # Append the user query and model response to the history
    st.session_state['history'] += [user_query, response.text]
    return response.text
 
# Streamlit UI
# st.title("Generate Job Description")
 
# with st.form("job_spec_form"):
#     role = st.text_input("Job Role", placeholder="e.g., React JS Senior Developer")
#     # Slider for selecting a range of experience
#     min_exp, max_exp = st.slider("Experience Required (Years)", 1, 25, (5, 10))
#     # Text area for additional requirements
#     requirements = st.text_area("Additional Requirements", placeholder="Enter specific skills, qualifications, and other job requirements here.")
#     st.session_state.jdGenSubmit = st.form_submit_button("Generate")
 
# if submitted:
#     jd = generate_initial_jd(role, min_exp, max_exp, requirements)
#     st.session_state['jd'] = jd  # Store initial JD in session state
#     st.text_area("Draft Job Description", jd, height=300)
def handleEnrichSubmit():
    print(f"enrich contetn: {st.session_state.enrichContent}")
    prompt = f"""You are a skilled HR professional or talent recruiter with a knack for crafting compelling job descriptions (JDs). Your task is to follow the instructions given above with precision and care.
    Here is the original job description content
    {st.session_state.jd}
    Here are the modification instructions:
    {st.session_state.enrichContent}
    Your Objective: Modify the original job description according to the specific instructions provided in the modification request. It's crucial to adhere to these guidelines:
    Preserve Original Context: Do not heavily overwrite the original job description content. The core message and context of the job description must remain unchanged.
    Avoid Adding New Concepts: Do not introduce conceptualized or hypothetical information. The modification should strictly revolve around the existing content and instructions provided.
    Important Notes:
    Do not overwrite or eliminate existing content unless directly related to the specific modifications requested.
    Avoid making changes that are unrelated to the provided instructions. Only implement modifications that are explicitly asked for.
    Deliverable: Provide the updated job description content, ensuring it has been modified according to the provided instructions, while retaining the essence and context of the original job description."""
    
    response = chat.send_message(prompt)
    print(f" r=enrich response{response.text}")
    st.session_state.jd=None
    st.session_state.updatedJd= response.text
    # st.session_state.jdGenSubmit
    return response.text
async def jdGenMain():
    if not api_key:
        st.error("API key not found. Please check your .env file.")
        st.stop()
 
    configure(api_key=api_key)
 
# Initialize the Gemini Pro model and start chat session
    # try:
    #     model = GenerativeModel('gemini-pro')
    #     chat = model.start_chat()
    # except Exception as e:
    #     st.error(f"Failed to initialize the Gemini Pro model. Error: {e}")
    #     st.stop()
    # st.title("Generate Job Description")
    st.subheader("Enter details to craft a perfect job description!")
 
    with st.form("job_spec_form"):
        role = st.text_input("Job Role", placeholder="e.g., React JS Senior Developer")
        # Slider for selecting a range of experience
        min_exp, max_exp = st.slider("Experience Required (Years)", 1, 25, (5, 10))
        # Text area for additional requirements
        requirements = st.text_area("Additional Requirements", placeholder="Enter specific skills, qualifications, and other job requirements here.")
        st.form_submit_button("Submit",on_click=handleGenSubmit)
    if st.session_state.jdGenSubmit:
        if(role and min_exp and requirements):
            st.session_state['jd'] = generate_initial_jd(role, min_exp, max_exp, requirements)
        st.session_state.jdGenSubmit=False
        # Store initial JD in session state
        # st.text_area("Draft Job Description", st.session_state['jd'], height=300)
    if st.session_state.jd or st.session_state.updatedJd:
        if st.session_state.updatedJd:
            st.write(f"{st.session_state.updatedJd}")
        if st.session_state.jd:
            st.write(f"{st.session_state['jd']}")
        st.session_state.enrichContent = st.text_input("Enrich further:")
        st.button("Go",on_click=setEnrichClicked)
        if st.session_state.isEnrichClicked:
            handleEnrichSubmit()