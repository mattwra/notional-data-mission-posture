# MPD Dashboard Data Generation

## Overview
This project generates notional data for an MPD (Mission Personnel Data) dashboard. The data consists of two related datasets: personnel records and language test scores, with support for Attribute-Based Access Control (ABAC) token expressions.

## Project Structure

```
├── generate_mpd_data.py          # Main data generation script
├── json_to_sqlite.py             # JSON to SQLite database converter
├── mpd_data.xlsx                 # Schema definition (input)
├── mpd_notional_data.json        # Generated personnel data (output)
├── test_scores_notional_data.json # Generated test scores (output)
└── mpd_dashboard.db              # SQLite database (output)
```

## Quick Start

### Generate Data
```bash
# Generate 100k MPD records + 70k test score records (default)
python generate_mpd_data.py

# Generate custom number of records
python generate_mpd_data.py 5000
# Creates 5000 MPD records + ~3500 test score records
```

### Convert to SQLite Database
```bash
# Use default file names
python json_to_sqlite.py

# Use custom file names
python json_to_sqlite.py my_mpd.json my_tests.json my_database.db
```

## Data Generation Details

### Dataset 1: MPD Personnel Data (mpd_notional_data.json)

**Schema:** 36 fields including personnel information, organizational data, location, and ABAC tokens

**Key Fields:**
- `ID` (INTEGER): Primary key
- `SID` (VARCHAR): Unique 7-character alphanumeric identifier
- `SNAPSHOT` (VARCHAR): Time period (e.g., "FALL 2023", "SPRING 2024")
- `SNAPSHOT_MONTH` (DATE): Associated date (YYYY-10-31 for Fall, YYYY-02-28 for Spring)
- `FUNCTION` (VARCHAR): Job role
- `DOMAIN` (VARCHAR): Technology category
- `CITY`, `STATE`, `COUNTRY` (VARCHAR): Address fields
- `TOKENS` (VARCHAR): ABAC expression for access control

**Snapshot Periods (Semi-Annual):**
- Fall 2023 (2023-10-31)
- Spring 2024 (2024-02-28)
- Fall 2024 (2024-10-31)
- Spring 2025 (2025-02-28)

### Dataset 2: Test Scores (test_scores_notional_data.json)

**Schema:** 9 fields including language test information

**Key Fields:**
- `ID` (INTEGER): Primary key
- `SID` (VARCHAR): References MPD dataset (implied foreign key)
- `LANGUAGE` (VARCHAR): Star Wars language being tested
- `LISTEN_SCORE` (VARCHAR): Score value (1-5)
- `READ_SCORE` (VARCHAR): Score value (1-5)
- `TEST_GROUP` (VARCHAR): HIGH, MEDIUM, or LOW based on scores
- `SNAPSHOT`, `SNAPSHOT_MONTH`: Must match MPD record for same SID
- `TOKENS` (VARCHAR): ABAC expression for access control

**Referential Integrity:**
- Every SID in test scores exists in MPD data
- Snapshot periods match between datasets
- ~10% of SIDs have test records
- Average of 7 tests per SID with tests

**Test Group Logic:**
- HIGH: Either score ≥ 3
- MEDIUM: Highest score = 2
- LOW: Both scores < 2

## Critical Data Rules

### 1. CAPITALIZATION
**ALL field values MUST be in CAPITAL LETTERS**

Examples:
- ✅ "SAN ANTONIO" 
- ❌ "San Antonio"
- ✅ "SYSTEM ADMINISTRATOR"
- ❌ "System Administrator"

### 2. ADDRESS FORMAT

**City:**
- Full names, no abbreviations
- US Examples: "SAN ANTONIO", "COLORADO SPRINGS", "LOS ANGELES"
- International Examples: "RAMSTEIN", "YOKOTA", "OSAN"

**State:**
- US locations: Two-character abbreviation (TX, CO, OH, etc.)
- International locations: Empty string (blank)

**Country:**
- Full, spelled-out names
- Consistent spelling (always use the same format)
- Examples: "UNITED STATES OF AMERICA", "GERMANY", "JAPAN", "SOUTH KOREA"

**Region:**
- Currently left blank (empty string)

**Valid Address Examples:**
```
City: SAN ANTONIO, State: TX, Country: UNITED STATES OF AMERICA
City: RAMSTEIN, State: , Country: GERMANY
City: YOKOTA, State: , Country: JAPAN
```

### 3. DOMAIN FIELD (Technology Categories)

