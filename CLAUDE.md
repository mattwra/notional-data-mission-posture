# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This repository generates notional (synthetic) data for an MPD (Mission Personnel Data) dashboard. It creates two related datasets: personnel records and language test scores, with support for Attribute-Based Access Control (ABAC) token expressions.

**Key Design Principle**: All generated data uses CAPITAL LETTERS for consistency and ease of querying.

## Core Scripts

### generate-data.py
Main data generation script that creates two JSON files:
- `mpd_notional_data.json` - Personnel records (default: 100k records)
- `test_scores_notional_data.json` - Language test scores (default: 70k records, ~10% SID coverage)

**Command**:
```bash
# Generate default 100k MPD records + 70k test records
python generate-data.py

# Generate custom number of records
python generate-data.py 5000  # Creates 5k MPD + ~3.5k test records
```

### json_to_sqlite.py
Converts JSON files to SQLite database with proper schema, indexes, and referential integrity.

**Command**:
```bash
# Use default files
python json_to_sqlite.py

# Use custom files
python json_to_sqlite.py my_mpd.json my_tests.json my_database.db
```

## Data Architecture

### MPD Dataset (36 fields)
Primary personnel dataset with snapshot-based temporal structure. Each record represents a person's data at a specific point in time.

**Critical Fields**:
- `SID` (VARCHAR): Unique 7-character alphanumeric identifier per person (must be unique in MPD data)
- `SNAPSHOT` (VARCHAR): Semi-annual time period ("Fall 2023", "Spring 2024", "Fall 2024", "Spring 2025")
- `SNAPSHOT_MONTH` (DATE): Associated date (YYYY-10-31 for Fall, YYYY-02-28 for Spring)
- `FUNCTION` (VARCHAR): Job role (10 options: SOFTWARE ENGINEER, DATA ANALYST, etc.)
- `DOMAIN` (VARCHAR): Technology category (10 options: ARTIFICIAL INTELLIGENCE, CLOUD COMPUTING, etc.)
- `CITY`, `STATE`, `COUNTRY` (VARCHAR): Location fields (state blank for international)
- `AFFILIATION_TYPE` (VARCHAR): CONTRACTOR, CIVILIAN, or MILITARY
- `TOKENS` (VARCHAR): ABAC expression for access control

### Test Scores Dataset (9 fields)
Language test records that reference MPD personnel through SID.

**Critical Fields**:
- `SID` (VARCHAR): References MPD dataset (NOT unique - same person can have multiple tests)
- `LANGUAGE` (VARCHAR): Star Wars language being tested (18 options)
- `LISTEN_SCORE`, `READ_SCORE` (VARCHAR): Score values 1-5
- `TEST_GROUP` (VARCHAR): HIGH/MEDIUM/LOW based on score logic
- `SNAPSHOT`, `SNAPSHOT_MONTH`: Must match MPD record for same SID
- `TOKENS` (VARCHAR): ABAC expression

**Referential Integrity**:
- Every SID in test scores MUST exist in MPD data
- Snapshot periods MUST match between datasets for same SID
- ~10% of MPD SIDs have test records
- Average 7 tests per SID with tests

### Test Group Logic
- HIGH: Either score ≥ 3
- MEDIUM: Highest score = 2
- LOW: Both scores < 2

## Critical Data Rules

### 1. CAPITALIZATION
**ALL field values MUST be in CAPITAL LETTERS**
- ✅ "SAN ANTONIO", "SYSTEM ADMINISTRATOR"
- ❌ "San Antonio", "System Administrator"

### 2. ADDRESS FORMAT
**US Locations**: Full city name + 2-char state code + "UNITED STATES OF AMERICA"
- Example: ("SAN ANTONIO", "TX", "UNITED STATES OF AMERICA")

**International Locations**: Full city name + empty state + country name
- Example: ("RAMSTEIN", "", "GERMANY")

### 3. DOMAIN Field (Technology Categories)
10 valid technology domains:
```
ARTIFICIAL INTELLIGENCE, CLOUD COMPUTING, CYBERSECURITY, DATA SCIENCE,
ROBOTICS, BLOCKCHAIN, QUANTUM, BIOMETRICS, SATELLITE, WIRELESS
```

### 4. FUNCTION Field (Job Roles)
10 valid job roles that work across any technology domain:
```
SOFTWARE ENGINEER, DATA ANALYST, SYSTEM ADMINISTRATOR, PROJECT MANAGER,
CYBERSECURITY SPECIALIST, TECHNICAL LEAD, OPERATIONS MANAGER,
RESEARCH ANALYST, QUALITY ASSURANCE, BUSINESS ANALYST
```

