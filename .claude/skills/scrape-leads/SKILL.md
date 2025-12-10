---
name: scrape-leads
description: Scrape business leads for a given industry and location using FireCrawl. Use when the user asks to find leads, scrape businesses, or search for companies.
---

# Scrape Leads

## Instructions

1. **Ask for required inputs** before running:
   - **Industry/Profession**: What type of business? (e.g., "Dentists", "Plumbers", "Real Estate Agents")
   - **Location**: What city/region? (e.g., "Edmonton, Alberta", "Toronto, Ontario")
   - **Limit** (optional): How many leads? (default: 5)

2. **Reference the directive** at `directives/scrape_leads.md` for detailed process logic.

3. **Run the workflow script**:
   ```bash
   ./venv/bin/python execution/run_workflow.py --query "<INDUSTRY>" --location "<LOCATION>" --limit <LIMIT> --sheet_id 15AUTU4tPmaoOulXgqU4mztXiavifZfUecZ7ME7tlih8
   ```

4. **Report results** to user:
   - Number of leads scraped
   - Validation ratio
   - Confirmation of upload to Google Sheet

## Examples

**User**: "Scrape leads for me"
**Claude**: "Sure! I can help you scrape leads. What industry or profession are you targeting, and what location?"

**User**: "Find plumbers in Calgary"
**Claude**: Runs the workflow with `--query "Plumbers" --location "Calgary, Alberta"`
