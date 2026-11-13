"""
Build script to convert the APC/Tinubu 2023 vs. 2027 manifesto comparison,
inventories, 101-pledge accomplishment audit, and independent verification
report into Civic Lens broadsheet HTML web readers.
"""

import html
import os
import re
import markdown

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INVESTIGATIONS_DIR = os.path.join(WORKSPACE, "investigations")
GITHUB_BASE = "https://github.com/TherealE2O/research/blob/main/investigations"

MASTER_PAGE = {
    "md_file": "TINUBU_MANIFESTOS_2023_VS_2027_MASTER.md",
    "html_file": "tinubu_manifestos.html",
    "kicker": "Special Report / Presidential Platform & Delivery Audit",
    "title": "Tinubu Manifestos (2023 vs. 2027): Promise Comparison & 101-Pledge Delivery Audit (2023–2026)",
    "deck": (
        "A strictly neutral, page-cited comparison between the 2023 Renewed Hope Action Plan (80 pp., 8 Priority Areas) "
        "and the 2027 Agenda 2027–2031: From Reforms to Prosperity manifesto (109 pp., 4 Pillars), paired with an empirical "
        "audit of 101 measurable 2023 pledges over May 2023–November 2026."
    ),
    "meta_unit": "Civic Lens Policy & Macroeconomic Forensics Desk",
    "meta_sources": "APC 2023 & 2027 Manifestos, CBN, NBS, DMO, NERC, NRS, IMF & World Bank Records",
    "is_master": True,
}

SUB_PAGES = [
    {
        "index": 1,
        "md_file": "tinubu_manifesto_notes_01_2023_action_plan.md",
        "html_file": "manifesto_2023.html",
        "label": "Manifesto Note 01: 2023 Renewed Hope Action Plan Inventory (80 PDF pp., 16 Chapters)",
        "kicker": "Civic Lens Forensic Inquiry • Manifesto Dossier File 01",
        "title": "2023 Renewed Hope Action Plan: Complete Chapter-by-Chapter Inventory & Audit Checklist",
        "summary": (
            "Full WinRT OCR + page-render inventory of the 80-page 2023 manifesto (PDF p. N = printed p. N−2): "
            "heterodox oil-decoupled fiscal doctrine, anti-rate-hike stance, managed FX, 10% GDP/$780.9B chart, and measurable targets."
        ),
    },
    {
        "index": 2,
        "md_file": "tinubu_manifesto_notes_02_2027_agenda.md",
        "html_file": "manifesto_2027.html",
        "label": "Manifesto Note 02: 2027 Agenda 2027–2031 Inventory (109 PDF pp., 4 Pillars)",
        "kicker": "Civic Lens Forensic Inquiry • Manifesto Dossier File 02",
        "title": "2027 APC Manifesto ('From Reforms to Prosperity'): Complete 109-Page Inventory & Scorecard Map",
        "summary": (
            "PyMuPDF + visual page-by-page breakdown of Agenda 2027–2031: 4 Pillars + 4 Foundations, 2031 KPI tables, "
            "Fiscal Federation matrix, First 100 Days checklist, Independent Validation claims, Glossary additions & 9 internal variations."
        ),
    },
    {
        "index": 3,
        "md_file": "tinubu_manifesto_notes_03_comparison_matrix.md",
        "html_file": "manifesto_comparison.html",
        "label": "Manifesto Note 03: Side-by-Side 2023 vs. 2027 Comparison Matrix & Documentary Map",
        "kicker": "Civic Lens Forensic Inquiry • Manifesto Dossier File 03",
        "title": "2023 vs. 2027 Manifesto Comparison: Doctrinal Pivots, 30-Sector Matrix & Dropped/New Pledges",
        "summary": (
            "Structural and doctrinal shifts (heterodox expansionism to orthodox consolidation), recalibrated targets, "
            "15 dropped/replaced 2023 pledges, 11 new 2027 proposals, 30-row sector table & 8 Civic Lens visual pairings."
        ),
    },
    {
        "index": 4,
        "md_file": "tinubu_manifesto_notes_04_accomplishment_audit.md",
        "html_file": "manifesto_audit_2023.html",
        "label": "Manifesto Note 04: 2023–2026 Empirical Accomplishment Audit (101 Concrete Pledges)",
        "kicker": "Civic Lens Forensic Inquiry • Manifesto Dossier File 04",
        "title": "101-Pledge Delivery Audit (May 29, 2023 – Nov 13, 2026) & 2027 Self-Reported Claims Cross-Check",
        "summary": (
            "Triangulated audit across 16 chapters (4 Implemented, 55 Partial, 11 Mixed/Disputed, 27 Not Achieved/Reversed, 4 Insufficient Data), "
            "plus 251 verified primary/independent citations and cross-checks of Section 4 2027 claims."
        ),
    },
    {
        "index": 5,
        "md_file": "tinubu_manifesto_notes_05_verification_report.md",
        "html_file": "manifesto_verification.html",
        "label": "Manifesto Note 05: Independent Quality-Assurance & Source Verification Report",
        "kicker": "Civic Lens Forensic Inquiry • Manifesto Dossier File 05",
        "title": "Independent Verification Report: Page Pagination, Tally Math, Web Spot-Checks & Errata Log",
        "summary": (
            "Source-level verification log covering all 80 (2023) and 109 (2027) PDF pages, OCR recovery checks, "
            "101-pledge reconciliation, 140 unique external URLs, 20+ empirical spot-checks & PDF typography quirks."
        ),
    },
]