### 5. TOKENS Field (ABAC Expressions)
**Token Set**: AAA, BBB, CCC, DDD, XXX, YYY, ZZZ
**Operators**: `&` (AND), `|` (OR), `()` (precedence)

**Complexity Distribution**:
- 40% Simple (1-2 tokens): `AAA`, `AAA&BBB`, `CCC|DDD`
- 35% Medium (3-4 tokens): `AAA&BBB&CCC` (favored pattern 30% of time), `(AAA|BBB)&CCC`
- 25% Complex (5+ tokens): `(AAA&BBB)&(CCC|DDD|XXX)`, `AAA&(BBB|CCC)&(DDD|YYY)`

### 6. LANGUAGES (Test Scores)
18 Star Wars languages (capitalized):
```
BASIC, HUTTESE, SHYRIIWOOK, RODIAN, TWI'LEKI, DROIDSPEAK,
EWOKESE, JAWAESE, MANDALOIAN, BOCCE, SULLUSTESE, DURESE,
ZABRAK, CEREAN, GUNGAN, NABOO, CORELLIAN, ALDERAANIAN
```

## Database Schema

### Table: mpd_data
36 columns including ID (primary key), personnel fields, organizational data, and TOKENS.

**Key Indexes**:
- `idx_mpd_sid` on SID
- `idx_mpd_snapshot` on SNAPSHOT
- `idx_mpd_affiliation` on AFFILIATION_TYPE

### Table: test_scores
9 columns including ID (primary key), SID (foreign reference), test data, and TOKENS.

**Key Indexes**:
- `idx_test_sid` on SID
- `idx_test_snapshot` on SNAPSHOT
- `idx_test_group` on TEST_GROUP
- `idx_test_language` on LANGUAGE

## Viewing Data

### DB Browser for SQLite
Download: https://sqlitebrowser.org/
1. Open Database → select mpd_dashboard.db
2. Browse Data tab → view tables
3. Execute SQL tab → run queries

### Command Line
```bash
sqlite3 mpd_dashboard.db
.tables                    # List tables
.schema mpd_data          # Show table structure
.headers on               # Show column headers
.mode column              # Pretty format
SELECT COUNT(*) FROM mpd_data;
```

## Common Operations

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

-- Join personnel with test scores
SELECT
    m.SID, m.FUNCTION, m.DOMAIN,
    t.LANGUAGE, t.LISTEN_SCORE, t.READ_SCORE, t.TEST_GROUP
FROM mpd_data m
JOIN test_scores t ON m.SID = t.SID
WHERE m.CITY = 'SAN ANTONIO';

-- Test coverage by snapshot
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

## Data Validation Checklist

When generating or modifying data:
- [ ] All text values are in CAPITAL LETTERS
- [ ] US addresses have 2-character state codes
- [ ] International addresses have blank state field
- [ ] All SIDs in test_scores exist in mpd_data
- [ ] SNAPSHOT values match between datasets for same SID
- [ ] TEST_GROUP values follow score logic
- [ ] TOKENS expressions use only valid tokens (AAA-ZZZ) and operators (&, |, ())
- [ ] DOMAIN values are from approved 10-item list
- [ ] FUNCTION values are from approved 10-item list
- [ ] LANGUAGE values are from 18-item Star Wars list
- [ ] No duplicate SIDs in mpd_data

## Design Decisions

**Why CAPITAL LETTERS?**
Makes querying easier and more consistent. No case sensitivity issues.

**Why separate City/State/Country fields?**
Allows flexible filtering on location dimensions independently.

**Why technology domains instead of warfare domains?**
More broadly applicable and easier to understand for testing purposes.

**Why Star Wars languages?**
Clearly notional/placeholder data that won't be confused with real programs.

**Why ~10% test coverage?**
Realistic scenario for testing joins and null handling in dashboards.

**Why favor AAA&BBB&CCC token pattern?**
Provides a common access pattern for "majority access" testing in ABAC scenarios.

## Key Implementation Details

### SID Generation (generate-data.py:110-113)
7-character alphanumeric string using uppercase letters and digits. Note: Current implementation uses random generation which could theoretically create duplicates. For guaranteed uniqueness, implement SID tracking with a set.

### Token Expression Generation (generate-data.py:119-165)
Weighted complexity distribution with lambda pattern generators for each complexity level. Medium complexity has special 30% weighting for "AAA&BBB&CCC" pattern.

### Test Scores Dataset Generation (generate-data.py:222-340)
Creates a lookup table of MPD records by SID+SNAPSHOT to ensure referential integrity. Each test record selects a random valid SID/snapshot combination from this lookup.

### Database Conversion (json_to_sqlite.py)
- Removes existing database before creating new one
- Uses parameterized queries for safe insertion
- Creates indexes after data insertion for performance
- Provides progress indicators for large datasets
- Validates referential integrity at completion
