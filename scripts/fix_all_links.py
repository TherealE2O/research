"""
Script to fix all live website and GitHub links across:
- README.md
- atiku.html
- notes_agent1.html to notes_agent5.html
"""

import os
import re

WORKSPACE = r"c:\Users\DELL\Documents\ai law"

# 1. Update README.md
readme_path = os.path.join(WORKSPACE, "README.md")
readme_content = """# Civic Lens Investigative Research Hub

Independent investigative research dossiers and primary documentary archives on Nigerian governance, political economy, and multinational corporate accountability.

**Live Web Portal:** [https://thereale2o.github.io/research/](https://thereale2o.github.io/research/)  
**Channel & Production:** Civic Lens Media (`@civiclensng`)  
**Editorial Standard:** Primary Judicial Records, Court Transcripts, Sworn Depositions, and Macroeconomic Audits  

---

## 🌐 Live Web Portal Access:
* **Home Page / All Inquiries:** [https://thereale2o.github.io/research/](https://thereale2o.github.io/research/)
* **Case File 01 (Bola Ahmed Tinubu):** [https://thereale2o.github.io/research/tinubu.html](https://thereale2o.github.io/research/tinubu.html)
* **Case File 02 (Atiku Abubakar):** [https://thereale2o.github.io/research/atiku.html](https://thereale2o.github.io/research/atiku.html)
* **Case File 03 (Big Tech Moderation Hubs):** [https://thereale2o.github.io/research/bigtech.html](https://thereale2o.github.io/research/bigtech.html)

---

## 1. Election Special: Bola Ahmed Tinubu (360° Forensic Audit)

* **Master Web Reader:** [https://thereale2o.github.io/research/tinubu.html](https://thereale2o.github.io/research/tinubu.html)
* **Master Markdown Dossier:** [`investigations/TINUBU_360_INVESTIGATIVE_DOSSIER.md`](investigations/TINUBU_360_INVESTIGATIVE_DOSSIER.md)

### Primary Deep-Dive Field Notes:

| File Reference | Scope & Era Covered | Live Web Reader | GitHub Markdown |
| :--- | :--- | :--- | :--- |
| **Field Note 01** | **Origins, CSU Deposition & 1993 US Court Forfeiture** (1952–1993) | [Web Reader](https://thereale2o.github.io/research/notes_agent1.html) | [Markdown](investigations/notes_agent1_origins_education_us_records.md) |
| **Field Note 02** | **3rd Republic Senate, June 12 & Radio Kudirat Resistance** (1992–1998) | [Web Reader](https://thereale2o.github.io/research/notes_agent2.html) | [Markdown](investigations/notes_agent2_nadeco_democracy_struggle.md) |
| **Field Note 03** | **Lagos Governorship Audit, IGR & Alpha-Beta Concession** (1999–2007) | [Web Reader](https://thereale2o.github.io/research/notes_agent3.html) | [Markdown](investigations/notes_agent3_lagos_governor_audit.md) |
| **Field Note 04** | **The Kingmaker Era, Party Mergers & Aso Rock Cold War** (2007–2023) | [Web Reader](https://thereale2o.github.io/research/notes_agent4.html) | [Markdown](investigations/notes_agent4_kingmaker_apc_rise.md) |
| **Field Note 05** | **The Presidency Audit, Economic Shocks & Official Defenses** (2023–Present) | [Web Reader](https://thereale2o.github.io/research/notes_agent5.html) | [Markdown](investigations/notes_agent5_presidency_policies_excuses.md) |

---

## 2. Election Special: Atiku Abubakar (360° Forensic Audit)

* **Master Web Reader:** [https://thereale2o.github.io/research/atiku.html](https://thereale2o.github.io/research/atiku.html)
* **Master Markdown Dossier:** [`investigations/ATIKU_360_INVESTIGATIVE_DOSSIER.md`](investigations/ATIKU_360_INVESTIGATIVE_DOSSIER.md)

### Primary Deep-Dive Field Notes:

| File Reference | Scope & Era Covered | Live Web Reader | GitHub Markdown |
| :--- | :--- | :--- | :--- |
| **Field Note 01** | **Origins, Jada Trust Territory, Dynastic Tree & Plebiscite** (1946–2023) | [Web Reader](https://thereale2o.github.io/research/atiku_notes_agent1.html) | [Markdown](investigations/atiku_notes_agent1_origins_family_citizenship.md) |
| **Field Note 02** | **20-Year Customs Career, 1984 53 Suitcases & INTELS Empire** (1969–1989) | [Web Reader](https://thereale2o.github.io/research/atiku_notes_agent2.html) | [Markdown](investigations/atiku_notes_agent2_customs_intels_wealth.md) |
| **Field Note 03** | **PDM Apprenticeship, 1993 Jos Deal & Economic Reform Era** (1989–2003) | [Web Reader](https://thereale2o.github.io/research/atiku_notes_agent3.html) | [Markdown](investigations/atiku_notes_agent3_politics_vp_reform_era.md) |
| **Field Note 04** | **Obasanjo War, Third Term Defeat, FBI Probe & US Senate Report** (2003–2010) | [Web Reader](https://thereale2o.github.io/research/atiku_notes_agent4.html) | [Markdown](investigations/atiku_notes_agent4_scandals_obasanjo_war.md) |
| **Field Note 05** | **30-Year Serial Candidacy, 2022 Zoning Breach & Final Ledger** (1993–2023) | [Web Reader](https://thereale2o.github.io/research/atiku_notes_agent5.html) | [Markdown](investigations/atiku_notes_agent5_candidacy_roadmap_verdict.md) |

---

## 3. Technology & Human Rights: Big Tech African Moderation Hubs

* **Master Web Reader:** [https://thereale2o.github.io/research/bigtech.html](https://thereale2o.github.io/research/bigtech.html)
* **Master Markdown Dossier:** [`investigations/SILICON_VALLEY_AFRICAN_SWEATSHOPS_DOSSIER.md`](investigations/SILICON_VALLEY_AFRICAN_SWEATSHOPS_DOSSIER.md)
* **Summary:** An investigation into Big Tech outsourcing toxic content moderation and AI data labeling to African workers in Nairobi.
"""

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(readme_content)
print("  [OK] Updated README.md with live GitHub Pages links")

