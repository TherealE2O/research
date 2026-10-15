"""
Update navigation breadcrumbs across all notes files:
- notes_agent1.html through notes_agent5.html (Tinubu)
- atiku_notes_agent1.html through atiku_notes_agent5.html (Atiku)
"""

import os
import re

WORKSPACE = r"c:\Users\DELL\Documents\ai law"

# 1. Update notes_agent1.html to notes_agent5.html
for i in range(1, 6):
    file_path = os.path.join(WORKSPACE, f"notes_agent{i}.html")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Update the header nav links
        pattern = r'<div style="display: flex; gap: 16px; align-items: center;">[\s\S]*?</div>\s*</div>\s*</header>'
        replacement = """<div style="display: flex; gap: 16px; align-items: center;">
        <a href="index.html" class="nav-back-link">← Home</a>
        <a href="tinubu.html" class="nav-back-link">Tinubu Master Dossier</a>
        <a href="https://github.com/TherealE2O/research/blob/main/investigations/TINUBU_360_INVESTIGATIVE_DOSSIER.md" target="_blank" rel="noopener" class="nav-back-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>
      </div>
    </div>
  </header>"""
        new_html = re.sub(pattern, replacement, html, count=1)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  [OK] Updated nav in notes_agent{i}.html")

# 2. Update build_atiku_website.py template and re-run it
build_script = os.path.join(WORKSPACE, "scripts", "build_atiku_website.py")
with open(build_script, "r", encoding="utf-8") as f:
    b_code = f.read()

old_atiku_nav = """      <div style="display: flex; gap: 16px; align-items: center;">
        <a href="index.html" class="nav-back-link">← Master Dossier Portal</a>
        <a href="https://github.com/TherealE2O/research/blob/main/investigations/{md_file}" target="_blank" rel="noopener" class="nav-back-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>
      </div>"""

new_atiku_nav = """      <div style="display: flex; gap: 16px; align-items: center;">
        <a href="index.html" class="nav-back-link">← Home</a>
        <a href="atiku.html" class="nav-back-link">Atiku Master Dossier</a>
        <a href="https://github.com/TherealE2O/research/blob/main/investigations/{md_file}" target="_blank" rel="noopener" class="nav-back-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>
      </div>"""

if old_atiku_nav in b_code:
    b_code = b_code.replace(old_atiku_nav, new_atiku_nav)
    with open(build_script, "w", encoding="utf-8") as f:
        f.write(b_code)
    print("  [OK] Updated build_atiku_website.py")

