"""
Rearchitect the Civic Lens Investigative Portal:
1. Extract Tinubu Master Dossier -> tinubu.html
2. Extract Atiku Master Dossier -> atiku.html
3. Extract Big Tech African Hubs -> bigtech.html
4. Build a prestigious, clean, editorial Home Page -> index.html
5. Update header navigation in notes_agent*.html and atiku_notes_agent*.html
"""

import os
import re

WORKSPACE = r"c:\Users\DELL\Documents\ai law"

with open(os.path.join(WORKSPACE, "index.html"), "r", encoding="utf-8") as f:
    full_index = f.read()

# Common head & styles
HEAD_AND_CSS = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} — Civic Lens Investigative Desk</title>
  <meta name="description" content="{desc}">
  <style>
    :root {
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
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--color-bg);
      color: var(--color-text);
      font-family: var(--font-body);
      font-size: 16px;
      line-height: 1.75;
      -webkit-font-smoothing: antialiased;
    }

    .pub-header {
      border-top: 4px solid var(--color-border-dark);
      border-bottom: 1px solid var(--color-border);
      background: #FFFFFF;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .pub-header-inner {
      max-width: 1080px;
      margin: 0 auto;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }

    .pub-brand {
      font-family: var(--font-headline);
      font-size: 19px;
      font-weight: 700;
      color: var(--color-text);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .pub-tagline {
      font-family: var(--font-body);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      font-weight: 600;
      color: var(--color-accent-red);
      border-left: 1px solid var(--color-border);
      padding-left: 12px;
    }

    .nav-links {
      display: flex;
      gap: 16px;
      align-items: center;
      font-size: 13.5px;
      font-weight: 600;
    }

    .nav-link {
      color: var(--color-link);
      text-decoration: none;
    }
    .nav-link:hover { text-decoration: underline; }

    .article-container {
      max-width: 880px;
      margin: 0 auto;
      padding: 36px 20px 100px;
    }

    .inquiry-kicker {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--color-accent-red);
      margin-bottom: 10px;
    }

    h1.inquiry-title {
      font-family: var(--font-headline);
      font-size: 36px;
      line-height: 1.22;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 16px;
      color: var(--color-text);
    }

    .inquiry-deck {
      font-family: var(--font-headline);
      font-size: 20px;
      line-height: 1.45;
      font-style: italic;
      color: var(--color-text-secondary);
      margin-bottom: 24px;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--color-border);
    }

    .metadata-bar {
      font-size: 13px;
      color: var(--color-text-muted);
      margin-bottom: 32px;
      display: flex;
      flex-wrap: wrap;
      gap: 16px;
      border-bottom: 1px solid var(--color-border);
      padding-bottom: 14px;
    }
    .metadata-item strong { color: var(--color-text); }

    .table-of-contents {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      padding: 20px 24px;
      margin-bottom: 44px;
    }

    .toc-title {
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--color-text);
      margin-bottom: 12px;
    }

    .toc-list {
      list-style-type: none;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px 24px;
    }
    @media (max-width: 680px) {
      .toc-list { grid-template-columns: 1fr; }
    }

    .toc-list a {
      color: var(--color-link);
      text-decoration: none;
      font-size: 13.5px;
    }
    .toc-list a:hover { text-decoration: underline; }

    article p {
      margin-bottom: 20px;
      color: var(--color-text);
      font-size: 16.5px;
      line-height: 1.75;
    }

    article h2 {
      font-family: var(--font-headline);
      font-size: 26px;
      line-height: 1.3;
      font-weight: 700;
      margin: 48px 0 18px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--color-border-dark);
      scroll-margin-top: 80px;
    }

    article h3 {
      font-family: var(--font-headline);
      font-size: 19px;
      line-height: 1.4;
      font-weight: 700;
      margin: 28px 0 12px;
      color: var(--color-text);
    }

    article ul, article ol {
      margin: 16px 0 24px 24px;
      font-size: 16px;
      line-height: 1.7;
    }
    article li { margin-bottom: 10px; }

    .primary-source-box {
      border: 1px solid var(--color-border);
      border-left: 4px solid var(--color-border-dark);
      background: var(--color-surface);
      padding: 16px 20px;
      margin: 24px 0;
      font-size: 14.5px;
    }
    .primary-source-box.alert {
      border-left-color: var(--color-accent-red);
    }
    .source-box-title {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--color-text-secondary);
      margin-bottom: 6px;
    }
    .source-box-title.red { color: var(--color-accent-red); }

    .source-link-action {
      display: block;
      margin-top: 10px;
      font-weight: 600;
    }
    .source-link-action a {
      color: var(--color-link);
      text-decoration: underline;
    }

    blockquote.formal-quote {
      border-left: 3px solid var(--color-border-dark);
      padding: 12px 20px;
      margin: 24px 0;
      background: #FFFFFF;
    }
    blockquote.formal-quote p {
      font-family: var(--font-headline);
      font-size: 17.5px;
      line-height: 1.6;
      font-style: italic;
      color: #1F2937;
      margin-bottom: 8px;
    }
    .quote-citation {
      font-family: var(--font-body);
      font-size: 13px;
      font-style: normal;
      font-weight: 600;
      color: var(--color-text-secondary);
    }

    .table-wrapper {
      margin: 28px 0;
      border: 1px solid var(--color-border);
      overflow-x: auto;
    }
    table.report-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
      text-align: left;
    }
    table.report-table th, table.report-table td {
      padding: 10px 14px;
      border-bottom: 1px solid var(--color-border);
    }
    table.report-table th {
      background: var(--color-surface);
      font-weight: 700;
      color: var(--color-text);
      border-bottom: 2px solid var(--color-border);
    }

    .sources-section {
      margin-top: 60px;
      padding-top: 30px;
      border-top: 2px solid var(--color-border-dark);
    }
    .sources-title {
      font-family: var(--font-headline);
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 18px;
    }
    .sources-list {
      list-style-type: decimal;
      padding-left: 20px;
      font-size: 13.5px;
      line-height: 1.6;
      color: var(--color-text-secondary);
    }
    .sources-list li { margin-bottom: 10px; }
    .sources-list a {
      color: var(--color-link);
      text-decoration: underline;
      word-break: break-all;
    }

    footer {
      border-top: 1px solid var(--color-border);
      background: var(--color-surface);
      padding: 30px 20px;
      text-align: center;
      font-size: 13px;
      color: var(--color-text-muted);
    }

    /* Diagram visual components */
    .visual-diagram-card {
      background: #FFFFFF;
      border: 2px solid var(--color-border-dark);
      padding: 24px;
      margin: 28px 0;
    }
    .diagram-kicker {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--color-accent-red);
      margin-bottom: 6px;
    }
    .diagram-desc {
      font-size: 14.5px;
      color: var(--color-text-secondary);
      margin-bottom: 20px;
    }
    .diagram-columns {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 18px;
      margin-bottom: 18px;
    }
    .diagram-column {
      padding: 18px;
      border-width: 1.5px;
      border-style: solid;
    }
    .diagram-node {
      background: #FFFFFF;
      padding: 12px 14px;
      margin-bottom: 8px;
      border-width: 1px;
      border-style: solid;
    }
    .diagram-arrow {
      text-align: center;
      font-weight: bold;
      font-size: 12px;
      margin: 2px 0 8px;
    }
    .mermaid {
      background: #FFFFFF;
      border: 1.5px solid var(--color-border);
      padding: 24px 16px;
      margin: 24px 0;
      display: flex;
      justify-content: center;
      overflow-x: auto;
      border-radius: 2px;
    }
  </style>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      mermaid.initialize({
        startOnLoad: true,
        theme: 'neutral',
        securityLevel: 'loose',
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
      });
    });
  </script>
