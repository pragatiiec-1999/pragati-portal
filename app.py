import streamlit as st
import time
import json
import streamlit.components.v1 as components
from supabase import create_client, Client
from streamlit_oauth import OAuth2Component
import chatbot_logic as logic 
import rm_config as config  # Pulls directly from your generated file
import base64
from PIL import Image
import os
    
# ==========================================
# 1. ENTERPRISE UI CONFIGURATION
# ==========================================
try:
    icon_path = "static/icon4.png" 
    tab_icon = Image.open(icon_path)
except Exception as e:
    tab_icon = "File" 

st.set_page_config(
    page_title="IEC | Process Tracker 2026-2027", 
    page_icon=tab_icon, 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- REFRESH CAUTION (DATA LOSS WARNING) ---
components.html("""
    <script>
        const parent = window.parent;
        parent.addEventListener('beforeunload', function (e) {
            e.preventDefault();
            e.returnValue = 'Are you sure you want to leave? Unsaved data will be lost.';
        });
    </script>
""", height=0)

# --- BASE64 IMAGE CONVERTER ---
def get_base64(file_path):
    clean_path = file_path.replace("app/", "")
    if os.path.exists(clean_path):
        with open(clean_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

bg1_b64 = get_base64("static/bg1.jpg")
bg2_b64 = get_base64("static/bg2.jpg")
bg3_b64 = get_base64("static/bg3.jpg")
bg4_b64 = get_base64("static/bg4.jpg")
logo_b64 = get_base64("static/logo_clear.png")

# --- PROFESSIONAL DARK MODE & ADAPTIVE STYLING ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    theme_bg_gradient = "linear-gradient(135deg, #131314 0%, #1e1f20 100%)"
    theme_card = "#26272b"  
    theme_text = "#FFFFFF"      # Pure white for high contrast
    theme_border = "#444746"
    theme_muted = "#e0e0e0"     # Brighter gray for secondary text
else:
    theme_bg_gradient = "linear-gradient(-45deg, #f8fafc, #e0f2fe, #f1f5f9, #ecfdf5)"
    theme_card = "#ffffff"
    theme_text = "#0f172a"
    theme_border = "#cbd5e1"
    theme_muted = "#64748b"

# ==========================================
# FINAL OPTIMIZED CSS (GLASSMORPHISM EDITION)
# ==========================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    @keyframes gradientBG {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    @keyframes floatLetters {{ 0% {{ transform: translateY(5vh) translateX(0px) rotate(0deg); opacity: 0; }} 10% {{ opacity: 0.04; }} 90% {{ opacity: 0.04; }} 100% {{ transform: translateY(-20vh) translateX(-20px) rotate(5deg); opacity: 0; }} }}
    
    .fade-in {{ animation: fadeIn 1.2s ease-in-out; }}
    @keyframes fadeIn {{ 0% {{ opacity: 0; transform: translateY(10px); }} 100% {{ opacity: 1; transform: translateY(0); }} }}
    
    [data-testid="stHeader"] {{ display: none !important; }}
    
    .stApp {{ background: {theme_bg_gradient} !important; background-size: 300% 300% !important; animation: gradientBG 18s ease-in-out infinite !important; font-family: 'Inter', sans-serif; color: {theme_text} !important; }}
    .stApp::before {{ content: 'A अ 1 B आ 2 C इ 3 D ई 4 E उ 5 F ऊ 6 G ऋ 7 H ए 8 I ऐ 9 J ओ 0 K औ L क M ख N ग O घ P ङ Q च R छ S ज T झ U ञ V ट W ठ X ड Y ढ Z ण 0 त 1 थ 2 द 3 ध 4 न 5 प 6 फ 7 ब 8 भ 9 म A य B र C ल D व E श F ष G स H ह I क्ष J त्र K ज्ञ'; position: fixed; top: -10%; left: -10%; width: 120%; height: 120%; font-size: 42px; font-weight: 600; word-spacing: 80px; line-height: 130px; text-align: justify; color: {theme_text}; opacity: 0.04; pointer-events: none; z-index: 0; animation: floatLetters 35s linear infinite; }}

    .block-container {{ position: relative; z-index: 10; padding-top: 0px !important; padding-bottom: 100px !important; max-width: 1000px; color: {theme_text} !important; margin-top: 0px !important; background: transparent !important; box-shadow: none !important; }} 
    
    /* Force high visibility on all labels and standard text */
    h1, h2, h3, h4, p, span, label, 
    [data-testid="stWidgetLabel"] p, 
    [data-testid="stMarkdownContainer"] p {{ 
        color: {theme_text} !important; 
        font-weight: 500 !important;
    }}
    
    .stSelectbox div[data-baseweb="select"] {{ background-color: {theme_card} !important; border-radius: 12px !important; border-color: {theme_border} !important; }}
    
    /* Ensure the text inside dropdowns and inputs is readable */
    div[data-baseweb="select"] span, 
    div[data-baseweb="input"] input {{ 
        color: {theme_text} !important; 
        -webkit-text-fill-color: {theme_text} !important; 
    }}

    .full-bleed-banner {{ width: 100vw; height: 260px; position: relative; left: 50%; transform: translateX(-50%); overflow: hidden; margin-top: 0rem; margin-bottom: 10px; mask-image: linear-gradient(to bottom, black 60%, transparent 100%); -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%); }}
    .slider-track {{ display: flex; width: 500%; height: 100%; animation: slideLeft 24s infinite cubic-bezier(0.645, 0.045, 0.355, 1); }}
    .slider-track img {{ width: 20%; height: 100%; object-fit: cover; object-position: center top; }} 
    @keyframes slideLeft {{ 0%, 18% {{ transform: translateX(0); }} 25%, 43% {{ transform: translateX(-20%); }} 50%, 68% {{ transform: translateX(-40%); }} 75%, 93% {{ transform: translateX(-60%); }} 100% {{ transform: translateX(-80%); }} }}
    .banner-logo {{ height: 110px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.4)); }}
    
    /* =========================================
       FILE UPLOADER (TOTAL THEME LOCKDOWN)
       ========================================= */
    [data-testid="stFileUploadDropzone"] {{ 
        background-color: #ffffff !important; 
        border: 2px dashed #cbd5e1 !important; 
        border-radius: 12px !important;
    }}
    
    /* Forces ALL text to stay dark via double-braces so Python doesn't eat the rule */
    [data-testid="stFileUploadDropzone"] div, 
    [data-testid="stFileUploadDropzone"] p, 
    [data-testid="stFileUploadDropzone"] span, 
    [data-testid="stFileUploadDropzone"] small {{ 
        color: #0f172a !important; 
        -webkit-text-fill-color: #0f172a !important; 
    }}
    
    /* Forces the Cloud Icon to stay dark gray */
    [data-testid="stFileUploadDropzone"] svg path {{ 
        fill: #64748b !important; 
    }}

    /* Locks the Browse files button background and text */
    [data-testid="stFileUploadDropzone"] button {{
        background-color: #f8fafc !important;
        color: #0f172a !important;
        -webkit-text-fill-color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
    }}
    
    /* =========================================
       UNIVERSAL BUTTON GLASSMORPHISM
       ========================================= */
    /* Standard & Login Buttons */
    .stButton > button, 
    div[data-testid="stMarkdownContainer"] button,
    [data-testid="stBaseButton-secondary"] {{
        background: rgba(150, 150, 150, 0.1) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(150, 150, 150, 0.2) !important; /* The 'Glass Edge' */
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        color: {theme_text} !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        text-align: center !important;
    }}

    /* Hover Effect for a premium feel */
    .stButton > button:hover, 
    div[data-testid="stMarkdownContainer"] button:hover {{
        background: rgba(150, 150, 150, 0.2) !important;
        border: 1px solid rgba(150, 150, 150, 0.4) !important;
    }}

    /* Primary Action Buttons (Blue Tinted Glass) */
    .stButton > button[kind="primary"] {{
        background: rgba(0, 114, 206, 0.15) !important;
        border: 1px solid rgba(0, 114, 206, 0.3) !important;
        color: #0072CE !important; 
        font-weight: 600 !important;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        background: rgba(0, 114, 206, 0.25) !important;
    }}

    /* Fix to keep OAuth text centered inside the glass button */
    div[data-testid="stMarkdownContainer"] button div {{ margin: 0 auto !important; }}

    /* =========================================
       WARNING NOTE (RED GLASSMORPHISM)
       ========================================= */
    .red-tilt-note {{ 
        color: #d93025 !important; 
        background: rgba(217, 48, 37, 0.08) !important; 
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(217, 48, 37, 0.2) !important;
        box-shadow: 0 4px 15px rgba(217, 48, 37, 0.05) !important;
        text-align: center; 
        padding: 12px;
        border-radius: 8px;
        display: block; 
        margin-top: 25px; 
        font-weight: 500; 
        font-size: 0.95rem; 
        font-family: 'Inter', sans-serif;
    }}

    [data-testid="stVerticalBlock"] > div:empty {{ display: none !important; }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* =========================================
       TOTAL CONTAINER REMOVAL (NUCLEAR FIX)
       ========================================= */
    /* Targets the outer box and forced it to be invisible */
    [data-testid="stFileUploadDropzone"], 
    [data-testid="stFileUploadDropzone"] > div,
    [data-testid="stFileUploadDropzone"] section {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0px !important;
    }}

    /* Removes the gray hover effect that Streamlit adds */
    [data-testid="stFileUploadDropzone"]:hover {{
        background: transparent !important;
    }}

    /* "Drag and drop" text - Pure adaptive text */
    [data-testid="stFileUploadDropzone"] p, 
    [data-testid="stFileUploadDropzone"] span,
    [data-testid="stFileUploadDropzone"] small {{
        color: {theme_text} !important;
        -webkit-text-fill-color: {theme_text} !important;
        font-weight: 500 !important;
    }}

    /* Cloud Icon - Adaptive color */
    [data-testid="stFileUploadDropzone"] svg path {{
        fill: {theme_muted} !important;
    }}

    /* "Browse files" button - Professional Glass Style */
    [data-testid="stFileUploadDropzone"] button {{
        background: rgba(150, 150, 150, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid {theme_border} !important;
        color: {theme_text} !important;
        border-radius: 8px !important;
        margin-top: 10px !important;
    }}
    /* =========================================
       GLASSMORPHISM FOR CONTAINERS (LOGIN BOX)
       ========================================= */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: rgba(150, 150, 150, 0.05) !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(150, 150, 150, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1) !important;
    }}
    
    /* Hides the hoverable anchor link icon next to h1, h2, h3, h4 */
    .stApp h1 a, .stApp h2 a, .stApp h3 a, .stApp h4 a {{
        display: none !important;
    }}

    /* Prevents the header from shifting when you hover near it */
    [data-testid="stHeaderActionElements"] {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- JAVASCRIPT SCROLL ---
def scroll_to_top():
    components.html("""<script>setTimeout(function() { window.parent.scrollTo({top: 0, behavior: 'smooth'}); }, 100);</script>""", height=0)


# ==========================================
# 2. LOGIN PAGE (THE GATEKEEPER)
# ==========================================

# -------------------------------------------------------------------------
# NON-TECHNICAL HOW-TO: TURNING OFF THE LOGIN SCREEN COMPLETELY
# If you decide you DO NOT want a login screen anymore, just remove the 
# hashtag (#) from the start of the line below. 
# This gives everyone an automatic "VIP Pass" so the app skips the login gate.
# -------------------------------------------------------------------------
# st.session_state["user_email"] = "vip_user@no-login-needed.com"


# This checks if the user has a VIP pass or has already logged in.
if "user_email" not in st.session_state:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    # Outer columns to center the white login box on the screen
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        with st.container(border=True):
            st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{logo_b64}' style='height: 100px; margin-bottom: 20px;'></div>", unsafe_allow_html=True)
            st.markdown("<h3 style='text-align: center;'> Secure Portal Login</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: {theme_muted};'>Please sign in with your authorized office email.</p>", unsafe_allow_html=True)
            st.write("")
            
            try:
                client_id = st.secrets["google"]["client_id"]
                client_secret = st.secrets["google"]["client_secret"]
                authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
                token_url = "https://oauth2.googleapis.com/token"
                refresh_token_url = "https://oauth2.googleapis.com/token"
                revoke_url = "https://oauth2.googleapis.com/revoke"

                oauth2 = OAuth2Component(client_id, client_secret, authorize_url, token_url, refresh_token_url, revoke_url)
                
                # --- NEW: CORNER FIX ---
                # This forces the button (and its hidden iframe) to have perfectly rounded corners on both sides
                st.markdown("""
                    <style>
                    iframe, .stButton > button, div[data-testid="stMarkdownContainer"] button {
                        border-radius: 8px !important;
                    }
                    </style>
                """, unsafe_allow_html=True)

                # --- SMART REDIRECT URL ---
                # Automatically switches between local testing and the live website
                if os.environ.get("RENDER"):
                    auth_redirect_uri = "https://iec-pragati-portal.onrender.com/"
                else:
                    auth_redirect_uri = "http://localhost:8501"

                # --- THE SQUEEZE FIX ---
                # These inner columns "squeeze" the button so the text looks perfectly centered.
                inner_c1, inner_c2, inner_c3 = st.columns([1.5, 2.5, 1.5])
                with inner_c2:
                    result = oauth2.authorize_button(
                        "Login", 
                        redirect_uri=auth_redirect_uri, 
                        scope="openid email profile"
                    )

                if result and "token" in result:
                    id_token = result["token"]["id_token"]
                    payload = id_token.split(".")[1]
                    payload += "=" * ((4 - len(payload) % 4) % 4)
                    decoded_payload = json.loads(base64.b64decode(payload).decode("utf-8"))
                    st.session_state["user_email"] = decoded_payload.get("email")
                    st.rerun()
                
            except Exception as e:
                # If the login breaks (e.g., missing secrets), show an error message but NO bypass button.
                st.error(f"Setup Error: {e}") 
                st.markdown(f"<p style='text-align: center; color: {theme_muted}; font-size: 0.9rem;'>Authentication credentials not found in secrets.toml.</p>", unsafe_allow_html=True)
                    
    # Stop the rest of the app from loading until login is successful (or bypassed above)
    st.stop()


# ==========================================
# 3. SECURE APP INITIALIZATION 
# ==========================================
# 1. Connection initialize karein
@st.cache_resource
def init_connection():
    try:
        return create_client(st.secrets["supabase"]["url"], st.secrets["supabase"]["key"])
    except: return None

supabase = init_connection()

# 2. HEARTBEAT PING (Cron-job.org ke liye)
# Yeh har page load par Supabase ko ek "Hello" bhejega bina cache ke
if supabase:
    try:
        # Sirf ek row check karna activity register karne ke liye kaafi hai
        supabase.table("process_submissions_2026").select("id").limit(1).execute()
    except:
        pass

# --- STATE MANAGEMENT ---
if 'step' not in st.session_state: st.session_state.step = 'GATEWAY'
if 'responses' not in st.session_state: st.session_state.responses = {}
if 'trigger_scroll' not in st.session_state: st.session_state.trigger_scroll = False
if 'form_completed' not in st.session_state: st.session_state.form_completed = False

# --- SPLASH SCREEN ---
if 'app_initialized' not in st.session_state:
    loader_placeholder = st.empty()
    solid_bg = "#1e1f20" if st.session_state.dark_mode else "#f8fafc"
    loader_placeholder.markdown(f"""
        <div id="true-splash-screen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: {solid_bg}; z-index: 9999999; display: flex; justify-content: center; align-items: center;">
            <div style="display: flex; flex-direction: column; align-items: center; transform: translateY(-5vh);">
                <img src='data:image/png;base64,{logo_b64}' style="height: 160px; margin-bottom: 30px; animation: pulse 2s infinite;">
                <h4 style="color: #0072CE; font-weight: 600; margin-bottom: 20px; font-size: 1.3rem;">Initializing Secure Portal...</h4>
                <div style="width: 300px; height: 6px; background: {theme_border}; border-radius: 10px; overflow: hidden;">
                    <div style="width: 50%; height: 100%; background: #0072CE; animation: slide 1.5s infinite linear;"></div>
                </div>
            </div>
        </div>
        <style>
            @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.05); opacity: 1; }} 100% {{ transform: scale(1); opacity: 0.8; }} }} 
            @keyframes slide {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(200%); }} }}
        </style>
    """, unsafe_allow_html=True)
    time.sleep(1.5) 
    loader_placeholder.empty() 
    st.session_state.app_initialized = True
    st.rerun() 

if st.session_state.trigger_scroll:
    scroll_to_top()
    st.session_state.trigger_scroll = False

# ==========================================
# 4. UNIVERSAL HEADER 
# ==========================================
html_banner = f"""
<div class="full-bleed-banner">
    <div class="slider-track">
        <img src="data:image/jpeg;base64,{bg1_b64}"><img src="data:image/jpeg;base64,{bg2_b64}">
        <img src="data:image/jpeg;base64,{bg3_b64}"><img src="data:image/jpeg;base64,{bg4_b64}">
        <img src="data:image/jpeg;base64,{bg1_b64}">
    </div>
    <div style="position: absolute; top:0; left:0; right:0; height: 140px; background: linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 100%); z-index: 5;"></div>
    <div style="position: absolute; top: 15px; left: 5%; z-index: 10;">
        <img class="banner-logo" src="data:image/png;base64,{logo_b64}">
    </div>
</div>"""
st.markdown(html_banner, unsafe_allow_html=True)

nav_col1, toggle_col = st.columns([0.8, 0.2])
with nav_col1:
    st.caption(f"Authenticated: {st.session_state['user_email']}")
with toggle_col:
    st.toggle("Dark Theme", key="dark_mode")

# ==========================================
# 5. FLOW ROUTING
# ==========================================
if st.session_state.form_completed:
    st.markdown(f"""
        <div class="fade-in" style="text-align: center; padding: 50px 20px; background: {theme_card}; border-radius: 15px; border: 1px solid {theme_border};">
            <img src="data:image/png;base64,{logo_b64}" style="height: 140px; margin-bottom: 25px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.15));">
            <h2 style="color: #0072CE;">Your response has been recorded.</h2>
            <p style="color: {theme_muted}; font-size: 1.1rem;">Thank you for completing the assessment.</p>
        </div>
    """, unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Submit another response", type="primary", use_container_width=True):
            keys_to_keep = ['user_email', 'app_initialized', 'dark_mode']
            for key in list(st.session_state.keys()):
                if key not in keys_to_keep:
                    del st.session_state[key]
            st.rerun()

elif st.session_state.step == 'GATEWAY':
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("<h3 style='text-align: center;'>Gateway</h3>", unsafe_allow_html=True)
            
            t_names = sorted(list(set([r.get("Teachers' Name") for r in config.RM_DATA if r.get("Teachers' Name")])))
            
            u_name_choice = st.selectbox("Observer Name", t_names + ["Other (Manual Entry)"], index=None, placeholder="Select your name...")
            if u_name_choice == "Other (Manual Entry)":
                u_name = st.text_input("Type your name here")
            else:
                u_name = u_name_choice
                
            u_proc = st.selectbox("Process", ["Teacher's Collective", "Classroom Observation","School Visit", "GP", "BPM", "DIET", "BESC"], index=None, placeholder="Select process...")
            
            if u_name and u_proc:
                st.session_state.responses['observer_name'] = u_name
                st.session_state.responses['process_type'] = u_proc
                st.session_state.step = 'QUESTIONNAIRE'
                st.session_state.trigger_scroll = True
                st.rerun()

elif st.session_state.step == 'QUESTIONNAIRE':
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    proc = st.session_state.responses['process_type']
    if proc in ["Teacher's Collective", "Classroom Observation", "School Visit"]:
        active_list = logic.get_form_questions(proc)
        heading = "सभी प्रश्न अनिवार्य हैं / All questions are mandatory"
    else:
        active_list = logic.get_process_indicators(proc)
        heading = "कृपया इंडिकेटर चुनें / Please select indicators"

    total_q = len(active_list)
    answered = len([k for k, v in st.session_state.responses.items() if k in [q['id'] for q in active_list] and v is not None and v is not False and str(v).strip() != ""])
    progress = int((answered / total_q) * 100) if total_q > 0 else 0

    st.markdown(f"""
        <div style="position: sticky; top: 20px; z-index: 100; margin-bottom: 30px; padding: 15px; background: {theme_card}; border-radius: 10px; border: 1px solid {theme_border}; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-weight: bold; color: #0072CE;">Assessment Progress</span>
                <span style="font-weight: bold; color: {theme_text};">{progress}% ({answered}/{total_q})</span>
            </div>
            <div style="background:#e2e8f0; border-radius:10px; height:8px; width:100%; margin: 8px 0;">
                <div style="background:#0072CE; height:8px; width:{progress}%; border-radius:10px; transition: width 0.3s ease;"></div>
            </div>
            <div style="text-align: center; font-weight: 600; font-size: 0.95rem; color: {theme_muted};">{heading}</div>
        </div>
    """, unsafe_allow_html=True)

    for i, q in enumerate(active_list):
        with st.container(border=True):
            if proc in ["Teacher's Collective", "Classroom Observation", "School Visit"]:
                st.markdown(f"**Q{i + 1}. {q['text']}**")
                ans_key = q['id']
                q_type = str(q.get('type', 'dropdown')).strip().lower()

                if q_type in ['dropdown', 'multiple choice']:
                    if q.get('options'):
                        st.session_state.responses[ans_key] = st.selectbox(
                            "Options", q['options'], index=None, placeholder="Select this according to the question...", 
                            label_visibility="collapsed", key=f"ans_{ans_key}"
                        )
                    else:
                        st.session_state.responses[ans_key] = st.text_input("Input", placeholder="Type your answer here...", label_visibility="collapsed", key=f"ans_{ans_key}")
                elif q_type == 'numeric':
                    st.session_state.responses[ans_key] = st.number_input("Number", value=None, step=1.0, placeholder="Enter a number...", label_visibility="collapsed", key=f"ans_{ans_key}")
                elif q_type == 'date':
                    st.session_state.responses[ans_key] = st.date_input("Date", value=None, label_visibility="collapsed", key=f"ans_{ans_key}")
                else:
                    st.session_state.responses[ans_key] = st.text_area("Text", placeholder="Provide detailed observations...", label_visibility="collapsed", key=f"ans_{ans_key}")
            else:
                st.markdown(f"**{i + 1}. {q['text']}**")
                # Ensure the checkbox updates the session state correctly
                st.session_state.responses[q['id']] = st.checkbox(f"Select {q['id']}", key=f"ans_{q['id']}", label_visibility="collapsed")

    st.divider()
    
    # This remains transparent due to the CSS we updated earlier
    st.file_uploader("Browse Document", type=['pdf', 'xlsx', 'docx'], label_visibility="collapsed")
    
    st.markdown('<div class="red-tilt-note">सबमिट करने के बाद कोई बदलाव संभव नहीं है / Final Submission: Records cannot be modified after confirmation.</div>', unsafe_allow_html=True)
    st.write("")

    # --- ENHANCED NEXT BUTTON WITH VALIDATION ---
    if st.button("Next", type="primary", use_container_width=True):
        # Mandatory Checkbox Validation for Indicator Processes
        if proc not in ["Teacher's Collective", "Classroom Observation", "School Visit"]:
            indicator_ids = [q['id'] for q in active_list]
            is_any_checked = any(st.session_state.responses.get(idx) for idx in indicator_ids)
            
            if not is_any_checked:
                st.error("⚠️ कृपया कम से कम एक इंडिकेटer चुनें / Please select at least one indicator.")
                st.stop()
        
        # Proceed if validation passes
        st.session_state.step = 'RM_PAGE'
        st.session_state.trigger_scroll = True
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
# ------------------------------------------
# 4. STEP 3: RM PAGE (RELATIONAL DATA, NO AUTO-FILL)
# ------------------------------------------
elif st.session_state.step == 'RM_PAGE':
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.title("School Identification & Validation")
    st.info("Please fill the hierarchy to register this submission.")

    # Access the relational data list of dictionaries
    raw_data = config.RM_DATA

    # --- 1. STATE SELECTION (STRICTLY MANDATORY) ---
    state_list = sorted(list(set([r.get('State') for r in raw_data if r.get('State')])))
    selected_state = st.selectbox("State (Mandatory)", state_list, index=None, placeholder="Select State...")

    # Cascading Logic: Filter data based on selected state
    filtered_data = [r for r in raw_data if r.get('State') == selected_state] if selected_state else raw_data

    c1, c2 = st.columns(2)
    
    with c1:
        # DISTRICT (Strict Dropdown)
        d_list = sorted(list(set([r.get('District') for r in filtered_data if r.get('District')])))
        dist = st.selectbox("District", d_list, index=None, placeholder="Select District...")
        if dist: filtered_data = [r for r in filtered_data if r.get('District') == dist]

        # BLOCK (Strict Dropdown)
        b_list = sorted(list(set([r.get('Block') for r in filtered_data if r.get('Block')])))
        block = st.selectbox("Block", b_list, index=None, placeholder="Select Block...")
        if block: filtered_data = [r for r in filtered_data if r.get('Block') == block]

        # CLUSTER (Strict Dropdown)
        c_list = sorted(list(set([r.get('Cluster') for r in filtered_data if r.get('Cluster')])))
        cluster = st.selectbox("Cluster", c_list, index=None, placeholder="Select Cluster...")
        if cluster: filtered_data = [r for r in filtered_data if r.get('Cluster') == cluster]
        
        # GP/NP TYPE (Strict Dropdown)
        gp_np_list = sorted(list(set([r.get('GP/NP') for r in filtered_data if r.get('GP/NP')])))
        gp_np_sel = st.selectbox("GP / NP Type", gp_np_list, index=None, placeholder="Select Type...")
        
        # GRAM PANCHAYAT (Manual Entry Allowed)
        gp_list = sorted(list(set([r.get('Gram Panchayat') for r in filtered_data if r.get('Gram Panchayat')])))
        gp_choice = st.selectbox("Gram Panchayat Name", gp_list + ["Other (Manual Entry)"], index=None, placeholder="Select GP...")
        gp_sel = st.text_input("Type Gram Panchayat Name") if gp_choice == "Other (Manual Entry)" else gp_choice

    with c2:
        # SCHOOL NAME (Manual Entry Allowed)
        s_list = sorted(list(set([r.get('School Name') for r in filtered_data if r.get('School Name')])))
        school_choice = st.selectbox("School Name", s_list + ["Other (Manual Entry)"], index=None, placeholder="Select School...")
        school_sel = st.text_input("Type School Name") if school_choice == "Other (Manual Entry)" else school_choice
        
        # --- HIDDEN UDISE CAPTURE LOGIC (No visual auto-fill) ---
        hidden_udise = ""
        if school_choice and school_choice != "Other (Manual Entry)":
            # We check raw_data directly so it always finds the UDISE
            for r in raw_data:
                if r.get('School Name') == school_choice:
                    hidden_udise = r.get('UDISE Code', '')
                    break

        # TEACHER NAME (Manual Entry Allowed)
        t_list = sorted(list(set([r.get("Teachers' Name") for r in filtered_data if r.get("Teachers' Name")])))
        teacher_choice = st.selectbox("Teacher Name", t_list + ["Other (Manual Entry)"], index=None, placeholder="Select Teacher...")
        teacher_sel = st.text_input("Type Teacher Name") if teacher_choice == "Other (Manual Entry)" else teacher_choice

        # SCHOOL TYPE (Strict Dropdown - No Autofill)
        stype_list = sorted(list(set([r.get('School Type') for r in raw_data if r.get('School Type')])))
        school_type = st.selectbox("School Type", stype_list, index=None, placeholder="Select Type...")

        # ROLE (Strict Dropdown - No Autofill)
        role_list = sorted(list(set([r.get('Relevant Role') for r in raw_data if r.get('Relevant Role')])))
        role = st.selectbox("Role", role_list, index=None, placeholder="Select Role...")
        
        # POST (Strict Dropdown - No Autofill)
        post_list = sorted(list(set([r.get('Post') for r in raw_data if r.get('Post')])))
        post = st.selectbox("Post", post_list, index=None, placeholder="Select Post...")

    st.markdown('<div class="red-tilt-note">सबमिट करने के बाद कोई बदलाव संभव नहीं है / Final Submission: Records cannot be modified after confirmation.</div>', unsafe_allow_html=True)
    
    if st.button("Confirm & Submit Assessment", type="primary", use_container_width=True):
        if not selected_state:
            st.error("Error: State is mandatory. Please select a state before submitting.")
        else:
            with st.spinner("Writing to Database..."):
                # PAYLOAD ALIGNED TO YOUR DATABASE SCHEMA
                db_payload = {
                    "verified_email": st.session_state.get('user_email', 'Unauthenticated User'),
                    "selected_name": st.session_state.responses.get('observer_name'), # Matches your 'selected_name' column
                    "process_type": st.session_state.responses.get('process_type'),  # Fixed spelling to match your DB 'procees_type'
                    "state": selected_state,
                    "district": dist,
                    "block": block,
                    "cluster": cluster,
                    "gp_np": gp_np_sel,       # Fixed from 'gp_np_type' to match your DB 'gp_np'
                    "gram_panchayat": gp_sel,
                    "school_type": school_type,
                    "udise_code": hidden_udise,
                    "teachers_name": teacher_sel, # Fixed to match your DB 'teachers_name'
                    "role": role,
                    "post": post,
                    "answers": {k:v for k,v in st.session_state.responses.items() if k not in ['observer_name', 'process_type']}
                }
                
                if supabase:
                    try:
                        # Database insert attempt
                        supabase.table("process_submissions_2026").insert(db_payload).execute()
                        
                        # --- SUCCESS PATH ---
                        time.sleep(1)
                        st.session_state.form_completed = True
                        st.session_state.trigger_scroll = True
                        st.rerun()
                        
                    except Exception as e:
                        # --- ERROR PATH ---
                        st.error(f"Database Error: {e}")
                        st.warning("Data save nahi hua. Please ensure column names match exactly.")
                        st.stop() 
                else:
                    st.error("Supabase Connection Error: Database initialize nahi ho paya.")
                    st.stop()