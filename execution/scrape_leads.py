import os
import json
import argparse
import requests

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

def scrape_leads_firecrawl(query, location, limit=5):
    """
    Scrape leads using FireCrawl Search API.
    """
    load_env()
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY not found in environment variables.")

    full_query = f"{query} near {location}"
    print(f"Searching via FireCrawl for: '{full_query}' (Limit: {limit})...")
    
    url = "https://api.firecrawl.dev/v1/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "query": full_query,
        "limit": limit,
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        print(f"Error calling FireCrawl: {response.text}")
        response.raise_for_status()
        
    data = response.json()
    # FireCrawl search response typically has 'data' key which is a list of results
    # Each result has title, url, description, etc.
    
    results = data.get("data", [])
    
    # Normalize to leads format expected by validate/update scripts
    leads = []
    for item in results:
        leads.append({
            "name": item.get("title", "Unknown"),
            # Map description to industry for validation purposes since Search doesn't give structured 'industry' field
            "industry": item.get("description", ""), 
            "location": location, # Inferred from query
            "url": item.get("url", ""),
            "source": "FireCrawl"
        })
        
    return leads

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
