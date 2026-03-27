import streamlit as st
from supabase import create_client, Client
import json

def init_connection() -> Client:
    """
    Initializes the connection to Supabase using secrets.
    """
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def submit_data_to_db(email, name, process, state, school, udise, responses_dict, document_urls=None):
    """
    Packages the Multi-Page form data and sends it to Supabase.
    The 171 questions are automatically handled inside the 'responses' JSONB column.
    """
    supabase = init_connection()
    
    # Clean the dictionary: remove empty string answers to save database space
    cleaned_responses = {k: v for k, v in responses_dict.items() if v != ""}
    
    # Add document URLs to the JSONB object if any were uploaded
    if document_urls:
        cleaned_responses["Supporting_Documents"] = document_urls

    # Map the data exactly to the 18 columns created in the SQL script
    db_payload = {
        "verified_email": email,           # Captured via Google OAuth
        "selected_name": name,             # Page 1
        "process_type": process,           # Page 1
        "state": state,                    # Page 2
        "school_name": school,             # Page 2
        "udise_code": udise,               # Page 2 (Auto-mapped)
        "responses": cleaned_responses     # The 171 dynamic questions + Media
    }
    
    try:
        # Push to the Wide Table
        response = supabase.table("process_submissions_2026").insert(db_payload).execute()
        return True, "सफलतापूर्वक सबमिट किया गया! / Submitted Successfully!"
    except Exception as e:
        return False, f"Error: {str(e)}"

def keep_alive_ping():
    """
    This function is triggered by your Cron-job.org setup.
    It performs a tiny 1-row read to register 'active traffic' on Supabase,
    ensuring your 500MB free tier is never paused.
    """
    try:
        supabase = init_connection()
        supabase.table("process_submissions_2026").select("id").limit(1).execute()
        return True
    except Exception:
        return False