</head>
<body>
  <header class="pub-header">
    <div class="pub-header-inner">
      <div style="display: flex; align-items: center; gap: 12px;">
        <a href="index.html" class="pub-brand">CIVIC LENS INVESTIGATIONS</a>
        <span class="pub-tagline">Primary Evidence Desk</span>
      </div>
      <nav class="nav-links">
        <a href="index.html" class="nav-link">← Home (All Inquiries)</a>
        <a href="{github_url}" target="_blank" rel="noopener" class="nav-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>
      </nav>
    </div>
  </header>

{main_body}

  <footer>
    <p>CIVIC LENS INVESTIGATIVE DESK • SPECIAL FACTUAL ARCHIVE</p>
    <p style="margin-top: 6px;">All findings compiled from sworn court transcripts, primary judicial dockets, and verified on-the-ground investigative reporting.</p>
  </footer>
</body>
</html>
"""

# Extract the body of each inquiry
tinubu_match = re.search(r'<main class="article-container" id="inquiry-tinubu">([\s\S]*?)</main>', full_index)
atiku_match = re.search(r'<main class="article-container" id="inquiry-atiku"[^>]*>([\s\S]*?)</main>', full_index)
meta_match = re.search(r'<main class="article-container" id="inquiry-meta"[^>]*>([\s\S]*?)</main>', full_index)

def render_page(title, desc, github_url, main_body):
    res = HEAD_AND_CSS
    res = res.replace("{title}", title)
    res = res.replace("{desc}", desc)
    res = res.replace("{github_url}", github_url)
    res = res.replace("{main_body}", main_body)
    return res

if tinubu_match:
    tinubu_body = f'<main class="article-container" id="inquiry-tinubu">{tinubu_match.group(1)}</main>'
    tinubu_page = render_page(
        title="Bola Ahmed Tinubu: 360° Forensic Audit",
        desc="A forensic investigation into Bola Ahmed Tinubu's origins, financial networks, Chicago court records, and state power.",
        github_url="https://github.com/TherealE2O/research/blob/main/investigations/TINUBU_360_INVESTIGATIVE_DOSSIER.md",
        main_body=tinubu_body
    )
    with open(os.path.join(WORKSPACE, "tinubu.html"), "w", encoding="utf-8") as f:
        f.write(tinubu_page)
    print("  [OK] Generated tinubu.html")

if atiku_match:
    atiku_body = f'<main class="article-container" id="inquiry-atiku">{atiku_match.group(1)}</main>'
    atiku_body = atiku_body.replace('style="display: none;"', '')
    atiku_page = render_page(
        title="Atiku Abubakar: 360° Forensic Audit",
        desc="A forensic investigation into Atiku Abubakar's origins, port logistics monopoly, reform architecture, and 30-year ambition.",
        github_url="https://github.com/TherealE2O/research/blob/main/investigations/atiku_notes_agent1_origins_family_citizenship.md",
        main_body=atiku_body
    )
    with open(os.path.join(WORKSPACE, "atiku.html"), "w", encoding="utf-8") as f:
        f.write(atiku_page)
    print("  [OK] Generated atiku.html")

if meta_match:
    meta_body = f'<main class="article-container" id="inquiry-meta">{meta_match.group(1)}</main>'
    meta_body = meta_body.replace('style="display: none;"', '')
    meta_page = render_page(
        title="Silicon Valley's African Trauma Factory",
        desc="How Big Tech outsources graphic content moderation and AI data labeling to Kenya and Nigeria.",
        github_url="https://github.com/TherealE2O/research/blob/main/investigations/SILICON_VALLEY_AFRICAN_SWEATSHOPS_DOSSIER.md",
        main_body=meta_body
    )
    with open(os.path.join(WORKSPACE, "bigtech.html"), "w", encoding="utf-8") as f:
        f.write(meta_page)
    print("  [OK] Generated bigtech.html")

# Now let's construct the prestigious, clean, editorial Home Page in index.html
HOME_PAGE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Civic Lens Investigative Desk | Primary Evidence Portal</title>
  <meta name="description" content="Independent investigative journalism and primary source archives on Nigerian governance, political economy, and corporate accountability.">
  <style>
    :root {
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
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background-color: var(--color-bg);
      color: var(--color-text);
      font-family: var(--font-body);
      font-size: 16px;
      line-height: 1.7;
      -webkit-font-smoothing: antialiased;
    }

    /* TOP PUBLICATION HEADER */
    .pub-header {
      border-top: 4px solid var(--color-border-dark);
      border-bottom: 1px solid var(--color-border);
      background: #FFFFFF;
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .pub-header-inner {
      max-width: 1080px;
      margin: 0 auto;
      padding: 16px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }

    .pub-brand {
      font-family: var(--font-headline);
      font-size: 22px;
      font-weight: 700;
      letter-spacing: 0.5px;
      color: var(--color-text);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .pub-tagline {
      font-family: var(--font-body);
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      font-weight: 600;
      color: var(--color-accent-red);
      border-left: 1px solid var(--color-border);
      padding-left: 12px;
    }

    .nav-links {
      display: flex;
      gap: 20px;
      font-size: 13.5px;
      font-weight: 600;
    }
    .nav-link {
      color: var(--color-text-secondary);
      text-decoration: none;
    }
    .nav-link:hover { color: var(--color-link); }

    /* HOME HERO BANNER */
    .home-hero {
      border-bottom: 2px solid var(--color-border-dark);
      background: var(--color-surface);
      padding: 44px 20px 36px;
    }

    .hero-container {
      max-width: 1080px;
      margin: 0 auto;
    }

    .hero-kicker {
      font-size: 12px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--color-accent-red);
      margin-bottom: 8px;
    }

    .hero-title {
      font-family: var(--font-headline);
      font-size: 38px;
      line-height: 1.2;
      font-weight: 700;
      color: var(--color-text);
      margin-bottom: 12px;
    }

    .hero-sub {
      font-family: var(--font-headline);
      font-size: 19px;
      line-height: 1.5;
      font-style: italic;
      color: var(--color-text-secondary);
      max-width: 860px;
      margin-bottom: 20px;
    }

    .standards-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 24px;
      font-size: 13px;
      color: var(--color-text-muted);
      border-top: 1px solid var(--color-border);
      padding-top: 14px;
    }
    .standards-bar strong { color: var(--color-text); }

    /* MAIN INQUIRIES CONTAINER */
    .main-content {
      max-width: 1080px;
      margin: 0 auto;
      padding: 44px 20px 80px;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      border-bottom: 2px solid var(--color-border-dark);
      padding-bottom: 10px;
      margin-bottom: 32px;
    }

    .section-title {
      font-family: var(--font-headline);
      font-size: 22px;
      font-weight: 700;
      color: var(--color-text);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .section-counter {
      font-size: 13px;
      font-weight: 600;
      color: var(--color-text-muted);
    }

    /* INQUIRY CARD COMPONENT */
    .inquiry-grid {
      display: flex;
      flex-direction: column;
      gap: 36px;
    }

    .inquiry-card {
      border: 1px solid var(--color-border);
      background: #FFFFFF;
      transition: border-color 0.2s ease, box-shadow 0.2s ease;
      display: grid;
      grid-template-columns: 1fr;
    }
    .inquiry-card:hover {
      border-color: var(--color-border-dark);
      box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .card-inner {
      padding: 32px 36px;
    }

    .card-kicker-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 12px;
    }

    .card-badge {
      font-size: 11.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--color-accent-red);
    }

    .card-meta {
      font-size: 12.5px;
      color: var(--color-text-muted);
      font-family: var(--font-mono);
    }

    .card-title {
      font-family: var(--font-headline);
      font-size: 28px;
      line-height: 1.25;
      font-weight: 700;
      color: var(--color-text);
      margin-bottom: 10px;
    }
    .card-title a {
      color: var(--color-text);
      text-decoration: none;
    }
    .card-title a:hover {
      color: var(--color-link);
    }

    .card-deck {
      font-family: var(--font-headline);
      font-size: 17px;
      line-height: 1.5;
      font-style: italic;
      color: var(--color-text-secondary);
      margin-bottom: 18px;
    }

    .card-points {
      margin: 16px 0 24px 20px;
      font-size: 15px;
      color: var(--color-text);
      line-height: 1.65;
    }
    .card-points li { margin-bottom: 8px; }

    /* ACTION BAR */
    .card-actions {
      border-top: 1px solid var(--color-border);
      padding-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }

    .btn-primary {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: var(--color-border-dark);
      color: #FFFFFF;
      padding: 10px 22px;
      font-size: 13.5px;
      font-weight: 600;
      text-decoration: none;
      letter-spacing: 0.3px;
      transition: background 0.2s ease;
    }
    .btn-primary:hover {
      background: var(--color-link-hover);
      color: #FFFFFF;
    }

    .deep-dive-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      font-size: 12.5px;
    }

    .pill-label {
      font-weight: 700;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.8px;
      color: var(--color-text-muted);
    }

    .field-link {
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      color: var(--color-link);
      padding: 4px 10px;
      text-decoration: none;
      font-weight: 600;
      border-radius: 2px;
      transition: background 0.15s ease, border-color 0.15s ease;
    }
    .field-link:hover {
      background: var(--color-surface-subtle);
      border-color: var(--color-link);
    }

    /* UPCOMING INQUIRIES */
    .pipeline-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin-top: 24px;
    }

    .pipeline-card {
      border: 1px solid var(--color-border);
      background: var(--color-surface);
      padding: 22px;
    }
    .pipeline-badge {
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--color-text-muted);
      margin-bottom: 6px;
    }
    .pipeline-title {
      font-family: var(--font-headline);
      font-size: 18px;
      font-weight: 700;
      color: var(--color-text);
      margin-bottom: 8px;
    }
    .pipeline-desc {
      font-size: 13.5px;
      color: var(--color-text-secondary);
      line-height: 1.55;
    }

    /* FOOTER */
    footer {
      border-top: 2px solid var(--color-border-dark);
      background: var(--color-surface);
      padding: 36px 20px;
      text-align: center;
      font-size: 13px;
      color: var(--color-text-muted);
    }
    footer a { color: var(--color-link); text-decoration: none; }
    footer a:hover { text-decoration: underline; }
  </style>
</head>
<body>

  <!-- PUBLICATION HEADER -->
  <header class="pub-header">
    <div class="pub-header-inner">
      <div style="display: flex; align-items: center; gap: 12px;">
        <a href="index.html" class="pub-brand">CIVIC LENS INVESTIGATIONS</a>
        <span class="pub-tagline">Primary Evidence Desk</span>
      </div>

      <nav class="nav-links">
        <a href="#inquiries" class="nav-link">Active Inquiries</a>
        <a href="#pipeline" class="nav-link">Investigation Docket</a>
        <a href="https://github.com/TherealE2O/research" target="_blank" rel="noopener" class="nav-link">GitHub Archive ↗</a>
      </nav>
    </div>
  </header>

  <!-- HOME HERO BANNER -->
  <section class="home-hero">
    <div class="hero-container">
      <div class="hero-kicker">Open-Source Intelligence • Primary Judicial Records • Forensic Analysis</div>
      <h1 class="hero-title">The Primary Evidence Desk</h1>
      <p class="hero-sub">
        Exhaustive, verifiable investigative dossiers on Nigerian political leadership, sovereign wealth management, and corporate accountability. Zero creative embellishment; strictly verified judicial records, sworn depositions, and macroeconomic audits.
      </p>

      <div class="standards-bar">
        <span><strong>Editorial Rule:</strong> Direct Judicial Dockets & Sworn Testimony Verified</span>
        <span><strong>Primary Repositories:</strong> Supreme Court of Nigeria • US Federal Courts • US Senate Levin Committee</span>
        <span><strong>Format:</strong> Broadsheet Executive Dossiers & Uncompressed Field Notes</span>
      </div>
    </div>
  </section>

  <!-- ACTIVE INQUIRIES -->
  <main class="main-content" id="inquiries">
    <div class="section-header">
      <h2 class="section-title">Active Forensic Inquiries</h2>
      <span class="section-counter">3 Major Case Files Published</span>
    </div>

    <div class="inquiry-grid">

      <!-- INQUIRY 1: TINUBU -->
      <article class="inquiry-card">
        <div class="card-inner">
          <div class="card-kicker-row">
            <span class="card-badge">Case File 01 • National Governance & State Power</span>
            <span class="card-meta">FILE ID: CL-BAT-1952-2026 • 100+ KB PRIMARY ARCHIVE</span>
          </div>

          <h3 class="card-title">
            <a href="tinubu.html">Bola Ahmed Tinubu: A Forensic Investigation into Origins, Financial Networks, and State Power (1952–2026)</a>
          </h3>

          <p class="card-deck">
            An exhaustive factual audit examining Chicago court forfeiture records, academic certifications, the Lagos revenue architecture, and the macroeconomic realities of Nigeria's 16th Presidency.
          </p>

          <ul class="card-points">
            <li><strong>Origins & Chicago Deposition:</strong> Iragbiji roots, maternal kinship with Gboyega Oyetola, and Registrar Caleb Westberg’s sworn October 2023 deposition on CSU admission, graduation, and replacement diploma discrepancies.</li>
            <li><strong>The $460,000 Chicago Forfeiture:</strong> US District Court Case 93 C 4483 compromise order signed by Judge John A. Nordberg; civil in rem forfeiture vs. criminal conviction distinctions.</li>
            <li><strong>The Lagos Revenue Machine:</strong> Internally Generated Revenue expansion from ₦600M to ₦8.2B/month; the Alpha-Beta exclusive concession, Dapo Apara’s 2020 High Court litigation, and the 2019 Bourdillon bullion vans.</li>
            <li><strong>Presidency Audit & Macroeconomic Medicine:</strong> Day-one petrol subsidy abolition, currency floating (₦460 to ₦1,650/$), ₦150B Airbus A330 jet purchase, direct LGA autonomy (SC/CV/343/2024), and the administration's ₦30T Ways & Means deficit defense.</li>
          </ul>

          <div class="card-actions">
            <a href="tinubu.html" class="btn-primary">
              Open Master Dossier →
            </a>

            <div class="deep-dive-pills">
              <span class="pill-label">Field Files:</span>
              <a href="notes_agent1.html" class="field-link">01: Origins & CSU (56 KB)</a>
              <a href="notes_agent2.html" class="field-link">02: Senate & June 12 (59 KB)</a>
              <a href="notes_agent3.html" class="field-link">03: Lagos Governor (62 KB)</a>
              <a href="notes_agent4.html" class="field-link">04: Kingmaker Era (92 KB)</a>
              <a href="notes_agent5.html" class="field-link">05: Presidency (40 KB)</a>
            </div>
          </div>
        </div>
      </article>

      <!-- INQUIRY 2: ATIKU ABUBAKAR -->
      <article class="inquiry-card">
        <div class="card-inner">
          <div class="card-kicker-row">
            <span class="card-badge">Case File 02 • Political Economy & Sovereign Wealth</span>
            <span class="card-meta">FILE ID: CL-AA-1946-2026 • 300+ KB PRIMARY ARCHIVE</span>
          </div>

          <h3 class="card-title">
            <a href="atiku.html">Atiku Abubakar: A Forensic Investigation into Origins, Port Logistics Monopoly, Reform Architecture, and 30-Year Presidential Ambition (1946–2026)</a>
          </h3>

          <p class="card-deck">
            An exhaustive factual audit examining the 1961 UN plebiscite citizenship challenge, the 1984 53 suitcases customs breach, the Onne Port/INTELS logistics monopoly, the 2001 GSM revolution, the William Jefferson FBI freezer sting, the 2010 US Senate Levin $40M money laundering findings, and the 2022 zoning rupture.
          </p>

          <ul class="card-points">
            <li><strong>Origins & Plebiscite Citizenship:</strong> Jada British Northern Cameroons UN mandate; 1957 paternal drowning; 5 wives and 28 children across Yoruba, Igbo, and Fulani ties; Supreme Court citizenship ruling (SC.348/2023).</li>
            <li><strong>20-Year Customs Career & 53 Suitcases:</strong> From Idi-Iroko border cadet to Deputy Director; the April 1984 MMIA luggage clearance under Buhari's military regime; armed soldiers overriding civilian customs inspection.</li>
            <li><strong>The INTELS Port Monopoly:</strong> Co-founding NICOTES with Gabriele Volpi & Shehu Yar'Adua; Onne Port dedicated free zone; 28% NPA revenue commission; constitutional civil service conflict of interest; $100M+ family divestment.</li>
            <li><strong>Reforms, Third Term & Foreign Inquiries:</strong> 2001 GSM spectrum auction ($285M); recruiting Okonjo-Iweala & El-Rufai; killing Obasanjo’s 2006 Third Term; PTDF mutual counter-dossiers; William Jefferson $90k FBI freezer sting; 2010 US Senate Levin Report documenting $40M suspect wire inflows.</li>
            <li><strong>The 30-Year Ambition:</strong> 6 presidential runs (1993–2023); May 2022 southern zoning breach; G5/Wike revolt; opposition fracture arithmetic (14.58M opposition votes vs. Tinubu's 8.79M).</li>
          </ul>

          <div class="card-actions">
            <a href="atiku.html" class="btn-primary">
              Open Master Dossier →
            </a>

            <div class="deep-dive-pills">
              <span class="pill-label">Field Files:</span>
              <a href="atiku_notes_agent1.html" class="field-link">01: Origins & Family (61 KB)</a>
              <a href="atiku_notes_agent2.html" class="field-link">02: Customs & INTELS (59 KB)</a>
              <a href="atiku_notes_agent3.html" class="field-link">03: VP Reforms & PDM (66 KB)</a>
              <a href="atiku_notes_agent4.html" class="field-link">04: Scandals & US Senate (64 KB)</a>
              <a href="atiku_notes_agent5.html" class="field-link">05: Candidacy & Verdict (51 KB)</a>
            </div>
          </div>
        </div>
      </article>

      <!-- INQUIRY 3: BIG TECH MODERATION HUBS -->
      <article class="inquiry-card">
        <div class="card-inner">
          <div class="card-kicker-row">
            <span class="card-badge">Case File 03 • Technology & Labor Human Rights</span>
            <span class="card-meta">FILE ID: CL-TECH-2026-SAMA • PRIMARY LEGAL DOCKET</span>
          </div>

          <h3 class="card-title">
            <a href="bigtech.html">Silicon Valley's African Trauma Factory: How Big Tech Outsources Content Moderation to Kenya and Nigeria</a>
          </h3>

          <p class="card-deck">
            An investigation into the human cost of artificial intelligence and social media safety, examining worker exploitation in Nairobi, sub-$2 hourly wages, and landmark labor trials against Meta and OpenAI.
          </p>

          <ul class="card-points">
            <li><strong>The HumAngle Investigation:</strong> Nigerian university graduates lured to Nairobi under linguistic translation pretenses, placed in front of unedited Boko Haram executions and bandit atrocities (Kauna Malgwi & Mustafa Mukhtar profiles).</li>
            <li><strong>Sweatshop Working Conditions:</strong> 50-second mandatory timer per violent ticket, sub-$2 hourly wages ($1.50–$2.20/hr vs. $18–$25 in US/Europe), and 81% severe clinical PTSD rate confirmed by psychiatric evaluations.</li>
            <li><strong>OpenAI ChatGPT Labeling & Ethiopian War Lawsuit:</strong> Kenyan workers paid $1.32/hr to read explicit trauma for AI safety guardrails; $2 Billion wrongful death lawsuit against Meta following the targeted murder of Prof. Meareg Amare.</li>
            <li><strong>Landmark Appellate Court Rulings:</strong> Kenyan Court of Appeal rejecting Meta's jurisdictional immunity in September 2024; $1.6 Billion compensation and healthcare trust litigation.</li>
          </ul>

          <div class="card-actions">
            <a href="bigtech.html" class="btn-primary">
              Open Master Dossier →
            </a>

            <div class="deep-dive-pills">
              <span class="pill-label">Primary Sources:</span>
              <span style="font-size: 13px; color: var(--color-text-secondary);">HumAngle • TIME Magazine • Kenyan Court of Appeal (Civil Appeal No. E186 of 2023)</span>
            </div>
          </div>
        </div>
      </article>

    </div>
  </main>

  <!-- UPCOMING INVESTIGATIONS DOCKET -->
  <section style="background: var(--color-surface); border-top: 1px solid var(--color-border); padding: 50px 20px 80px;" id="pipeline">
    <div style="max-width: 1080px; margin: 0 auto;">
      <div class="section-header">
        <h2 class="section-title">Investigation Pipeline & Upcoming Dockets</h2>
        <span class="section-counter">In Active Research</span>
      </div>

      <div class="pipeline-grid">
        <div class="pipeline-card">
          <div class="pipeline-badge">Case File 04 • In Active Research</div>
          <h3 class="pipeline-title">Peter Gregory Obi: The Offshore Corporate Architecture & Anambra Fiscal Audit</h3>
          <p class="pipeline-desc">
            Forensic analysis of the Pandora Papers leak, British Virgin Islands shell vehicles (Gabriella Investments), Next International UK filings, the ₦2 Billion SABMiller state investment, and the 13-month Anambra medical strike.
          </p>
        </div>

        <div class="pipeline-card">
          <div class="pipeline-badge">Case File 05 • In Active Research</div>
          <h3 class="pipeline-title">Rabiu Musa Kwankwaso: The Kwankwasiyya Red Cap Machine & Kano Political Economy</h3>
          <p class="pipeline-desc">
            Auditing the grassroots red-cap mass movement, the Kano education scholarship trust, political battles with Abdullahi Ganduje, and the NNPP's 2023 northern electoral fortress.
          </p>
        </div>

        <div class="pipeline-card">
          <div class="pipeline-badge">Case File 06 • In Active Research</div>
          <h3 class="pipeline-title">The Central Bank Ways & Means Overdraft: Anatomy of a ₦30 Trillion Hole</h3>
          <p class="pipeline-desc">
            Deconstructing Godwin Emefiele’s illegal overdraft financing to the Buhari Presidency, currency redesign logistics, and sovereign debt monetization.
          </p>
        </div>
      </div>
    </div>
  </section>

  <!-- FORMAL FOOTER -->
  <footer>
    <p>CIVIC LENS INVESTIGATIVE DESK • SPECIAL FACTUAL ARCHIVE</p>
    <p style="margin-top: 6px;">All findings compiled from sworn court transcripts, primary judicial dockets, and verified on-the-ground investigative reporting.</p>
    <p style="margin-top: 12px; font-size: 12px;">
      <a href="tinubu.html">Bola Ahmed Tinubu Dossier</a> • 
      <a href="atiku.html">Atiku Abubakar Dossier</a> • 
      <a href="bigtech.html">Big Tech Moderation Hubs</a> • 
      <a href="https://github.com/TherealE2O/research" target="_blank" rel="noopener">GitHub Repository</a>
    </p>
  </footer>

</body>
</html>
"""

with open(os.path.join(WORKSPACE, "index.html"), "w", encoding="utf-8") as f:
    f.write(HOME_PAGE_HTML)

print("  [OK] Successfully rebuilt index.html as the official Civic Lens Home Page")
