import os
from supabase import create_client

def keep_supabase_awake():
    # These will be pulled from your GitHub Secrets
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        print("Missing Environment Variables.")
        return

    supabase = create_client(url, key)
    
    try:
        # Pinging your specific table
        supabase.table("process_submissions_2026").select("id").limit(1).execute()
        print("Successfully sent heartbeat to Supabase.")
    except Exception as e:
        print(f"Heartbeat failed: {e}")

if __name__ == "__main__":
    keep_supabase_awake()