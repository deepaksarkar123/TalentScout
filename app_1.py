import streamlit as st;
from streamlit_option_menu import option_menu
import asyncio
from src.components.ats import atsMain
from src.components.jdGeneration import jdGenMain
from src.components.questions import questionsMain
# state variables
if 'selected' not in st.session_state:
    st.session_state.selected = "ATS"
if 'jdGenSubmit' not in st.session_state:
    st.session_state.jdGenSubmit = False
if 'isEnrichClicked' not in st.session_state:
    st.session_state.isEnrichClicked = False
if 'enrichContent' not in st.session_state:
    st.session_state.enrichContent=None
if 'jd' not in st.session_state:
    st.session_state.jd=None
if 'updatedJd' not in st.session_state:
    st.session_state.updatedJd=""
async def initialize():
    with st.sidebar:  
        st.session_state.selected = option_menu(
            menu_title="Talent Scout",
            options=[
                
                "Talent Craft",
                "Talent Tracking",
                "Talent Screening",
                "Talent Recap",
                "Talent Sense"              
            ],
            # icons=[                
            #     "house",
               
            #     "fast-forward",
            #     "rewind"              
               
            # ],
            menu_icon="none",
        )
    if st.session_state.selected == "Talent Tracking":
        await atsMain()
    if st.session_state.selected == "Talent Craft":
        await jdGenMain()
    if st.session_state.selected == "Talent Screening":
        await questionsMain()
       
if  __name__ == '__main__':
    
    asyncio.run(initialize())
