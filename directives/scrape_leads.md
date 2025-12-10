# Scrape Leads Directive

**Goal:** Scrape leads from a specific industry, validate quality, and save to Google Sheets.

**Inputs:**
- `industry`: Target industry (e.g., "Software Companies")
- `location`: Target location (e.g., "San Francisco, CA")
- `sheet_id`: Google Sheet ID to save results

**Tools:**
- `execution/scrape_leads.py`: Scrapes leads using FireCrawl.
- `execution/validate_leads.py`: Checks if leads match the industry.
- `execution/update_sheet.py`: Adds data to Google Sheet.

**Process:**

1.  **Test Run:**
    - Run `execution/scrape_leads.py` with `limit=3` (FireCrawl search).
    - Output: `leads_temp.json`.

2.  **Validation:**
    - Run `execution/validate_leads.py` on `leads_temp.json` with `industry`.
    - Check output ratio.
    - **Logic:**
        - If match_rate >= 0.8: Proceed to Full Run.
        - If match_rate < 0.8: Stop and notify user to adjust filters (or implement auto-retry with different keywords).

3.  **Full Run (if validated):**
    - Run `execution/scrape_leads.py` with full limit (default or specified).
    - Output: `leads_final.json`.

4.  **Save:**
    - Run `execution/update_sheet.py` with `leads_final.json` and `sheet_id`.
