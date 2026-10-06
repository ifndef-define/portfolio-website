import html
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Base Paths (resolves relative to script location)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROJECTS_JSON_PATH = PROJECT_ROOT / "assets" / "jsons" / "projects.json"
MDS_DIR_PATH = PROJECT_ROOT / "assets" / "mds"
PROJECTS_DIR_PATH = PROJECT_ROOT / "projects"

# HTML Page Scaffolding Template
PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title} | Anissh Guruprasad</title>
    <meta
      name="description"
      content="{meta_description}"
    />
    <link rel="icon" type="image/x-icon" href="../assets/AG_logo.svg" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Cascadia+Code:wght@300;400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="../style.css" />
  </head>
  <body>
    <!-- Header -->
    <header class="site-header">
      <nav class="nav container">
        <button type="button" class="brand-btn" onclick="window.location.href='../index.html'" aria-label="Back to home"><span class="brand-bracket">[</span><span class="brand-name">anissh</span><span class="brand-dotdev">.dev</span><span class="brand-bracket">]</span></button>
        <button type="button" class="hamburger-btn" id="hamburger-toggle" aria-label="Toggle navigation menu" aria-expanded="false">
          <span class="hamburger-box" aria-hidden="true">
            <span class="hamburger-bar"></span>
            <span class="hamburger-bar"></span>
            <span class="hamburger-bar"></span>
          </span>
        </button>
        <div class="nav-links" id="nav-links-menu">
          <a href="../index.html#about">[About]</a>
          <a href="../index.html#projects">[Projects]</a>
          <a href="../index.html#experience">[Experience]</a>
          <a href="../index.html#skills">[Skills]</a>
          <a href="../index.html#contact">[Contact]</a>
        </div>
      </nav>
    </header>

    <main>
      <section class="project-detail-hero">
        <div class="container">
          <a href="../index.html#projects" class="back-link">← Back to Projects</a>
          <div class="project-detail-header">
            <h1>{title}</h1>
            <div class="project-tags">
{tags_html}
            </div>
          </div>
        </div>
      </section>

      <section class="project-detail-content">
        <div class="container">
          <div class="project-detail-main">
            <article class="detail-section crosshair-card">
{note_html}
{content_html}
            </article>
          </div>
        </div>
      </section>

      <section class="project-nav">
        <div class="container">
          <p>← <a href="../index.html#projects">Back to all projects</a></p>
        </div>
      </section>
    </main>

    <!-- Footer (Identical to Main Page) -->
    <footer id="contact" class="site-footer">
      <div class="container footer-inner">
        <div>
          <p class="section-eyebrow">[<span class="eyebrow-addr">0xF0 - 0xFF</span> // <span class="eyebrow-title">TRANSMISSION</span>]</p>
          <h2 class="footer-title">Let's build something thoughtful.</h2>
          <p class="footer-subtitle">Open for engineering opportunities and technical collaboration.</p>
          <div class="footer-cta-row">
            <button type="button" class="button primary-connect" id="connect-button-footer">Let's Connect</button>
            <span class="footer-cta-divider">or reach out directly</span>
            <a id="portfolio-email-contact" class="button secondary">Email</a>
          </div>
        </div>

        <div class="footer-links-group">
          <div class="footer-nav">
            <a href="https://www.linkedin.com/in/anissh-guru/" target="_blank" rel="noreferrer">
              <svg class="footer-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="2" r="2"/></svg>
              <span>LinkedIn</span>
              <span class="arrow" aria-hidden="true">↗</span>
            </a>
            <a href="https://github.com/ifndef-define" target="_blank" rel="noreferrer">
              <svg class="footer-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
              <span>GitHub</span>
              <span class="arrow" aria-hidden="true">↗</span>
            </a>
            <a href="https://github.com/ifndef-define/portfolio-website/issues" target="_blank" rel="noreferrer">
              <svg class="footer-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              <span>Report Issue</span>
              <span class="arrow" aria-hidden="true">↗</span>
            </a>
          </div>
        </div>

        <div class="footer-bottom">
          <p class="copyright">&copy; <span id="year"></span> Anissh Guruprasad &mdash; <a href="https://github.com/ifndef-define/portfolio-website" target="_blank" rel="noreferrer">Site source code</a></p>
        </div>
      </div>
    </footer>

    <!-- VS Code Styled Recruiter Contact Modal -->
    <div class="contact-modal" id="contact-modal" aria-hidden="true">
      <div class="modal-backdrop" data-close-modal></div>
      <section class="code-editor" role="dialog" aria-modal="true" aria-label="Recruiter contact form">
        <div class="editor-titlebar">
          <div class="editor-traffic-lights">
            <span class="editor-dot dot-red" data-close-modal title="Close"></span>
            <span class="editor-dot dot-yellow"></span>
            <span class="editor-dot dot-green"></span>
          </div>
          <span class="editor-filename">recruiter_contact.py</span>
          <button type="button" class="modal-close" aria-label="Close contact form" data-close-modal>&times;</button>
        </div>
        <div class="editor-accessibility" aria-label="Accessibility options">
          <button type="button" class="accessibility-toggle" id="light-mode-toggle" aria-pressed="false">Use light mode</button>
          <div class="font-size-control">
            <select id="font-size-select" aria-label="Editor text size">
              <option value="normal" selected>Normal</option>
              <option value="large">Large</option>
              <option value="very-large">Very large</option>
            </select>
          </div>
        </div>
        <div class="editor-body">
          <div class="editor-code">
            <div class="code-line" id="import-contact-system" title="Triple-click for debug mode"><span class="line-number">1</span><span class="code-text"><span class="token keyword">import</span> <span class="token type">contact_system</span></span></div>
            <div class="code-line"><span class="line-number">2</span><span class="code-text"></span></div>
            <div class="code-line"><span class="line-number">3</span><span class="code-text"><span class="token comment"># Recruiter Contact Interface — Sends directly to me</span></span></div>
            <div class="code-line"><span class="line-number">4</span><span class="code-text"><span class="token comment"># Feel free to use this form, or directly reach out via email</span></span></div>
            <div class="code-line"><span class="line-number">5</span><span class="code-text"><span class="token keyword">def</span> <span class="token function">recruiter_contact</span>():</span></div>
            <div class="code-line"><span class="line-number">6</span><span class="code-text indent-4">candidate = <span class="token string">"Anissh Guruprasad"</span></span></div>
            <div class="code-line"><span class="line-number">7</span><span class="code-text indent-4">recruiter_name = <span class="token string">"<span class="editable-code-region"><input class="inline-code-input recruiter-name" id="recruiter-name" name="recruiterName" type="text" value="&lt;Recruiter Name&gt;" aria-label="Recruiter name" maxlength="50" autocomplete="name" required /></span>"</span></span></div>
            <div class="code-line"><span class="line-number">8</span><span class="code-text indent-4">recruiter_email = <span class="token string">"<span class="editable-code-region"><input class="inline-code-input recruiter-email" id="recruiter-email" name="recruiterEmail" type="email" value="&lt;recruiter@company.com&gt;" aria-label="Recruiter email" maxlength="60" autocomplete="email" required /></span>"</span></span></div>
            <div class="code-line"><span class="line-number">9</span><span class="code-text indent-4">reason_for_contact = <span class="token string">\"\"\"<span class="editable-code-region multiline-region"><textarea class="inline-code-textarea recruiter-message" id="recruiter-message" name="recruiterMessage" rows="2" aria-label="Reason for reaching out">&lt;Why you are reaching out / role details&gt;</textarea></span>\"\"\"</span></span></div>
            <div class="code-line"><span class="line-number">10</span><span class="code-text"></span></div>
            <div class="code-line"><span class="line-number">11</span><span class="code-text indent-4"><span class="token function">contact_system.transmit</span>(</span></div>
            <div class="code-line"><span class="line-number">12</span><span class="code-text indent-4">    to=candidate,</span></div>
            <div class="code-line"><span class="line-number">13</span><span class="code-text indent-4">    sender=recruiter_name,</span></div>
            <div class="code-line"><span class="line-number">14</span><span class="code-text indent-4">    email=recruiter_email,</span></div>
            <div class="code-line"><span class="line-number">15</span><span class="code-text indent-4">    body=reason_for_contact</span></div>
            <div class="code-line"><span class="line-number">16</span><span class="code-text indent-4">)</span></div>
            <div class="code-line"><span class="line-number">17</span><span class="code-text"></span></div>
            <div class="code-line"><span class="line-number">18</span><span class="code-text"><span class="token keyword">if</span> __name__ == <span class="token string">"__main__"</span>:</span></div>
            <div class="code-line"><span class="line-number">19</span><span class="code-text indent-4"><span class="token function">recruiter_contact</span>()</span></div>
          </div>
          <div class="terminal-divider" aria-hidden="true"></div>
          <form id="contact-form" novalidate>
            <input type="checkbox" name="botcheck" id="botcheck" class="code-param-opt" tabindex="-1" autocomplete="off" />
            <div class="terminal-console-bar">
              <button type="submit" class="send-button">
                <span class="send-label">Run &gt;</span>
                <span class="send-loader" aria-hidden="true"></span>
              </button>
              <span class="console-cmd">python recruiter_contact.py</span>
            </div>
            <p class="email-error" id="email-error" role="alert"></p>
          </form>
        </div>
      </section>
    </div>

    <script src="../script.js"></script>
  </body>
</html>
"""


def load_projects_metadata() -> Dict[str, Dict[str, Any]]:
    """Loads projects.json and maps project slugs (e.g. 'fpga') to project metadata."""
    if not PROJECTS_JSON_PATH.exists():
        return {}

    with open(PROJECTS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    projects_map = {}
    for p in data.get("projects", []):
        # Match by links[].page, e.g. "projects/project-fpga.html" -> "fpga"
        matched = False
        for link in p.get("links", []):
            page = link.get("page", "")
            if page.startswith("projects/project-") and page.endswith(".html"):
                slug = page[len("projects/project-") : -len(".html")]
                projects_map[slug] = p
                matched = True
        if not matched:
            # Fallback slug derived from title
            slug = re.sub(r"[^a-zA-Z0-9]+", "-", p.get("title", "").lower()).strip("-")
            if slug:
                projects_map[slug] = p

    return projects_map


def adjust_relative_path(path_str: str) -> str:
    """Adjusts asset paths relative to the projects/ subfolder."""
    path_str = path_str.strip()
    if path_str.startswith("http://") or path_str.startswith("https://") or path_str.startswith("//"):
        return path_str
    if path_str.startswith("../"):
        return path_str
    if path_str.startswith("/"):
        return f"..{path_str}"
    return f"../{path_str}"


def format_inline_markdown(text: str) -> str:
    """Formats inline markdown elements like bold, italic, code, and links."""
    # Escape ampersands not already part of an entity
    text = re.sub(r"&(?!(?:[a-zA-Z]+|#\d+|#x[a-fA-F0-9]+);)", "&amp;", text)

    # Bold: **text**
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)

    # Italic: *text* (excluding bold delimiters)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", text)

    # Inline code: `code`
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)

    # Standard Markdown Links: [text](url) - ignore images ![
    def link_replacer(match: re.Match) -> str:
        label = match.group(1)
        url = adjust_relative_path(match.group(2))
        return f'<a href="{url}">{label}</a>'

    text = re.sub(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)", link_replacer, text)
    return text


def parse_image_line(line: str) -> Optional[Tuple[str, str, Optional[str]]]:
    """Detects and parses markdown image syntax:

    - Linked: [![caption](img_url)](link_url)
    - Direct: ![caption](img_url)
    Returns (caption, img_url, link_url) or None.
    """
    line = line.strip()
    # Linked image
    linked_match = re.match(r"^\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)$", line)
    if linked_match:
        caption = linked_match.group(1).strip()
        img_url = linked_match.group(2).strip()
        link_url = linked_match.group(3).strip()
        return caption, img_url, link_url

    # Direct image
    direct_match = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)$", line)
    if direct_match:
        caption = direct_match.group(1).strip()
        img_url = direct_match.group(2).strip()
        return caption, img_url, None

    return None


def render_figure_html(caption: str, img_url: str, link_url: Optional[str] = None) -> str:
    """Renders a center-aligned <figure> with image and visible caption."""
    safe_img_url = adjust_relative_path(img_url)
    safe_caption = html.escape(caption)

    if link_url:
        safe_link_url = adjust_relative_path(link_url)
        img_tag = f'                  <a href="{safe_link_url}" target="_blank" rel="noreferrer">\n                    <img src="{safe_img_url}" alt="{safe_caption}" />\n                  </a>'
    else:
        img_tag = f'                  <img src="{safe_img_url}" alt="{safe_caption}" />'

    caption_tag = f"                  <figcaption>{safe_caption}</figcaption>" if caption else ""

    return (
        f'              <figure class="project-figure">\n{img_tag}\n{caption_tag}\n              </figure>'
    )


def parse_markdown_content(raw_md: str) -> str:
    """Parses markdown into semantic HTML subsections, tech stack lists, and figures."""
    # Filter out comment lines starting with %
    lines = [line.strip() for line in raw_md.splitlines() if not line.strip().startswith("%")]

    # Group lines by top-level section: # Heading
    sections: List[Tuple[str, List[str]]] = []
    current_title = ""
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("# "):
            if current_title or current_lines:
                sections.append((current_title, current_lines))
            current_title = line[2:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_title or current_lines:
        sections.append((current_title, current_lines))

    output_blocks: List[str] = []

    for section_title, sec_lines in sections:
        clean_sec_lines = [l for l in sec_lines if l.strip()]

        # Standalone image block without section header
        if not section_title and clean_sec_lines:
            for l in clean_sec_lines:
                img_info = parse_image_line(l)
                if img_info:
                    cap, img_src, link_src = img_info
                    output_blocks.append(render_figure_html(cap, img_src, link_src))
                else:
                    output_blocks.append(
                        f'              <div class="detail-subsection">\n                <p>{format_inline_markdown(l)}</p>\n              </div>'
                    )
            continue

        # Tech Stack Section
        if section_title.lower() == "tech stack":
            tech_items_html: List[str] = []
            trailing_figures: List[str] = []

            for l in clean_sec_lines:
                img_info = parse_image_line(l)
                if img_info:
                    cap, img_src, link_src = img_info
                    trailing_figures.append(render_figure_html(cap, img_src, link_src))
                    continue

                # Strip bullet prefix if present: - **Key:** Value
                item_line = l
                if item_line.startswith("- ") or item_line.startswith("* "):
                    item_line = item_line[2:].strip()

                formatted_item = format_inline_markdown(item_line)
                tech_items_html.append(
                    f'                  <div class="tech-item">\n                    {formatted_item}\n                  </div>'
                )

            block = (
                f'              <div class="detail-subsection tech-stack">\n'
                f'                <h2>{html.escape(section_title)}</h2>\n'
                f'                <div class="tech-items">\n'
                + "\n".join(tech_items_html)
                + "\n                </div>\n"
                f"              </div>"
            )
            output_blocks.append(block)

            # Append any trailing figures specified at the end of the section
            for fig in trailing_figures:
                output_blocks.append(fig)
            continue

        # Standard Detail Subsection
        inner_html_parts: List[str] = []
        inner_html_parts.append(f"                <h2>{html.escape(section_title)}</h2>")

        # Parse sub-elements: paragraphs, <h3> subheadings, <ul> lists, figures
        in_list = False
        list_items: List[str] = []
        para_lines: List[str] = []

        def flush_list():
            nonlocal in_list, list_items
            if in_list and list_items:
                inner_html_parts.append("                <ul>")
                for li in list_items:
                    inner_html_parts.append(f"                  <li>{li}</li>")
                inner_html_parts.append("                </ul>")
                list_items = []
                in_list = False

        def flush_paragraph():
            nonlocal para_lines
            if para_lines:
                full_para = " ".join(para_lines)
                inner_html_parts.append(f"                <p>\n                  {format_inline_markdown(full_para)}\n                </p>")
                para_lines = []

        for line in sec_lines:
            trimmed = line.strip()
            if not trimmed:
                flush_paragraph()
                flush_list()
                continue

            # Check for image line
            img_info = parse_image_line(trimmed)
            if img_info:
                flush_paragraph()
                flush_list()
                cap, img_src, link_src = img_info
                inner_html_parts.append(render_figure_html(cap, img_src, link_src))
                continue

            # Subheading ##
            if trimmed.startswith("## "):
                flush_paragraph()
                flush_list()
                sub_title = html.escape(trimmed[3:].strip())
                inner_html_parts.append(f"                <h3>{sub_title}</h3>")
                continue

            # Bullet List Item - or *
            if trimmed.startswith("- ") or trimmed.startswith("* "):
                flush_paragraph()
                in_list = True
                item_content = format_inline_markdown(trimmed[2:].strip())
                list_items.append(item_content)
                continue

            # Plain paragraph text
            if in_list:
                flush_list()
            para_lines.append(trimmed)

        flush_paragraph()
        flush_list()

        block = '              <div class="detail-subsection">\n' + "\n".join(inner_html_parts) + "\n              </div>"
        output_blocks.append(block)

    return "\n\n".join(output_blocks)


def generate_note_html(note: Optional[Dict[str, Any]]) -> str:
    """Generates the minimal note alert if present in project metadata."""
    if not note or not note.get("message"):
        return ""

    note_type = note.get("type", "note")
    if note_type == "good":
        icon = "✓"
        type_class = "note-good"
    elif note_type == "bad":
        icon = "⚠"
        type_class = "note-bad"
    else:
        icon = "ℹ"
        type_class = "note-note"

    message = html.escape(note["message"])
    return (
        f'              <div class="project-system-note-minimal {type_class}">\n'
        f'                <span class="note-icon">{icon}</span>\n'
        f'                <span class="note-text">{message}</span>\n'
        f"              </div>\n"
    )


def convert_markdown_file(
    md_file_path: Path,
    projects_meta: Dict[str, Dict[str, Any]],
    output_dir: Path = PROJECTS_DIR_PATH,
) -> Path:
    """Converts a single markdown file into a styled project HTML page."""
    slug = md_file_path.stem
    project_meta = projects_meta.get(slug, {})

    # Extract metadata with sensible fallbacks
    title = project_meta.get("title") or slug.replace("-", " ").title()
    meta_description = project_meta.get("description") or f"Project overview and technical details for {title}."
    skills = project_meta.get("skills", [])
    note = project_meta.get("note")

    tags_html = "\n".join([f'              <span class="tag">{html.escape(skill)}</span>' for skill in skills])

    note_html = generate_note_html(note)

    raw_md = md_file_path.read_text(encoding="utf-8")
    content_html = parse_markdown_content(raw_md)

    rendered_html = PAGE_TEMPLATE.format(
        title=html.escape(title),
        meta_description=html.escape(meta_description),
        tags_html=tags_html,
        note_html=note_html,
        content_html=content_html,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    out_file_path = output_dir / f"project-{slug}.html"
    out_file_path.write_text(rendered_html, encoding="utf-8")
    print(f"Generated: {out_file_path.relative_to(PROJECT_ROOT)}")
    return out_file_path


def convert_markdown_to_html(
    mds_dir: Path = MDS_DIR_PATH,
    output_dir: Path = PROJECTS_DIR_PATH,
) -> List[Path]:
    """Scans mds_dir for all .md files and generates corresponding HTML pages in output_dir."""
    if not mds_dir.exists():
        print(f"Directory {mds_dir} not found. Skipping markdown conversion.")
        return []

    projects_meta = load_projects_metadata()
    generated_files: List[Path] = []

    for md_file in sorted(mds_dir.glob("*.md")):
        # Only process files that have actual content (size > 0)
        if md_file.stat().st_size == 0:
            print(f"Skipping empty markdown file: {md_file.name}")
            continue

        out_path = convert_markdown_file(md_file, projects_meta, output_dir)
        generated_files.append(out_path)

    return generated_files


if __name__ == "__main__":
    convert_markdown_to_html()