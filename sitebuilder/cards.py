import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Base Paths (resolves relative to script location)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROJECTS_JSON_PATH = PROJECT_ROOT / "assets" / "jsons" / "projects.json"
PROJECT_DESC_DIR_PATH = PROJECT_ROOT / "assets" / "project_desc"
EXPERIENCES_JSON_PATH = PROJECT_ROOT / "assets" / "jsons" / "experiences.json"
EXPERIENCE_DESC_DIR_PATH = PROJECT_ROOT / "assets" / "experience_desc"
SKILLS_JSON_PATH = PROJECT_ROOT / "assets" / "jsons" / "skills.json"
SKILL_DESC_DIR_PATH = PROJECT_ROOT / "assets" / "skill_desc"
OUTPUT_HTML_PATH = SCRIPT_DIR / "output.html"
MAIN_HTML_PATH = PROJECT_ROOT / "index.html"

# In-memory cache to prevent duplicate parsing during single build run
_CACHED_PROJECTS_HTML: Optional[str] = None
_CACHED_EXPERIENCES_DATA: Optional[List[Dict[str, Any]]] = None
_CACHED_EXP_HTML_MAIN: Optional[str] = None
_CACHED_EXP_HTML_PREVIEW: Optional[str] = None
_CACHED_SKILLS_HTML: Optional[str] = None

# ==============================================================================
# CSS CLASS CONSTANTS (for modularity & easy renaming)
# ==============================================================================
CLASS_PROJECT_ITEM = "project-item"
CLASS_CROSSHAIR_CARD = "crosshair-card"
CLASS_IS_FEATURED = "is-featured"

CLASS_EXPERIENCE_LIST = "experience-list"
CLASS_EXPERIENCE_ITEM = "experience-item"
CLASS_EXP_HEADER_ROW = "exp-header-row"
CLASS_EXP_ICON_PLACEHOLDER = "exp-icon-placeholder"
CLASS_EXP_HEADER_CONTENT = "exp-header-content"
CLASS_EXP_TOP = "exp-top"
CLASS_EXP_ROLE = "exp-role"
CLASS_EXP_ORG = "exp-org"
CLASS_EXP_TIME = "exp-time"
CLASS_EXP_TIME_PRESENT = "is-present"
CLASS_EXP_TIME_PAST = "is-past"
CLASS_EXP_POINTS = "exp-points"
CLASS_EXP_SKILLS = "exp-skills"

CLASS_SKILLS_LIST = "skills-list"
CLASS_SKILL_GROUP = "skill-group"
CLASS_SKILL_CATEGORY = "skill-category"
CLASS_SKILL_ITEMS = "skill-items"
CLASS_SKILL_TAGS = "skill-tags"

CLASS_PROJECT_TOPBAR = "project-topbar"
CLASS_PROJECT_TITLE_GROUP = "project-title-group"
CLASS_PROJECT_STAR = "project-star"
CLASS_STAR_EMPTY = "empty"
CLASS_PROJECT_NAME = "project-name"
CLASS_PROJECT_BADGE = "project-badge"

CLASS_PROJECT_STATUS_COL = "project-status-col"
CLASS_STATUS_IN_PROGRESS = "status-in-progress-text"
CLASS_STATUS_ON_HOLD = "status-on-hold-text"
CLASS_STATUS_COMPLETED = "status-completed-text"
CLASS_ON_HOLD_PIPE = "pipe"
CLASS_ON_HOLD_DATE = "on-hold-date"
CLASS_PROJECT_YEAR = "project-year"

CLASS_LIVE_SCORE_LINE = "live-score-line"
CLASS_LIVE_SCORE_ACTIVE = "active"
CLASS_LIVE_SCORE_BLUE = "blue-live-line"
CLASS_LIVE_SCORE_COMPLETED = "completed"
CLASS_LIVE_SCORE_ON_HOLD = "on-hold"

CLASS_NOTE_MINIMAL = "project-system-note-minimal"
CLASS_NOTE_GOOD = "note-good"
CLASS_NOTE_NOTE = "note-note"
CLASS_NOTE_BAD = "note-bad"
CLASS_NOTE_ICON = "note-icon"
CLASS_NOTE_TEXT = "note-text"

CLASS_PROJECT_SUMMARY = "project-summary"
CLASS_PROJECT_TAGS = "project-tags"
CLASS_TAG = "tag"

CLASS_PROJECT_ACTIONS = "project-actions"
CLASS_SYSTEM_LINK = "system-link"
CLASS_LINK_ARROW = "arrow"
CLASS_LINK_ARROW_EXTERNAL = "arrow-external"

