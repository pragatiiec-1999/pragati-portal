import pandas as pd
import json
import os

def generate_rm_config():
    excel_file = "Process Tracker-2026-27 (1).xlsx"
    output_file = "rm_config.py"
    
    if not os.path.exists(excel_file):
        print(f"Error: Could not find '{excel_file}'.")
        return

    print(f"Reading 'RM' sheet from {excel_file}...")
    
    try:
        # We read the entire sheet
        df = pd.read_excel(excel_file, sheet_name="RM")
    except Exception as e:
        print(f"Error: {e}")
        return
            
    # 1. Clean column names
    df.columns = [str(c).strip() for c in df.columns]
    
    # 2. Convert all data to string and handle empty cells
    df = df.fillna("")
    
    # 3. Create the Relational Data (List of Records)
    # This keeps State, District, School, and UDISE linked together
    rm_data = df.to_dict(orient='records')

    print(f"Writing relational data to {output_file}...")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# ==========================================\n")
        f.write("# AUTO-GENERATED RELATIONAL RM DATA\n")
        f.write("# ==========================================\n\n")
        
        # We write the full list of dictionaries
        f.write("RM_DATA = ")
        f.write(json.dumps(rm_data, indent=4, ensure_ascii=False))
        f.write("\n")

    print("Done! rm_config.py generated with linked data.")

if __name__ == "__main__":
    generate_rm_config()