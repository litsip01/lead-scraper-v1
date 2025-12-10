import os
import json
import argparse

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_env():
    """Manually load .env file if python-dotenv is not available."""
    env_path = os.path.join(os.getcwd(), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def update_sheet(file_path, sheet_id):
    """
    Uploads leads to Google Sheet using gspread.
    """
    load_env()
    creds_path = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    
    if not creds_path:
        raise ValueError("GOOGLE_SHEETS_CREDENTIALS not found in .env (should be path to json key).")
    
    if not os.path.exists(creds_path):
        # Check if it was passed as a string content instead of path
        if creds_path.startswith('{'):
             # Handle raw JSON string if needed, but path is preferred
             pass
        else:
             raise FileNotFoundError(f"Credentials file not found at: {creds_path}")

    # Define scope
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Authenticate
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    
    # Open Sheet
    display_val = sheet_id
    try:
        # Try opening by ID first
        sheet = client.open_by_key(sheet_id).sheet1
    except gspread.SpreadsheetNotFound:
        try:
            # Fallback: Try opening by name
            sheet = client.open(sheet_id).sheet1
        except gspread.SpreadsheetNotFound:
            print(f"Debug: Available sheets: {[s.title for s in client.openall()]}")
            raise ValueError(f"Spreadsheet '{sheet_id}' not found. Check ID/Name and ensure Service Account ({creds.service_account_email}) is shared as Editor.")
    
    # Read Leads
    with open(file_path, "r") as f:
        leads = json.load(f)
        
    print(f"Uploading {len(leads)} leads...")
    
    # Prepare data for upload (headers + rows)
    if not leads:
        print("No leads to upload.")
        return

    headers = list(leads[0].keys())
    
    # Check if sheet is empty to decide on headers
    existing_data = sheet.get_all_values()
    is_empty = len(existing_data) == 0
    
    rows_to_append = []
    if is_empty:
        rows_to_append.append(headers)
        
    for lead in leads:
        rows_to_append.append([str(lead.get(h, "")) for h in headers])
        
    # Append to Sheet
    if rows_to_append:
        sheet.append_rows(rows_to_append)
        print(f"Appended {len(rows_to_append)} rows (including headers if new sheet).")
    else:
        print("No new data to append.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload leads to Google Sheet")
    parser.add_argument("--file", required=True, help="Path to the JSON file containing leads")
    parser.add_argument("--sheet_id", required=True, help="Google Sheet ID or Name")
    
    args = parser.parse_args()

    try:
        update_sheet(args.file, args.sheet_id)
    except Exception as e:
        print(f"Error: {e}")