CLASS_PROJECTS_LIST = "projects-list"

# Star symbol, Arrow symbols & Note emoji mappings
STAR_CHAR = "*"
ARROW_INTERNAL = "→"
ARROW_EXTERNAL = "↗"
NOTE_ICONS = {
    "good": "✅",
    "note": "📋",
    "bad": "⚠️",
}
NOTE_TYPE_CLASSES = {
    "good": CLASS_NOTE_GOOD,
    "note": CLASS_NOTE_NOTE,
    "bad": CLASS_NOTE_BAD,
}


def validate_link(link: Dict[str, Any], project_title: str) -> Tuple[str, bool]:
    """Validates that exactly one of 'page' or 'url' is specified.
    
    Returns (target_href, is_external).
    Raises ValueError if both or neither are provided.
    """
    text = link.get("text", "")
    page = (link.get("page") or "").strip()
    url = (link.get("url") or "").strip()

    if page and url:
        raise ValueError(
            f"Project '{project_title}' link '{text}' specifies both page ('{page}') and url ('{url}'). Exactly one must be specified."
        )
    if not page and not url:
        raise ValueError(
            f"Project '{project_title}' link '{text}' specifies neither page nor url. Exactly one must be specified."
        )

    if page:
        return page, False
    return url, True


def render_project_status(date_info: Dict[str, Any]) -> str:
    """Renders the right status column (date/status text + live score line)."""
    status = (date_info.get("status") or "").strip().lower()
    date_string = (date_info.get("date_string") or "").strip()

    if status == "wip":
        return (
            f'                  <div class="{CLASS_PROJECT_STATUS_COL}">\n'
            f'                    <span class="{CLASS_STATUS_IN_PROGRESS}">In Progress</span>\n'
            f'                    <div class="{CLASS_LIVE_SCORE_LINE} {CLASS_LIVE_SCORE_ACTIVE} {CLASS_LIVE_SCORE_BLUE}" aria-hidden="true"></div>\n'
            f'                  </div>'
        )
    elif status == "on-hold":
        return (
            f'                  <div class="{CLASS_PROJECT_STATUS_COL}">\n'
            f'                    <span class="{CLASS_STATUS_ON_HOLD}">On Hold<span class="{CLASS_ON_HOLD_PIPE}">|</span><span class="{CLASS_ON_HOLD_DATE}">{date_string}</span></span>\n'
            f'                    <div class="{CLASS_LIVE_SCORE_LINE} {CLASS_LIVE_SCORE_ON_HOLD}" aria-hidden="true"></div>\n'
            f'                  </div>'
        )
    else:  # "complete" or default fallback
        return (
            f'                  <div class="{CLASS_PROJECT_STATUS_COL}">\n'
            f'                    <span class="{CLASS_STATUS_COMPLETED}">{date_string}</span>\n'
            f'                    <div class="{CLASS_LIVE_SCORE_LINE} {CLASS_LIVE_SCORE_COMPLETED}" aria-hidden="true"></div>\n'
            f'                  </div>'
        )


