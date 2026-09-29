import re
from datetime import datetime
from pathlib import Path

from cards import build_output_html, inject_into_main_html
from marktohtml import convert_markdown_to_html

# Base Paths (resolves relative to script location)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
MAIN_HTML_PATH = PROJECT_ROOT / "index.html"
MDS_DIR_PATH = PROJECT_ROOT / "assets" / "mds"
SITEMAP_XML_PATH = PROJECT_ROOT / "sitemap.xml"


def update_date_version_tag(html_path: Path = MAIN_HTML_PATH) -> None:
    """Updates the [vMM.DD.YYYY] version tag in index.html to today's date."""
    if not html_path.exists():
        print(f"Warning: {html_path} not found. Skipping date version update.")
        return

    today_str = datetime.now().strftime("%m.%d.%Y")
    new_tag = f"[v{today_str}]"

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Pattern matches <span class="identity-tag">[v...]</span> with any spacing or existing date format
    pattern = r'(<span\s+class=["\']identity-tag["\']>\[v)[^\]]+(\]</span>)'
    updated_content, count = re.subn(pattern, rf"\g<1>{today_str}\g<2>", content)

    if count > 0:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Updated date version tag in {html_path.name} to {new_tag}")
    else:
        print(f"Notice: identity-tag element not found in {html_path.name}.")


def update_sitemap_xml(
    mds_dir: Path = MDS_DIR_PATH,
    sitemap_path: Path = SITEMAP_XML_PATH,
    base_url: str = "https://anissh.dev"
) -> None:
    """Updates sitemap.xml with index.html, summary4bot.html, and all project-<project_name>.html pages indexed from assets/mds."""
    project_files = []
    if mds_dir.exists():
        for md_file in sorted(mds_dir.glob("*.md")):
            project_name = md_file.stem
            project_files.append(f"projects/project-{project_name}.html")

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines.append('  <url>')
    lines.append(f'    <loc>{base_url}/index.html</loc>')
    lines.append('  </url>')
    lines.append('  <url>')
    lines.append(f'    <loc>{base_url}/summary4bot.html</loc>')
    lines.append('  </url>')

    for project_page in project_files:
        lines.append('  <url>')
        lines.append(f'    <loc>{base_url}/{project_page}</loc>')
        lines.append('  </url>')

    lines.append('</urlset>\n')

    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Updated {sitemap_path.name} with summary4bot.html and {len(project_files)} project page(s) from {mds_dir.name}.")


# Run card generation and inject into main HTML
inject_into_main_html()
build_output_html()

# Run markdown conversion for project descriptions
convert_markdown_to_html()

# Update the date version box in the main HTML file
update_date_version_tag()

# Update the xml sitemap file with the latest project pages
update_sitemap_xml()