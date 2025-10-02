import json
import random
import string
from datetime import datetime

def generate_mpd_dataset(total_rows=100000):
    """
    Generate 100k rows of notional MPD dashboard data
    """
    data = []
    
    # Define the 4 snapshots
    snapshots = [
        {"snapshot": "Fall 2023", "date": "2023-10-31"},
        {"snapshot": "Spring 2024", "date": "2024-02-28"},
        {"snapshot": "Fall 2024", "date": "2024-10-31"},
        {"snapshot": "Spring 2025", "date": "2025-02-28"}
    ]
    
    # Define valid values for constrained fields
    nipf_priority = ["1", "2", "3", "4", "NONE"]
    affiliation_type = ["CONTRACTOR", "CIVILIAN", "MILITARY"]
    domain_two_three = ["YES", "NO"]
    site_resilience = ["ABC", "DEF", "GHI", "JKL"]
    
    # ABAC tokens
    tokens = ["AAA", "BBB", "CCC", "DDD", "XXX", "YYY", "ZZZ"]
    
    # Sample data arrays for realistic values - ALL CAPITALIZED
    ranks = ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", 
             "O1", "O2", "O3", "O4", "O5", "O6", "GS-12", "GS-13", "GS-14", "GS-15"]
    orgs = ["AFMC", "ACC", "AMC", "AETC", "AFGSC", "AFRC", "ANG", "PACAF", "USAFE", "CENTCOM"]
    
    # Updated FUNCTION field - Job Roles that work across technology domains
    functions = ["SOFTWARE ENGINEER", "DATA ANALYST", "SYSTEM ADMINISTRATOR", "PROJECT MANAGER",
                "CYBERSECURITY SPECIALIST", "TECHNICAL LEAD", "OPERATIONS MANAGER",
                "RESEARCH ANALYST", "QUALITY ASSURANCE", "BUSINESS ANALYST"]
    
    buildings = ["BLDG 1", "BLDG 2", "BLDG 3", "BLDG 4", "BLDG 5", "ANNEX A", "ANNEX B", "HQ"]
    categories = ["OFFICER", "ENLISTED", "CIVILIAN", "CONTRACTOR"]
    
    # Realistic address combinations (City, State, Country) - ALL CAPITALIZED
    addresses = [
        # United States locations
        ("SAN ANTONIO", "TX", "UNITED STATES OF AMERICA"),
        ("COLORADO SPRINGS", "CO", "UNITED STATES OF AMERICA"),
        ("DAYTON", "OH", "UNITED STATES OF AMERICA"),
        ("WASHINGTON", "DC", "UNITED STATES OF AMERICA"),
        ("NORFOLK", "VA", "UNITED STATES OF AMERICA"),
        ("TAMPA", "FL", "UNITED STATES OF AMERICA"),
        ("LAS VEGAS", "NV", "UNITED STATES OF AMERICA"),
        ("LOS ANGELES", "CA", "UNITED STATES OF AMERICA"),
        ("OMAHA", "NE", "UNITED STATES OF AMERICA"),
        ("MONTGOMERY", "AL", "UNITED STATES OF AMERICA"),
        ("SHREVEPORT", "LA", "UNITED STATES OF AMERICA"),
        ("SPOKANE", "WA", "UNITED STATES OF AMERICA"),
        ("TUCSON", "AZ", "UNITED STATES OF AMERICA"),
        ("GOLDSBORO", "NC", "UNITED STATES OF AMERICA"),
        ("LITTLE ROCK", "AR", "UNITED STATES OF AMERICA"),
        ("BILOXI", "MS", "UNITED STATES OF AMERICA"),
        ("DEL RIO", "TX", "UNITED STATES OF AMERICA"),
        ("VALDOSTA", "GA", "UNITED STATES OF AMERICA"),
        ("GREAT FALLS", "MT", "UNITED STATES OF AMERICA"),
        ("MINOT", "ND", "UNITED STATES OF AMERICA"),
        ("CHEYENNE", "WY", "UNITED STATES OF AMERICA"),
        ("SALT LAKE CITY", "UT", "UNITED STATES OF AMERICA"),
        ("ANCHORAGE", "AK", "UNITED STATES OF AMERICA"),
        ("HONOLULU", "HI", "UNITED STATES OF AMERICA"),
        
        # International locations (no state for international)
        ("RAMSTEIN", "", "GERMANY"),
        ("SPANGDAHLEM", "", "GERMANY"),
        ("KAISERSLAUTERN", "", "GERMANY"),
        ("STUTTGART", "", "GERMANY"),
        ("WIESBADEN", "", "GERMANY"),
        ("YOKOTA", "", "JAPAN"),
        ("KADENA", "", "JAPAN"),
        ("MISAWA", "", "JAPAN"),
        ("OSAN", "", "SOUTH KOREA"),
        ("KUNSAN", "", "SOUTH KOREA"),
        ("LAKENHEATH", "", "UNITED KINGDOM"),
        ("MILDENHALL", "", "UNITED KINGDOM"),
        ("CROUGHTON", "", "UNITED KINGDOM"),
        ("AVIANO", "", "ITALY"),
        ("SIGONELLA", "", "ITALY"),
        ("INCIRLIK", "", "TURKEY"),
        ("AL UDEID", "", "QATAR"),
        ("AL DHAFRA", "", "UNITED ARAB EMIRATES"),
        ("ANDERSEN", "", "GUAM"),
        ("DIEGO GARCIA", "", "BRITISH INDIAN OCEAN TERRITORY"),
        ("THULE", "", "GREENLAND"),
        ("KEFLAVIK", "", "ICELAND")
    ]
    
    statuses = ["ACTIVE", "RESERVE", "GUARD", "CIVILIAN", "CONTRACT"]
    skills = ["CYBERSECURITY", "ENGINEERING", "INTELLIGENCE", "LOGISTICS", 
              "MEDICAL", "PILOT", "MAINTENANCE", "COMMUNICATIONS"]
    focus_areas = ["CYBER OPERATIONS", "AIR SUPERIORITY", "GLOBAL STRIKE", "MOBILITY", "ISR"]
    functional_roles = ["ANALYST", "TECHNICIAN", "MANAGER", "SPECIALIST", "ADMINISTRATOR"]
    
    # Updated DOMAIN field - Technology Categories  
    domains = ["ARTIFICIAL INTELLIGENCE", "CLOUD COMPUTING", "CYBERSECURITY", "DATA SCIENCE", "ROBOTICS",
              "BLOCKCHAIN", "QUANTUM", "BIOMETRICS", "SATELLITE", "WIRELESS"]
              
    work_roles = ["ANALYST", "ENGINEER", "OPERATOR", "MANAGER", "TECHNICIAN"]
    rank_categories = ["JUNIOR", "MID-LEVEL", "SENIOR", "EXECUTIVE"]
    loe_justifications = ["MISSION CRITICAL", "SUPPORT", "ADMINISTRATIVE", "TRAINING"]
    critical_skills_options = ["YES", "NO"]
    
    def generate_sid():
        """Generate unique 7 character alphanumeric SID"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(7))
    
    def generate_fte():
        """Generate FTE value between 0.1 and 1.0"""
        return round(random.uniform(0.1, 1.0), 2)
    
    def generate_token_expression():
        """Generate ABAC token expressions with weighted complexity"""
        # Weighted complexity distribution
        complexity_weights = [40, 35, 25]  # Simple, Medium, Complex percentages
        complexity_choice = random.choices(['simple', 'medium', 'complex'], weights=complexity_weights)[0]
        
        if complexity_choice == 'simple':
            return generate_simple_tokens()
        elif complexity_choice == 'medium':
            return generate_medium_tokens()
        else:
            return generate_complex_tokens()
    
    def generate_simple_tokens():
        """Generate simple token expressions (1-2 tokens)"""
        patterns = [
            lambda: random.choice(tokens),  # Single token: AAA
            lambda: f"{random.choice(tokens)}&{random.choice(tokens)}",  # Two AND: AAA&BBB
            lambda: f"{random.choice(tokens)}|{random.choice(tokens)}",  # Two OR: AAA|BBB
        ]
        return random.choice(patterns)()
    
    def generate_medium_tokens():
        """Generate medium complexity expressions (3-4 tokens), favoring AAA&BBB&CCC"""
        # 30% chance for the favored AAA&BBB&CCC pattern
        if random.random() < 0.3:
            return "AAA&BBB&CCC"
        
        patterns = [
            lambda: f"{random.choice(tokens)}&{random.choice(tokens)}&{random.choice(tokens)}",  # Three AND
            lambda: f"{random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)}",  # Three OR
            lambda: f"({random.choice(tokens)}|{random.choice(tokens)})&{random.choice(tokens)}",  # (A|B)&C
            lambda: f"{random.choice(tokens)}&({random.choice(tokens)}|{random.choice(tokens)})",  # A&(B|C)
            lambda: f"({random.choice(tokens)}&{random.choice(tokens)})|{random.choice(tokens)}",  # (A&B)|C
        ]
        return random.choice(patterns)()
    
    def generate_complex_tokens():
        """Generate complex token expressions (5+ tokens with nesting)"""
        patterns = [
            lambda: f"({random.choice(tokens)}&{random.choice(tokens)})&({random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)})",  # (A&B)&(C|D|E)
            lambda: f"{random.choice(tokens)}&({random.choice(tokens)}|{random.choice(tokens)})&({random.choice(tokens)}|{random.choice(tokens)})",  # A&(B|C)&(D|E)
            lambda: f"({random.choice(tokens)}&{random.choice(tokens)}&{random.choice(tokens)})|({random.choice(tokens)}&{random.choice(tokens)})",  # (A&B&C)|(D&E)
            lambda: f"({random.choice(tokens)}|{random.choice(tokens)})&({random.choice(tokens)}|{random.choice(tokens)})&{random.choice(tokens)}",  # (A|B)&(C|D)&E
            lambda: f"{random.choice(tokens)}&{random.choice(tokens)}&({random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)})",  # A&B&(C|D|E|F)
        ]
        return random.choice(patterns)()
    
    print(f"Generating {total_rows:,} MPD records...")
    
    for i in range(1, total_rows + 1):
        snapshot = random.choice(snapshots)
        
        # Select a random address (ensures city/state/country consistency)
        city, state, country = random.choice(addresses)
        
        record = {
            "ID": i,
            "SID": generate_sid(),
            "SNAPSHOT": snapshot["snapshot"],
            "SNAPSHOT_MONTH": snapshot["date"],
            "CIMPL_RANK": random.choice(ranks),
            "DUTY_ORG": random.choice(orgs),
            "FUNCTION": random.choice(functions),
            "BUILDING": random.choice(buildings),
            "POP_CATEGORY": random.choice(categories),
            "GROUPS": f"GROUP {random.randint(1, 20)}",
            "FOCUS_AREA": random.choice(focus_areas),
            "NIAB_CATEGORY": f"CATEGORY {random.choice(['A', 'B', 'C', 'D', 'E'])}",
            "FUNCTIONAL_ROLE": random.choice(functional_roles),
            "COUNTRY": country,
            "NIPF_PRIORITY": random.choice(nipf_priority),
            "DOMAIN": random.choice(domains),
            "FTE": generate_fte(),
            "EMPLOYEE_SKILL_COMMUNITY": random.choice(skills),
            "MISSION_ELEMENT": f"ME-{random.randint(1, 100)}",
            "LOCATION_SPECIFIC": f"LOCATION {random.randint(1, 50)}",
            "STATE": state,
            "DFP": f"DFP-{random.randint(100, 1099)}",
            "WORK_ROLE": random.choice(work_roles),
            "CITY": city,
            "CIMPL_RANK_CATEGORY": random.choice(rank_categories),
            "ASSIGNED_ORG_TD": random.choice(orgs),
            "STATUS": random.choice(statuses),
            "SITE": f"SITE {random.randint(1, 10)}",
            "LOE_JUSTIFICATION": random.choice(loe_justifications),
            "REGION": "",  # Leaving blank as requested
            "AFFILIATION_TYPE": random.choice(affiliation_type),
            "ACTIVITY_DAF": f"ACTIVITY {random.randint(1, 100)}",
            "CRITICAL_SKILLS": random.choice(critical_skills_options),
            "DOMAIN_TWO_PLUS_THREE": random.choice(domain_two_three),
            "SITE_RESILIENCE": random.choice(site_resilience),
            "TOKENS": generate_token_expression()
        }
        
        data.append(record)
        
        # Progress indicator
        if i % 25000 == 0:
            print(f"Generated {i:,} MPD records...")
    
    return data

def generate_test_scores_dataset(mpd_data, total_test_records=7000):
    """
    Generate test scores dataset with SIDs that reference the MPD dataset
    """
    test_data = []
    
    # Star Wars languages - ALL CAPITALIZED
    star_wars_languages = [
        "BASIC", "HUTTESE", "SHYRIIWOOK", "RODIAN", "TWI'LEKI", "DROIDSPEAK",
        "EWOKESE", "JAWAESE", "MANDALORIAN", "BOCCE", "SULLUSTESE", "DURESE",
        "ZABRAK", "CEREAN", "GUNGAN", "NABOO", "CORELLIAN", "ALDERAANIAN"
    ]
    
    # ABAC tokens
    tokens = ["AAA", "BBB", "CCC", "DDD", "XXX", "YYY", "ZZZ"]
    
    # Create a lookup for MPD data by SID and snapshot for referential integrity
    mpd_lookup = {}
    for record in mpd_data:
        key = f"{record['SID']}_{record['SNAPSHOT']}"
        if key not in mpd_lookup:
            mpd_lookup[key] = []
        mpd_lookup[key].append(record)
    
    # Get all unique SID/snapshot combinations
    valid_sid_snapshots = list(mpd_lookup.keys())
    
    def determine_test_group(listen_score, read_score):
        """Determine test group based on scores"""
        max_score = max(listen_score, read_score)
        if max_score >= 3:
            return "HIGH"
        elif max_score == 2:
            return "MEDIUM"
        else:
            return "LOW"
    
    def generate_token_expression():
        """Generate ABAC token expressions with weighted complexity"""
        # Weighted complexity distribution
        complexity_weights = [40, 35, 25]  # Simple, Medium, Complex percentages
        complexity_choice = random.choices(['simple', 'medium', 'complex'], weights=complexity_weights)[0]
        
        if complexity_choice == 'simple':
            return generate_simple_tokens()
        elif complexity_choice == 'medium':
            return generate_medium_tokens()
        else:
            return generate_complex_tokens()
    
    def generate_simple_tokens():
        """Generate simple token expressions (1-2 tokens)"""
        patterns = [
            lambda: random.choice(tokens),  # Single token: AAA
            lambda: f"{random.choice(tokens)}&{random.choice(tokens)}",  # Two AND: AAA&BBB
            lambda: f"{random.choice(tokens)}|{random.choice(tokens)}",  # Two OR: AAA|BBB
        ]
        return random.choice(patterns)()
    
    def generate_medium_tokens():
        """Generate medium complexity expressions (3-4 tokens), favoring AAA&BBB&CCC"""
        # 30% chance for the favored AAA&BBB&CCC pattern
        if random.random() < 0.3:
            return "AAA&BBB&CCC"
        
        patterns = [
            lambda: f"{random.choice(tokens)}&{random.choice(tokens)}&{random.choice(tokens)}",  # Three AND
            lambda: f"{random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)}",  # Three OR
            lambda: f"({random.choice(tokens)}|{random.choice(tokens)})&{random.choice(tokens)}",  # (A|B)&C
            lambda: f"{random.choice(tokens)}&({random.choice(tokens)}|{random.choice(tokens)})",  # A&(B|C)
            lambda: f"({random.choice(tokens)}&{random.choice(tokens)})|{random.choice(tokens)}",  # (A&B)|C
        ]
        return random.choice(patterns)()
    
    def generate_complex_tokens():
        """Generate complex token expressions (5+ tokens with nesting)"""
        patterns = [
            lambda: f"({random.choice(tokens)}&{random.choice(tokens)})&({random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)})",  # (A&B)&(C|D|E)
            lambda: f"{random.choice(tokens)}&({random.choice(tokens)}|{random.choice(tokens)})&({random.choice(tokens)}|{random.choice(tokens)})",  # A&(B|C)&(D|E)
            lambda: f"({random.choice(tokens)}&{random.choice(tokens)}&{random.choice(tokens)})|({random.choice(tokens)}&{random.choice(tokens)})",  # (A&B&C)|(D&E)
            lambda: f"({random.choice(tokens)}|{random.choice(tokens)})&({random.choice(tokens)}|{random.choice(tokens)})&{random.choice(tokens)}",  # (A|B)&(C|D)&E
            lambda: f"{random.choice(tokens)}&{random.choice(tokens)}&({random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)}|{random.choice(tokens)})",  # A&B&(C|D|E|F)
        ]
        return random.choice(patterns)()
    
    print(f"Generating {total_test_records:,} test score records...")
    
    for i in range(1, total_test_records + 1):
        # Select a random valid SID/snapshot combination
        selected_key = random.choice(valid_sid_snapshots)
        sid, snapshot = selected_key.split('_', 1)
        
        # Get the corresponding snapshot date
        mpd_record = mpd_lookup[selected_key][0]
        snapshot_date = mpd_record['SNAPSHOT_MONTH']
        
        # Generate scores (1-5)
        listen_score = random.randint(1, 5)
        read_score = random.randint(1, 5)
        
        test_record = {
            "ID": i,
            "SID": sid,
            "LANGUAGE": random.choice(star_wars_languages),
            "LISTEN_SCORE": str(listen_score),
            "READ_SCORE": str(read_score),
            "TEST_GROUP": determine_test_group(listen_score, read_score),
            "SNAPSHOT": snapshot,
            "SNAPSHOT_MONTH": snapshot_date,
            "TOKENS": generate_token_expression()
        }
        
        test_data.append(test_record)
        
        # Progress indicator
        if i % 1000 == 0:
            print(f"Generated {i:,} test score records...")
    
    return test_data

def save_to_json(data, filename):
    """Save data to JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename):
    """Save data to CSV file using pandas"""
    try:
        import pandas as pd
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    except ImportError:
        print("pandas not installed. Install with: pip install pandas")

