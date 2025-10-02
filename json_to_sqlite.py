import json
import sqlite3
import sys
import os
from datetime import datetime

def create_mpd_table(cursor):
    """Create the MPD table with proper schema"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mpd_data (
            ID INTEGER PRIMARY KEY,
            SID VARCHAR(128),
            SNAPSHOT VARCHAR(128),
            SNAPSHOT_MONTH DATE,
            CIMPL_RANK VARCHAR(128),
            DUTY_ORG VARCHAR(128),
            FUNCTION VARCHAR(128),
            BUILDING VARCHAR(128),
            POP_CATEGORY VARCHAR(128),
            GROUPS VARCHAR(128),
            FOCUS_AREA VARCHAR(128),
            NIAB_CATEGORY VARCHAR(128),
            FUNCTIONAL_ROLE VARCHAR(128),
            COUNTRY VARCHAR(128),
            NIPF_PRIORITY VARCHAR(128),
            DOMAIN VARCHAR(128),
            FTE REAL,
            EMPLOYEE_SKILL_COMMUNITY VARCHAR(128),
            MISSION_ELEMENT VARCHAR(128),
            LOCATION_SPECIFIC VARCHAR(256),
            STATE VARCHAR(128),
            DFP VARCHAR(256),
            WORK_ROLE VARCHAR(128),
            CITY VARCHAR(128),
            CIMPL_RANK_CATEGORY VARCHAR(128),
            ASSIGNED_ORG_TD VARCHAR(128),
            STATUS VARCHAR(128),
            SITE VARCHAR(128),
            LOE_JUSTIFICATION VARCHAR(128),
            REGION VARCHAR(128),
            AFFILIATION_TYPE VARCHAR(128),
            ACTIVITY_DAF VARCHAR(128),
            CRITICAL_SKILLS VARCHAR(128),
            DOMAIN_TWO_PLUS_THREE VARCHAR(10),
            SITE_RESILIENCE VARCHAR(128),
            TOKENS VARCHAR(500)
        )
    ''')

def create_test_scores_table(cursor):
    """Create the test scores table with proper schema"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_scores (
            ID INTEGER PRIMARY KEY,
            SID VARCHAR(25),
            LANGUAGE VARCHAR(150),
            LISTEN_SCORE VARCHAR(25),
            READ_SCORE VARCHAR(25),
            TEST_GROUP VARCHAR(25),
            SNAPSHOT VARCHAR(25),
            SNAPSHOT_MONTH DATE,
            TOKENS VARCHAR(500)
        )
    ''')

def insert_mpd_data(cursor, data):
    """Insert MPD data into the database"""
    print(f"Inserting {len(data):,} MPD records...")
    
    insert_query = '''
        INSERT INTO mpd_data (
            ID, SID, SNAPSHOT, SNAPSHOT_MONTH, CIMPL_RANK, DUTY_ORG, FUNCTION, 
            BUILDING, POP_CATEGORY, GROUPS, FOCUS_AREA, NIAB_CATEGORY, 
            FUNCTIONAL_ROLE, COUNTRY, NIPF_PRIORITY, DOMAIN, FTE, 
            EMPLOYEE_SKILL_COMMUNITY, MISSION_ELEMENT, LOCATION_SPECIFIC, 
            STATE, DFP, WORK_ROLE, CITY, CIMPL_RANK_CATEGORY, ASSIGNED_ORG_TD, 
            STATUS, SITE, LOE_JUSTIFICATION, REGION, AFFILIATION_TYPE, 
            ACTIVITY_DAF, CRITICAL_SKILLS, DOMAIN_TWO_PLUS_THREE, 
            SITE_RESILIENCE, TOKENS
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                 ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    records_inserted = 0
    for record in data:
        try:
            cursor.execute(insert_query, (
                record['ID'],
                record['SID'],
                record['SNAPSHOT'],
                record['SNAPSHOT_MONTH'],
                record['CIMPL_RANK'],
                record['DUTY_ORG'],
                record['FUNCTION'],
                record['BUILDING'],
                record['POP_CATEGORY'],
                record['GROUPS'],
                record['FOCUS_AREA'],
                record['NIAB_CATEGORY'],
                record['FUNCTIONAL_ROLE'],
                record['COUNTRY'],
                record['NIPF_PRIORITY'],
                record['DOMAIN'],
                record['FTE'],
                record['EMPLOYEE_SKILL_COMMUNITY'],
                record['MISSION_ELEMENT'],
                record['LOCATION_SPECIFIC'],
                record['STATE'],
                record['DFP'],
                record['WORK_ROLE'],
                record['CITY'],
                record['CIMPL_RANK_CATEGORY'],
                record['ASSIGNED_ORG_TD'],
                record['STATUS'],
                record['SITE'],
                record['LOE_JUSTIFICATION'],
                record['REGION'],
                record['AFFILIATION_TYPE'],
                record['ACTIVITY_DAF'],
                record['CRITICAL_SKILLS'],
                record['DOMAIN_TWO_PLUS_THREE'],
                record['SITE_RESILIENCE'],
                record['TOKENS']
            ))
            records_inserted += 1
            
            if records_inserted % 10000 == 0:
                print(f"  Inserted {records_inserted:,} MPD records...")
                
        except Exception as e:
            print(f"Error inserting MPD record {record.get('ID', 'Unknown')}: {e}")
    
    print(f"✅ Successfully inserted {records_inserted:,} MPD records")
    return records_inserted

def insert_test_scores_data(cursor, data):
    """Insert test scores data into the database"""
    print(f"Inserting {len(data):,} test score records...")
    
    insert_query = '''
        INSERT INTO test_scores (
            ID, SID, LANGUAGE, LISTEN_SCORE, READ_SCORE, TEST_GROUP, 
            SNAPSHOT, SNAPSHOT_MONTH, TOKENS
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    records_inserted = 0
    for record in data:
        try:
            cursor.execute(insert_query, (
                record['ID'],
                record['SID'],
                record['LANGUAGE'],
                record['LISTEN_SCORE'],
                record['READ_SCORE'],
                record['TEST_GROUP'],
                record['SNAPSHOT'],
                record['SNAPSHOT_MONTH'],
                record['TOKENS']
            ))
            records_inserted += 1
            
            if records_inserted % 1000 == 0:
                print(f"  Inserted {records_inserted:,} test score records...")
                
        except Exception as e:
            print(f"Error inserting test score record {record.get('ID', 'Unknown')}: {e}")
    
    print(f"✅ Successfully inserted {records_inserted:,} test score records")
    return records_inserted

def load_json_file(filename):
    """Load and parse JSON file"""
    if not os.path.exists(filename):
        print(f"❌ Error: File '{filename}' not found")
        return None
    
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data):,} records from {filename}")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON file '{filename}': {e}")
        return None
    except Exception as e:
        print(f"❌ Error loading file '{filename}': {e}")
        return None

def create_indexes(cursor):
    """Create indexes for better query performance"""
    print("Creating database indexes...")
    
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_mpd_sid ON mpd_data(SID)",
        "CREATE INDEX IF NOT EXISTS idx_mpd_snapshot ON mpd_data(SNAPSHOT)",
        "CREATE INDEX IF NOT EXISTS idx_mpd_affiliation ON mpd_data(AFFILIATION_TYPE)",
        "CREATE INDEX IF NOT EXISTS idx_test_sid ON test_scores(SID)",
        "CREATE INDEX IF NOT EXISTS idx_test_snapshot ON test_scores(SNAPSHOT)",
        "CREATE INDEX IF NOT EXISTS idx_test_group ON test_scores(TEST_GROUP)",
        "CREATE INDEX IF NOT EXISTS idx_test_language ON test_scores(LANGUAGE)"
    ]
    
    for index_sql in indexes:
        cursor.execute(index_sql)
    
    print("✅ Database indexes created")

def get_database_stats(cursor):
    """Get statistics about the created database"""
    cursor.execute("SELECT COUNT(*) FROM mpd_data")
    mpd_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM test_scores")
    test_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT SID) FROM mpd_data")
    unique_mpd_sids = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(DISTINCT SID) FROM test_scores")
    unique_test_sids = cursor.fetchone()[0]
    
    print(f"\n📊 Database Statistics:")
    print(f"  MPD records: {mpd_count:,}")
    print(f"  Test score records: {test_count:,}")
    print(f"  Unique SIDs in MPD: {unique_mpd_sids:,}")
    print(f"  Unique SIDs with tests: {unique_test_sids:,}")
    
    if unique_mpd_sids > 0:
        coverage = (unique_test_sids / unique_mpd_sids) * 100
        print(f"  Test coverage: {coverage:.1f}% of MPD SIDs")
    
    if unique_test_sids > 0:
        avg_tests = test_count / unique_test_sids
        print(f"  Average tests per SID: {avg_tests:.1f}")

def main():
    print("=== JSON to SQLite Database Converter ===\n")
    
    # Default file names
    mpd_file = "mpd_notional_data.json"
    test_file = "test_scores_notional_data.json"
    db_file = "development.db"
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        mpd_file = sys.argv[1]
    if len(sys.argv) > 2:
        test_file = sys.argv[2]
    if len(sys.argv) > 3:
        db_file = sys.argv[3]
    
    print(f"Input files:")
    print(f"  MPD data: {mpd_file}")
    print(f"  Test scores: {test_file}")
    print(f"Output database: {db_file}\n")
    
    # Load JSON data
    mpd_data = load_json_file(mpd_file)
    if mpd_data is None:
        return 1
    
    test_data = load_json_file(test_file)
    if test_data is None:
        return 1
    
    # Create/connect to SQLite database
    try:
        # Remove existing database if it exists
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"🗑️  Removed existing database: {db_file}")
        
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print(f"✅ Connected to database: {db_file}")
        
        # Create tables
        print("\nCreating database tables...")
        create_mpd_table(cursor)
        create_test_scores_table(cursor)
        print("✅ Database tables created")
        
        # Insert data
        print("\nInserting data...")
        mpd_inserted = insert_mpd_data(cursor, mpd_data)
        test_inserted = insert_test_scores_data(cursor, test_data)
        
        # Create indexes
        create_indexes(cursor)
        
        # Commit changes
        conn.commit()
        print("\n✅ All data committed to database")
        
        # Show statistics
        get_database_stats(cursor)
        
        # Close connection
        conn.close()
        
        print(f"\n🎉 Successfully created database: {db_file}")
        print(f"   MPD records: {mpd_inserted:,}")
        print(f"   Test records: {test_inserted:,}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return 1

def show_usage():
    """Show usage instructions"""
    print("Usage:")
    print("  python json_to_sqlite.py [mpd_file] [test_file] [database_file]")
    print("")
    print("Examples:")
    print("  python json_to_sqlite.py")
    print("    Uses defaults: mpd_notional_data.json, test_scores_notional_data.json -> development.db")
    print("")
    print("  python json_to_sqlite.py my_mpd.json my_tests.json my_database.db")
    print("    Uses custom file names")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
        sys.exit(0)
    
    exit_code = main()
    sys.exit(exit_code)