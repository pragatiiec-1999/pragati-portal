import gspread
from oauth2client.service_account import ServiceAccountCredentials
from modules.chatbot_logic import questions_list

def setup_google_sheet():
    # 1. Connection Setup
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
        client = gspread.authorize(creds)
        
        # 2. Open the sheet
        sheet = client.open("IEC Process Tracker 2026").sheet1
        
        # 3. Define the Metadata Headers (15 Columns)
        metadata_headers = [
            "Submission ID", "Date", "Time", 
            "State", "District", "Block", "Cluster", 
            "GP/NP", "Gram Panchayat", "School Type", 
            "School Name", "UDISE Code", "Observer Name",
            "Role", "Post"
        ]
        
        # 4. Extract Question Text (This will now pull exactly 56 questions)
        question_headers = [f"Q{i+1}: {q['text']}" for i, q in enumerate(questions_list)]
        
        # 5. Combine them (Total 71 Columns)
        full_headers = metadata_headers + question_headers
        
        # 6. Wipe and insert
        sheet.insert_row(full_headers, 1)
        
        print(f"✅ Success! Headers created for {len(questions_list)} Questions.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_google_sheet()