def get_mpd_data_summary(data):
    """Print summary statistics of the MPD data"""
    print(f"\nMPD Dataset Summary:")
    print(f"Total records: {len(data):,}")
    
    # Count by snapshot
    snapshot_counts = {}
    for record in data:
        snapshot = record['SNAPSHOT']
        snapshot_counts[snapshot] = snapshot_counts.get(snapshot, 0) + 1
    
    print("\nDistribution by Snapshot:")
    for snapshot, count in sorted(snapshot_counts.items()):
        percentage = (count / len(data)) * 100
        print(f"  {snapshot}: {count:,} records ({percentage:.1f}%)")
    
    # Count by affiliation type
    affiliation_counts = {}
    for record in data:
        affiliation = record['AFFILIATION_TYPE']
        affiliation_counts[affiliation] = affiliation_counts.get(affiliation, 0) + 1
    
    print("\nDistribution by Affiliation Type:")
    for affiliation, count in sorted(affiliation_counts.items()):
        percentage = (count / len(data)) * 100
        print(f"  {affiliation}: {count:,} records ({percentage:.1f}%)")
    
    # Token complexity analysis for MPD data
    token_complexity = {"Simple": 0, "Medium": 0, "Complex": 0}
    aaa_bbb_ccc_count = 0
    
    for record in data:
        tokens = record['TOKENS']
        if tokens == "AAA&BBB&CCC":
            aaa_bbb_ccc_count += 1
        
        # Count operators to estimate complexity
        and_count = tokens.count('&')
        or_count = tokens.count('|')
        paren_count = tokens.count('(')
        operator_count = and_count + or_count
        
        if operator_count <= 1 and paren_count == 0:
            token_complexity["Simple"] += 1
        elif operator_count <= 3 and paren_count <= 2:
            token_complexity["Medium"] += 1
        else:
            token_complexity["Complex"] += 1
    
    print("\nMPD Token Complexity Distribution:")
    for complexity, count in token_complexity.items():
        percentage = (count / len(data)) * 100
        print(f"  {complexity}: {count:,} records ({percentage:.1f}%)")
    
    aaa_percentage = (aaa_bbb_ccc_count / len(data)) * 100
    print(f"  AAA&BBB&CCC (favored pattern): {aaa_bbb_ccc_count:,} records ({aaa_percentage:.1f}%)")

