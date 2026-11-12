import streamlit as st
import pdfplumber
import os
from google import genai
from dotenv import load_dotenv
from PIL import Image

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="ClockIt!!!", page_icon="⏱️", layout="wide")

# Basic styling for background (Buttons will use default Streamlit styling)
st.markdown("""
    <style>
    .stApp { background-color: #0A0A0A; color: #E0E0E0; }
    </style>
""", unsafe_allow_html=True)

# State management
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'field' not in st.session_state:
    st.session_state.field = None

# ==========================================
# 2. PAGE ROUTING LOGIC
# ==========================================

# --- PAGE 1: HOME SCREEN ---
if st.session_state.page == "home":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            # Load and display the new logo
            logo = Image.open("logo.png")
            st.image(logo, width="stretch")
        except:
            pass

        # ADDED SUBTITLE HERE
        st.markdown("<h3 style='text-align: center; color: #C0C0C0; margin-top: -10px;'>Your AI based Resume Reviewer!!!</h3>", unsafe_allow_html=True)

        st.write("---")
        
        # Buttons
        if st.button("RESUME TEMPLATE", type="primary", width="stretch", key="btn_home_1"):
            st.session_state.page = "template_menu"
            st.rerun()

        st.write("### Pick your field!!!")
        st.write("Select a field to start the review (Upload Resume):")

        if st.button("💻 Technical & STEM", type="primary", width="stretch", key="btn_home_2"):
            st.session_state.field = "Tech"
            st.session_state.page = "upload_review"
            st.rerun()
            
        if st.button("💼 Business, Law & Management", type="primary", width="stretch", key="btn_home_3"):
            st.session_state.field = "Business"
            st.session_state.page = "upload_review"
            st.rerun()
            
        if st.button("🎨 Creative, Media & Design", type="primary", width="stretch", key="btn_home_4"):
            st.session_state.field = "Creative"
            st.session_state.page = "upload_review"
            st.rerun()


# --- PAGE 2: TEMPLATE MENU ---
elif st.session_state.page == "template_menu":
    st.title("Pick your field!!!")
    st.write("Select a field to view its standard resume template.")
    st.write("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Technology & STEM", type="primary", width="stretch", key="btn_menu_1"):
            st.session_state.field = "Tech"
            st.session_state.page = "view_template"
            st.rerun()

    with col2:
        if st.button("Business & Management", type="primary", width="stretch", key="btn_menu_2"):
            st.session_state.field = "Business"
            st.session_state.page = "view_template"
            st.rerun()

    with col3:
        if st.button("Creative & Design", type="primary", width="stretch", key="btn_menu_3"):
            st.session_state.field = "Creative"
            st.session_state.page = "view_template"
            st.rerun()

    st.write("---")
    if st.button("⬅️ Back to Home", type="primary", key="btn_menu_back"):
        st.session_state.page = "home"
        st.rerun()


# --- PAGE 3: VIEW TEMPLATE ONLY ---
elif st.session_state.page == "view_template":
    st.title("Standard Resume Template")
    st.write("---")
    
    if st.session_state.field == "Tech":
        try: st.image("tech_template.png", width="stretch")
        except: st.warning("tech_template.png not found.")
    elif st.session_state.field == "Business":
        try: st.image("business_template.png", width="stretch")
        except: st.warning("business_template.png not found.")
    else:
        try: st.image("creative_template.png", width="stretch")
        except: st.warning("creative_template.png not found.")

    st.write("---")
    if st.button("⬅️ Back to Menu", type="primary", key="btn_view_back"):
        st.session_state.page = "template_menu"
        st.rerun()