**Definition:** Technology domain/category where personnel work

**Valid Values (10 options):**
```
ARTIFICIAL INTELLIGENCE
CLOUD COMPUTING
CYBERSECURITY
DATA SCIENCE
ROBOTICS
BLOCKCHAIN
QUANTUM
BIOMETRICS
SATELLITE
WIRELESS
```

### 4. FUNCTION FIELD (Job Roles)

**Definition:** Job role/function that can work across any technology domain

**Valid Values (10 options):**
```
SOFTWARE ENGINEER
DATA ANALYST
SYSTEM ADMINISTRATOR
PROJECT MANAGER
CYBERSECURITY SPECIALIST
TECHNICAL LEAD
OPERATIONS MANAGER
RESEARCH ANALYST
QUALITY ASSURANCE
BUSINESS ANALYST
```

**Cross-Domain Examples:**
- DOMAIN: "ARTIFICIAL INTELLIGENCE" + FUNCTION: "DATA ANALYST" ✅
- DOMAIN: "CLOUD COMPUTING" + FUNCTION: "SYSTEM ADMINISTRATOR" ✅
- DOMAIN: "CYBERSECURITY" + FUNCTION: "SOFTWARE ENGINEER" ✅

### 5. TOKENS FIELD (ABAC Expressions)

**Definition:** Attribute-Based Access Control expressions for record visibility

**Token Set (7 tokens):**
```
AAA, BBB, CCC, DDD, XXX, YYY, ZZZ
```

**Operators:**
- `&` = AND operator
- `|` = OR operator
- `()` = Parentheses for precedence

**Complexity Distribution:**
- 40% Simple (1-2 tokens)
- 35% Medium (3-4 tokens) - 30% of these use "AAA&BBB&CCC" (favored pattern)
- 25% Complex (5+ tokens with nesting)

**Expression Examples:**
- Simple: `AAA`, `AAA&BBB`, `CCC|DDD`
- Medium: `AAA&BBB&CCC`, `(AAA|BBB)&CCC`, `AAA&(BBB|CCC)`
- Complex: `(AAA&BBB)&(CCC|DDD|XXX)`, `AAA&(BBB|CCC)&(DDD|YYY)`

**Logic Examples:**
- `(AAA&BBB)|CCC` = Must have (AAA AND BBB) OR just CCC
- `AAA&(BBB|CCC)` = Must have AAA AND (either BBB OR CCC)

### 6. SID UNIQUENESS

**MPD Dataset:** Each SID should be unique (no duplicates)

**Test Scores Dataset:** 
- SIDs reference MPD dataset
- Same SID can appear multiple times (multiple tests per person)
- All SIDs must exist in MPD dataset

### 7. LANGUAGES (Test Scores Dataset)

**Star Wars Languages (Capitalized):**
```
BASIC, HUTTESE, SHYRIIWOOK, RODIAN, TWI'LEKI, DROIDSPEAK,
EWOKESE, JAWAESE, MANDALORIAN, BOCCE, SULLUSTESE, DURESE,
ZABRAK, CEREAN, GUNGAN, NABOO, CORELLIAN, ALDERAANIAN
```

## Other Field Values

### Constrained Fields

**NIPF_PRIORITY:**
```
1, 2, 3, 4, NONE
```

**AFFILIATION_TYPE:**
```
CONTRACTOR, CIVILIAN, MILITARY
```

**DOMAIN_TWO_PLUS_THREE:**
```
YES, NO
```

**SITE_RESILIENCE:**
```
ABC, DEF, GHI, JKL
```

### Sample Data Arrays

**Ranks:**
```
E1-E9, O1-O6, GS-12 through GS-15
```

**Organizations:**
```
AFMC, ACC, AMC, AETC, AFGSC, AFRC, ANG, PACAF, USAFE, CENTCOM
```

**Buildings:**
```
BLDG 1, BLDG 2, BLDG 3, BLDG 4, BLDG 5, ANNEX A, ANNEX B, HQ
```

**Categories:**
```
OFFICER, ENLISTED, CIVILIAN, CONTRACTOR
```

**Statuses:**
```
ACTIVE, RESERVE, GUARD, CIVILIAN, CONTRACT
```

**Skills:**
```
CYBERSECURITY, ENGINEERING, INTELLIGENCE, LOGISTICS, 
MEDICAL, PILOT, MAINTENANCE, COMMUNICATIONS
```