def get_test_scores_summary(test_data, mpd_data):
    """Print summary statistics of the test scores data"""
    print(f"\nTest Scores Dataset Summary:")
    print(f"Total test records: {len(test_data):,}")
    
    # Count unique SIDs in test data
    unique_test_sids = set(record['SID'] for record in test_data)
    unique_mpd_sids = set(record['SID'] for record in mpd_data)
    
    print(f"Unique SIDs with test scores: {len(unique_test_sids):,}")
    print(f"Percentage of MPD SIDs with tests: {(len(unique_test_sids)/len(unique_mpd_sids)*100):.1f}%")
    
    # Average tests per SID
    avg_tests = len(test_data) / len(unique_test_sids)
    print(f"Average tests per SID: {avg_tests:.1f}")
    
    # Distribution by test group
    test_group_counts = {}
    for record in test_data:
        group = record['TEST_GROUP']
        test_group_counts[group] = test_group_counts.get(group, 0) + 1
    
    print("\nDistribution by Test Group:")
    for group, count in sorted(test_group_counts.items()):
        percentage = (count / len(test_data)) * 100
        print(f"  {group}: {count:,} records ({percentage:.1f}%)")
    
    # Distribution by language
    language_counts = {}
    for record in test_data:
        lang = record['LANGUAGE']
        language_counts[lang] = language_counts.get(lang, 0) + 1
    
    print("\nTop 10 Languages by Test Volume:")
    sorted_languages = sorted(language_counts.items(), key=lambda x: x[1], reverse=True)
    for lang, count in sorted_languages[:10]:
        percentage = (count / len(test_data)) * 100
        print(f"  {lang}: {count:,} tests ({percentage:.1f}%)")
    
    # Token complexity analysis
    token_complexity = {"Simple": 0, "Medium": 0, "Complex": 0}
    aaa_bbb_ccc_count = 0
    
    for record in test_data:
        tokens = record['TOKENS']
        if tokens == "AAA&BBB&CCC":
            aaa_bbb_ccc_count += 1
        
        # Count operators to estimate complexity
        and_count = tokens.count('&')
        or_count = tokens.count('|')
        paren_count = tokens.count('(')
        operator_count = and_count + or_count
        
        if operator_count <= 1 and paren_count == 0:
            token_complexity["Simple"] += 1
        elif operator_count <= 3 and paren_count <= 2:
            token_complexity["Medium"] += 1
        else:
            token_complexity["Complex"] += 1
    
    print("\nToken Complexity Distribution:")
    for complexity, count in token_complexity.items():
        percentage = (count / len(test_data)) * 100
        print(f"  {complexity}: {count:,} records ({percentage:.1f}%)")
    
    aaa_percentage = (aaa_bbb_ccc_count / len(test_data)) * 100
    print(f"  AAA&BBB&CCC (favored pattern): {aaa_bbb_ccc_count:,} records ({aaa_percentage:.1f}%)")
    
    # Sample token expressions
    print("\nSample Token Expressions:")
    sample_tokens = random.sample([record['TOKENS'] for record in test_data], min(10, len(test_data)))
    for i, token_expr in enumerate(sample_tokens, 1):
        print(f"  {i}. {token_expr}")

