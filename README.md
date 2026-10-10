# Polititrace Nigeria: Political Investigative Research Pipeline
### Deep Historical Tenure Scraping & Documentary Evidence Miner: Bola Ahmed Tinubu & Peter Gregory Obi

An automated, forensic investigation pipeline built for investigative journalists, documentary producers, political researchers, and citizens. It goes far beyond superficial search engine hits to reconstruct the historical records, tenure actions, public sector crises, controversies, and verbatim quotes of Nigeria's foremost political candidates.

---

## 💡 The Core Thesis: "The Illusion of Choice"

> *"We do not remember the history of our politicians, and that actually warps the way we perceive them and the way we vote for them."*

Public discourse frequently paints contemporary Nigerian politics in binary strokes:
- The **"Builder of Modern Lagos"** (Bola Ahmed Tinubu)
- The **"Prudent Frugal Technocrat"** (Peter Gregory Obi)

By indexing contemporaneously reported news items, judicial rulings, investigative reports, and broadcast interviews from their **active tenures**, this pipeline provides evidence showing that regardless of candidate brand, both figures presided over governance models defined by:
1. **Executive opacity and private financial entanglement** (Alpha Beta tax collection monopoly vs. Pandora Papers secret offshore shell companies & SABMiller state equity).
2. **Paralyzing public sector labor crises** (Federal-state LG funding standoff leaving council workers unpaid for 14 months vs. a 13-month medical doctors' strike shuttering public hospitals).
3. **Suppression of local democracy** (Unilateral 37 LCDAs under party machine control vs. nearly 8-year boycott of Local Government elections).
4. **Unresolved security and human rights events** (Lekki Toll Gate EndSARS shootings & EndBadGovernance crackdowns vs. Ezu River corpses linked to Awkuzu SARS).
5. **Rhetoric vs. Governance Reality** (Anti-subsidy mass protests in 2012 vs. abrupt subsidy abolition in 2023; N75B liquid savings claim vs. N127B liabilities audit).

---

## 🔍 Data Source Architecture

1. **Nigerian Broadcast TV Archives**:
   - **Channels Television** (`channelstv.com` & broadcast channel)
   - **TVC News** (`tvcnews.tv`)
   - **Arise News** (`arisenews.tv`)
   - **NTA News** (`nta.ng`)
2. **Investigative & Digital Print Outlets**:
   - **Premium Times** (`premiumtimesng.com` - Pandora Papers, Alpha Beta, audits)
   - **The Punch** (`punchng.com`)
   - **Vanguard News** (`vanguardngr.com` - extensive 1999–2014 archives)
   - **TheCable** (`thecable.ng`)
   - **Daily Trust** (`dailytrust.com`)
   - **ThisDay Live** (`thisdaylive.com`)
3. **International Media**:
   - **BBC News** (`bbc.com`)
   - **CNN** (`cnn.com`)
   - **Reuters** (`reuters.com`)
4. **Archival Time Machines**:
   - **Wayback Machine (Internet Archive CDX API)**: Queries pre-redesign newspaper snapshots from 1999–2014.

---

## 🛠️ System Components

- `cli.py`: Unified Command-Line Interface for scraping, searching, quote extraction, timeline inspection, and dossier compilation.
- `core/database.py`: High-performance SQLite engine with **FTS5 (Full-Text Search)** virtual tables and SHA-256 deduplication.
- `extractors/`:
  - `parser.py`: Clean article body extraction via `trafilatura` and fallback HTML parsers.
  - `quote_miner.py`: Natural Language / regex rules identifying direct speech quotes attributed to candidates and speakers.
  - `classifier.py`: Automatically classifies articles into candidate, historical era, and thematic category.
- `scrapers/`:
  - `targeted_engine.py`: Multi-source crawler querying historical era keywords across selected domains.
  - `broadcast_engine.py`: Targeted scraper for TV broadcast bulletins and news hours.
  - `wayback_engine.py`: Scrapes archived 1999–2014 newspaper snapshots.
- `analysis/dossier_generator.py`: Generates the complete documentary script and comparative balance sheet markdown report.
- `web/`:
  - `dashboard.html`: Interactive dark-mode web application for browsing quotes, timeline milestones, and full-text searches.
  - `server.py`: Built-in zero-dependency HTTP server with JSON REST API.

---

## 🚀 Quickstart & Usage Guide

### 1. Initialize and Seed Curated Archive
Seed the database with verified judicial milestones, investigative records, and historical quotes:
```powershell
python cli.py init
```

### 2. Run Deep Multi-Source Scraping
Scrape live Nigerian news outlets (Premium Times, Punch, Vanguard, Channels TV, TVC, BBC):
```powershell
# Scrape both candidates
python cli.py scrape --candidate both --max-results 5

# Scrape specific candidate
python cli.py scrape --candidate tinubu
python cli.py scrape --candidate obi

# Enable Wayback Machine deep historical harvesting (1999–2014 snapshots)
python cli.py scrape --candidate both --deep
```

### 3. Check Database Stats
```powershell
python cli.py stats
```

### 4. Search Indexed Records (Instant SQLite FTS5)
Search by policy keywords, controversies, or phrases:
```powershell
python cli.py search "subsidy"
python cli.py search "strike"
python cli.py search "Alpha Beta"
python cli.py search "Pandora"
python cli.py search "SABMiller"
python cli.py search "Ezu River"
```

### 5. Inspect Direct Quotes and Verbatim Statements
Browse candidate statements extracted from media reports:
```powershell
# All quotes from Bola Ahmed Tinubu
python cli.py quotes --candidate tinubu

# All quotes from Peter Gregory Obi
python cli.py quotes --candidate obi

# Filter quotes by keyword
python cli.py quotes --keyword "money"
```

### 6. View Chronological Investigative Timeline
```powershell
python cli.py timeline
```

### 7. Generate Full Documentary Dossier
Compiles the latest database contents into a comprehensive investigative report:
```powershell
python cli.py dossier
```
The output is saved to: `dossiers/NIGERIA_POLITICAL_INVESTIGATIVE_DOSSIER.md`.

### 8. Launch Interactive Web Dashboard
Run the built-in dashboard server:
```powershell
python cli.py serve --port 8080
```
Then open your browser to: **`http://localhost:8080`** to interactively search quotes, filter candidate eras, view the timeline, and explore articles.