MD_TO_HTML_MAP = {
    MASTER_PAGE["md_file"]: MASTER_PAGE["html_file"],
    "TINUBU_360_INVESTIGATIVE_DOSSIER.md": "tinubu.html",
    "ATIKU_360_INVESTIGATIVE_DOSSIER.md": "atiku.html",
    "SILICON_VALLEY_AFRICAN_SWEATSHOPS_DOSSIER.md": "bigtech.html",
}
for page in SUB_PAGES:
    MD_TO_HTML_MAP[page["md_file"]] = page["html_file"]

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

    .pub-brand-wrap {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .pub-brand {{
      font-family: var(--font-headline);
      font-size: 19px;
      font-weight: 700;
      color: var(--color-text);
      text-decoration: none;
    }}

    .pub-tagline {{
      font-family: var(--font-body);
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      font-weight: 600;
      color: var(--color-accent-red);
      border-left: 1px solid var(--color-border);
      padding-left: 12px;
    }}

    .nav-links {{
      display: flex;
      gap: 16px;
      align-items: center;
      flex-wrap: wrap;
    }}

    .nav-back-link {{
      font-size: 13px;
      font-weight: 600;
      color: var(--color-link);
      text-decoration: none;
    }}
    .nav-back-link:hover {{ text-decoration: underline; }}

    .article-container {{
      max-width: 900px;
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
      line-height: 1.24;
      font-weight: 700;
      letter-spacing: -0.5px;
      margin-bottom: 14px;
      color: var(--color-text);
    }}

    .inquiry-deck {{
      font-family: var(--font-headline);
      font-size: 19px;
      line-height: 1.48;
      font-style: italic;
      color: var(--color-text-secondary);
      margin-bottom: 22px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--color-border);
    }}

    .inquiry-meta-bar {{
      border-top: 1px solid var(--color-border);
      border-bottom: 1px solid var(--color-border);
      padding: 12px 0;
      margin: 18px 0 32px;
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
      padding: 2px 8px;
    }}

    .table-of-contents {{
      background: var(--color-surface);
      border: 1px solid var(--color-border);
      padding: 20px 24px;
      margin-bottom: 32px;
    }}

    .toc-title {{
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--color-text);
      margin-bottom: 12px;
    }}

    .toc-list {{
      list-style-type: none;
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px 24px;
      margin: 0;
    }}
    @media (max-width: 680px) {{
      .toc-list {{ grid-template-columns: 1fr; }}
      .pub-tagline {{ display: none; }}
    }}

    .toc-list li {{ margin-bottom: 2px; }}
    .toc-list a {{
      color: var(--color-link);
      text-decoration: none;
      font-size: 13.5px;
    }}
    .toc-list a:hover {{ text-decoration: underline; }}

    .evidence-box {{
      background: var(--color-surface);
      border: 2px solid var(--color-border-dark);
      padding: 22px 24px;
      margin-bottom: 40px;
    }}

    .evidence-box-kicker {{
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      color: var(--color-accent-red);
      margin-bottom: 6px;
    }}

    .evidence-box-desc {{
      font-size: 14.5px;
      color: var(--color-text-secondary);
      margin-bottom: 16px;
    }}

    .evidence-row {{
      border-top: 1px solid var(--color-border);
      padding-top: 12px;
      margin-top: 12px;
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      flex-wrap: wrap;
      gap: 10px;
    }}

    .evidence-row-meta {{
      font-size: 13px;
      color: var(--color-text-muted);
      margin-top: 3px;
    }}

    .evidence-row-links {{
      display: flex;
      gap: 14px;
      font-size: 13px;
      font-weight: 600;
      white-space: nowrap;
    }}

    h2 {{
      font-family: var(--font-headline);
      font-size: 24px;
      line-height: 1.35;
      margin: 42px 0 16px;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--color-border-dark);
      color: var(--color-text);
      scroll-margin-top: 84px;
    }}

    h3 {{
      font-family: var(--font-headline);
      font-size: 19px;
      line-height: 1.4;
      margin: 28px 0 12px;
      color: var(--color-text);
      scroll-margin-top: 84px;
    }}

    h4 {{
      font-size: 16px;
      font-weight: 700;
      margin: 20px 0 8px;
      color: var(--color-text);
    }}

    p {{ margin-bottom: 16px; color: var(--color-text); }}

    ul, ol {{
      margin: 0 0 20px 24px;
    }}
    li {{ margin-bottom: 8px; }}

    code {{
      font-family: var(--font-mono);
      font-size: 0.87em;
      background: var(--color-surface-subtle);
      border: 1px solid #E2E8F0;
      padding: 1px 5px;
      border-radius: 3px;
      color: var(--color-text);
    }}

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
    pre code {{
      background: transparent;
      border: 0;
      padding: 0;
      font-size: inherit;
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
      border-left: 4px solid var(--color-border-dark);
      padding: 14px 20px;
      margin: 22px 0;
      background: var(--color-surface);
      font-size: 15px;
      color: var(--color-text-secondary);
    }}
    blockquote p {{ margin-bottom: 8px; color: var(--color-text-secondary); }}
    blockquote p:last-child, blockquote ul:last-child {{ margin-bottom: 0; }}
    blockquote ul {{ margin: 8px 0 4px 20px; }}

    a {{ color: var(--color-link); text-decoration: underline; word-break: break-word; }}
    a:hover {{ color: var(--color-link-hover); }}

    .table-wrapper {{
      margin: 24px 0;
      border: 1px solid var(--color-border);
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      background: #FFFFFF;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 0;
      font-size: 13.5px;
      line-height: 1.55;
    }}
    th, td {{
      padding: 10px 13px;
      border: 1px solid var(--color-border);
      text-align: left;
      vertical-align: top;
    }}
    th {{
      background: var(--color-surface-subtle);
      font-weight: 700;
      color: var(--color-text);
      white-space: nowrap;
    }}
    tr:nth-child(even) td {{
      background: #FAFAFA;
    }}

    hr {{
      border: 0;
      border-top: 1px solid var(--color-border);
      margin: 34px 0;
    }}

    footer {{
      border-top: 1px solid var(--color-border);
      background: var(--color-surface);
      padding: 26px 20px;
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
      <div class="pub-brand-wrap">
        <a href="index.html" class="pub-brand">CIVIC LENS INVESTIGATIONS</a>
        <span class="pub-tagline">Primary Evidence Desk</span>
      </div>
      <nav class="nav-links">
        {nav_html}
      </nav>
    </div>
  </header>

  <main class="article-container">
    <div class="inquiry-kicker">{kicker}</div>
    <h1 class="inquiry-title">{title}</h1>
    {deck_html}
    <div class="inquiry-meta-bar">
      <div>Primary Field File: <span class="file-pill">{md_file}</span></div>
      <div>Editorial Standard: <strong>Neutral, Source-Attributed Broadsheet</strong></div>
    </div>

    {toc_html}
    {evidence_box_html}

    <article>
{content}
    </article>
  </main>

  <footer>
    <p>CIVIC LENS INVESTIGATIVE DESK • PRESIDENTIAL MANIFESTO &amp; DELIVERY ARCHIVE</p>
    <p style="margin-top: 6px;">All claims, targets, and empirical outcomes compiled strictly from official APC 2023 &amp; 2027 manifestos alongside CBN, NBS, DMO, NERC, NRS, judicial, multilateral, and independent press records.</p>
  </footer>
</body>
</html>
"""


def strip_leading_h1(md_text):
    """Remove the top-level Markdown H1 line since HTML renders h1.inquiry-title."""
    lines = md_text.splitlines()
    if lines and lines[0].startswith("# "):
        idx = 1
        while idx < len(lines) and not lines[idx].strip():
            idx += 1
        return "\n".join(lines[idx:])
    return md_text


def normalize_tight_lists(md_text):
    """Insert a blank line before lists immediately following paragraphs (outside fences)."""
    lines = md_text.splitlines()
    out = []
    in_fence = False
    list_re = re.compile(r"^(>\s*)?(?:[-*+] |\d+\. )")
    non_para_prev_re = re.compile(r"^\s*(?:$|[-*+] |\d+\. |\||#|---|===|```)")

    for line in lines:
        if re.match(r"^\s*`{3,}", line):
            in_fence = not in_fence
            out.append(line)
            continue

        if not in_fence and out:
            prev = out[-1]
            # Handle blockquote tight lists (`> header:` followed by `> - item`)
            if prev.startswith(">") and line.startswith(">"):
                prev_inner = prev.lstrip("> ")
                cur_inner = line.lstrip("> ")
                if prev_inner and not re.match(r"^(?:[-*+] |\d+\. |>|#)", prev_inner) and re.match(r"^(?:[-*+] |\d+\. )", cur_inner):
                    out.append(">")
            elif not non_para_prev_re.match(prev) and not prev.lstrip().startswith(">") and list_re.match(line):
                out.append("")

        out.append(line)

    return "\n".join(out)


def rewrite_md_crosslinks(md_text):
    """Rewrite relative links to local .md archive files into their target .html filenames."""
    def replace_link(match):
        label, target = match.group(1), match.group(2)
        if target.startswith(("http://", "https://", "#")):
            return match.group(0)
        base, frag = (target.split("#", 1) + [""])[:2]
        base_name = os.path.basename(base)
        if base_name in MD_TO_HTML_MAP:
            html_target = MD_TO_HTML_MAP[base_name]
            if frag:
                html_target = f"{html_target}#{frag}"
            return f"[{label}]({html_target})"
        return match.group(0)

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", replace_link, md_text)


def escape_bare_lt(text):
    """
    Escape bare '<' before digits or symbols (e.g. '<40', '<=8%', '<5%', '<50%')
    outside backtick code spans, fenced blocks, and valid HTML tags like '<br>'.
    Prevents Python Markdown from swallowing '<40 ... >' text spans as raw HTML.
    """
    # Split out fenced code blocks and inline backtick code spans
    token_re = re.compile(r"(`{3,}[\s\S]*?`{3,}|`[^`\n]+`)")
    parts = token_re.split(text)
    bare_lt_re = re.compile(r"<(?=[0-9=~$₦£\-])")

    for i in range(0, len(parts), 2):
        # Preserve explicit HTML tags like <br>, <br/>, <a>, etc.; escape numeric/symbolic '<'
        parts[i] = bare_lt_re.sub("&lt;", parts[i])
    return "".join(parts)


def convert_markdown_to_html(md_text):
    """Extract Mermaid fences, normalize lists/links/escapes, render Markdown, and wrap tables."""
    mermaid_blocks = []

    def store_mermaid(match):
        code = match.group(1).strip()
        idx = len(mermaid_blocks)
        mermaid_blocks.append(code)
        return f"\n\nQQQMERMAIDBLOCK{idx}QQQ\n\n"

    processed = strip_leading_h1(md_text)
    processed = re.sub(r"`{3,}\s*mermaid\s*\n([\s\S]*?)\n\s*`{3,}", store_mermaid, processed)
    processed = rewrite_md_crosslinks(processed)
    processed = normalize_tight_lists(processed)
    processed = escape_bare_lt(processed)

    md_engine = markdown.Markdown(
        extensions=["extra", "tables", "fenced_code", "nl2br", "toc"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )
    rendered = md_engine.convert(processed)

    # Wrap every <table>...</table> in <div class="table-wrapper"> for mobile scrolling
    rendered = re.sub(
        r"(<table\b[^>]*>[\s\S]*?</table>)",
        r'<div class="table-wrapper">\n\1\n</div>',
        rendered,
    )

    # Restore Mermaid blocks
    for idx, code in enumerate(mermaid_blocks):
        clean_code = html.unescape(code)
        mermaid_tag = f'<div class="mermaid">\n{clean_code}\n</div>'
        rendered = rendered.replace(f"<p>QQQMERMAIDBLOCK{idx}QQQ</p>", mermaid_tag)
        rendered = rendered.replace(f"QQQMERMAIDBLOCK{idx}QQQ", mermaid_tag)

    return rendered, md_engine.toc_tokens


def build_toc_html(toc_tokens, include_evidence_anchor=False):
    """Render a clean 2-column Table of Contents box from Markdown H2 tokens."""
    items = []
    if include_evidence_anchor:
        items.append('<li><a href="#primary-evidence-files">Primary Deep-Dive Evidence Files (Notes 01–05)</a></li>')
    for tok in toc_tokens:
        if tok.get("level") == 2 and tok.get("id") and tok.get("name"):
            label = html.escape(html.unescape(tok["name"]))
            href = html.escape(tok["id"])
            items.append(f'<li><a href="#{href}">{label}</a></li>')
    if not items:
        return ""
    joined = "\n        ".join(items)
    return (
        '<div class="table-of-contents">\n'
        '      <div class="toc-title">Table of Contents / Jump to Section</div>\n'
        '      <ul class="toc-list">\n'
        f"        {joined}\n"
        "      </ul>\n"
        "    </div>"
    )


def build_evidence_box_html():
    """Render the Primary Deep-Dive Evidence Files box on the Master Reader."""
    rows_html = []
    for item in SUB_PAGES:
        md_path = os.path.join(INVESTIGATIONS_DIR, item["md_file"])
        size_kb = round(os.path.getsize(md_path) / 1024) if os.path.exists(md_path) else 0
        gh_url = f"{GITHUB_BASE}/{item['md_file']}"
        rows_html.append(
            f"""        <div class="evidence-row">
          <div>
            <strong style="font-size: 15px;">{html.escape(item['label'])}</strong>
            <div class="evidence-row-meta">{size_kb} KB • {html.escape(item['summary'])}</div>
          </div>
          <div class="evidence-row-links">
            <a href="{item['html_file']}">Read Full File (HTML) →</a>
            <a href="{gh_url}" target="_blank" rel="noopener">GitHub Markdown</a>
          </div>
        </div>"""
        )
    return (
        '<div class="evidence-box" id="primary-evidence-files">\n'
        '      <div class="evidence-box-kicker">Primary Deep-Dive Evidence Files (Manifesto Inventories, Matrix &amp; 101-Pledge Audit)</div>\n'
        '      <p class="evidence-box-desc">\n'
        "        Access all five standalone research files—covering the full 2023 and 2027 page inventories, 30-sector comparison matrix, "
        "101-pledge empirical audit, and independent quality-assurance log—in web reader or raw GitHub Markdown format:\n"
        "      </p>\n"
        + "\n".join(rows_html)
        + "\n    </div>"
    )


def build_nav_html(md_file, is_master=False):
    """Build top header navigation matching Civic Lens broadsheet style."""
    gh_url = f"{GITHUB_BASE}/{md_file}"
    if is_master:
        return (
            '<a href="index.html" class="nav-back-link">← Home</a>\n'
            '        <a href="tinubu.html" class="nav-back-link">Tinubu 360° Dossier</a>\n'
            f'        <a href="{gh_url}" target="_blank" rel="noopener" class="nav-back-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>'
        )
    return (
        '<a href="index.html" class="nav-back-link">← Home</a>\n'
        '        <a href="tinubu_manifestos.html" class="nav-back-link">Manifesto Master Dossier</a>\n'
        '        <a href="tinubu.html" class="nav-back-link">Tinubu 360° Dossier</a>\n'
        f'        <a href="{gh_url}" target="_blank" rel="noopener" class="nav-back-link" style="color: var(--color-text-secondary);">GitHub Markdown ↗</a>'
    )


def render_page(page_cfg):
    """Convert one Markdown file into a standalone broadsheet HTML page."""
    md_path = os.path.join(INVESTIGATIONS_DIR, page_cfg["md_file"])
    html_path = os.path.join(WORKSPACE, page_cfg["html_file"])
    if not os.path.exists(md_path):
        raise FileNotFoundError(f"Missing Markdown source: {md_path}")

    with open(md_path, "r", encoding="utf-8") as f:
        raw_md = f.read()

    content_html, toc_tokens = convert_markdown_to_html(raw_md)
    is_master = page_cfg.get("is_master", False)
    toc_html = build_toc_html(toc_tokens, include_evidence_anchor=is_master)
    evidence_box_html = build_evidence_box_html() if is_master else ""
    deck_html = (
        f'<div class="inquiry-deck">{html.escape(page_cfg["deck"])}</div>'
        if page_cfg.get("deck")
        else ""
    )

    full_html = HTML_TEMPLATE.format(
        title=html.escape(page_cfg["title"]),
        kicker=html.escape(page_cfg["kicker"]),
        deck_html=deck_html,
        md_file=html.escape(page_cfg["md_file"]),
        nav_html=build_nav_html(page_cfg["md_file"], is_master=is_master),
        toc_html=toc_html,
        evidence_box_html=evidence_box_html,
        content=content_html,
    )

    with open(html_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(full_html)
    print(f"  [OK] Generated: {page_cfg['html_file']} ({len(full_html.encode('utf-8')):,} bytes)")
    return html_path


def main():
    print("Building Tinubu 2023 vs. 2027 Manifesto & Audit broadsheet HTML readers...")
    all_pages = [MASTER_PAGE] + SUB_PAGES
    for cfg in all_pages:
        render_page(cfg)


if __name__ == "__main__":
    main()