def gen_project(project_data: Dict[str, Any]) -> str:
    """Generates an HTML snippet for a single project card."""
    title = project_data.get("title", "Untitled Project")
    description = project_data.get("description", "")
    featured = bool(project_data.get("featured", False))
    date_info = project_data.get("date", {})
    note_info = project_data.get("note", {})
    skills = project_data.get("skills", [])
    raw_links = project_data.get("links", [])

    # Validate links and identify optional primary page link for title
    primary_page_link: Optional[str] = None
    validated_links = []
    for link in raw_links:
        target, is_external = validate_link(link, title)
        validated_links.append({
            "text": link.get("text", "Link"),
            "target": target,
            "is_external": is_external,
        })
        if not is_external and primary_page_link is None:
            primary_page_link = target

    # Card container classes
    card_classes = [CLASS_PROJECT_ITEM, CLASS_CROSSHAIR_CARD]
    if featured:
        card_classes.append(CLASS_IS_FEATURED)
    card_class_str = " ".join(card_classes)

    lines: List[str] = []
    lines.append(f'            <article class="{card_class_str}">')
    lines.append(f'              <div class="{CLASS_PROJECT_TOPBAR}">')
    lines.append(f'                <div class="{CLASS_PROJECT_TITLE_GROUP}">')

    # Title (wrapped in link if a page link exists)
    if primary_page_link:
        lines.append(f'                  <h3 class="{CLASS_PROJECT_NAME}"><a href="{primary_page_link}">{title}</a></h3>')
    else:
        lines.append(f'                  <h3 class="{CLASS_PROJECT_NAME}">{title}</h3>')

    if featured:
        lines.append(f'                  <span class="{CLASS_PROJECT_BADGE}">FEATURED</span>')

    lines.append('                </div>')

    # Status Column
    lines.append(render_project_status(date_info))
    lines.append('              </div>')

    # Summary Description
    if description:
        lines.append(f'              <p class="{CLASS_PROJECT_SUMMARY}">{description}</p>')

    # Optional Note
    if isinstance(note_info, dict):
        note_type = (note_info.get("type") or "").strip().lower()
        note_msg = (note_info.get("message") or "").strip()
        if note_type and note_msg:
            icon = NOTE_ICONS.get(note_type, "")
            type_class = NOTE_TYPE_CLASSES.get(note_type, "")
            note_classes = [CLASS_NOTE_MINIMAL]
            if type_class:
                note_classes.append(type_class)
            note_class_str = " ".join(note_classes)
            lines.append(f'              <div class="{note_class_str}">')
            lines.append(f'                <span class="{CLASS_NOTE_ICON}">{icon}</span>')
            lines.append(f'                <span class="{CLASS_NOTE_TEXT}">{note_msg}</span>')
            lines.append('              </div>')

    # Skills Tags
    if skills:
        lines.append(f'              <div class="{CLASS_PROJECT_TAGS}">')
        for skill in skills:
            lines.append(f'                <span class="{CLASS_TAG}">{skill}</span>')
        lines.append('              </div>')

    # Action Links
    if validated_links:
        lines.append(f'              <div class="{CLASS_PROJECT_ACTIONS}">')
        for link_item in validated_links:
            text = link_item["text"]
            target = link_item["target"]
            if link_item["is_external"]:
                lines.append(
                    f'                <a href="{target}" class="{CLASS_SYSTEM_LINK}" target="_blank" rel="noreferrer">{text} <span class="{CLASS_LINK_ARROW} {CLASS_LINK_ARROW_EXTERNAL}">{ARROW_EXTERNAL}</span></a>'
                )
            else:
                lines.append(
                    f'                <a href="{target}" class="{CLASS_SYSTEM_LINK}">{text} <span class="{CLASS_LINK_ARROW}">{ARROW_INTERNAL}</span></a>'
                )
        lines.append('              </div>')

    lines.append('            </article>')
    return "\n".join(lines)