**Focus Areas:**
```
CYBER OPERATIONS, AIR SUPERIORITY, GLOBAL STRIKE, MOBILITY, ISR
```

**Functional Roles:**
```
ANALYST, TECHNICIAN, MANAGER, SPECIALIST, ADMINISTRATOR
```

**Work Roles:**
```
ANALYST, ENGINEER, OPERATOR, MANAGER, TECHNICIAN
```

**Rank Categories:**
```
JUNIOR, MID-LEVEL, SENIOR, EXECUTIVE
```

**LOE Justifications:**
```
MISSION CRITICAL, SUPPORT, ADMINISTRATIVE, TRAINING
```

**Critical Skills:**
```
YES, NO
```

## Location Data

### US Military Locations (with State codes)
```
SAN ANTONIO, TX
COLORADO SPRINGS, CO
DAYTON, OH
WASHINGTON, DC
NORFOLK, VA
TAMPA, FL
LAS VEGAS, NV
LOS ANGELES, CA
OMAHA, NE
MONTGOMERY, AL
ANCHORAGE, AK
HONOLULU, HI
... (24 total US locations)
```

### International Military Locations (no State)
```
RAMSTEIN, GERMANY
YOKOTA, JAPAN
OSAN, SOUTH KOREA
LAKENHEATH, UNITED KINGDOM
AVIANO, ITALY
INCIRLIK, TURKEY
AL UDEID, QATAR
... (18 total international locations)
```

## Database Schema

### Table: mpd_data
```sql
CREATE TABLE mpd_data (
    ID INTEGER PRIMARY KEY,
    SID VARCHAR(128),
    SNAPSHOT VARCHAR(128),
    SNAPSHOT_MONTH DATE,
    -- ... (36 total columns including TOKENS)
);
```

### Table: test_scores
```sql
CREATE TABLE test_scores (
    ID INTEGER PRIMARY KEY,
    SID VARCHAR(25),
    LANGUAGE VARCHAR(150),
    LISTEN_SCORE VARCHAR(25),
    READ_SCORE VARCHAR(25),
    TEST_GROUP VARCHAR(25),
    SNAPSHOT VARCHAR(25),
    SNAPSHOT_MONTH DATE,
    TOKENS VARCHAR(500)
);
```

### Database Indexes
```sql
-- MPD indexes
CREATE INDEX idx_mpd_sid ON mpd_data(SID);
CREATE INDEX idx_mpd_snapshot ON mpd_data(SNAPSHOT);
CREATE INDEX idx_mpd_affiliation ON mpd_data(AFFILIATION_TYPE);

-- Test scores indexes
CREATE INDEX idx_test_sid ON test_scores(SID);
CREATE INDEX idx_test_snapshot ON test_scores(SNAPSHOT);
CREATE INDEX idx_test_group ON test_scores(TEST_GROUP);
CREATE INDEX idx_test_language ON test_scores(LANGUAGE);
```

## Usage Examples

### Query Examples

```sql
-- Basic counts
SELECT COUNT(*) FROM mpd_data;
SELECT COUNT(*) FROM test_scores;

-- Personnel by technology domain
SELECT DOMAIN, COUNT(*) as count
FROM mpd_data 
GROUP BY DOMAIN 
ORDER BY count DESC;

-- Test scores by language
SELECT LANGUAGE, COUNT(*) as test_count
FROM test_scores 
GROUP BY LANGUAGE 
ORDER BY test_count DESC;

-- Join personnel with test scores
SELECT 
    m.SID,
    m.FUNCTION,
    m.DOMAIN,
    t.LANGUAGE,
    t.LISTEN_SCORE,
    t.READ_SCORE,
    t.TEST_GROUP
FROM mpd_data m
JOIN test_scores t ON m.SID = t.SID
WHERE m.CITY = 'SAN ANTONIO';

-- Token analysis
SELECT 
    CASE 
        WHEN TOKENS LIKE '%(%' THEN 'COMPLEX'
        WHEN TOKENS LIKE '%&%&%' OR TOKENS LIKE '%|%|%' THEN 'MEDIUM'
        ELSE 'SIMPLE'
    END as complexity,
    COUNT(*) as count
FROM mpd_data 
GROUP BY complexity;

-- Coverage by snapshot
SELECT 
    m.SNAPSHOT,
    COUNT(DISTINCT m.SID) as total_personnel,
    COUNT(DISTINCT t.SID) as personnel_with_tests,
    ROUND(100.0 * COUNT(DISTINCT t.SID) / COUNT(DISTINCT m.SID), 1) as coverage_pct
FROM mpd_data m
LEFT JOIN test_scores t ON m.SID = t.SID AND m.SNAPSHOT = t.SNAPSHOT
GROUP BY m.SNAPSHOT
ORDER BY m.SNAPSHOT;
```

