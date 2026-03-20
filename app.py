import streamlit as st
import time
import streamlit.components.v1 as components
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from modules.chatbot_logic import questions_list
import base64
from PIL import Image
import os

# --- 1. ENTERPRISE UI CONFIGURATION ---
try:
    icon_path = "static/icon4.png" 
    tab_icon = Image.open(icon_path)
except Exception as e:
    tab_icon = "📄" 

st.set_page_config(
    page_title="Pragati Portal | IEC", 
    page_icon=tab_icon, 
    layout="wide" 
)

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

# --- 1.5 PROFESSIONAL DARK MODE & ANIMATED BACKGROUND ---
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if st.session_state.dark_mode:
    theme_bg_gradient = "linear-gradient(135deg, #131314 0%, #1e1f20 100%)"
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
    theme_fade_color = "#f8fafc"   
    theme_card = "#ffffff"
    theme_text = "#0f172a"
    theme_border = "#cbd5e1"
    theme_bot_bubble = "#ffffff"
    theme_user_bubble = "#e0f2fe"
    theme_user_border = "#bae6fd"
    theme_muted = "#64748b"

# ==========================================
# EXACT CSS FROM YOUR ORIGINAL CODE + PALETTE SCROLL FIX
# ==========================================
# ==========================================
# FINAL OPTIMIZED CSS - HEROICON READY
# ==========================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* ANIMATIONS */
    @keyframes gradientBG {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
    @keyframes floatLetters {{ 0% {{ transform: translateY(5vh) translateX(0px) rotate(0deg); opacity: 0; }} 10% {{ opacity: 0.04; }} 90% {{ opacity: 0.04; }} 100% {{ transform: translateY(-20vh) translateX(-20px) rotate(5deg); opacity: 0; }} }}
    
    /* CORE APP STYLING */
    .stApp {{ 
        background: {theme_bg_gradient} !important; 
        background-size: 300% 300% !important; 
        animation: gradientBG 18s ease-in-out infinite !important; 
        font-family: 'Inter', sans-serif; 
        color: {theme_text} !important; 
    }}
    
    .stApp::before {{ 
        content: 'A अ 1 B आ 2 C इ 3 D ई 4 E उ 5 F ऊ 6 G ऋ 7 H ए 8 I ऐ 9 J ओ 0 K औ L क M ख N ग O घ P ङ Q च R छ S ज T झ U ञ V ट W ठ X ड Y ढ Z ण 0 त 1 थ 2 द 3 ध 4 न 5 प 6 फ 7 ब 8 भ 9 म A य B र C ल D व E श F ष G स H ह I क्ष J त्र K ज्ञ'; 
        position: fixed; top: -10%; left: -10%; width: 120%; height: 120%; 
        font-size: 42px; font-weight: 600; word-spacing: 80px; line-height: 130px; 
        text-align: justify; color: {theme_text}; opacity: 0.04; pointer-events: none; z-index: 0; animation: floatLetters 35s linear infinite; 
    }}

    /* CONTAINER SPACING (Reduced top-padding since Header is gone) */
    .block-container {{ 
        position: relative; 
        z-index: 10; 
        padding-top: 60px !important; 
        padding-bottom: 100px !important; 
        max-width: 1200px; 
    }} 

    /* PROFESSIONAL BUTTONS */
    div.stButton > button {{ border-radius: 25px !important; border: 1.5px solid #0072CE !important; background-color: transparent !important; width: 100% !important; transition: all 0.3s ease !important; }}
    div.stButton > button p {{ color: #0072CE !important; font-weight: 600 !important; }}
    div.stButton > button:hover {{ background-color: #0072CE !important; transform: translateY(-2px) !important; }}
    div.stButton > button:hover p {{ color: #ffffff !important; }}
    div.stButton > button[kind="primary"] {{ background-color: #0072CE !important; border: none !important; }}
    div.stButton > button[kind="primary"] p {{ color: #ffffff !important; }}

    /* INPUTS & SELECTBOXES */
    .stSelectbox div[data-baseweb="select"] {{ background-color: {theme_card} !important; border-radius: 12px !important; border-color: {theme_border} !important; }}
    label p, label span, div[data-testid="stWidgetLabel"] p {{ color: {theme_text} !important; }}
    div[data-baseweb="input"] input, div[data-baseweb="base-input"] textarea {{ color: {theme_text} !important; background-color: transparent !important; }}

    /* BANNER SYSTEM */
    .full-bleed-banner {{ width: 100vw; height: 380px; position: relative; left: 50%; transform: translateX(-50%); overflow: hidden; margin-top: -3rem; margin-bottom: -50px; mask-image: linear-gradient(to bottom, black 60%, transparent 100%); -webkit-mask-image: linear-gradient(to bottom, black 60%, transparent 100%); }}
    .slider-track {{ display: flex; width: 500%; height: 100%; animation: slideLeft 24s infinite cubic-bezier(0.645, 0.045, 0.355, 1); }}
    .slider-track img {{ width: 20%; height: 100%; object-fit: cover; object-position: center 20%; }}
    @keyframes slideLeft {{ 0%, 18% {{ transform: translateX(0); }} 25%, 43% {{ transform: translateX(-20%); }} 50%, 68% {{ transform: translateX(-40%); }} 75%, 93% {{ transform: translateX(-60%); }} 100% {{ transform: translateX(-80%); }} }}
    .banner-logo {{ height: 130px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.4)); }}

    /* --- THE PALETTE GRID (JEE STYLE) --- */
    .palette-box {{
        background: {theme_card};
        padding: 15px;
        border-radius: 15px;
        border: 1px solid {theme_border};
        max-height: 75vh;
        overflow-y: auto;
    }}

    .palette-grid {{
        display: grid !important;
        grid-template-columns: repeat(5, 1fr) !important;
        gap: 10px !important;
        padding: 10px 0 !important;
    }}

    .palette-grid div[data-testid="stButton"] {{ width: 100% !important; }}
    .palette-grid button {{ height: 42px !important; padding: 0 !important; font-size: 0.9rem !important; }}

    /* POPOVER LABEL FIX (DARK & BOLD) */
    div[data-testid="stPopover"] > div:first-child p {{
        color: #000000 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
    }}
    
    div[data-baseweb="popover"] > div {{ background-color: {theme_card} !important; border: 1px solid {theme_border} !important; }}

    /* NUKE GHOST CONTAINERS & BARS */
    [data-testid="stVerticalBlock"] > div:empty {{ display: none !important; }}
    hr {{ margin: 10px 0 !important; opacity: 0.2; }}

    /* FORCE 3-COLUMN GRID ON MOBILE (BETTER READABILITY) */
    @media screen and (max-width: 768px) {{
        .palette-grid {{
            grid-template-columns: repeat(3, 1fr) !important; /* Changed from 5 to 3 for mobile */
            gap: 12px !important;
        }}

        /* NUKE THE SMALL BLANK BOX ABOVE PALETTE */
        [data-testid="column"]:empty, 
        [data-testid="stHorizontalBlock"]:empty,
        div[class*="st-key-temp_q1_sel"] + div {{
            display: none !important;
            height: 0px !important;
            margin: 0px !important;
            padding: 0px !important;
        }}
        
        /* DARK TEXT FOR POPOVER LABELS */
        div[data-testid="stPopover"] p {{
            color: #000000 !important;
            font-weight: 700 !important;
        }}
    }}

    /* Global Fix to hide any empty vertical space */
    [data-testid="stVerticalBlock"] > div:empty {{
        display: none !important;
    }}
    </style>
""", unsafe_allow_html=True)
# --- THE BADGE NUKE ---
components.html("""
    <script>
        function destroyBadges() {
            const doc = window.parent.document;
            const badges = doc.querySelectorAll('[class*="viewerBadge"], [class*="stDeployButton"]');
            badges.forEach(badge => badge.remove());
            const iframes = doc.querySelectorAll('iframe');
            iframes.forEach(iframe => {
                if (iframe.title === "streamlit_app" || (iframe.src && iframe.src.includes('badge'))) {
                    if(iframe.style.height === "0px") return; 
                    iframe.style.display = 'none';
                }
            });
        }
        destroyBadges();
        setInterval(destroyBadges, 1000);
    </script>
""", height=0)

# --- 2. JAVASCRIPT SCROLL ---
def scroll_to_top():
    components.html("""<script>setTimeout(function() { window.parent.scrollTo({top: 0, behavior: 'smooth'}); const mainView = window.parent.document.querySelector('.main'); if (mainView) { mainView.scrollTo({top: 0, behavior: 'smooth'}); } }, 100);</script>""", height=0)

# --- 3. GOOGLE SHEETS SAVING LOGIC (ZERO JITTER) ---
def save_to_google_sheets(rm_data):
    import time
    from datetime import datetime
    import gspread
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    submission_id = f"REQ-{int(time.time())}"

    data_row = [
        submission_id, date_str, time_str,
        rm_data.get("State", ""), rm_data.get("District", ""),
        rm_data.get("Block", ""), rm_data.get("Cluster", ""),
        rm_data.get("GP_NP", ""), rm_data.get("Gram_Panchayat", ""),
        rm_data.get("School_Type", ""), rm_data.get("School_Name", ""),
        rm_data.get("UDISE", ""), rm_data.get("Observer", ""),
        rm_data.get("Role", ""), rm_data.get("Post", "")
    ]
    
    for q in questions_list:
        ans = st.session_state.answers_dict.get(q['id'], None)  # Grabs from permanent memory
        if ans is None or ans == "":
            data_row.append("")
        else:
            data_row.append(str(ans))

    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = st.secrets["gcp_service_account"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key("1pKoScZ4MjIe_m-UNAUQAgq7VSgn4nRJQEXfLfOEC61w").sheet1
        sheet.append_row(data_row)
        return True
    except Exception as e:
        st.error(f"Database Connection Error: {e}")
        return False

@st.cache_data(show_spinner=False)
def load_rm_data():
    # This ensures it finds the file on your local computer
    base_path = os.path.dirname(__file__)
    file_name = os.path.join(base_path, "Process Tracker-2026-27.xlsx - RM.csv")
    
    try:
        # Restoring your working Excel-based logic
        xl = pd.ExcelFile(file_name, engine='openpyxl')
        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name)
            # Standardizing column names
            df.columns = [str(col).strip().replace('\ufeff', '') for col in df.columns]
            
            # This is the line that makes the Search box work
            if 'UDISE Code' in df.columns: 
                df['School_Display'] = df['UDISE Code'].astype(str) + " - " + df['School Name'].astype(str)
                return df
    except Exception as e:
        # Temporarily show this if it still fails so we can see why
        # st.error(f"Loader error: {e}") 
        pass 
    return pd.DataFrame()

# --- 5. STATE MANAGEMENT & CUSTOM LOADER ---
if 'current_page' not in st.session_state: st.session_state.current_page = 'RM_PAGE'; scroll_to_top() 
if 'rm_data' not in st.session_state: st.session_state.rm_data = {}
if 'active_q_idx' not in st.session_state: st.session_state.active_q_idx = 0
if 'form_completed' not in st.session_state: st.session_state.form_completed = False
if 'trigger_scroll' not in st.session_state: st.session_state.trigger_scroll = False
if 'answers_dict' not in st.session_state: st.session_state.answers_dict = {}

if 'data_loaded' not in st.session_state:
    loader_placeholder = st.empty()
    solid_bg = "#1e1f20" if st.session_state.dark_mode else "#f8fafc"
    
    loader_placeholder.markdown(f"""
        <div id="true-splash-screen">
            <div class="splash-content">
                <img src='data:image/png;base64,{logo_b64}' class="splash-logo">
                <h4 class="splash-text">Initializing Secure Portal...</h4>
                <div class="loading-track"><div class="loading-bar"></div></div>
            </div>
        </div>
        <style>
            #true-splash-screen {{ position: fixed !important; top: 0 !important; left: 0 !important; right: 0 !important; bottom: 0 !important; width: 100vw !important; height: 100vh !important; background-color: {solid_bg} !important; z-index: 9999999 !important; display: flex !important; justify-content: center !important; align-items: center !important; margin: 0 !important; padding: 0 !important; }}
            .splash-content {{ display: flex; flex-direction: column; align-items: center; transform: translateY(-5vh); }}
            .splash-logo {{ height: 160px; margin-bottom: 30px; animation: pulse 2s infinite; }}
            .splash-text {{ color: #0072CE; font-weight: 600; margin-bottom: 20px; font-size: 1.3rem; }}
            .loading-track {{ width: 300px; height: 6px; background: {theme_border}; border-radius: 10px; overflow: hidden; }}
            .loading-bar {{ width: 50%; height: 100%; background: #0072CE; animation: slide 1.5s infinite linear; }}
            @keyframes pulse {{ 0% {{ transform: scale(1); opacity: 0.8; }} 50% {{ transform: scale(1.05); opacity: 1; }} 100% {{ transform: scale(1); opacity: 0.8; }} }} 
            @keyframes slide {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(200%); }} }}
        </style>
    """, unsafe_allow_html=True)
    
    df_rm = load_rm_data()
    time.sleep(1.5) 
    loader_placeholder.empty() 
    st.session_state.data_loaded = True
else:
    df_rm = load_rm_data()

# ==========================================
# --- 6. PAGE 1: RM_PAGE (SMART SEARCH) ---
# ==========================================
if st.session_state.current_page == 'RM_PAGE':
    
    if st.session_state.trigger_scroll:
        scroll_to_top()
        st.session_state.trigger_scroll = False
        
    st.markdown("<style>.block-container { padding-top: 0rem !important; }</style>", unsafe_allow_html=True)
    
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

    # This keeps the toggle aligned to the right without creating an empty 0.8 width container above your questions
    _, toggle_col = st.columns([0.8, 0.2])
    with toggle_col:
        st.toggle("Dark Theme", key="dark_mode")

    with st.container(border=True):
        st.subheader("1. Identify School & Observer")
        if not df_rm.empty:
            
            # Removed the search_col wrapper to fix the NameError and ghost container
            selected_school_raw = st.selectbox(
                "Search by UDISE Code or School Name", 
                df_rm['School_Display'].dropna().unique().tolist(), 
                index=None, 
                placeholder="Type UDISE or School Name..."
            )
                
            if selected_school_raw:
                s_udise = selected_school_raw.split(" - ")[0].strip()
                row = df_rm[df_rm['UDISE Code'].astype(str) == s_udise].iloc[0]
                
                # Heroicon Location Alert
                st.markdown(f"""<div style='background-color: rgba(0, 114, 206, 0.1); color: #0072CE; padding: 15px; border-radius: 8px; border: 1px solid rgba(0, 114, 206, 0.2); margin-bottom: 15px; display: flex; align-items: center;'>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px; margin-right: 10px;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 10.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 10.5c0 7.142-7.5 11.25-7.5 11.25S4.5 17.642 4.5 10.5a7.5 7.5 0 1 1 15 0Z" />
                    </svg> <b>Location:&nbsp;</b> {row.get('State','')} > {row.get('District','')} > {row.get('Block','')} > {row.get('School Name','')}</div>""", unsafe_allow_html=True)
                
                teacher_list = df_rm[df_rm['UDISE Code'].astype(str) == s_udise]["Teachers' Name"].dropna().unique().tolist()
                s_teacher = st.selectbox("Select Observer Name", teacher_list, index=None, placeholder="Who is conducting the observation?")
                
                if s_teacher:
                    # Pull Role and Post
                    t_row = df_rm[(df_rm['UDISE Code'].astype(str) == s_udise) & (df_rm["Teachers' Name"] == s_teacher)].iloc[0]
                    role = t_row.get("Relevant Role", "None")
                    post = t_row.get("Post", "None")
                    
                    if pd.isna(role) or str(role).strip() == "": role = "None"
                    if pd.isna(post) or str(post).strip() == "": post = "None"
                    
                    # Heroicon Profile Alert
                    st.markdown(f"""<div style='background-color: rgba(16, 185, 129, 0.1); color: #10b981; padding: 15px; border-radius: 8px; border: 1px solid rgba(16, 185, 129, 0.2); margin-bottom: 15px; display: flex; align-items: center;'>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 20px; height: 20px; margin-right: 10px;">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0ZM4.501 20.118a7.5 7.5 0 0 1 14.998 0A17.933 17.933 0 0 1 12 21.75c-2.676 0-5.216-.584-7.499-1.632Z" />
                        </svg> <b>Profile:&nbsp;</b> Role: {role} | Post: {post}</div>""", unsafe_allow_html=True)
                    
                    st.write("---")
                    if st.button("Enter Examination Portal", type="primary"):
                        st.session_state.rm_data = {
                            "State": row.get("State",""), "District": row.get("District",""), "Block": row.get("Block",""),
                            "Cluster": row.get("Cluster",""), "GP_NP": row.get("GP/NP",""), "Gram_Panchayat": row.get("Gram Panchayat",""),
                            "School_Type": row.get("School Type",""), "School_Name": row.get("School Name",""),
                            "UDISE": s_udise, "Observer": s_teacher, "Role": role, "Post": post
                        }
                        st.session_state.current_page = 'PORTAL_PAGE'
                        st.session_state.trigger_scroll = True
                        st.rerun()
        else:
            st.warning("Awaiting Data. Please ensure the Excel/CSV file is in the folder.")

# ==========================================
# --- 7. PAGE 2: PORTAL INTERFACE (JEE) ---
# ==========================================
elif st.session_state.current_page == 'PORTAL_PAGE':

    total_q = len(questions_list)

    if not st.session_state.form_completed:
        components.html("""<script> const parentWindow = window.parent; parentWindow.addEventListener('beforeunload', function (e) { e.preventDefault(); e.returnValue = ''; }); </script>""", height=0)

    if st.session_state.trigger_scroll:
        scroll_to_top()
        st.session_state.trigger_scroll = False

    if st.session_state.form_completed:
        st.markdown(f"""
            <div class="success-card">
               <img src="data:image/png;base64,{logo_b64}" style="height: 130px; margin-bottom: 25px; filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.15));">
                <h2 style="color: #0072CE;">Your response has been recorded.</h2>
                <p style="color: {theme_muted}; font-size: 1.1rem;">Thank you for completing the assessment.</p>
            </div>
        """, unsafe_allow_html=True)
        st.write("<br>", unsafe_allow_html=True)
        if st.button("Submit another response", type="primary"):
            st.session_state.clear()
            st.rerun()

    else:
        # THE FLICKER FIX: Calculate values instantly before injecting the HTML
        answered_count = len([k for k,v in st.session_state.answers_dict.items() if v not in [None, ""]])
        progress_pct = int((answered_count / total_q) * 100) if total_q > 0 else 0

        # Inject fixed header directly (No empty placeholder delay)
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
                    <span>Question Portal ({answered_count}/{total_q} Answered)</span>
                    <span>{progress_pct}%</span>
                </div>
                <div style="width: 100%; background-color: {theme_border}; border-radius: 10px; height: 8px;">
                    <div style="width: {progress_pct}%; background-color: #0072CE; height: 8px; border-radius: 10px; transition: width 0.4s ease;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.toggle("Dark Theme", key="dark_mode")

        left_col, right_col = st.columns([0.65, 0.35])

        with right_col:
            # THE SCROLL JUMP FIX: Wrap the palette in the scrollable CSS container
            st.markdown("<div class='palette-box'>", unsafe_allow_html=True)
            
            st.markdown(f"""
    <div style='display: flex; align-items: center; margin-bottom: 10px;'>
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="#0072CE" style="width: 24px; height: 24px; margin-right: 10px;">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 0 0-3.375-3.375h-1.5A1.125 1.125 0 0 1 13.5 7.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 0 0-9-9Z" />
        </svg>
        <h3 style='margin:0; color: {theme_text};'>Question Palette</h3>
    </div>
""", unsafe_allow_html=True)
            st.caption("🟩 Answered | ⬜ Unanswered")
            
            # Function to make text bold using Unicode (Workaround for st.popover)
            def make_bold(text):
                bold_map = str.maketrans(
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789",
                    "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
                )
                return text.translate(bold_map)

            for category in ["Teacher's Collective", "Classroom Observation"]:
                cat_qs = [q for q in questions_list if q.get("category") == category]
                ans_cat = sum(1 for q in cat_qs if st.session_state.answers_dict.get(q['id']) not in [None, ""])
                
                # Using 📄 Unicode icon for the label
                clean_label = f"📄 {category} ({ans_cat}/{len(cat_qs)})"
                
                with st.popover(clean_label, use_container_width=True):
                    st.markdown("<div class='palette-grid'>", unsafe_allow_html=True)
                    
                    for q in cat_qs:
                        g_idx = questions_list.index(q)
                        is_ans = st.session_state.answers_dict.get(q['id']) not in [None, ""]
                        
                        if st.button(str(g_idx+1), key=f"pal_{g_idx}", type="primary" if is_ans else "secondary", use_container_width=True):
                            st.session_state.active_q_idx = g_idx
                            scroll_to_top()
                            st.rerun()
                            
                    st.markdown("</div>", unsafe_allow_html=True)
            st.write("")

            st.divider()
            if st.button("FINAL SUBMIT", type="primary", icon=":material/cloud_upload:"):
                success = save_to_google_sheets(st.session_state.rm_data)
                if success:
                    st.session_state.form_completed = True
                    scroll_to_top()
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with left_col:
            active_q = questions_list[st.session_state.active_q_idx]
            q_num = st.session_state.active_q_idx + 1
            
            st.markdown(f"""<h4 style='display: flex; align-items: center; color: {theme_text}; margin-bottom: 25px; border-bottom: 1px solid {theme_border}; padding-bottom: 10px;'>
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" style="width: 28px; height: 28px; margin-right: 10px; color: #0072CE;">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z" />
                </svg> {st.session_state.rm_data.get('School_Name', 'School')} Assessment</h4>""", unsafe_allow_html=True)
            
            st.markdown(f"<h5 style='color:{theme_muted};'>{active_q.get('category', 'General')}</h5>", unsafe_allow_html=True)
            
            with st.container(border=True):
                st.markdown(f"#### Q{q_num}. {active_q['text']}")
                st.write("")
                
                ans_key = f"ans_{active_q['id']}"
                saved_val = st.session_state.answers_dict.get(active_q['id'])

                # Callback function to instantly save data to permanent memory
                def update_answer(q_id):
                    st.session_state.answers_dict[q_id] = st.session_state[f"ans_{q_id}"]
                
                # MERGED Q1 LOGIC
                if active_q["id"] == "Q1":
                    opts = active_q["options"]
                    is_custom = saved_val not in opts and saved_val not in [None, ""]
                    idx = opts.index("Other") if is_custom else (opts.index(saved_val) if saved_val in opts else None)
                    
                    sel = st.selectbox("Select your name:", opts, index=idx, key="temp_q1_sel")
                    
                    if sel == "Other":
                        st.write("---")
                        custom_val = saved_val if is_custom else ""
                        st.text_input("Type your name:", value=custom_val, key=ans_key, on_change=update_answer, args=(active_q['id'],))
                    else:
                        st.session_state.answers_dict["Q1"] = sel

                elif active_q["type"] == "dropdown":
                    options = active_q["options"]
                    idx = options.index(saved_val) if saved_val in options else None
                    st.selectbox("Select an option:", options, index=idx, key=ans_key, on_change=update_answer, args=(active_q['id'],))
                        
                elif active_q["type"] == "numeric":
                    val = float(saved_val) if saved_val not in [None, ""] else None
                    st.number_input("Enter a number:", value=val, step=1.0, key=ans_key, on_change=update_answer, args=(active_q['id'],))

                elif active_q["type"] == "text":
                    val = saved_val if saved_val is not None else ""
                    st.text_area("Observations:", value=val, height=150, placeholder="Enter detailed observations here...", key=ans_key, on_change=update_answer, args=(active_q['id'],))

                elif active_q["type"] == "date":
                    val = saved_val if saved_val not in [None, ""] else None
                    st.date_input("Select a Date:", value=val, key=ans_key, on_change=update_answer, args=(active_q['id'],))

            st.write("")
            
            nav_col1, nav_col2, nav_col3 = st.columns([0.3, 0.4, 0.3])
            with nav_col1:
                if st.session_state.active_q_idx > 0:
                    if st.button("Back", icon=":material/arrow_back:"):
                        st.session_state.active_q_idx -= 1
                        scroll_to_top()
                        st.rerun()
            with nav_col3:
                if st.session_state.active_q_idx < total_q - 1:
                    if st.button("Next", type="primary", icon=":material/arrow_forward:"):
                        st.session_state.active_q_idx += 1
                        scroll_to_top()
                        st.rerun()