import streamlit as st
import pandas as pd
import time
import streamlit.components.v1 as components
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from modules.chatbot_logic import questions_list
import base64
from PIL import Image

# --- 1. ENTERPRISE UI CONFIGURATION ---
try:
    # 1. We define the path (ensure this matches GitHub exactly!)
    icon_path = "static/icon4.png" 
    
    # 2. Open it with PIL
    tab_icon = Image.open(icon_path)
except Exception as e:
    # Fallback if the file is missing or path is wrong
    tab_icon = "📄" 

st.set_page_config(
    page_title="Pragati Portal | IEC", 
    page_icon=tab_icon, # Passing the PIL Image object here
    layout="centered"
)

# --- BASE64 IMAGE CONVERTER (The Cloud Fix) ---
def get_base64(file_path):
    import os
    # We remove the "app/" prefix because GitHub/Streamlit root starts at the repo level
    clean_path = file_path.replace("app/", "")
    
    if os.path.exists(clean_path):
        with open(clean_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

# Updated Paths (Removing 'app/' prefix)
bg1_b64 = get_base64("static/bg1.jpg")
bg2_b64 = get_base64("static/bg2.jpg")
bg3_b64 = get_base64("static/bg3.jpg")
bg4_b64 = get_base64("static/bg4.jpg")
logo_b64 = get_base64("static/logo_clear.png")
iec_logo_b64 = get_base64("static/iec_logo.png")

# --- 1.5 PROFESSIONAL DARK MODE & ANIMATED BACKGROUND ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    theme_bg_gradient = "linear-gradient(135deg, #131314 0%, #1e1f20 100%)" # Sleek charcoal gradient
    theme_fade_color = "#131314"   
    theme_card = "#1e1f20"  
    theme_text = "#e3e3e3"      
    theme_border = "#444746"
    theme_bot_bubble = "#1e1f20"
    theme_user_bubble = "#333538" 
    theme_user_border = "#444746"
    theme_muted = "#c4c7c5"
else:
    theme_bg_gradient = "linear-gradient(-45deg, #f8fafc, #e0f2fe, #f1f5f9, #ecfdf5)"
    theme_fade_color = "#f8fafc"   # NEW: Matches the light background
    theme_card = "#ffffff"
    theme_text = "#0f172a"
    theme_border = "#cbd5e1"
    theme_bot_bubble = "#ffffff"
    theme_user_bubble = "#e0f2fe"
    theme_user_border = "#bae6fd"
    theme_muted = "#64748b"
    theme_card_rgb = "255, 255, 255"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    @keyframes gradientBG {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    .stApp {{ background: {theme_bg_gradient} !important; background-size: 300% 300% !important; animation: gradientBG 18s ease-in-out infinite !important; font-family: 'Inter', sans-serif; color: {theme_text} !important; }}
    @keyframes floatLetters {{ 0% {{ transform: translateY(5vh) translateX(0px) rotate(0deg); opacity: 0; }} 10% {{ opacity: 0.04; }} 90% {{ opacity: 0.04; }} 100% {{ transform: translateY(-20vh) translateX(-20px) rotate(5deg); opacity: 0; }} }}
    .stApp::before {{ content: 'A अ 1 B आ 2 C इ 3 D ई 4 E उ 5 F ऊ 6 G ऋ 7 H ए 8 I ऐ 9 J ओ 0 K औ L क M ख N ग O घ P ङ Q च R छ S ज T झ U ञ V ट W ठ X ड Y ढ Z ण 0 त 1 थ 2 द 3 ध 4 न 5 प 6 फ 7 ब 8 भ 9 म A य B र C ल D व E श F ष G स H ह I क्ष J त्र K ज्ञ'; position: fixed; top: -10%; left: -10%; width: 120%; height: 120%; font-size: 42px; font-weight: 600; word-spacing: 80px; line-height: 130px; text-align: justify; color: {theme_text}; opacity: 0.04; pointer-events: none; z-index: 0; overflow: hidden; display: block; animation: floatLetters 35s linear infinite; }}
    .block-container {{ position: relative; z-index: 10; padding-top: 150px !important; padding-bottom: 100px !important; max-width: 800px; }}
    .true-fixed-header {{ position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; background: {theme_card} !important; z-index: 999999 !important; border-bottom: 1px solid {theme_border} !important; border-top: 5px solid #0072CE !important; padding: 10px 10% 15px 10% !important; box-shadow: 0 4px 15px rgba(0,0,0,0.03) !important; }}
    /* --- CHAT BUBBLE LAYOUT & ALIGNMENT --- */
    .chat-row {{ display: flex; margin-bottom: 20px; width: 100%; }}
    .row-bot {{ justify-content: flex-start; }}
    .row-user {{ justify-content: flex-end; }}
    
    .bubble {{ max-width: 80%; padding: 12px 18px; border-radius: 15px; font-size: 1rem; line-height: 1.5; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
    
    /* Bot Bubble (Left side, flat bottom-left corner) */
    .bubble-bot {{ background-color: {theme_bot_bubble}; border: 1px solid {theme_border}; color: {theme_text}; border-bottom-left-radius: 4px; }}
    
    /* User Bubble (Right side, flat bottom-right corner) */
    .bubble-user {{ background-color: {theme_user_bubble}; border: 1px solid {theme_user_border}; color: {theme_text}; border-bottom-right-radius: 4px; }}
    div.stButton > button {{ border-radius: 25px !important; border: 1.5px solid #0072CE !important; background-color: transparent !important; width: 100% !important; transition: all 0.3s ease !important; }}
    div.stButton > button p {{ color: #0072CE !important; font-weight: 600 !important; }}
    div.stButton > button:hover {{ background-color: #0072CE !important; transform: translateY(-2px) !important; }}
    div.stButton > button:hover p {{ color: #ffffff !important; }}
    div.stButton > button[kind="primary"] {{ background-color: #0072CE !important; border: none !important; }}
    div.stButton > button[kind="primary"] p {{ color: #ffffff !important; }}
    .stSelectbox div[data-baseweb="select"] {{ background-color: {theme_card} !important; border-radius: 12px !important; border-color: {theme_border} !important; }}
    
    /* Widget Labels & Dropdown Fixes */
    div[data-testid="stWidgetLabel"] p, div[data-testid="stWidgetLabel"] span, div[data-testid="stToggle"] p, div[data-testid="stSelectbox"] p, div[data-testid="stSelectbox"] label {{ color: {theme_text} !important; transition: color 0.4s ease !important; }}
    div[data-baseweb="select"] span {{ color: {theme_text} !important; }}
    ul[data-baseweb="menu"] {{ background-color: {theme_card} !important; border: 1px solid {theme_border} !important; }}
    ul[data-baseweb="menu"] li {{ color: {theme_text} !important; }}

    /* --- THE BANNER (DESKTOP) --- */
    .full-bleed-banner {{ 
        width: 100vw; height: 380px; position: relative; left: 50%; transform: translateX(-50%); overflow: hidden; 
        margin-top: -3rem; margin-bottom: -50px; background-color: transparent; 
        box-shadow: none !important; border-bottom: none !important; 
        mask-image: linear-gradient(to bottom, black 60%, transparent 100%); 
        -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%); 
    }}
    .full-bleed-banner::after {{ 
        content: ""; position: absolute; bottom: 0; left: 0; right: 0; height: 160px; 
        background: linear-gradient(to bottom, transparent 0%, {theme_fade_color} 100%); 
        z-index: 2; pointer-events: none; 
    }}
    .slider-track {{ display: flex; width: 500%; height: 100%; animation: slideLeft 24s infinite cubic-bezier(0.645, 0.045, 0.355, 1); }}
    .slider-track img {{ width: 20%; height: 100%; object-fit: cover; object-position: center 20%; filter: brightness(1.15) contrast(1.05); }}
    @keyframes slideLeft {{ 0%, 18% {{ transform: translateX(0); }} 25%, 43% {{ transform: translateX(-20%); }} 50%, 68% {{ transform: translateX(-40%); }} 75%, 93% {{ transform: translateX(-60%); }} 100% {{ transform: translateX(-80%); }} }}
    .success-card {{ background: white; padding: 40px; border-radius: 20px; text-align: center; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }}
    header {{visibility: hidden;}}

    /* --- LOGO SIZING --- */
    .banner-logo {{ height: 130px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.4)); transition: all 0.3s ease; }}

    /* --- MOBILE RESPONSIVENESS RULES (The Phone Fix) --- */
    @media screen and (max-width: 768px) {{
        .full-bleed-banner {{ height: 50vw !important; min-height: 200px !important; margin-bottom: -20px !important; }}
        .full-bleed-banner::after {{ height: 70px !important; }}
        .banner-logo {{ height: 45px !important; margin-top: -5px !important; }}
        .slider-track img {{ object-position: center 10% !important; }}
        .block-container {{ padding-top: 80px !important; }}
    }}
    
    /* --- HIDE ALL STREAMLIT BRANDING & CLOUD BADGES --- */
    #MainMenu {{ visibility: hidden !important; }}
    header {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}
    .stDeployButton {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    
    /* The Ultimate Streamlit Ribbon Nuke */
    div[class*="viewerBadge"] {{ 
        display: none !important; 
        opacity: 0 !important; 
        visibility: hidden !important; 
        pointer-events: none !important; 
        z-index: -9999 !important; 
    }}
    
    </style>
""", unsafe_allow_html=True)

# --- THE BADGE NUKE (Actively destroys the Streamlit Ribbon) ---
components.html("""
    <script>
        function destroyBadges() {
            // Target the parent window where Streamlit lives
            const doc = window.parent.document;
            
            // Hunt down the specific elements by class or text
            const badges = doc.querySelectorAll('[class*="viewerBadge"], [class*="stDeployButton"]');
            badges.forEach(badge => badge.remove());
            
            // Streamlit sometimes hides the ribbon in an iframe at the bottom
            const iframes = doc.querySelectorAll('iframe');
            iframes.forEach(iframe => {
                if (iframe.title === "streamlit_app" || (iframe.src && iframe.src.includes('badge'))) {
                    // Do not delete our own components, only the badge iframe
                    if(iframe.style.height === "0px") return; 
                    iframe.style.display = 'none';
                }
            });
        }
        
        // Run immediately, and then keep checking every 1 second
        destroyBadges();
        setInterval(destroyBadges, 1000);
    </script>
""", height=0)

# --- 2. JAVASCRIPT SCROLL & LEAF ANIMATION ---
def trigger_leaf():
    components.html("""
        <style>
            @keyframes leafFloat {
                0% { transform: translateX(-50px) translateY(0) rotate(0deg); opacity: 0; }
                10% { opacity: 0.8; }
                90% { opacity: 0.8; }
                100% { transform: translateX(100vw) translateY(50px) rotate(45deg); opacity: 0; }
            }
            .leaf-trigger {
                position: fixed; top: 30%; left: 0; width: 35px; height: 35px;
                fill: #8CC63F; opacity: 0; z-index: 9999; pointer-events: none;
                animation: leafFloat 2.5s ease-in-out forwards;
            }
        </style>
        <svg class="leaf-trigger" viewBox="0 0 24 24"><path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8.12,20C11,20 14.27,15.5 17,12C18,12 20,12 22,10C22,7 19,5 17,5C15,5 12,7 12,8C12,8 12,8 17,8Z"/></svg>
    """, height=0)

def scroll_to_top():
    components.html("""<script>setTimeout(function() { window.parent.scrollTo({top: 0, behavior: 'smooth'}); const mainView = window.parent.document.querySelector('.main'); if (mainView) { mainView.scrollTo({top: 0, behavior: 'smooth'}); } }, 100);</script>""", height=0)

# --- 3. GOOGLE SHEETS SAVING LOGIC ---
def save_to_google_sheets(rm_data, chat_history):
    import time
    from datetime import datetime
    
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    submission_id = f"REQ-{int(time.time())}"

    # FIX: Add Q1, Q2, Q3 Serial Numbers to the Google Sheet output
    user_answers = []
    q_idx = 1
    for msg in chat_history:
        if msg["role"] == "user":
            user_answers.append(f"Q{q_idx}. {msg['content']}")
            q_idx += 1

    data_row = [
        submission_id, date_str, time_str,
        rm_data.get("State", ""), rm_data.get("District", ""),
        rm_data.get("Block", ""), rm_data.get("Cluster", ""),
        rm_data.get("GP_NP", ""), rm_data.get("Gram_Panchayat", ""),
        rm_data.get("School_Type", ""), rm_data.get("School_Name", ""),
        rm_data.get("UDISE", ""), rm_data.get("Observer", "")
    ] + user_answers

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        # PASTE YOUR ACTUAL SHEET ID BETWEEN THE QUOTES BELOW
        sheet = client.open_by_key("Y1pKoScZ4MjIe_m-UNAUQAgq7VSgn4nRJQEXfLfOEC61w").sheet1
        sheet.append_row(data_row)
        return True
        
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return False

# --- 4. DATA LOADER (WITH CUSTOM UI SPINNER) ---
# show_spinner=False removes the ugly Streamlit code block
@st.cache_data(show_spinner=False)
def load_rm_data():
    file_name = "Process Tracker-2026-27.xlsx - RM.csv"
    try:
        xl = pd.ExcelFile(file_name, engine='openpyxl')
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)
            df.columns = [str(col).strip().replace('\ufeff', '') for col in df.columns]
            if 'State' in df.columns: return df
    except Exception: pass 
    return pd.DataFrame() 

# --- 5. STATE MANAGEMENT & CUSTOM LOADER ---
if 'current_page' not in st.session_state: st.session_state.current_page = 'RM_PAGE'; scroll_to_top() 
if 'rm_data' not in st.session_state: st.session_state.rm_data = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'current_q_index' not in st.session_state: st.session_state.current_q_index = 0
if 'form_completed' not in st.session_state: st.session_state.form_completed = False
if 'trigger_scroll' not in st.session_state: st.session_state.trigger_scroll = False
if 'trigger_leaf' not in st.session_state: st.session_state.trigger_leaf = False

# The Professional Animated Loader
if 'data_loaded' not in st.session_state:
    loader_placeholder = st.empty()
    loader_placeholder.markdown(f"""
        <div style='text-align: center; padding-top: 25vh;'>
            <img src='data:image/png;base64,{logo_b64}' style='height: 80px; margin-bottom: 25px; animation: pulse 2s infinite;'>
            <h4 style='color: #0072CE; font-weight: 500;'>Initializing Secure Portal...</h4>
            <div style='width: 250px; height: 4px; background: {theme_border}; margin: 0 auto; border-radius: 4px; overflow: hidden;'>
                <div style='width: 50%; height: 100%; background: #0072CE; animation: slide 1.5s infinite linear;'></div>
            </div>
        </div>
        <style>
            @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.05); opacity: 1; }} 100% {{ transform: scale(1); opacity: 0.8; }} }}
            @keyframes slide {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(200%); }} }}
        </style>
    """, unsafe_allow_html=True)
    
    df_rm = load_rm_data()
    time.sleep(1.5) # Let the user see the premium loading animation briefly
    loader_placeholder.empty() # Remove the loader
    st.session_state.data_loaded = True
else:
    df_rm = load_rm_data()

if st.session_state.trigger_scroll:
    scroll_to_top()
    st.session_state.trigger_scroll = False
    
    # 1. REMOVE ALL STREAMLIT PADDING (Pushes banner to the absolute roof)
    st.markdown("<style>.block-container { padding-top: 0rem !important; }</style>", unsafe_allow_html=True)
    
   # 2. FULL-BLEED SLIDING BANNER (With Base64 Injection for Cloud)
    html_banner = f"""
    <div class="full-bleed-banner">
        <div class="slider-track">
            <img src="data:image/jpeg;base64,{bg1_b64}">
            <img src="data:image/jpeg;base64,{bg2_b64}">
            <img src="data:image/jpeg;base64,{bg3_b64}">
            <img src="data:image/jpeg;base64,{bg4_b64}">
            <img src="data:image/jpeg;base64,{bg1_b64}">
        </div>
        <div style="position: absolute; top:0; left:0; right:0; height: 140px; background: linear-gradient(to bottom, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 100%); z-index: 5;"></div>
        <div style="position: absolute; top: 15px; left: 5%; z-index: 10;">
            <img class="banner-logo" src="data:image/png;base64,{logo_b64}">
        </div>
    </div>"""
    st.markdown(html_banner, unsafe_allow_html=True)

    # 3. HEADER TOOLS (Moved below the banner for a true website layout)
    colA, colB = st.columns([0.8, 0.2])
    with colB:
        st.toggle("Dark Theme", key="dark_mode")


    with st.container(border=True):
        if not df_rm.empty:
            df_filtered = df_rm.copy()
            
            # --- ROW 1 ---
            col1, col2 = st.columns(2)
            with col1:
                s_state = st.selectbox("1. State", [""] + df_filtered['State'].dropna().unique().tolist())
                if s_state: df_filtered = df_filtered[df_filtered['State'] == s_state]
            with col2:
                s_dist = st.selectbox("2. District", [""] + df_filtered['District'].dropna().unique().tolist() if s_state else [])
                if s_dist: df_filtered = df_filtered[df_filtered['District'] == s_dist]
                
            # --- ROW 2 ---
            col3, col4 = st.columns(2)
            with col3:
                s_block = st.selectbox("3. Block", [""] + df_filtered['Block'].dropna().unique().tolist() if s_dist else [])
                if s_block: df_filtered = df_filtered[df_filtered['Block'] == s_block]
            with col4:
                s_cluster = st.selectbox("4. Cluster", [""] + df_filtered['Cluster'].dropna().unique().tolist() if s_block else [])
                if s_cluster: df_filtered = df_filtered[df_filtered['Cluster'] == s_cluster]
                
            # --- ROW 3 ---
            col5, col6 = st.columns(2)
            with col5:
                s_gp_np = st.selectbox("5. GP/NP", [""] + df_filtered['GP/NP'].dropna().unique().tolist() if s_cluster else [])
                if s_gp_np: df_filtered = df_filtered[df_filtered['GP/NP'] == s_gp_np]
            with col6:
                s_gram_panchayat = st.selectbox("6. Gram Panchayat", [""] + df_filtered['Gram Panchayat'].dropna().unique().tolist() if s_gp_np else [])
                if s_gram_panchayat: df_filtered = df_filtered[df_filtered['Gram Panchayat'] == s_gram_panchayat]

            # --- ROW 4 ---
            col7, col8 = st.columns(2)
            with col7:
                s_school_type = st.selectbox("7. School Type", [""] + df_filtered['School Type'].dropna().unique().tolist() if s_gram_panchayat else [])
                if s_school_type: df_filtered = df_filtered[df_filtered['School Type'] == s_school_type]
            with col8:
                s_school_name = st.selectbox("8. School Name", [""] + df_filtered['School Name'].dropna().unique().tolist() if s_school_type else [])
                if s_school_name: df_filtered = df_filtered[df_filtered['School Name'] == s_school_name]

            # --- ROW 5 ---
            col9, col10 = st.columns(2)
            with col9:
                s_udise = st.selectbox("9. UDISE Code", [""] + df_filtered['UDISE Code'].dropna().unique().tolist() if s_school_name else [])
                if s_udise: df_filtered = df_filtered[df_filtered['UDISE Code'] == s_udise]
            with col10:
                s_teacher = st.selectbox("10. Teachers' Name", [""] + df_filtered["Teachers' Name"].dropna().unique().tolist() if s_udise else [])

            st.write("---")
            if st.button("Start Assessment", type="primary"):
                if s_state and s_teacher:
                    st.session_state.rm_data = {
                        "State": s_state, "District": s_dist, "Block": s_block,
                        "Cluster": s_cluster, "GP_NP": s_gp_np, "Gram_Panchayat": s_gram_panchayat,
                        "School_Type": s_school_type, "School_Name": s_school_name,
                        "UDISE": s_udise, "Observer": s_teacher
                    }
                    
                    # FIX: Restored the proper starting message for Question 1
                    initial_msg = f"Welcome, {s_teacher}. Let's begin the tracking for {s_school_name}.<br><br><b>Q1. {questions_list[0]['text']}</b>"
                    
                    st.session_state.chat_history = [{"role": "assistant", "content": initial_msg}]
                    st.session_state.current_page = 'CHAT_PAGE'
                    st.session_state.trigger_scroll = True 
                    st.rerun()
                else:
                    st.error("Please complete the location hierarchy to proceed.")
        else:
            st.warning("Awaiting Data. Please ensure the Excel/CSV file is in the folder.")

# --- 7. PAGE 2: CHAT INTERFACE ---
elif st.session_state.current_page == 'CHAT_PAGE':
    
    total_q = len(questions_list)

    # --- ENTERPRISE SAFETY NET (Prevents Accidental Refresh/Close) ---
    if not st.session_state.form_completed:
        components.html("""
            <script>
                const parentWindow = window.parent;
                parentWindow.addEventListener('beforeunload', function (e) {
                    e.preventDefault();
                    e.returnValue = ''; 
                });
            </script>
        """, height=0)
    
    # 1. CREATE EMPTY PLACEHOLDER FOR HEADER (Anti-Flicker Fix)
    header_placeholder = st.empty()

    # --- CHAT PAGE DARK MODE TOGGLE ---
    colA, colB = st.columns([0.8, 0.2])
    with colB:
        st.toggle("Dark Theme", key="dark_mode")
    # ---------------------------------------

    if st.session_state.trigger_leaf:
        trigger_leaf()
        st.session_state.trigger_leaf = False

   # 2. SUCCESS PAGE UI (Hides Chat)
    if st.session_state.form_completed:
        st.markdown(f"""
            <div class="success-card">
               <img src="data:image/png;base64,{logo_b64}" style="height: 60px; margin-bottom: 20px;">
               
                <h2 style="color: #0072CE;">Your response has been recorded.</h2>
                <p style="color: #5f6368;">Thank you for completing the assessment.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Submit another response", type="primary"):
            st.session_state.clear()
            st.rerun()

    # 3. ACTIVE CHAT UI
    else:
        for msg in st.session_state.chat_history:
            role_class = "row-bot" if msg["role"] == "assistant" else "row-user"
            bubble_class = "bubble-bot" if msg["role"] == "assistant" else "bubble-user"
            st.markdown(f'<div class="chat-row {role_class}"><div class="bubble {bubble_class}">{msg["content"]}</div></div>', unsafe_allow_html=True)

        if st.session_state.get('is_typing', False):
            st.markdown('<div class="chat-row row-bot"><div class="bubble bubble-bot"><i>loading...</i></div></div>', unsafe_allow_html=True)
            time.sleep(0.5)
            st.session_state.is_typing = False
            st.rerun()

        if not st.session_state.get('is_typing', False):
            
            # --- 1. SAFETY NET: Check if we are out of questions ---
            if st.session_state.current_q_index < total_q:
                current_q = questions_list[st.session_state.current_q_index]
                
                # --- PROGRESSION LOGIC ---
                def process_answer(ans_val):
                    st.session_state.chat_history.append({"role": "user", "content": str(ans_val)})
                    st.session_state.current_q_index += 1
                    st.session_state.trigger_leaf = True
                    st.session_state.is_typing = True
                    
                    if st.session_state.current_q_index < total_q:
                        q_num = st.session_state.current_q_index + 1
                        formatted_question = f"<b>Q{q_num}.</b> {questions_list[st.session_state.current_q_index]['text']}"
                        st.session_state.chat_history.append({"role": "assistant", "content": formatted_question})
                    else: 
                        save_success = save_to_google_sheets(st.session_state.rm_data, st.session_state.chat_history)
                        if save_success:
                            st.session_state.form_completed = True
                    st.rerun()

                # --- RENDER INPUTS ---
                if current_q["type"] == "dropdown":
                    options = current_q["options"]
                    if len(options) <= 5:
                        st.write("---")
                        cols = st.columns(2)
                        for i, opt in enumerate(options):
                            with cols[i % 2]:
                                if st.button(str(opt), key=f"btn_{st.session_state.current_q_index}_{i}"):
                                    process_answer(opt)
                    else:
                        st.write("---")
                        selected_opt = st.selectbox("Select an option:", [""] + options, key=f"sel_{st.session_state.current_q_index}")
                        if selected_opt != "":
                            if st.button("Submit Answer", type="primary"):
                                process_answer(selected_opt)

                elif current_q["type"] in ["text", "numeric"]:
                    ans = st.chat_input("Type your response here...")
                    if ans: process_answer(ans)

                elif current_q["type"] == "date":
                    with st.container(border=True):
                        selected_date = st.date_input("Select a Date:")
                        if st.button("Submit Date", type="primary"):
                            process_answer(selected_date)
            
            # --- 2. FALLBACK: If saving failed, show a retry button instead of crashing ---
            else:
                st.error("⚠️ Database Connection Error. Your response could not be saved to Google Sheets.")
                st.info("Check if your Google Sheet ID and GCP Service Account credentials are correct in Streamlit Secrets.")
                if st.button("Retry Saving", type="primary"):
                    save_success = save_to_google_sheets(st.session_state.rm_data, st.session_state.chat_history)
                    if save_success:
                        st.session_state.form_completed = True
                        st.rerun()

    # 4. DRAW HEADER IN PLACEHOLDER (Ensures no flicker)
    if not st.session_state.form_completed:
        progress_val = st.session_state.current_q_index / total_q
        progress_pct = int(progress_val * 100)
        q_num = st.session_state.current_q_index + 1
        
        with header_placeholder:
            st.markdown(f"""
                <div class="true-fixed-header">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                        <img src="data:image/png;base64,{logo_b64}" alt="IEC Logo" style="height: 55px; object-fit: contain; transform: scale(1.6); transform-origin: left center;">
                        <div style="text-align: right; font-size: 0.85rem; color: {theme_muted}; line-height: 1.2;">
                            <b>Observer:</b> {st.session_state.rm_data.get('Observer', 'Unknown')}<br>
                            <b>School:</b> {st.session_state.rm_data.get('School_Name', 'Unknown')}
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #0072CE; font-weight: 600; margin-bottom: 4px;">
                        <span>Question {min(q_num, total_q)} of {total_q}</span>
                        <span>{progress_pct}%</span>
                    </div>
                    <div style="width: 100%; background-color: {theme_border}; border-radius: 10px; height: 8px;">
                        <div style="width: {progress_pct}%; background-color: #0072CE; height: 8px; border-radius: 10px; transition: width 0.4s ease;"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
