import json
import argparse

def validate_leads(file_path, target_industry):
    """
    Validates leads by checking if the industry matches the target.
    Returns the percentage of valid leads.
    """
    with open(file_path, "r") as f:
        leads = json.load(f)
    
    if not leads:
        return 0.0

    valid_count = 0
    for lead in leads:
        # Simple string matching for now. 
        # In a real scenario, could use fuzzy matching or LLM classification.
        if target_industry.lower() in lead.get("industry", "").lower():
            valid_count += 1
            
    ratio = valid_count / len(leads)
    return ratio

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--industry", required=True)
    args = parser.parse_args()

    ratio = validate_leads(args.file, args.industry)
    print(f"Validation Ratio: {ratio:.2f}")
    
    # Output for shell scripts to capture
    if ratio >= 0.8:
        print("STATUS: PASS")
    else:
        print("STATUS: FAIL")
