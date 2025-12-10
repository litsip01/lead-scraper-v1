import os
import json
import argparse
import requests
import re

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

def extract_emails_from_text(text):
    """Extract email addresses from text using regex."""
    if not text:
        return []
    # Common email regex pattern
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, text)
    # Filter out common false positives
    filtered = [e for e in emails if not e.endswith('.png') and not e.endswith('.jpg') and not e.endswith('.gif')]
    return list(set(filtered))  # Remove duplicates

def scrape_page_for_email(url, api_key):
    """Scrape a single page and extract emails from it. Tries multiple pages."""
    scrape_url = "https://api.firecrawl.dev/v1/scrape"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Try multiple pages that commonly have emails
    base = url.rstrip('/')
    urls_to_try = [
        url,
        base + '/contact',
        base + '/contact-us',
        base + '/about',
        base + '/about-us',
        base + '/team',
        base + '/staff',
    ]
    
    for try_url in urls_to_try:
        payload = {
            "url": try_url,
            "formats": ["markdown"]
        }
        
        try:
            response = requests.post(scrape_url, json=payload, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                markdown = data.get("data", {}).get("markdown", "")
                emails = extract_emails_from_text(markdown)
                if emails:
                    return emails[0]
        except Exception:
            continue
    
    return ""


def scrape_leads_firecrawl(query, location, limit=5, require_email=True):
    """
    Scrape leads using FireCrawl Search API, then extract emails from each page.
    If require_email is True, only returns leads with valid emails.
    Will fetch more results progressively until limit leads with emails are found.
    """
    load_env()
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not found in environment variables.")

    full_query = f"{query} near {location}"
    
    url = "https://api.firecrawl.dev/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    leads_with_email = []
    seen_urls = set()
    search_limit = limit * 3  # Fetch more to compensate for filtering
    max_attempts = 3
    
    for attempt in range(max_attempts):
        print(f"Searching via FireCrawl for: '{full_query}' (Attempt {attempt+1}, fetching {search_limit})...")
        
        payload = {
            "query": full_query,
            "limit": search_limit,
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            print(f"Error calling FireCrawl: {response.text}")
            response.raise_for_status()
            
        data = response.json()
        results = data.get("data", [])
        
        print(f"Processing {len(results)} results...")
        for i, item in enumerate(results):
            page_url = item.get("url", "")
            
            # Skip duplicates
            if page_url in seen_urls:
                continue
            seen_urls.add(page_url)
            
            print(f"  [{len(leads_with_email)+1}/{limit}] Scraping {page_url[:50]}...")
            email = scrape_page_for_email(page_url, api_key) if page_url else ""
            
            if require_email and not email:
                print(f"    -> No email found, skipping.")
                continue
                
            leads_with_email.append({
                "name": item.get("title", "Unknown"),
                "industry": item.get("description", ""), 
                "location": location,
                "url": page_url,
                "email": email,
                "source": "FireCrawl"
            })
            
            # Stop if we have enough
            if len(leads_with_email) >= limit:
                print(f"Found {limit} leads with emails!")
                return leads_with_email
        
        # If we haven't found enough, increase search limit for next attempt
        search_limit = search_limit * 2
        print(f"Only found {len(leads_with_email)} leads with emails so far...")
    
    print(f"Finished with {len(leads_with_email)} leads (target was {limit}).")
    return leads_with_email



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--location", required=True)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--output", default="leads.json")
    args = parser.parse_args()

    try:
        leads = scrape_leads_firecrawl(args.query, args.location, args.limit)
        
        with open(args.output, "w") as f:
            json.dump(leads, f, indent=2)
        
        print(f"Saved {len(leads)} leads to {args.output}")
    except Exception as e:
        print(f"Error: {e}")
