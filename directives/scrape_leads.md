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

**Email Requirement:**
- **Only include leads with valid email addresses.**
- If a lead has no email, skip it and continue searching.
- Continue scraping until the target number of leads WITH emails is reached.
- Default target: 5 leads with emails.

**Process:**

1.  **Scrape with Email Filter:**
    - Run `execution/scrape_leads.py` with `--require-email` flag.
    - Script will fetch more results and filter to only those with emails.
    - Output: `leads_temp.json` (only contains leads with emails).

2.  **Validation:**
    - Run `execution/validate_leads.py` on `leads_temp.json` with `industry`.
    - Check output ratio.

3.  **Save:**
    - Run `execution/update_sheet.py` with `leads_temp.json` and `sheet_id`.
