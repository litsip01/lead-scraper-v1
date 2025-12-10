import argparse
import sys
import os
import json

# Add current directory to path so we can import siblings
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrape_leads import scrape_leads_firecrawl
from validate_leads import validate_leads
from update_sheet import update_sheet

def main():
    parser = argparse.ArgumentParser(description="End-to-end Lead Scraping Workflow")
    parser.add_argument("--query", required=True, help="Search term (e.g., 'Plumbers')")
    parser.add_argument("--location", required=True, help="Location (e.g., 'Chicago')")
    parser.add_argument("--limit", type=int, default=5, help="Number of leads to fetch")
    parser.add_argument("--sheet_id", required=True, help="Google Sheet ID or Name")
    parser.add_argument("--industry", help="Target industry for validation (defaults to query)")
    
    args = parser.parse_args()
    
    # Define temp file path
    temp_file = os.path.join(os.getcwd(), "leads_temp.json")

    # 1. Scrape
    print(f"--- STEP 1: Scraping '{args.query}' in '{args.location}' ---")
    try:
        leads = scrape_leads_firecrawl(args.query, args.location, args.limit)
        with open(temp_file, "w") as f:
            json.dump(leads, f, indent=2)
        print(f"Scraped {len(leads)} leads.")
    except Exception as e:
        print(f"ERROR: Scraping failed: {e}")
        sys.exit(1)

    # 2. Validate
    target_industry = args.industry if args.industry else args.query
    print(f"--- STEP 2: Validating for industry '{target_industry}' ---")
    try:
        ratio = validate_leads(temp_file, target_industry)
        print(f"Validation Ratio: {ratio:.2f}")
        if ratio == 0.0 and len(leads) > 0:
             print("WARNING: No leads passed validation? Checking manually is advised.")
    except Exception as e:
        print(f"ERROR: Validation logic failed: {e}")
        sys.exit(1)

    # 3. Upload
    print(f"--- STEP 3: Uploading to Sheet '{args.sheet_id}' ---")
    try:
        update_sheet(temp_file, args.sheet_id)
    except Exception as e:
        print(f"ERROR: Upload failed: {e}")
        sys.exit(1)
        
    print("\nWorkflow Completed Successfully!")

if __name__ == "__main__":
    main()
