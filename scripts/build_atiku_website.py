"""
Build script to convert Atiku Abubakar investigative markdown dossiers into
broadsheet BBC/Reuters-style HTML readers and update index.html.
"""

import os
import re
import html
import markdown

WORKSPACE = r"c:\Users\DELL\Documents\ai law"
INVESTIGATIONS_DIR = os.path.join(WORKSPACE, "investigations")

DOSSIERS = [
    {
        "index": 1,
        "md_file": "atiku_notes_agent1_origins_family_citizenship.md",
        "html_file": "atiku_notes_agent1.html",
        "kicker": "Civic Lens Forensic Inquiry • Atiku Dossier File 01",
        "title": "Origins, Family Background, Dynastic Lineage & The 1961 UN Plebiscite Citizenship Challenge (1946–2023)",
        "subtitle": "Jada British Cameroons mandate, 1957 paternal drowning, 5 wives & 28 children across ethnic fault lines, ABU law diploma, and the 2019/2023 Supreme Court citizenship litigation."
    },
    {
        "index": 2,
        "md_file": "atiku_notes_agent2_customs_intels_wealth.md",
        "html_file": "atiku_notes_agent2.html",
        "kicker": "Civic Lens Forensic Inquiry • Atiku Dossier File 02",
        "title": "20-Year Customs Career, The 1984 '53 Suitcases' MMIA Breach & The INTELS Maritime Empire (1969–1989)",
        "subtitle": "From Idi-Iroko border cadet to Deputy Director of Customs; the Emir of Gwandu 53 suitcases clearance; Gabriele Volpi partnership, NICOTES Onne Port monopoly, and $100M+ divestment."
    },
    {
        "index": 3,
        "md_file": "atiku_notes_agent3_politics_vp_reform_era.md",
        "html_file": "atiku_notes_agent3.html",
        "kicker": "Civic Lens Forensic Inquiry • Atiku Dossier File 03",
        "title": "PDM Apprenticeship, The 1993 Jos SDP Primary Deal, Vice Presidency & The Economic Reform Era (1989–2003)",
        "subtitle": "Mentorship under Shehu Musa Yar'Adua; stepping down for M.K.O. Abiola; 1999 VP selection; 2001 GSM digital mobile auction; recruiting Okonjo-Iweala & El-Rufai; and the 2003 near-coup against Obasanjo."
    },
    {
        "index": 4,
        "md_file": "atiku_notes_agent4_scandals_obasanjo_war.md",
        "html_file": "atiku_notes_agent4.html",
        "kicker": "Civic Lens Forensic Inquiry • Atiku Dossier File 04",
        "title": "The Obasanjo War, Third Term Defeat, PTDF Slush Funds, FBI Freezer Sting & The US Senate $40M Report (2003–2010)",
        "subtitle": "Killing the 2006 Third Term Agenda; PTDF mutual counter-dossiers; William Jefferson $90k FBI freezer sting and Potomac raid; 2010 US Senate Levin money laundering findings; and Supreme Court victories on executive tenure."
    },
    {
        "index": 5,
        "md_file": "atiku_notes_agent5_candidacy_roadmap_verdict.md",
        "html_file": "atiku_notes_agent5.html",
        "kicker": "Civic Lens Forensic Inquiry • Atiku Dossier File 05",
        "title": "30-Year Serial Candidacy (1993–2023), The G5 Zoning Rupture, Economic Roadmap & Historical Balance Sheet",
        "subtitle": "Six presidential runs across four parties; Jan 2019 Trump Hotel DC breakthrough; May 2022 southern zoning breach and Wike/G5 revolt; AUN Yola business footprint; and the definitive historical ledger."
    }
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Civic Lens Investigation</title>
  <style>
    :root {{
      --font-headline: "Georgia", "Times New Roman", serif;
      --font-body: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-mono: "Consolas", "Courier New", monospace;
      
      --color-bg: #FFFFFF;
      --color-surface: #F8F9FA;
      --color-surface-subtle: #F1F5F9;
      --color-border: #D1D5DB;
      --color-border-dark: #111827;
      --color-text: #111827;
      --color-text-secondary: #374151;
      --color-text-muted: #6B7280;
      --color-link: #1D4ED8;
      --color-link-hover: #1E40AF;
      --color-accent-red: #B91C1C;
      --color-accent-blue: #1D4ED8;
      --color-accent-green: #15803d;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      background-color: var(--color-bg);
      color: var(--color-text);
      font-family: var(--font-body);
      font-size: 16px;
      line-height: 1.75;
      -webkit-font-smoothing: antialiased;
    }}

    .pub-header {{
      border-top: 4px solid var(--color-border-dark);
      border-bottom: 1px solid var(--color-border);
      background: #FFFFFF;
      position: sticky;
      top: 0;
      z-index: 100;
    }}

    .pub-header-inner {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }}

    .pub-brand {{
      font-family: var(--font-headline);
      font-size: 19px;
      font-weight: 700;
      color: var(--color-text);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    .nav-back-link {{
      font-size: 13px;
      font-weight: 600;
      color: var(--color-link);
      text-decoration: none;
    }}
    .nav-back-link:hover {{ text-decoration: underline; }}

    .article-container {{
      max-width: 880px;
      margin: 0 auto;
      padding: 36px 20px 100px;
    }}

    .inquiry-kicker {{
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--color-accent-red);
      margin-bottom: 10px;
    }}

    h1.inquiry-title {{
      font-family: var(--font-headline);
      font-size: 34px;
      line-height: 1.25;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 14px;
      color: var(--color-text);
    }}

    .inquiry-meta-bar {{
      border-top: 1px solid var(--color-border);
      border-bottom: 1px solid var(--color-border);
      padding: 12px 0;
      margin: 20px 0 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 13px;
      color: var(--color-text-secondary);
    }}

    .inquiry-meta-bar strong {{ color: var(--color-text); }}

    .file-pill {{
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 12px;
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      padding: 3px 8px;
    }}

    h2 {{
      font-family: var(--font-headline);
      font-size: 24px;
      line-height: 1.35;
      margin: 40px 0 16px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--color-border);
      color: var(--color-text);
    }}

    h3 {{
      font-family: var(--font-headline);
      font-size: 19px;
      line-height: 1.4;
      margin: 28px 0 12px;
      color: var(--color-text);
    }}

    h4 {{
      font-size: 16px;
      font-weight: 700;
      margin: 20px 0 8px;
      color: var(--color-text);
    }}

    p {{ margin-bottom: 18px; color: var(--color-text); }}

    ul, ol {{
      margin: 0 0 20px 24px;
    }}
    li {{ margin-bottom: 8px; }}

    pre {{
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      padding: 14px;
      font-family: var(--font-mono);
      font-size: 13px;
      overflow-x: auto;
      margin: 20px 0;
      line-height: 1.45;
    }}

    .mermaid {{
      background: #FFFFFF;
      border: 1.5px solid var(--color-border);
      padding: 24px 16px;
      margin: 24px 0;
      display: flex;
      justify-content: center;
      overflow-x: auto;
      border-radius: 2px;
    }}

    blockquote {{
      border-left: 3px solid var(--color-border-dark);
      padding: 12px 18px;
      margin: 20px 0;
      background: var(--color-surface);
      font-style: italic;
    }}

    blockquote p {{ margin-bottom: 6px; }}

    .source-box {{
      border: 1px solid var(--color-border);
      border-left: 4px solid var(--color-border-dark);
      background: var(--color-surface);
      padding: 14px 18px;
      margin: 20px 0;
      font-size: 14.5px;
    }}

    a {{ color: var(--color-link); text-decoration: underline; }}
    a:hover {{ color: var(--color-link-hover); }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 22px 0;
      font-size: 14px;
      border: 1px solid var(--color-border);
    }}
    th, td {{
      padding: 10px 14px;
      border: 1px solid var(--color-border);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: var(--color-surface-subtle);
      font-weight: 700;
      color: var(--color-text);
    }}
    tr:nth-child(even) td {{
      background: #FAFAFA;
    }}

    hr {{
      border: 0;
      border-top: 1px solid var(--color-border);
      margin: 36px 0;
    }}

    footer {{
      border-top: 1px solid var(--color-border);
      background: var(--color-surface);
      padding: 24px 20px;
      text-align: center;
      font-size: 12.5px;
      color: var(--color-text-muted);
    }}
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      mermaid.initialize({{
        startOnLoad: true,
        theme: 'neutral',
        securityLevel: 'loose',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
      }});
    }});
  </script>
