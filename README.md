# Lead Scraping Automation

This project automates the process of scraping leads from the web, validating them, and uploading them to a Google Sheet.

## Prerequisites

1.  **Python Environment**:
    -   Ensure you have the virtual environment set up: `python3 -m venv venv`
    -   Install dependencies: `./venv/bin/pip install -r requirements.txt` (or manually: `gspread oauth2client requests`)

2.  **Environment Variables**:
    -   Create a `.env` file in this directory.
    -   `FIRECRAWL_API_KEY`: Your FireCrawl API key.
    -   `GOOGLE_SHEETS_CREDENTIALS`: Path to your Service Account JSON file.

3.  **Google Sheet Access**:
    -   Ensure your Google Sheet is shared with the service account email found in your JSON credentials file.

## Usage

Run the automated workflow using the `run_workflow.py` script.

### Command Structure
```bash
./venv/bin/python execution/run_workflow.py \
  --query "SEARCH_TERM" \
  --location "LOCATION" \
  --sheet_id "YOUR_GOOGLE_SHEET_ID_OR_URL" \
  --limit 5
```

### Examples

**Search for Real Estate Agencies in Miami:**
```bash
cd /home/simbahmso/Example-Workspace
./venv/bin/python execution/run_workflow.py --query "Your Search Term" --location "City, State" --sheet_id <YOUR_SHEET_ID>
```

**Search for Plumbers in Chicago (limit 10):**
```bash
cd /home/simbahmso/Example-Workspace
./venv/bin/python execution/run_workflow.py --query "Plumbers" --location "Chicago" --limit 10 --sheet_id 15AUTU4tPmaoOulXgqU4mztXiavifZfUecZ7ME7tlih8
```

**Search for Dentists in Edmonton, Alberta:**
```bash
cd /home/simbahmso/Example-Workspace
./venv/bin/python execution/run_workflow.py --query "Dentists" --location "Edmonton, Alberta" --sheet_id 15AUTU4tPmaoOulXgqU4mztXiavifZfUecZ7ME7tlih8
```

## Troubleshooting

-   **Permission Denied**: Check that the Google Sheet is shared with the specific service account email address.
-   **Validation Failed**: Try setting a broader `--industry` string or checking manually if the descriptions are vague.