# Main execution
if __name__ == "__main__":
    import sys
    
    print("=== MPD Dashboard Data Generation ===\n")
    
    # Get MPD record count from command line argument, default to 100000
    mpd_record_count = 100000
    if len(sys.argv) > 1:
        try:
            mpd_record_count = int(sys.argv[1])
            print(f"Using command line argument: {mpd_record_count:,} MPD records")
        except ValueError:
            print(f"Invalid argument '{sys.argv[1]}'. Using default: {mpd_record_count:,} records")
    else:
        print(f"No argument provided. Using default: {mpd_record_count:,} MPD records")
    
    # Calculate test scores record count based on MPD records
    # Use ~10% of SIDs with average of 7 tests each = ~70% of MPD record count
    test_record_count = max(1, int(mpd_record_count * 0.7))
    print(f"Will generate approximately {test_record_count:,} test score records")
    print(f"Expected SIDs with tests: ~{int(test_record_count/7):,} ({(test_record_count/7)/mpd_record_count*100:.1f}% of MPD SIDs)")
    
    # Generate the MPD dataset
    mpd_data = generate_mpd_dataset(mpd_record_count)
    
    # Generate the test scores dataset (referencing MPD data)
    test_scores_data = generate_test_scores_dataset(mpd_data, test_record_count)
    
    # Show summaries
    get_mpd_data_summary(mpd_data)
    get_test_scores_summary(test_scores_data, mpd_data)
    
    # Save MPD data
    save_to_json(mpd_data, "mpd_notional_data.json")
    
    # Save test scores data
    save_to_json(test_scores_data, "test_scores_notional_data.json")
    
    # Optionally save to CSV (requires pandas)
    # save_to_csv(mpd_data, "mpd_notional_data.csv")
    # save_to_csv(test_scores_data, "test_scores_notional_data.csv")
    
    print("\n=== Generation Complete! ===")
    print("Files created:")
    print(f"- mpd_notional_data.json ({mpd_record_count:,} MPD records)")
    print(f"- test_scores_notional_data.json ({len(test_scores_data):,} test score records)")
    print("- Uncomment save_to_csv() lines to also create CSV files")
    print(f"\nUsage: python generate_mpd_data.py [number_of_mpd_records]")
    print(f"Example: python generate_mpd_data.py 1000")
    print(f"  - Creates 1000 MPD records")
    print(f"  - Creates ~700 test score records (~10% of SIDs with avg 7 tests each)")
    
    # Verify referential integrity
    print(f"\nReferential Integrity Check:")
    mpd_sids = set(record['SID'] for record in mpd_data)
    test_sids = set(record['SID'] for record in test_scores_data)
    orphaned_sids = test_sids - mpd_sids
    print(f"Orphaned SIDs in test data: {len(orphaned_sids)} (should be 0)")
    
    if len(orphaned_sids) == 0:
        print("✅ All test score SIDs have matching records in MPD data")
    else:
        print("❌ Some test score SIDs do not exist in MPD data")

# Example: Generate smaller samples for testing
def generate_samples(mpd_rows=1000, test_rows=100):
    """Generate smaller samples for testing"""
    sample_mpd = generate_mpd_dataset(mpd_rows)
    sample_test = generate_test_scores_dataset(sample_mpd, test_rows)
    
    save_to_json(sample_mpd, f"mpd_sample_{mpd_rows}.json")
    save_to_json(sample_test, f"test_scores_sample_{test_rows}.json")
    
    return sample_mpd, sample_test

# Uncomment to generate samples:
# sample_mpd, sample_test = generate_samples(1000, 100)