# 2. Update atiku.html header GitHub Markdown link
atiku_path = os.path.join(WORKSPACE, "atiku.html")
with open(atiku_path, "r", encoding="utf-8") as f:
    atiku_html = f.read()

atiku_html = re.sub(
    r'href="https://github\.com/TherealE2O/research/blob/main/investigations/atiku_notes_agent1_origins_family_citizenship\.md"',
    'href="https://github.com/TherealE2O/research/blob/main/investigations/ATIKU_360_INVESTIGATIVE_DOSSIER.md"',
    atiku_html
)
with open(atiku_path, "w", encoding="utf-8") as f:
    f.write(atiku_html)
print("  [OK] Updated atiku.html header GitHub link to ATIKU_360_INVESTIGATIVE_DOSSIER.md")

# 3. Update notes_agent1.html to notes_agent5.html specific markdown links
tinubu_notes_map = {
    1: "notes_agent1_origins_education_us_records.md",
    2: "notes_agent2_nadeco_democracy_struggle.md",
    3: "notes_agent3_lagos_governor_audit.md",
    4: "notes_agent4_kingmaker_apc_rise.md",
    5: "notes_agent5_presidency_policies_excuses.md"
}

for i, md_name in tinubu_notes_map.items():
    file_path = os.path.join(WORKSPACE, f"notes_agent{i}.html")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
        html = re.sub(
            r'href="https://github\.com/TherealE2O/research/blob/main/investigations/TINUBU_360_INVESTIGATIVE_DOSSIER\.md"',
            f'href="https://github.com/TherealE2O/research/blob/main/investigations/{md_name}"',
            html
        )
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [OK] Updated notes_agent{i}.html header link to {md_name}")