# --- PAGE 4: UPLOAD & REVIEW ---
elif st.session_state.page == "upload_review":
    st.title("Upload your Resume")
    
    if st.session_state.field == "Tech":
        st.subheader("💻 Technical & STEM Track")
    elif st.session_state.field == "Business":
        st.subheader("💼 Business & Management Track")
    else:
        st.subheader("🎨 Creative & Design Track")
        
    st.write("---")
    
    uploaded_file = st.file_uploader("Upload Resume (PDF only, Max 2MB)", type=["pdf"])
    pasted_text = st.text_area("Or paste your resume text here:")
    
    col_a, col_b = st.columns([1, 1])
    with col_a:
        analyze_btn = st.button("Clock My Resume 🚀", type="primary", width="stretch", key="btn_upload_1")
    with col_b:
        if st.button("⬅️ Back to Home", type="primary", width="stretch", key="btn_upload_2"):
            st.session_state.page = "home"
            st.session_state.field = None
            st.rerun()

    # ==========================================
    # 3. EDGE CASE HANDLING & ATS ENGINE
    # ==========================================
    if analyze_btn:
        resume_text = ""
        
        if uploaded_file is not None:
            if uploaded_file.size > 2 * 1024 * 1024:
                st.error("File is too large. Please compress your document to a maximum of 2MB.")
                st.stop()
            try:
                with pdfplumber.open(uploaded_file) as pdf:
                    if len(pdf.pages) > 2:
                        st.error("Resume is too long. Please compress your document to a maximum of 2 Pages.")
                        st.stop()
                    for page in pdf.pages:
                        extracted = page.extract_text()
                        if extracted:
                            resume_text += extracted + "\n"
            except Exception:
                st.error("File is locked or corrupted. Please give an unprotected PDF.")
                st.stop()
        elif pasted_text.strip():
            resume_text = pasted_text
        else:
            st.warning("Please upload a PDF or paste your resume text.")
            st.stop()

        if len(resume_text.strip()) < 100:
            st.error("Document is not machine-readable or does not appear to be a resume. Please use standard text.")
            st.stop()

        # --- THE AI ENGINE ---
        with st.spinner("Clocking your resume... This might take a few seconds."):
            
            if st.session_state.field == "Tech":
                rubric = """
                You are evaluating a Technical & STEM resume.
                1. Core Identity & Contact (15 pts): Name top (3), Pro Email (3), Phone (3), LinkedIn (3), GitHub (3).
                2. Strict Parsability & Formatting (20 pts): Single-Column (7), Standard Headers (5), White-Text Penalty (5), Date Consistency (3).
                3. Keyword Context & Stack Match (30 pts): Hard Skill Frequency (15), Contextual Application (10), Dev Environment (5).
                4. Technical Projects & Impact (20 pts): XYZ Formula (8), Embedded Repo Links (6), Execution Verbs (6).
                5. Education & Credentials (15 pts): Degree (5), Graduation Timeline (5), Certifications (5).
                MISSING LOGIC: Fresher (flag missing GitHub/projects), Mid (flag missing metrics/cloud), Senior (flag missing architecture/mentorship), Exec (flag missing strategy/financial impact).
                """
            elif st.session_state.field == "Business":
                rubric = """
                You are evaluating a Business, Law & Management resume.
                1. Core Identity & Network (15 pts): Name (3), Pro Email (3), Phone (3), LinkedIn (6).
                2. Strict Parsability & Structure (20 pts): Reverse-Chronological (7), Date Alignment (5), Standard Headers (5), Grammar (3).
                3. Industry Acumen (20 pts): Domain Tools (10), Strategy (10).
                4. Experience & Impact (30 pts): Financial Metrics (12), Leadership Verbs (8), Scope (10).
                5. Education (15 pts): Degree (5), Honors/GPA (5), Certs (5).
                MISSING LOGIC: Fresher (flag missing internships/GPA), Mid (flag missing financial metrics/lingering support verbs), Senior (flag missing P&L/headcount), Exec (flag missing M&A/board relations).
                """
            else:
                rubric = """
                You are evaluating a Creative, Media & Design resume.
                1. Identity & Portfolio (20 pts): Portfolio Link (8), LinkedIn (3), Name (3), Email (3), Phone (3).
                2. Parsability (15 pts): Text Extractability (7), Formatting (3), Headers (5).
                3. Tooling (25 pts): Industry Software (10), Workflow Tools (10), Contextual Tooling (5).
                4. Process & Impact (25 pts): Process Keywords (10), Engagement Metrics (10), Execution Verbs (5).
                5. Education (15 pts): Degree (5), Certifications (5), Awards (5).
                MISSING LOGIC: Fresher (flag missing live portfolio/process context), Mid (flag missing engagement metrics/collaboration), Senior (flag missing creative direction), Exec (flag missing agency management).
                """

            prompt = f"Act as an expert ATS. Review this resume based on:\n{rubric}\n\nOUTPUT:\n1. ATS Score /100\n2. Experience Level\n3. Breakdown\n4. What You Are Missing\n5. Actionable Feedback\n\nRESUME:\n{resume_text}"

            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                st.success("Analysis Complete!")
                st.markdown(response.text)
                
            except Exception as e:
                error_msg = str(e).lower()
                if "429" in error_msg or "503" in error_msg or "quota" in error_msg:
                    st.warning("We are experiencing exceptionally high traffic right now. Please wait a few moments & resubmit your document.")
                else:
                    st.error(f"An error occurred: {e}")