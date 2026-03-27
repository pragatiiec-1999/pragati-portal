import pandas as pd
import json

# 1. Point directly to your Excel file
excel_file = "Process Tracker-2026-27 (1).xlsx"

print(f"Reading from {excel_file}...")

try:
    # Read both tabs
    form_df = pd.read_excel(excel_file, sheet_name="Form")
    process_df = pd.read_excel(excel_file, sheet_name="Process", header=None)
except Exception as e:
    print(f"Error reading the Excel file: {e}")
    print("Ensure the file is closed and the tab names are exactly 'Form' and 'Process'.")
    exit()

def clean_nan(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

# 2. Extract Form Questions (Teacher's Collective & Classroom Observation)
questions_list = []
for index, row in form_df.iterrows():
    options = []
    raw_options = row.get('Options', '')
    if pd.notna(raw_options):
        options = [opt.strip() for opt in str(raw_options).replace(';', ',').split(',') if opt.strip()]
    
    questions_list.append({
        "id": f"Q{index+1}",
        "text": clean_nan(row.get('Question Text', '')),
        "type": clean_nan(row.get('Question Type', 'dropdown')),
        "category": clean_nan(row.get('Form Type', '')),
        "options": options
    })

# 3. Extract Process Indicators (Checkbox Data)
# Only allowing these specific blocks. "LN_Support" and "Other" are automatically ignored!
valid_form_types = ['GP', 'BPM', 'DIET', 'BESC']
indicator_list = []

for index, row in process_df.iterrows():
    form_type = clean_nan(row[3]) # Column index 3 contains the Form Type in your Process sheet
    
    if form_type in valid_form_types:
        indicator_list.append({
            "id": f"{form_type}_{index}", # Unique ID like GP_10, DIET_75
            "text": clean_nan(row[1]),    # Column index 1 contains the Indicator text
            "category": form_type
        })

# 4. Generate the chatbot_logic.py file
print("Writing data to chatbot_logic.py...")
with open("chatbot_logic.py", "w", encoding="utf-8") as f:
    f.write('"""\nAUTO-GENERATED FILE\nContains standard questions and checkbox indicators.\n"""\n\n')
    
    f.write("# --- PART 1: FORM FIELD QUESTIONS (Q1-Q56) ---\n")
    f.write("questions_list = " + json.dumps(questions_list, indent=4, ensure_ascii=False) + "\n\n")
    
    f.write("# --- PART 2: PROCESS FIELD INDICATORS (Checkboxes) ---\n")
    f.write("indicator_list = " + json.dumps(indicator_list, indent=4, ensure_ascii=False) + "\n\n")
    
    f.write("# --- PART 3: HELPER FUNCTIONS ---\n")
    f.write("def get_form_questions(selected_category):\n")
    f.write("    return [q for q in questions_list if q.get('category') == selected_category]\n\n")
    
    f.write("def get_process_indicators(selected_category):\n")
    f.write("    return [ind for ind in indicator_list if ind.get('category') == selected_category]\n")

print("✅ Success! chatbot_logic.py has been generated.")