def gen_all_projects(
    projects_file: Path = PROJECTS_JSON_PATH,
    project_dir: Path = PROJECT_DESC_DIR_PATH,
    force_reload: bool = False
) -> str:
    """Parses project definitions from assets/projects.json (or fallback directory) and generates combined HTML."""
    global _CACHED_PROJECTS_HTML
    if _CACHED_PROJECTS_HTML is not None and not force_reload:
        return _CACHED_PROJECTS_HTML

    projects_data: List[Dict[str, Any]] = []

    if projects_file.exists():
        print(f"Parsing projects from: {projects_file.name}")
        with open(projects_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            projects_data = data.get("projects", [])
        elif isinstance(data, list):
            projects_data = data
    elif project_dir.exists():
        print(f"Parsing projects from directory: {project_dir}")
        json_files = sorted([
            f for f in project_dir.glob("*.json")
            if not f.name.endswith("_options.json") and not f.name.startswith(".")
        ])
        for json_file in json_files:
            with open(json_file, "r", encoding="utf-8") as f:
                projects_data.append(json.load(f))
    else:
        raise FileNotFoundError(f"Neither {projects_file} nor {project_dir} found.")

    if not projects_data:
        print("Warning: No projects found.")
        return ""

    # Ensure featured projects appear first, preserving relative order within groups
    projects_data = sorted(
        projects_data,
        key=lambda p: (not p.get("featured", False))
    )

    for project in projects_data:
        title = project.get("title", "Untitled Project")
        print(f"  - {title}")

    cards_html: List[str] = []
    for project in projects_data:
        cards_html.append(gen_project(project))

    _CACHED_PROJECTS_HTML = "\n\n".join(cards_html)
    return _CACHED_PROJECTS_HTML


def gen_experience(exp_data: Dict[str, Any], for_sitebuilder: bool = False) -> str:
    """Generates an HTML snippet for a single experience card."""
    title = exp_data.get("title", "Experience Title")
    company_data = exp_data.get("company", {})
    company_name = company_data.get("name", "")
    company_url = (company_data.get("url") or "").strip()

    if company_url and not company_url.lower().startswith("optional"):
        norm_url = company_url
        if not norm_url.startswith("http://") and not norm_url.startswith("https://"):
            norm_url = f"https://{norm_url}"
        company_html = (
            f'<a href="{norm_url}" target="_blank" rel="noreferrer">'
            f'{company_name} <span class="{CLASS_LINK_ARROW} {CLASS_LINK_ARROW_EXTERNAL}">{ARROW_EXTERNAL}</span></a>'
        )
    else:
        company_html = company_name

    date_data = exp_data.get("date", {})
    date_start = (date_data.get("date_start") or "").strip()
    date_end = (date_data.get("date_end") or "").strip()
    date_status = (date_data.get("status") or "").strip().lower()

    if date_status == "present":
        date_str = f"{date_start} - Present"
        time_class = f"{CLASS_EXP_TIME} {CLASS_EXP_TIME_PRESENT}"
        line_html = f'<div class="{CLASS_LIVE_SCORE_LINE} {CLASS_LIVE_SCORE_ACTIVE} {CLASS_LIVE_SCORE_BLUE}" aria-hidden="true"></div>'
    else:
        date_str = f"{date_start} - {date_end}" if date_end else date_start
        time_class = f"{CLASS_EXP_TIME} {CLASS_EXP_TIME_PAST}"
        line_html = f'<div class="{CLASS_LIVE_SCORE_LINE} {CLASS_LIVE_SCORE_COMPLETED}" aria-hidden="true"></div>'

    image_path = (exp_data.get("image") or "").strip()
    if image_path and not image_path.lower().startswith("optional"):
        if for_sitebuilder and image_path.startswith("assets/"):
            resolved_img = f"../{image_path}"
        else:
            resolved_img = image_path
        icon_box = f'<div class="{CLASS_EXP_ICON_PLACEHOLDER}" title="{company_name}"><img src="{resolved_img}" alt="{company_name} Logo" /></div>'
    else:
        icon_box = f'<div class="{CLASS_EXP_ICON_PLACEHOLDER}" title="Company Logo Placeholder">?</div>'

    work = exp_data.get("work", [])
    work_html = ""
    if work:
        work_lines = [f'              <ul class="{CLASS_EXP_POINTS}">']
        for pt in work:
            work_lines.append(f'                <li>{pt}</li>')
        work_lines.append('              </ul>')
        work_html = "\n" + "\n".join(work_lines)

    skills = exp_data.get("skills", [])
    skills_html = ""
    if skills:
        skills_lines = [f'              <div class="{CLASS_PROJECT_TAGS} {CLASS_EXP_SKILLS}">']
        for skill in skills:
            skills_lines.append(f'                <span class="{CLASS_TAG}">{skill}</span>')
        skills_lines.append('              </div>')
        skills_html = "\n" + "\n".join(skills_lines)

    card_classes = [CLASS_EXPERIENCE_ITEM, CLASS_CROSSHAIR_CARD]
    if date_status == "present":
        card_classes.append(CLASS_IS_FEATURED)
    card_class_str = " ".join(card_classes)

    lines = [
        f'            <article class="{card_class_str}">',
        f'              <div class="{CLASS_EXP_HEADER_ROW}">',
        f'                {icon_box}',
        f'                <div class="{CLASS_EXP_HEADER_CONTENT}">',
        f'                  <div class="{CLASS_EXP_TOP}">',
        f'                    <h3 class="{CLASS_EXP_ROLE}">{title}</h3>',
        f'                    <div class="{time_class}">',
        f'                      <span>{date_str}</span>',
        f'                      {line_html}',
        f'                    </div>',
        f'                  </div>',
        f'                  <p class="{CLASS_EXP_ORG}">{company_html}</p>',
        f'                </div>',
        f'              </div>{work_html}{skills_html}',
        f'            </article>'
    ]
    return "\n".join(lines)


def gen_all_experiences(
    experiences_file: Path = EXPERIENCES_JSON_PATH,
    experience_dir: Path = EXPERIENCE_DESC_DIR_PATH,
    for_sitebuilder: bool = False,
    force_reload: bool = False,
) -> str:
    """Parses experience definitions from assets/experiences.json (or fallback directory) and generates combined HTML."""
    global _CACHED_EXPERIENCES_DATA, _CACHED_EXP_HTML_MAIN, _CACHED_EXP_HTML_PREVIEW
    if not force_reload:
        if for_sitebuilder and _CACHED_EXP_HTML_PREVIEW is not None:
            return _CACHED_EXP_HTML_PREVIEW
        if not for_sitebuilder and _CACHED_EXP_HTML_MAIN is not None:
            return _CACHED_EXP_HTML_MAIN

    if _CACHED_EXPERIENCES_DATA is None or force_reload:
        experiences_data: List[Dict[str, Any]] = []

        if experiences_file.exists():
            print(f"Parsing experiences from: {experiences_file.name}")
            with open(experiences_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                experiences_data = data.get("experiences", [])
            elif isinstance(data, list):
                experiences_data = data
        elif experience_dir.exists():
            print(f"Parsing experiences from directory: {experience_dir}")
            json_files = sorted([
                f for f in experience_dir.glob("*.json")
                if not f.name.endswith("_options.json") and not f.name.startswith(".")
            ])
            for json_file in json_files:
                with open(json_file, "r", encoding="utf-8") as f:
                    experiences_data.append(json.load(f))
        else:
            raise FileNotFoundError(f"Neither {experiences_file} nor {experience_dir} found.")

        if not experiences_data:
            print("Warning: No experiences found.")
            return ""

        # Ensure present experiences appear first, preserving relative order within groups
        experiences_data = sorted(
            experiences_data,
            key=lambda exp: (exp.get("date", {}).get("status", "").strip().lower() != "present")
        )

        for exp in experiences_data:
            title = exp.get("title", "Experience")
            company_name = exp.get("company", {}).get("name", "")
            if company_name:
                print(f"  - {title} @ {company_name}")
            else:
                print(f"  - {title}")

        _CACHED_EXPERIENCES_DATA = experiences_data

    cards_html: List[str] = []
    for exp in _CACHED_EXPERIENCES_DATA:
        cards_html.append(gen_experience(exp, for_sitebuilder=for_sitebuilder))

    result = "\n\n".join(cards_html)
    if for_sitebuilder:
        _CACHED_EXP_HTML_PREVIEW = result
    else:
        _CACHED_EXP_HTML_MAIN = result
    return result


def gen_skill_group(category: str, items: Any) -> str:
    """Generates an HTML snippet for a single skill topic group card with mini boxes."""
    if isinstance(items, list):
        skill_list = [str(it).strip() for it in items if str(it).strip()]
    elif isinstance(items, str):
        skill_list = [s.strip() for s in items.split(",") if s.strip()]
    else:
        skill_list = []

    tags_lines = [f'                <span class="{CLASS_TAG}">{s}</span>' for s in skill_list]
    tags_html = "\n".join(tags_lines)

    lines = [
        f'            <div class="{CLASS_SKILL_GROUP} {CLASS_CROSSHAIR_CARD}">',
        f'              <span class="{CLASS_SKILL_CATEGORY}">{category}</span>',
        f'              <div class="{CLASS_PROJECT_TAGS} {CLASS_SKILL_TAGS}">',
        f'{tags_html}',
        f'              </div>',
        f'            </div>'
    ]
    return "\n".join(lines)


def gen_all_skills(
    skills_file: Path = SKILLS_JSON_PATH,
    skills_dir: Path = SKILL_DESC_DIR_PATH,
    force_reload: bool = False,
) -> str:
    """Parses skill definitions from assets/skills.json (or fallback directory) and generates combined HTML."""
    global _CACHED_SKILLS_HTML
    if _CACHED_SKILLS_HTML is not None and not force_reload:
        return _CACHED_SKILLS_HTML

    skills_map: Any = None

    if skills_file.exists():
        print(f"Parsing skills from: {skills_file.name}")
        with open(skills_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            skills_map = data.get("skills", data)
        else:
            skills_map = data
    elif skills_dir.exists():
        print(f"Parsing skills from directory: {skills_dir}")
        json_files = sorted([
            f for f in skills_dir.glob("*.json")
            if not f.name.endswith("_options.json") and not f.name.startswith(".")
        ])
        skills_map = {}
        for json_file in json_files:
            with open(json_file, "r", encoding="utf-8") as f:
                sub_data = json.load(f)
                if isinstance(sub_data, dict):
                    skills_map.update(sub_data.get("skills", sub_data))
    else:
        raise FileNotFoundError(f"Neither {skills_file} nor {skills_dir} found.")

    if not skills_map:
        print("Warning: No skills found.")
        return ""

    blocks_html: List[str] = []
    if isinstance(skills_map, dict):
        for category, items in skills_map.items():
            print(f"  - {category}")
            blocks_html.append(gen_skill_group(category, items))
    elif isinstance(skills_map, list):
        for entry in skills_map:
            if isinstance(entry, dict):
                cat = entry.get("category") or entry.get("topic") or entry.get("name") or "Skills"
                print(f"  - {cat}")
                items = entry.get("items") or entry.get("skills") or []
                blocks_html.append(gen_skill_group(cat, items))

    _CACHED_SKILLS_HTML = "\n\n".join(blocks_html)
    return _CACHED_SKILLS_HTML


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Site Builder Preview</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Cascadia+Code:wght@300;400;500;600;700&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="copy.css" />
    <link rel="stylesheet" href="../style.css" />
  </head>
  <body>
    <main>
      <!-- Projects Registry Section -->
      <section id="projects" class="section">
        <div class="container">
          <div class="section-heading">
            <p class="section-eyebrow">[<span class="eyebrow-addr">0x50 - 0x8F</span> // <span class="eyebrow-title">SYSTEM REGISTRY</span>]</p>
            <h2 class="section-title">Projects</h2>
            <p class="section-desc">Engineered systems, hardware designs, and firmware architectures. Starred items denote flagship projects.</p>
          </div>

          <div class="projects-list">
{projects_html}
          </div>
        </div>
      </section>

      <!-- Experience Section -->
      <section id="experience" class="section">
        <div class="container">
          <div class="section-heading">
            <p class="section-eyebrow">[<span class="eyebrow-addr">0x90 - 0xCF</span> // <span class="eyebrow-title">EXPERIENCE</span>]</p>
            <h2 class="section-title">Experience</h2>
            <p class="section-desc">Engineering leadership, competitive robotics, and firmware architecture.</p>
          </div>

          <div class="experience-list">
{experiences_html}
          </div>
        </div>
      </section>

      <!-- Skills & Tools Section -->
      <section id="skills" class="section">
        <div class="container">
          <div class="section-heading">
            <p class="section-eyebrow">[<span class="eyebrow-addr">0xD0 - 0xEF</span> // <span class="eyebrow-title">CAPABILITIES</span>]</p>
            <h2 class="section-title">Skills &amp; Tools</h2>
            <p class="section-desc">Engineering domains, hardware platforms, and software stacks.</p>
          </div>

          <div class="skills-list">
{skills_html}
          </div>
        </div>
      </section>
    </main>
  </body>
</html>
"""


def inject_section(html: str, section_id: str, list_class: str, inner_html: str) -> str:
    """Injects inner_html into the target section's list container."""
    pattern = re.compile(
        rf'(<section\s+id="{section_id}"[^>]*>.*?<div\s+class="{list_class}">)(.*?)(</div>\s*</div>\s*</section>)',
        re.DOTALL
    )
    if not pattern.search(html):
        raise ValueError(f"Could not find section id='{section_id}' with list class='{list_class}'")
    return pattern.sub(
        lambda m: f"{m.group(1)}\n{inner_html}\n            </div>\n          </div>\n        </section>",
        html,
        count=1
    )


def inject_into_main_html(main_path: Path = MAIN_HTML_PATH):
    """Directly injects the generated projects, experiences, and skills HTML into index.html."""
    if not main_path.exists():
        raise FileNotFoundError(f"{main_path} does not exist.")

    projects_html = gen_all_projects()
    experiences_html = gen_all_experiences(for_sitebuilder=False)
    skills_html = gen_all_skills()

    print(f"Injecting into: {main_path.name}")
    with open(main_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = inject_section(content, "projects", CLASS_PROJECTS_LIST, projects_html)
    content = inject_section(content, "experience", CLASS_EXPERIENCE_LIST, experiences_html)
    content = inject_section(content, "skills", CLASS_SKILLS_LIST, skills_html)

    with open(main_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully updated {main_path}")


def build_output_html(output_path: Path = OUTPUT_HTML_PATH):
    """Generates project, experience, and skill cards and writes the complete preview page directly to output_path."""
    projects_html = gen_all_projects()
    experiences_html = gen_all_experiences(for_sitebuilder=True)
    skills_html = gen_all_skills()

    content = HTML_TEMPLATE.format(
        projects_html=projects_html,
        experiences_html=experiences_html,
        skills_html=skills_html,
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Successfully generated {output_path}")


if __name__ == "__main__":
    inject_into_main_html()
    build_output_html()