import os
from tempfile import template
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("no h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        source_md = f.read()

    with open(template_path) as f:
        template = f.read()
    
    html_content = markdown_to_html_node(source_md).to_html()
    title = extract_title(source_md)

    full_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    source_entries = os.listdir(dir_path_content)
    for entry in source_entries:
        source_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(source_path) and entry.endswith(".md"):
            generate_page(source_path, template_path, os.path.join(dest_dir_path, entry[:-3] + ".html"))
        else:
            generate_pages_recursive(source_path, template_path, os.path.join(dest_dir_path, entry))
