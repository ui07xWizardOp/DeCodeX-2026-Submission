import markdown
import os
from jinja2 import Template

# Configuration
SOURCE_DIR = "."
OUTPUT_DIR = "docs/reports"
TEMPLATE_PATH = "docs/assets/templates/base.html"

FILES_TO_CONVERT = [
    "EXECUTIVE_ACTION_PLAN.md",
    "AUDIT_SUMMARY_AND_FINDINGS.md",
    "COMPREHENSIVE_AUDIT_AND_REANALYSIS.md",
    "INDEX_AND_NAVIGATION.md",
    "QUICK_REFERENCE_GUIDE.md",
    "Strategic_Document_Portfolio_Analysis.md"
]

def convert_md_to_html():
    # Load Template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template_str = f.read()
    template = Template(template_str)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for filename in FILES_TO_CONVERT:
        input_path = os.path.join(SOURCE_DIR, filename)
        if not os.path.exists(input_path):
            print(f"Skipping {filename}: Not found.")
            continue

        print(f"Converting {filename}...")
        
        # Read Markdown
        with open(input_path, "r", encoding="utf-8") as f:
            md_content = f.read()

        # Convert to HTML
        html_content = markdown.markdown(
            md_content,
            extensions=['tables', 'fenced_code', 'toc', 'attr_list']
        )

        # Render Template
        title = filename.replace(".md", "").replace("_", " ").title()
        final_html = template.render(title=title, content=html_content)

        # Save HTML
        output_filename = filename.replace(".md", ".html").lower()
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_html)
            
        print(f"Saved to {output_path}")

if __name__ == "__main__":
    convert_md_to_html()