</head>
<body>
  <header class="pub-header">
    <div class="pub-header-inner">
      <a href="index.html" class="pub-brand">
        CIVIC LENS <span>INVESTIGATIONS</span>
      </a>
      <div style="display: flex; gap: 16px; align-items: center;">
        <a href="index.html" class="nav-back-link">← Master Dossier Portal</a>
        <a href="https://github.com/TherealE2O/research/blob/main/investigations/{md_file}" target="_blank" rel="noopener" class="nav-back-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>
      </div>
    </div>
  </header>

  <main class="article-container">
    <div class="inquiry-kicker">{kicker}</div>
    <h1 class="inquiry-title">{title}</h1>
    
    <div class="inquiry-meta-bar">
      <div>Primary Field File: <span class="file-pill">{md_file}</span></div>
      <div>Editorial Standard: <strong>Reuters / BBC Investigative Broadsheet</strong></div>
    </div>

    <article>
{content}
    </article>
  </main>

  <footer>
    <p>CIVIC LENS INVESTIGATIVE DESK • SPECIAL ARCHIVAL DOSSIER</p>
    <p style="margin-top: 6px;">All findings compiled from sworn court transcripts, primary judicial dockets, and verified on-the-ground investigative reporting.</p>
  </footer>
</body>
</html>
"""

def extract_and_convert(md_text):
    # Normalize multiple backtick mermaid fences
    mermaid_blocks = []
    
    def store_mermaid(match):
        code = match.group(1).strip()
        idx = len(mermaid_blocks)
        mermaid_blocks.append(code)
        return f"\n\nQQQMERMAIDBLOCK{idx}QQQ\n\n"

    # Match ```mermaid ... ``` or ````mermaid ... ````
    pattern = r"`{3,}\s*mermaid\s*\n([\s\S]*?)\n\s*`{3,}"
    processed_text = re.sub(pattern, store_mermaid, md_text)
    
    html_content = markdown.markdown(
        processed_text,
        extensions=['extra', 'tables', 'fenced_code', 'nl2br']
    )
    
    # Restore mermaid blocks as <div class="mermaid">
    for idx, code in enumerate(mermaid_blocks):
        clean_code = html.unescape(code)
        placeholder = f"<p>QQQMERMAIDBLOCK{idx}QQQ</p>"
        placeholder2 = f"QQQMERMAIDBLOCK{idx}QQQ"
        mermaid_tag = f'<div class="mermaid">\n{clean_code}\n</div>'
        if placeholder in html_content:
            html_content = html_content.replace(placeholder, mermaid_tag)
        else:
            html_content = html_content.replace(placeholder2, mermaid_tag)
            
    return html_content

def main():
    print("Building Atiku Abubakar HTML deep-dive files...")
    for item in DOSSIERS:
        md_path = os.path.join(INVESTIGATIONS_DIR, item["md_file"])
        html_path = os.path.join(WORKSPACE, item["html_file"])
        
        if not os.path.exists(md_path):
            print(f"Error: {md_path} does not exist.")
            continue
            
        with open(md_path, "r", encoding="utf-8") as f:
            raw_md = f.read()
            
        content_html = extract_and_convert(raw_md)
        
        full_html = HTML_TEMPLATE.format(
            title=item["title"],
            kicker=item["kicker"],
            md_file=item["md_file"],
            content=content_html
        )
        
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(full_html)
            
        print(f"  [OK] Generated: {item['html_file']} ({len(full_html):,} bytes)")

if __name__ == "__main__":
    main()
