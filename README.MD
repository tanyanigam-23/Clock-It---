# Clock It!!!
AI-based resume reviewer that gives an ATS score and tells you what your resume is missing.
![ClockIt Logo](logo.png)

## Features
- Pick a field: Technical & STEM, Business/Law & Management, or Creative/Media & Design
- Standard resume template for each field
- Upload a PDF (max 2 MB, max 2 pages) or paste resume text
- ATS score out of 100 with a field-specific rubric
- Shows what you are missing for your experience level
- Handles edge cases: too long, locked or corrupted PDF, non-resume documents

## Tech stack
Python, Streamlit, pdfplumber, Google Gemini API

## Setup
1. Clone the repo
2. `pip install -r requirements.txt`
3. Create a `.env` file (see `.env.example`) with your Gemini API key
4. `streamlit run app.py`

## Note
The ATS scoring criteria, edge-case rules and handling, debugging, UI design and logo are my own work. A few parts of code were generated using AI Assistance.

Built by Tanya Nigam {Foundation Year B.tech CSE Student(2026-2030)}