### Python Usage

```python
import json
import sqlite3

# Load JSON data
with open('mpd_notional_data.json', 'r') as f:
    mpd_data = json.load(f)

# Query SQLite database
conn = sqlite3.connect('mpd_dashboard.db')
cursor = conn.cursor()

# Example query
cursor.execute("""
    SELECT DOMAIN, FUNCTION, COUNT(*) as count 
    FROM mpd_data 
    GROUP BY DOMAIN, FUNCTION 
    ORDER BY count DESC 
    LIMIT 10
""")

results = cursor.fetchall()
for row in results:
    print(f"{row[0]}, {row[1]}: {row[2]}")

conn.close()
```

## Data Validation Checklist

Before using generated data, verify:

- [ ] All text values are in CAPITAL LETTERS
- [ ] US addresses have 2-character State codes
- [ ] International addresses have blank State field
- [ ] Country names are consistently spelled
- [ ] All SIDs in test_scores exist in mpd_data
- [ ] SNAPSHOT values match between datasets for same SID
- [ ] TEST_GROUP values follow score logic (HIGH/MEDIUM/LOW)
- [ ] TOKENS expressions are syntactically valid
- [ ] DOMAIN values are from approved technology category list
- [ ] FUNCTION values are from approved job role list
- [ ] No duplicate SIDs in mpd_data (each SID unique)

## Tools & Viewing Data

### DB Browser for SQLite
Download: https://sqlitebrowser.org/

**Usage:**
1. Open Database → select mpd_dashboard.db
2. Browse Data tab → view tables
3. Execute SQL tab → run queries
4. Export results to CSV

### Command Line
```bash
# Open database
sqlite3 mpd_dashboard.db

# Useful commands
.tables                    # List tables
.schema mpd_data          # Show table structure
.headers on               # Show column headers
.mode column              # Pretty format
SELECT COUNT(*) FROM mpd_data;
```

## Troubleshooting

### Issue: Duplicate SIDs in MPD data
**Solution:** The current implementation uses random generation. For guaranteed uniqueness, implement SID tracking with a set.

### Issue: Mismatched addresses (wrong city/state/country combinations)
**Solution:** Script now uses pre-defined address tuples to ensure consistency.

### Issue: Case sensitivity in queries
**Solution:** All values are now generated in CAPITAL LETTERS for consistent querying.

### Issue: TOKENS expressions look wrong
**Solution:** Verify expressions use only AAA, BBB, CCC, DDD, XXX, YYY, ZZZ and operators &, |, ()

## Design Decisions

### Why CAPITAL LETTERS?
Makes querying easier and more consistent. No need to worry about case sensitivity.

### Why separate address fields?
Allows flexible filtering on City, State (US only), or Country independently.

### Why technology domains instead of warfare domains?
More broadly applicable and easier to understand notional values for dashboard testing.

### Why Star Wars languages?
Clearly notional/placeholder data that won't be confused with real language testing programs.

### Why ~10% test coverage?
Realistic scenario where not all personnel have test records, good for testing joins and null handling.

### Why favor AAA&BBB&CCC token pattern?
Provides a common access pattern for "majority access" testing in ABAC scenarios.

## Future Enhancements

Potential improvements to consider:
- [ ] Add SID uniqueness enforcement with set tracking
- [ ] Add logical relationships (e.g., certain ranks more likely in certain domains)
- [ ] Add data export to additional formats (Parquet, Excel, etc.)
- [ ] Add data validation script
- [ ] Add sample dashboard queries library
- [ ] Add performance testing for large datasets
- [ ] Add incremental data generation (append to existing data)

## Version History

- **v1.0** - Initial implementation with 100k records, basic schema
- **v1.1** - Added TOKENS field with ABAC expressions
- **v1.2** - Updated address format (proper City/State/Country handling)
- **v1.3** - Converted all values to CAPITAL LETTERS
- **v1.4** - Updated DOMAIN to technology categories, FUNCTION to job roles

## Contact & Support

For questions or issues with this data generation system, refer back to the original Claude conversation in the "MPD Dashboard Data Generation" project.

## License

This is notional data generation code for testing purposes. All generated data is synthetic and does not represent real individuals or organizations.